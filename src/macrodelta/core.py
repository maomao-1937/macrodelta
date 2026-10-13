"""Pure review logic; scores are retrieval hints, never correctness verdicts."""

import re
from typing import Any, Protocol


class Embedder(Protocol):
    def similarities(self, queries: list[str], documents: list[str]) -> list[list[float]]: ...


def validate_records(data: Any, label: str, limit: int = 200) -> list[dict[str, str]]:
    if not isinstance(data, list) or not data or len(data) > limit:
        raise ValueError(f"{label} must be a non-empty JSON array of at most {limit} records")
    records: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, record in enumerate(data):
        if not isinstance(record, dict):
            raise ValueError(f"{label}[{index}] must be an object")
        rid, body = record.get("id"), record.get("text")
        if not isinstance(rid, str) or not rid.strip() or not isinstance(body, str) or not body.strip():
            raise ValueError(f"{label}[{index}] needs non-empty string id and text")
        if len(rid) > 120 or len(body) > 8000:
            raise ValueError(f"{label}[{index}] exceeds the id/text length limit")
        if rid in seen:
            raise ValueError(f"Duplicate {label} id: {rid}")
        seen.add(rid)
        records.append({"id": rid, "text": body.strip()})
    return records


def changes(old: list[dict[str, str]], new: list[dict[str, str]]) -> list[dict[str, str]]:
    new_by_id = {item["id"]: item["text"] for item in new}
    result = []
    for item in old:
        if item["id"] not in new_by_id:
            raise ValueError(f"Policy clause {item['id']} has no counterpart in the new policy; provide a stable id or remove it from both versions")
        current = new_by_id[item["id"]]
        if " ".join(item["text"].split()).casefold() != " ".join(current.split()).casefold():
            result.append({"id": item["id"], "old": item["text"], "new": current})
    return result


_VALUE = re.compile(r"(?<!\w)(?:[$€£]\s*)?\d+(?:[.,]\d+)?\s*(?:days?|hours?|weeks?|months?|years?|%|usd|eur|gbp)?\b", re.I)


def _values(text: str) -> set[str]:
    return {re.sub(r"\s+", "", match.group(0)).casefold() for match in _VALUE.finditer(text)}


def audit(old: list[dict[str, str]], new: list[dict[str, str]], macros: list[dict[str, str]], model: Embedder, threshold: float = 0.42) -> dict[str, Any]:
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    changed = changes(old, new)
    if not changed:
        return {"model": "not_run_no_changed_clauses", "changed_clauses": 0, "findings": [], "warning": "No changed clauses; macro content was not audited."}
    scores = model.similarities([item["old"] for item in changed], [item["text"] for item in macros])
    if len(scores) != len(changed) or any(len(row) != len(macros) for row in scores):
        raise RuntimeError("Embedding model returned an unexpected similarity matrix shape")
    findings = []
    for clause, row in zip(changed, scores, strict=True):
        obsolete = _values(clause["old"]) - _values(clause["new"])
        for macro, score in zip(macros, row, strict=True):
            old_values_in_macro = sorted(value for value in obsolete if value in _values(macro["text"]))
            if float(score) >= threshold or old_values_in_macro:
                findings.append({
                    "clause_id": clause["id"], "old_policy": clause["old"], "new_policy": clause["new"],
                    "macro_id": macro["id"], "macro_text": macro["text"],
                    "old_policy_similarity": round(float(score), 4),
                    "obsolete_value_hits": old_values_in_macro,
                    "reason": "old_value_and_semantic_match" if old_values_in_macro and score >= threshold else ("old_value_present" if old_values_in_macro else "semantic_match_review"),
                })
    findings.sort(key=lambda item: (bool(item["obsolete_value_hits"]), item["old_policy_similarity"]), reverse=True)
    return {
        "model": "sentence-transformers/all-MiniLM-L6-v2", "changed_clauses": len(changed), "findings": findings,
        "warning": "Review queue only. Similarity is not a calibrated probability; a matching number may be unrelated. No macro is rewritten or approved automatically. Unchanged clauses are outside this audit.",
    }
