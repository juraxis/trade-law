#!/usr/bin/env python3
"""
HTS Hierarchy Builder

Converts the flat USITC HTS JSON dump into a navigable indent tree
for GRI 6 subheading-level comparison.

The USITC bulk JSON (e.g., hts_2026_revision_2_json.json) is a flat array
where hierarchy is encoded via:
  - `indent` levels 0-4 (parent-child depth)
  - Blank `htsno` with `superior: true` = grouping headers
  - Entries are in sequential order within each chapter

Usage:
  python3 hts-hierarchy-builder.py <json_file> <heading>

  json_file: Path to the bulk HTS JSON file
  heading:   4-digit heading to extract (e.g., "8471" or "8471.60")

Examples:
  python3 hts-hierarchy-builder.py hts_2026_revision_2.json 8471
  python3 hts-hierarchy-builder.py hts_2026_revision_2.json 8507.10

Output:
  Indented tree showing the hierarchy under the specified heading,
  with HTS numbers, descriptions, and duty rates.
"""

import json
import sys
from typing import Optional


def load_hts_data(filepath: str) -> list[dict]:
    """Load the flat HTS JSON array."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_heading_entries(data: list[dict], heading: str) -> list[dict]:
    """
    Extract all entries under a given heading prefix.

    The heading can be:
      - 4-digit: "8471" → matches 8471.xx.xx
      - 6-digit: "8471.60" → matches 8471.60.xx
      - Any prefix of an HTS number
    """
    # Normalize: remove dots for matching
    heading_clean = heading.replace(".", "")

    results = []
    in_scope = False

    for entry in data:
        htsno = entry.get("htsno", "")
        htsno_clean = htsno.replace(".", "")
        is_superior = entry.get("superior") in (True, "true", "True")

        if htsno_clean.startswith(heading_clean):
            in_scope = True
            results.append(entry)
        elif in_scope and not htsno and is_superior:
            # Superior (grouping header) entries within the heading range
            results.append(entry)
        elif in_scope and htsno and not htsno_clean.startswith(heading_clean):
            # We've moved past the heading
            break
        elif in_scope and not htsno and not is_superior:
            # Descriptive entries within the heading
            results.append(entry)

    return results


def build_tree(entries: list[dict]) -> list[dict]:
    """
    Build a tree structure from flat entries using indent levels.

    Each node has:
      - All original fields
      - 'children': list of child nodes
    """
    root_nodes = []
    stack = []  # Stack of (indent_level, node)

    for entry in entries:
        indent = int(entry.get("indent", 0))
        node = {**entry, "children": []}

        # Pop stack until we find the parent
        while stack and stack[-1][0] >= indent:
            stack.pop()

        if stack:
            # Add as child of the top of stack
            stack[-1][1]["children"].append(node)
        else:
            # Root-level node
            root_nodes.append(node)

        stack.append((indent, node))

    return root_nodes


def format_tree(nodes: list[dict], depth: int = 0) -> str:
    """Format the tree as indented text output."""
    lines = []

    for node in nodes:
        indent_str = "  " * depth
        htsno = node.get("htsno", "")
        description = node.get("description", "")
        general = node.get("general", "")
        special = node.get("special", "")
        is_superior = node.get("superior") in (True, "true", "True")
        units = node.get("units", [])

        # Build the display line
        if htsno:
            rate_info = f" | General: {general}" if general else ""
            special_info = f" | Special: {special}" if special else ""
            unit_info = f" | Units: {', '.join(units)}" if units else ""
            line = f"{indent_str}{htsno}: {description}{rate_info}{special_info}{unit_info}"
        elif is_superior:
            line = f"{indent_str}[{description}]"
        else:
            line = f"{indent_str}  {description}"

        lines.append(line)

        # Add footnote indicators
        footnotes = node.get("footnotes", [])
        if footnotes:
            for fn in footnotes:
                fn_value = fn.get("value", "")
                if fn_value:
                    lines.append(f"{indent_str}  ** {fn_value}")

        # Recurse into children
        if node.get("children"):
            lines.append(format_tree(node["children"], depth + 1))

    return "\n".join(lines)


def format_comparison_table(entries: list[dict], target_indent: Optional[int] = None) -> str:
    """
    Format entries at the same indent level as a comparison table.
    This is specifically for GRI 6 analysis — comparing subheadings
    at the same level.
    """
    if target_indent is None:
        # Find the most common indent level (likely the subheading level)
        indent_counts: dict[int, int] = {}
        for entry in entries:
            if entry.get("htsno"):
                indent = int(entry.get("indent", 0))
                indent_counts[indent] = indent_counts.get(indent, 0) + 1
        if indent_counts:
            target_indent = max(indent_counts, key=indent_counts.get)
        else:
            target_indent = 1

    lines = [
        f"GRI 6 Comparison — Subheadings at indent level {target_indent}",
        "-" * 80,
        f"{'HTS Number':<16} {'Description':<40} {'General Rate':<15}",
        "-" * 80,
    ]

    for entry in entries:
        if int(entry.get("indent", 0)) == target_indent and entry.get("htsno"):
            htsno = entry.get("htsno", "")
            desc = entry.get("description", "")
            if len(desc) > 38:
                desc = desc[:35] + "..."
            general = entry.get("general", "")
            lines.append(f"{htsno:<16} {desc:<40} {general:<15}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    filepath = sys.argv[1]
    heading = sys.argv[2]

    print(f"Loading HTS data from: {filepath}")
    data = load_hts_data(filepath)
    print(f"Loaded {len(data)} total entries")

    print(f"\nExtracting entries under heading: {heading}")
    entries = extract_heading_entries(data, heading)
    print(f"Found {len(entries)} entries\n")

    if not entries:
        print(f"No entries found for heading '{heading}'")
        sys.exit(1)

    # Build and display the tree
    print("=" * 80)
    print(f"HIERARCHY TREE — Heading {heading}")
    print("=" * 80)
    tree = build_tree(entries)
    print(format_tree(tree))

    # Display GRI 6 comparison tables at each indent level
    indent_levels = sorted(set(
        int(e.get("indent", 0))
        for e in entries
        if e.get("htsno")
    ))

    for level in indent_levels:
        if level > 0:  # Skip the heading itself
            print(f"\n{'=' * 80}")
            print(format_comparison_table(entries, level))

    print()


if __name__ == "__main__":
    main()
