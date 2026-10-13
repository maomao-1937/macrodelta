"""CLI for read-only, locally inferred support-macro review."""

import argparse
import json
import sys
from pathlib import Path

from .core import audit, changes, validate_records
from .model import LocalEmbedder


def markdown(report: dict) -> str:
    lines = ["# MacroDelta review", "", report["warning"], "", f"Changed policy clauses: {report['changed_clauses']}", f"Model: `{report['model']}`", ""]
    if not report["findings"]:
        lines += ["No candidate macros found. This is **not** proof that all macros are current.", ""]
    for finding in report["findings"]:
        lines += [
            f"## Macro `{finding['macro_id']}` ↔ clause `{finding['clause_id']}`", "",
            f"- Reason: `{finding['reason']}`; old-policy semantic similarity: {finding['old_policy_similarity']:.3f}",
            f"- Old-only values in macro: {', '.join(finding['obsolete_value_hits']) or 'none'}",
            f"- Old policy: {finding['old_policy']}", f"- New policy: {finding['new_policy']}",
            f"- Macro to review: {finding['macro_text']}", "",
        ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Review support macros affected by policy changes using local semantic AI")
    parser.add_argument("old_policy", type=Path)
    parser.add_argument("new_policy", type=Path)
    parser.add_argument("macros", type=Path)
    parser.add_argument("--threshold", type=float, default=0.42)
    parser.add_argument("--out", type=Path, default=Path("report.md"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args(argv)
    try:
        old = validate_records(json.loads(args.old_policy.read_text(encoding="utf-8")), "old_policy")
        new = validate_records(json.loads(args.new_policy.read_text(encoding="utf-8")), "new_policy")
        macros = validate_records(json.loads(args.macros.read_text(encoding="utf-8")), "macros", 500)
        has_changes = bool(changes(old, new))
        if has_changes:
            model = LocalEmbedder()
        else:
            model = None
        report = audit(old, new, macros, model, args.threshold)  # type: ignore[arg-type]
        args.out.write_text(markdown(report), encoding="utf-8")
        if args.json_out:
            args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, RuntimeError, ImportError) as exc:
        print(f"MacroDelta error: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {args.out}: {report['changed_clauses']} changed clauses; {len(report['findings'])} macro review candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
