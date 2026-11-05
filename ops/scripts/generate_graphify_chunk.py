"""Build a manual semantic chunk for the Graphify knowledge graph.

This is a maintenance helper, not part of the ingestion pipeline. Run it from the
repository root during a checkpoint, then run ``merge_graph.py``.
"""

import json
from pathlib import Path

# Project root: ops/scripts/generate_graphify_chunk.py -> parents[2]
BASE_DIR = Path(__file__).resolve().parents[2]

nodes = []
edges = []
hyperedges = []


def add_node(node_id, label, file_type, source_file):
    nodes.append(
        {
            "id": node_id,
            "label": label,
            "file_type": file_type,
            "source_file": str(source_file),
            "source_location": None,
            "source_url": None,
            "captured_at": None,
            "author": None,
            "contributor": None,
        }
    )


def add_edge(source, target, relation, confidence, confidence_score, source_file):
    edges.append(
        {
            "source": source,
            "target": target,
            "relation": relation,
            "confidence": confidence,
            "confidence_score": confidence_score,
            "source_file": str(source_file),
            "source_location": None,
            "weight": 1.0,
        }
    )


FILE_AGENTS = BASE_DIR / "AGENTS.md"
FILE_PIPELINE = BASE_DIR / "CODE_PIPELINE.md"
FILE_README = BASE_DIR / "README.md"
FILE_REQUIREMENTS = BASE_DIR / "requirements.txt"
FILE_CUSTOM_SKILLS = BASE_DIR / "docs" / "CUSTOM_SKILLS.md"
FILE_CHANGELOG = BASE_DIR / "docs" / "CHANGELOG.md"
FILE_ICM_NOTES = BASE_DIR / "docs" / "reference" / "icm_course_notes.md"
FILE_DOCS_CONTEXT = BASE_DIR / "docs" / "CONTEXT.md"
FILE_DATA_CONTEXT = BASE_DIR / "data" / "CONTEXT.md"
FILE_OPS_CONTEXT = BASE_DIR / "ops" / "CONTEXT.md"
FILE_PLANNING_CONTEXT = BASE_DIR / "planning" / "CONTEXT.md"
FILE_SRC_CONTEXT = BASE_DIR / "src" / "CONTEXT.md"
FILE_TESTS_CONTEXT = BASE_DIR / "tests" / "CONTEXT.md"
FILE_TRACKER_SPEC = BASE_DIR / "planning" / "specs" / "flight_tracker_spec.md"

# Document nodes
add_node("agents_md", "AGENTS.md Layer 1 Routing Map", "document", FILE_AGENTS)
add_node("code_pipeline", "CODE_PIPELINE.md 9-Step Pipeline", "document", FILE_PIPELINE)
add_node("readme_md", "README.md Project Overview", "document", FILE_README)
add_node(
    "requirements_txt", "requirements.txt Dependencies", "document", FILE_REQUIREMENTS
)
add_node(
    "custom_skills", "CUSTOM_SKILLS.md Skill Registry", "document", FILE_CUSTOM_SKILLS
)
add_node("docs_changelog", "CHANGELOG.md Project History", "document", FILE_CHANGELOG)
add_node("icm_notes", "ICM Course Notes", "document", FILE_ICM_NOTES)
add_node("docs_context", "docs/CONTEXT.md Room Contract", "document", FILE_DOCS_CONTEXT)
add_node("data_context", "data/CONTEXT.md Room Contract", "document", FILE_DATA_CONTEXT)
add_node("ops_context", "ops/CONTEXT.md Room Contract", "document", FILE_OPS_CONTEXT)
add_node(
    "planning_context",
    "planning/CONTEXT.md Room Contract",
    "document",
    FILE_PLANNING_CONTEXT,
)
add_node("src_context", "src/CONTEXT.md Room Contract", "document", FILE_SRC_CONTEXT)
add_node(
    "tests_context", "tests/CONTEXT.md Room Contract", "document", FILE_TESTS_CONTEXT
)
add_node(
    "flight_tracker_spec",
    "Flight Tracker Feature Specification",
    "document",
    FILE_TRACKER_SPEC,
)

# Concept nodes
add_node(
    "concept_multi_airport",
    "Multi-Airport Routing Engine",
    "concept",
    FILE_TRACKER_SPEC,
)
add_node(
    "concept_price_tracking",
    "Time-Series Price Ingestion",
    "concept",
    FILE_TRACKER_SPEC,
)
add_node(
    "concept_analytics_dip",
    "Price Dip Moving Average Detection",
    "concept",
    FILE_TRACKER_SPEC,
)

# Relationships
add_edge(
    "planning_context",
    "flight_tracker_spec",
    "references",
    "EXTRACTED",
    1.0,
    FILE_PLANNING_CONTEXT,
)
add_edge(
    "flight_tracker_spec",
    "concept_multi_airport",
    "defines",
    "EXTRACTED",
    1.0,
    FILE_TRACKER_SPEC,
)
add_edge(
    "flight_tracker_spec",
    "concept_price_tracking",
    "defines",
    "EXTRACTED",
    1.0,
    FILE_TRACKER_SPEC,
)
add_edge(
    "flight_tracker_spec",
    "concept_analytics_dip",
    "defines",
    "EXTRACTED",
    1.0,
    FILE_TRACKER_SPEC,
)

for workspace_context in (
    "docs_context",
    "data_context",
    "ops_context",
    "planning_context",
    "src_context",
    "tests_context",
):
    add_edge(
        "agents_md",
        workspace_context,
        "defines_rules_for",
        "INFERRED",
        0.9,
        FILE_AGENTS,
    )
    add_edge("agents_md", workspace_context, "routes_to", "INFERRED", 0.9, FILE_AGENTS)

add_edge("agents_md", "code_pipeline", "enforces", "EXTRACTED", 1.0, FILE_AGENTS)
add_edge("agents_md", "custom_skills", "catalogues", "EXTRACTED", 1.0, FILE_AGENTS)
add_edge(
    "custom_skills", "agents_md", "classifies", "INFERRED", 0.9, FILE_CUSTOM_SKILLS
)
add_edge("icm_notes", "agents_md", "structures", "INFERRED", 0.8, FILE_ICM_NOTES)
add_edge("readme_md", "agents_md", "points_to", "EXTRACTED", 1.0, FILE_README)

output = {
    "nodes": nodes,
    "edges": edges,
    "hyperedges": hyperedges,
    "input_tokens": 0,
    "output_tokens": 0,
}

target = BASE_DIR / "graphify-out" / ".graphify_chunk_01.json"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(output, separators=(",", ":")), encoding="utf-8")

print(f"Manually generated semantic chunk written to: {target}")
