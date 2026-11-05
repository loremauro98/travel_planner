import json
import subprocess
import sys
from pathlib import Path

from graphify.build import build_from_json
from graphify.cluster import cluster
from graphify.export import to_json


def main():
    if len(sys.argv) < 2:
        print("Usage: python merge_graph.py <TARGET_DIR>")
        sys.exit(1)

    target_dir = Path(sys.argv[1]).resolve()
    graphify_out = target_dir / "graphify-out"

    detect_path = graphify_out / ".graphify_detect.json"
    semantic_path = graphify_out / ".graphify_semantic_new.json"
    extract_path = graphify_out / ".graphify_extract.json"

    if not detect_path.exists() or not semantic_path.exists():
        print(
            "Error: Missing .graphify_detect.json or .graphify_semantic_new.json in target directory."
        )
        sys.exit(1)

    detect_data = json.loads(detect_path.read_text(encoding="utf-8"))
    docs = detect_data.get("files", {}).get("document", [])

    semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
    nodes = list(semantic.get("nodes", []))
    edges = list(semantic.get("edges", []))

    doc_ids = {}
    for doc in docs:
        p = Path(doc)
        # Stem is filename without ext, lowercased, spaces/dots/hyphens replaced with underscores
        doc_id = p.stem.lower().replace(".", "_").replace("-", "_").replace(" ", "_")
        doc_ids[doc] = doc_id
        nodes.append(
            {
                "id": doc_id,
                "label": p.name,
                "file_type": "document",
                "source_file": doc,
                "source_location": None,
                "source_url": None,
            }
        )

    for n in semantic.get("nodes", []):
        sf = n.get("source_file")
        if sf and sf in doc_ids:
            edges.append(
                {
                    "source": doc_ids[sf],
                    "target": n["id"],
                    "relation": "contains_concept",
                    "confidence": "EXTRACTED",
                    "confidence_score": 1.0,
                    "source_file": sf,
                    "weight": 1.0,
                }
            )

    extract_data = {
        "nodes": nodes,
        "edges": edges,
        "hyperedges": semantic.get("hyperedges", []),
        "input_tokens": semantic.get("input_tokens", 0),
        "output_tokens": semantic.get("output_tokens", 0),
    }

    extract_path.write_text(
        json.dumps(extract_data, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("Building structural graph...")
    G = build_from_json(extract_data, root=str(target_dir), directed=False)
    communities = cluster(G)
    to_json(G, communities, str(graphify_out / "graph.json"), force=True)

    print("Exporting HTML...")
    subprocess.run(f"graphify export html --dir {target_dir}", shell=True)
    print(f"Graph Built! {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")


if __name__ == "__main__":
    main()
