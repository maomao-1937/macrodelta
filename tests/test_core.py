import pytest

from macrodelta.cli import markdown
from macrodelta.core import audit, changes, validate_records


class FakeEmbedder:
    def similarities(self, queries, documents):
        return [[0.8 if "refund" in document.lower() else 0.05 for document in documents] for _ in queries]


def sample():
    old = validate_records([{"id": "refund", "text": "Refund requests are accepted within 30 days."}], "old")
    new = validate_records([{"id": "refund", "text": "Refund requests are accepted within 14 days."}], "new")
    macros = validate_records([{"id": "stale", "text": "Ask for a refund in 30 days."}, {"id": "other", "text": "Hello."}], "macros")
    return old, new, macros


def test_changed_policy_routes_old_number_to_macro():
    report = audit(*sample(), FakeEmbedder())
    assert report["changed_clauses"] == 1
    assert [item["macro_id"] for item in report["findings"]] == ["stale"]
    assert report["findings"][0]["obsolete_value_hits"] == ["30days"]
    assert "not a calibrated probability" in markdown(report)


def test_no_change_skips_model():
    old, _, macros = sample()
    report = audit(old, old, macros, None)
    assert report["model"] == "not_run_no_changed_clauses"


def test_missing_policy_id_is_not_silent():
    old, _, _ = sample()
    with pytest.raises(ValueError, match="no counterpart"):
        changes(old, [{"id": "other", "text": "Other"}])


def test_duplicate_macro_rejected():
    with pytest.raises(ValueError, match="Duplicate"):
        validate_records([{"id": "x", "text": "a"}, {"id": "x", "text": "b"}], "macros")


def test_empty_records_rejected():
    with pytest.raises(ValueError, match="non-empty"):
        validate_records([], "macros")


def test_matrix_shape_rejected():
    class Broken:
        def similarities(self, queries, documents):
            return []

    with pytest.raises(RuntimeError, match="shape"):
        audit(*sample(), Broken())


def test_threshold_boundaries():
    with pytest.raises(ValueError, match="threshold"):
        audit(*sample(), FakeEmbedder(), -0.1)
