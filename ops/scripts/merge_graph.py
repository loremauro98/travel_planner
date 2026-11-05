import glob
import json
import shutil
import sys
from pathlib import Path

# Setup paths
base_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(base_dir))

# 1. Save old graph
if Path("graphify-out/graph.json").exists():
    shutil.copy("graphify-out/graph.json", "graphify-out/.graphify_old.json")

# 2. Get code files and run AST extraction
from graphify.detect import detect_incremental, save_manifest
from graphify.extract import collect_files, extract

result = detect_incremental(Path("."))
Path("graphify-out/.graphify_incremental.json").write_text(
    json.dumps(result, ensure_ascii=False), encoding="utf-8"
)
Path("graphify-out/.graphify_detect.json").write_text(
    json.dumps(
        {
            "files": result.get("new_files", {}),
            "all_files": result.get("files", {}),
            "total_files": result.get("new_total", 0),
            "total_words": result.get("total_words", 0),
            "skipped_sensitive": result.get("skipped_sensitive", []),
            "needs_graph": True,
        },
        ensure_ascii=False,
    ),
    encoding="utf-8",
)

code_files = []
for f in result.get("files", {}).get("code", []):
    code_files.extend(collect_files(Path(f)) if Path(f).is_dir() else [Path(f)])

if code_files:
    ast_result = extract(code_files, cache_root=Path("."))
    Path("graphify-out/.graphify_ast.json").write_text(
        json.dumps(ast_result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"AST: {len(ast_result['nodes'])} nodes, {len(ast_result['edges'])} edges")
else:
    ast_result = {"nodes": [], "edges": [], "input_tokens": 0, "output_tokens": 0}
    Path("graphify-out/.graphify_ast.json").write_text(
        json.dumps(ast_result, ensure_ascii=False), encoding="utf-8"
    )
    print("No code files - skipping AST extraction")

# 3. Merge semantic chunks
chunks = sorted(glob.glob("graphify-out/.graphify_chunk_*.json"))
all_nodes, all_edges, all_hyperedges = [], [], []
for c in chunks:
    d = json.loads(Path(c).read_text(encoding="utf-8"))
    all_nodes += d.get("nodes", [])
    all_edges += d.get("edges", [])
    all_hyperedges += d.get("hyperedges", [])

Path("graphify-out/.graphify_semantic.json").write_text(
    json.dumps(
        {
            "nodes": all_nodes,
            "edges": all_edges,
            "hyperedges": all_hyperedges,
            "input_tokens": 0,
            "output_tokens": 0,
        },
        indent=2,
        ensure_ascii=False,
    ),
    encoding="utf-8",
)
print(f"Merged {len(chunks)} chunks")

# 4. Merge AST + semantic
seen = {n["id"] for n in ast_result["nodes"]}
merged_nodes = list(ast_result["nodes"])
for n in all_nodes:
    if n["id"] not in seen:
        merged_nodes.append(n)
        seen.add(n["id"])

merged_edges = ast_result["edges"] + all_edges
final_merged = {
    "nodes": merged_nodes,
    "edges": merged_edges,
    "hyperedges": all_hyperedges,
    "input_tokens": 0,
    "output_tokens": 0,
}
Path("graphify-out/.graphify_extract.json").write_text(
    json.dumps(final_merged, indent=2, ensure_ascii=False), encoding="utf-8"
)

# 5. Build and merge graph
from graphify.analyze import god_nodes, suggest_questions, surprising_connections
from graphify.build import build_from_json, build_merge
from graphify.cluster import cluster, score_all
from graphify.export import to_json
from graphify.report import generate

deleted = list(result.get("deleted_files", []))
G = build_merge(
    [final_merged],
    graph_path="graphify-out/graph.json",
    prune_sources=deleted or None,
    root=".",
    directed=False,
)
merged_out = {
    "nodes": [{"id": n, **d} for n, d in G.nodes(data=True)],
    "edges": [
        {
            **{
                k: val
                for k, val in d.items()
                if k not in ("_src", "_tgt", "source", "target")
            },
            "source": d.get("_src", u),
            "target": d.get("_tgt", v),
        }
        for u, v, d in G.edges(data=True)
    ],
    "hyperedges": list(G.graph.get("hyperedges", [])),
    "input_tokens": 0,
    "output_tokens": 0,
}
Path("graphify-out/.graphify_extract.json").write_text(
    json.dumps(merged_out, ensure_ascii=False), encoding="utf-8"
)

# Save manifest to prevent incremental LLM re-run
save_manifest(result["files"], root=".")

# 6. Build graph outputs
G = build_from_json(merged_out, root=".", directed=False)
communities = cluster(G)
cohesion = score_all(G, communities)
gods = god_nodes(G)
surprises = surprising_connections(G, communities)
labels = {cid: "Community " + str(cid) for cid in communities}
questions = suggest_questions(G, communities, labels)

to_json(G, communities, "graphify-out/graph.json")
report = generate(
    G,
    communities,
    cohesion,
    labels,
    gods,
    surprises,
    result,
    {},
    ".",
    suggested_questions=questions,
)
Path("graphify-out/GRAPH_REPORT.md").write_text(report, encoding="utf-8")

# Clean up temp files
Path("graphify-out/.graphify_old.json").unlink(missing_ok=True)
Path("graphify-out/.graphify_incremental.json").unlink(missing_ok=True)
Path("graphify-out/.graphify_detect.json").unlink(missing_ok=True)
Path("graphify-out/.graphify_ast.json").unlink(missing_ok=True)
Path("graphify-out/.graphify_semantic.json").unlink(missing_ok=True)
Path("graphify-out/.graphify_extract.json").unlink(missing_ok=True)

print("Graph output successfully written with manual semantic chunk integration!")
