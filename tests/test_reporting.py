import pytest

from academic_profile import PointValue, ReportingScheme, ReportingSource, SchemeError
from academic_profile.reporting import SchemeEntry


def synthetic_scheme_data(**overrides):
    data = {
        "id": "synthetic-scheme",
        "title_is": "Tilbúið matskerfi",
        "status": "draft_for_review",
        "reviewed_on": "2026-01-01",
        "sources": [
            {
                "source_id": "example-2026",
                "title": "Example scheme document",
                "published_on": "2026-01",
                "reviewed_on": "2026-01-01",
                "url": "https://example.org/scheme.pdf",
                "role": "point_scheme",
            }
        ],
        "review_notes": ["Synthetic fixture, not a real scheme."],
        "sections": [
            {
                "code": "A",
                "label_is": "Rannsóknir",
                "source": ["example-2026"],
                "entries": [
                    {
                        "code": "A1",
                        "label_is": "Bækur",
                        "evidence_hint_is": "Eitt eintak af bók þarf að fylgja.",
                        "children": [
                            {"code": "A1.1", "label_is": "Ritrýnd útgáfa", "points": 20},
                            {
                                "code": "A1.2",
                                "label_is": "Aðrar bækur",
                                "points_min": 0,
                                "points_max": 5,
                                "review_note": "Range needs human review.",
                            },
                        ],
                    }
                ],
            }
        ],
    }
    data.update(overrides)
    return data


def test_scheme_builds_code_hierarchy():
    scheme = ReportingScheme.from_mapping(synthetic_scheme_data())

    assert scheme.codes() == ("A1", "A1.1", "A1.2")
    assert scheme.entry("a1.1").points == PointValue(exact=20)
    assert scheme.entry("A1.2").points.is_range is True
    assert scheme.entry("A9") is None


def test_scheme_preserves_icelandic_labels_and_hints():
    scheme = ReportingScheme.from_mapping(synthetic_scheme_data())

    assert scheme.title_is == "Tilbúið matskerfi"
    assert scheme.sections[0].label_is == "Rannsóknir"
    assert scheme.entry("A1").evidence_hint_is == "Eitt eintak af bók þarf að fylgja."


def test_scheme_reports_entries_needing_review():
    scheme = ReportingScheme.from_mapping(synthetic_scheme_data())

    assert [entry.code for entry in scheme.entries_needing_review()] == ["A1.2"]
    assert scheme.is_draft is True
    assert scheme.summary()["entries_needing_review"] == 1


def test_scheme_requires_a_cited_source():
    with pytest.raises(SchemeError, match="must cite at least one public source"):
        ReportingScheme.from_mapping(synthetic_scheme_data(sources=[]))


def test_scheme_rejects_missing_keys():
    data = synthetic_scheme_data()
    del data["reviewed_on"]

    with pytest.raises(SchemeError, match="missing key 'reviewed_on'"):
        ReportingScheme.from_mapping(data)


def test_scheme_rejects_duplicate_codes():
    data = synthetic_scheme_data()
    data["sections"][0]["entries"].append({"code": "A1", "label_is": "Tvítekið"})

    with pytest.raises(SchemeError, match="duplicate entry code A1"):
        ReportingScheme.from_mapping(data)


def test_scheme_rejects_unknown_source_reference():
    data = synthetic_scheme_data()
    data["sections"][0]["source"] = ["missing-source"]

    with pytest.raises(SchemeError, match="unknown source id 'missing-source'"):
        ReportingScheme.from_mapping(data)


def test_entry_requires_icelandic_label():
    with pytest.raises(SchemeError, match="must keep its Icelandic label"):
        SchemeEntry.from_mapping({"code": "A1", "label_is": " "})


def test_entry_keeps_unmodelled_keys_in_details():
    entry = SchemeEntry.from_mapping(
        {
            "code": "A11",
            "label_is": "Tilvitnanir",
            "tiers": [{"threshold_is": "Fyrstu 10 tilvitnanir", "points_per_citation": 1}],
        }
    )

    assert entry.points is None
    assert entry.details["tiers"][0]["points_per_citation"] == 1


def test_point_value_rejects_mixed_or_inverted_ranges():
    with pytest.raises(SchemeError, match="must not mix an exact value with a range"):
        PointValue(exact=5, maximum=10)
    with pytest.raises(SchemeError, match="minimum must not exceed its maximum"):
        PointValue(minimum=10, maximum=5)


def test_reporting_source_requires_review_date():
    with pytest.raises(ValueError, match="review date must not be empty"):
        ReportingSource(title="Example", url="https://example.org", reviewed_on=" ")
