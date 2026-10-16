#!/usr/bin/env python3
"""Lint the Infinite Brain graph in this repository and (optionally) regenerate the index.

Checks, per _system/FRONTMATTER-SCHEMA.md and _system/EDGE-TYPES.md:
  * frontmatter present, id matches filename, id prefix matches type
  * required fields present, types/visibility/edge types in the canonical sets
  * confidence in range, summary under 200 chars, tags 2-8 kebab-case
  * edges non-empty, every edge has target/type/weight/note, targets resolve
  * no self-edges, no duplicate ids, no markdown nodes inside raw/
  * orphans (no outgoing edges, no related links, nothing pointing in)
  * index rows match the files on disk (--check-index)

Usage:
  python _system/lint_vault.py                 # lint, exit 1 on errors
  python _system/lint_vault.py --write-index   # rewrite _system/INDEX.md tables in place (UTF-8)
  python _system/lint_vault.py --emit-index    # print the index tables to stdout
  python _system/lint_vault.py --check-index   # verify _system/INDEX.md rows match disk

Always regenerate the index with --write-index rather than piping --emit-index through a
shell: on Windows the console code page rewrites non-ASCII characters (em-dashes become
U+FFFD) on the way through the pipe. --write-index writes the file from Python as UTF-8.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NODE_DIRS = [
    "pillars", "decisions", "concepts", "questions", "playbooks", "tasks",
    "events", "patterns", "hypotheses", "facts", "sources", "bookmarks",
    "notes", "contacts", "references", "custom",
]
LOG_DIR = "logs"

TYPES = {
    "pillar", "decision", "concept", "question", "playbook", "task", "event",
    "pattern", "hypothesis", "fact", "source", "bookmark", "note", "contact",
    "reference", "custom", "log",
}
EDGE_TYPES = {
    "related_to", "depends_on", "derived_from", "contradicts", "supports",
    "part_of", "preceded_by", "followed_by", "authored_by", "tagged_with",
}
VISIBILITY = {"public", "namespace", "private", "system"}
LOG_OPS = {"convert-note", "query-vault", "organize-vault", "vault-health", "init-vault"}
INDEX_ORDER = [
    "pillar", "decision", "concept", "question", "playbook", "task", "event",
    "pattern", "hypothesis", "fact", "source", "bookmark", "note", "contact",
    "reference", "custom",
]

SCALAR_FIELDS = [
    "id", "title", "type", "namespace", "visibility", "summary", "auto_inject",
    "applicable_when", "confidence", "verified_at", "verified_by",
    "staleness_signal", "source_url", "operation", "date",
]
ARRAY_FIELDS = ["tags", "edges", "related", "affected_nodes"]
REQUIRED = [
    "id", "title", "type", "namespace", "visibility", "summary", "auto_inject",
    "applicable_when", "confidence", "verified_at", "verified_by",
    "staleness_signal", "tags", "edges", "source_url",
]
PREFIX = {
    "pillar": "pillar", "decision": "decision", "concept": "concept",
    "question": "question", "playbook": "playbook", "task": "task",
    "event": "event", "pattern": "pattern", "hypothesis": "hyp",
    "fact": "fact", "source": "source", "bookmark": "bookmark", "note": "note",
    "contact": "contact", "reference": "ref", "custom": "cust", "log": "log",
}
TAG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
LOGDATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
OBJ_RE = re.compile(r"\{[^{}]*\}")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")

errors: list[str] = []
warnings: list[str] = []


def err(rel: str, msg: str) -> None:
    errors.append(f"{rel}: {msg}")


def warn(rel: str, msg: str) -> None:
    warnings.append(f"{rel}: {msg}")


def split_frontmatter(text: str):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], i + 1
    return None, 0


def scalar(fm_lines, key):
    """Top-level scalar written on the same line as the key."""
    pat = re.compile(rf"^{re.escape(key)}:\s*(.*)$")
    for line in fm_lines:
        m = pat.match(line)
        if m:
            v = m.group(1).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            return v
    return None


def block_span(fm_lines, key):
    """Return the full text of a flow array/block that starts on the key line.

    Scans forward until the opening bracket of the value is matched, so arrays
    spanning many lines (the edges convention) are collected whole.
    """
    for i, line in enumerate(fm_lines):
        if not re.match(rf"^{re.escape(key)}:", line):
            continue
        depth = 0
        started = False
        out = []
        for j in range(i, len(fm_lines)):
            cur = fm_lines[j]
            out.append(cur)
            for ch in cur:
                if ch in "[{":
                    depth += 1
                    started = True
                elif ch in "]}":
                    depth -= 1
            if started and depth <= 0:
                return "\n".join(out)
        return "\n".join(out)
    return None


def parse_flow(text, key, rel):
    """Parse the flow array inside a block's text."""
    if text is None:
        return None, None
    start = text.find("[")
    if start < 0:
        return None, None
    depth = 0
    for idx in range(start, len(text)):
        if text[idx] in "[{":
            depth += 1
        elif text[idx] in "]}":
            depth -= 1
            if depth == 0:
                end = idx + 1
                break
    else:
        err(rel, f"{key}: unterminated flow array")
        return None, None
    raw = text[start:end]
    if raw.strip() in ("[]", "[ ]"):
        return [], None
    try:
        return json.loads(raw), None
    except json.JSONDecodeError as exc:
        err(rel, f"{key}: not valid JSON flow syntax ({exc.msg} at char {exc.pos}) — "
                f"each object must be one line with double-quoted keys and string values")
        return None, None


def check_common(node, rel, reduced=False):
    nid = node.get("id") or ""
    ntype = node.get("type") or ""
    if not nid:
        err(rel, "missing id")
    if ntype and ntype not in TYPES:
        err(rel, f"unknown type {ntype!r}")
    if ntype and nid and PREFIX.get(ntype) and not nid.startswith(PREFIX[ntype] + "-"):
        err(rel, f"id {nid!r} must use the {PREFIX[ntype]}- prefix required by type {ntype}")
    if node.get("namespace") and not TAG_RE.match(node["namespace"]):
        err(rel, f"namespace {node['namespace']!r} is not kebab-case")
    summary = node.get("summary") or ""
    if len(summary) > 200:
        err(rel, f"summary is {len(summary)} chars (limit 200)")
    for placeholder in ("TBD", "1-2 sentences", "TODO", "Lorem", "XXX"):
        if placeholder in summary:
            err(rel, f"summary contains placeholder text {placeholder!r}")
    tags = node.get("tags")
    if isinstance(tags, list):
        if not tags:
            err(rel, "tags array is empty")
        elif not reduced and not (2 <= len(tags) <= 8):
            warn(rel, f"tags count {len(tags)} outside the 2-8 range")
        for t in tags:
            if not TAG_RE.match(str(t)):
                err(rel, f"tag {t!r} is not lowercase kebab-case")
    else:
        err(rel, "tags missing or not parsed as an array")
    if reduced:
        # the log schema has no staleness_signal, no confidence and no edges
        return
    stale = (node.get("staleness_signal") or "").strip()
    if not stale:
        err(rel, "staleness_signal is empty")
    elif not stale.lower().startswith(("if ", "when ", "once ", "after ", "superseded")):
        warn(rel, "staleness_signal should read as a conditional statement")



def load_nodes():
    nodes = {}
    by_id = defaultdict(list)

    for folder_name in NODE_DIRS + [LOG_DIR]:
        folder = ROOT / folder_name
        if not folder.is_dir():
            continue
        is_log = folder_name == LOG_DIR
        for path in sorted(folder.rglob("*.md")):
            rel = path.relative_to(ROOT).as_posix()
            text = path.read_text(encoding="utf-8-sig")
            fm, body_start = split_frontmatter(text)
            if fm is None:
                err(rel, "no YAML frontmatter block")
                continue

            node = {}
            for key in SCALAR_FIELDS:
                v = scalar(fm, key)
                if v is not None:
                    node[key] = v
            for key in ARRAY_FIELDS:
                val, _ = parse_flow(block_span(fm, key), key, rel)
                if val is not None:
                    node[key] = val

            if is_log:
                for f in ("id", "type", "operation", "date", "namespace", "summary",
                          "affected_nodes", "tags"):
                    if node.get(f) is None:
                        err(rel, f"log node missing required field {f!r}")
                if node.get("operation") and node["operation"] not in LOG_OPS:
                    err(rel, f"unknown log operation {node['operation']!r}")
                if node.get("date") and not LOGDATE_RE.match(node["date"]):
                    err(rel, f"log date {node['date']!r} is not YYYY-MM-DDTHH:MM:SS")
                if path.stem != node.get("id"):
                    err(rel, f"filename {path.stem!r} != id {node.get('id')!r}")
                check_common(node, rel, reduced=True)
            else:
                for f in REQUIRED:
                    if node.get(f) is None:
                        err(rel, f"missing required field {f!r}")
                if path.stem != node.get("id"):
                    err(rel, f"filename {path.stem!r} != id {node.get('id')!r}")
                ntype = node.get("type")
                if ntype == "log":
                    err(rel, "type log nodes belong in logs/")
                if node.get("visibility") not in VISIBILITY:
                    err(rel, f"unknown or missing visibility {node.get('visibility')!r}")
                if node.get("auto_inject") not in ("true", "false"):
                    err(rel, f"auto_inject must be true or false, got {node.get('auto_inject')!r}")
                try:
                    c = float(node.get("confidence"))
                    if not 0.0 <= c <= 1.0:
                        err(rel, f"confidence {c} outside 0.0-1.0")
                    node["_confidence"] = c
                except (TypeError, ValueError):
                    err(rel, f"confidence {node.get('confidence')!r} is not a float")
                va = node.get("verified_at")
                if va not in (None, "Empty") and not DATE_RE.match(va):
                    err(rel, f"verified_at {va!r} is not MM/DD/YYYY")
                check_common(node, rel)

                edge_texts = block_span(fm, "edges") or ""
                edges = []
                for obj in OBJ_RE.findall(edge_texts):
                    try:
                        edges.append(json.loads(obj))
                    except json.JSONDecodeError as exc:
                        err(rel, f"edges: unparseable object {obj[:70]!r} — {exc.msg}")
                node["edge_objs"] = edges
                node["edges_count"] = len(edges)
                if not edges:
                    err(rel, "edges array is empty — established nodes need at least one edge")
                for e in edges:
                    for k in ("target", "type", "weight", "note"):
                        if k not in e:
                            err(rel, f"edge missing key {k!r}: {str(e)[:70]}")
                    if e.get("type") and e["type"] not in EDGE_TYPES:
                        err(rel, f"unknown edge type {e.get('type')!r}")
                    if e.get("target") == node.get("id"):
                        err(rel, f"self-referencing edge to {e.get('target')}")
                    if not str(e.get("note") or "").strip():
                        err(rel, f"edge to {e.get('target')} has an empty note")
                    w = e.get("weight")
                    if isinstance(w, bool) or not isinstance(w, (int, float)):
                        err(rel, f"edge weight {w!r} is not a number")
                    elif not 0.0 <= float(w) <= 1.0:
                        err(rel, f"edge weight {w} outside 0.0-1.0")

                body = "\n".join(text.split("\n")[body_start:]).strip()
                if len(body) < 120:
                    warn(rel, "body looks too short (under ~120 chars)")
                if EMOJI_RE.search(text):
                    err(rel, "contains emoji or decorative symbols")

            nid = node.get("id")
            node["_rel"] = rel
            if nid:
                by_id[nid].append(rel)
                nodes[nid] = node

    for nid, rels in by_id.items():
        if len(rels) > 1:
            err(rels[0], f"duplicate id {nid!r} also in {', '.join(rels[1:])}")
    return nodes


def index_tables(nodes, content_nodes):
    """Markdown for the per-type index tables, used by --emit-index and --write-index."""
    out = ["<!-- generated by: python _system/lint_vault.py --write-index -->"]
    for t in INDEX_ORDER:
        rows = [(nid, n) for nid, n in sorted(nodes.items()) if n.get("type") == t]
        out.append(f"\n## {t}\n")
        if not rows:
            out.append("*No nodes yet.*\n")
            continue
        out.append("| ID | Summary | Edges |")
        out.append("|---|---|---|")
        for nid, n in rows:
            summary = (n.get("summary") or "").replace("|", "\\|")
            out.append(f"| `{nid}` | {summary} | {n.get('edges_count', 0)} |")
        out.append("")
    live_types = len([t for t, c in counts_live(nodes).items() if c])
    out.append(f"---\n\n*{content_nodes} content nodes across {live_types} types; "
               f"log nodes are not indexed. Regenerate with "
               f"`python _system/lint_vault.py --write-index`.*")
    return "\n".join(out) + "\n"


def counts_live(nodes):
    c = defaultdict(int)
    for n in nodes.values():
        c[n.get("type") or "?"] += 1
    return c


def main() -> int:
    emit = "--emit-index" in sys.argv
    check_index = "--check-index" in sys.argv
    write_index = "--write-index" in sys.argv

    nodes = load_nodes()

    for p in (ROOT / "raw").rglob("*.md"):
        err(p.relative_to(ROOT).as_posix(),
            "markdown node inside raw/ — the raw layer holds source material only")

    unresolved = 0
    for nid, n in sorted(nodes.items()):
        for e in n.get("edge_objs") or []:
            tgt = e.get("target")
            if tgt and tgt not in nodes:
                unresolved += 1
                err(n["_rel"], f"edge target {tgt!r} ({e.get('type')}) does not resolve to any node")

    # related[] wikilinks must name a file, because Obsidian resolves [[...]] by filename
    bad_related = 0
    for nid, n in sorted(nodes.items()):
        for ref in (n.get("related") or []):
            name = str(ref).strip()
            m = re.match(r"^\[\[(.+?)\]\]$", name)
            if m:
                name = m.group(1).split("|")[0].strip()
            if name and name not in nodes:
                bad_related += 1
                warn(n["_rel"], f"related entry {ref!r} resolves to no node id — "
                                f"wikilinks must name the file, which is the id")

    inbound = set()
    for n in nodes.values():
        for e in n.get("edge_objs") or []:
            if e.get("target"):
                inbound.add(e["target"])
    orphans = [nid for nid, n in sorted(nodes.items())
               if n.get("type") != "log" and not n.get("edge_objs")
               and not n.get("related") and nid not in inbound]
    for nid in orphans:
        warn(nodes[nid]["_rel"], "orphan: no outgoing edges, no related links, no inbound edges")

    counts = defaultdict(int)
    for n in nodes.values():
        counts[n.get("type") or "?"] += 1
    content_nodes = sum(c for t, c in counts.items() if t != "log")

    if emit or write_index:
        tables = index_tables(nodes, content_nodes)
        if write_index:
            path = ROOT / "_system" / "INDEX.md"
            preamble = ""
            if path.is_file():
                existing = path.read_text(encoding="utf-8")
                cut = existing.find("\n## pillar")
                if cut > 0:
                    preamble = existing[:cut].rstrip() + "\n\n"
                else:
                    err("_system/INDEX.md", "no '## pillar' heading found; preamble not preserved")
            path.write_text(preamble + tables, encoding="utf-8")
            print(f"wrote _system/INDEX.md — {content_nodes} content nodes, UTF-8")
        else:
            print(tables)

    if check_index:
        index_path = ROOT / "_system" / "INDEX.md"
        if not index_path.is_file():
            err("_system/INDEX.md", "index file is missing")
        else:
            # only id-shaped tokens (known type prefixes) count as index rows;
            # namespace strings like `qwen4-exp-gaudi2` must not be mistaken for nodes
            id_prefixes = tuple(sorted(set(PREFIX.values())))
            tokens = re.findall(r"`([a-z][a-z0-9]+(?:-[a-z0-9]+)+)`",
                                index_path.read_text(encoding="utf-8"))
            listed = {t for t in tokens if t.startswith(id_prefixes)}
            for m in sorted(n for n in nodes
                            if nodes[n].get("type") != "log" and n not in listed):
                err("_system/INDEX.md", f"node {m} exists on disk but is not listed in the index")
            for s in sorted(x for x in listed if x not in nodes):
                warn("_system/INDEX.md", f"index lists {s} but no such node exists on disk")

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  ! {e}")
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ~ {w}")

    print("\n" + "=" * 70)
    print("nodes: " + " | ".join(f"{t}={c}" for t, c in sorted(counts.items())))
    print(f"content nodes: {content_nodes} | log nodes: {counts.get('log', 0)} | "
          f"orphans: {len(orphans)} | unresolved edge targets: {unresolved}")
    print(f"result: {'FAIL' if errors else 'PASS'} ({len(errors)} errors, {len(warnings)} warnings)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
