import pytest

from academic_profile import Publication, SchemeError
from academic_profile.schemes import available_schemes, get_plugin, load_scheme
from academic_profile.schemes.icelandic_universities import (
    PLUGIN,
    SCHEME_NAME,
    reporting_code,
)


def synthetic_publication(**overrides):
    fields = {
        "id": "pub-synthetic",
        "title": "Synthetic Study of Open Academic Profiles",
        "authors": ("Ada Example",),
        "year": 2026,
    }
    fields.update(overrides)
    return Publication(**fields)


def test_icelandic_scheme_is_bundled_and_valid():
    assert SCHEME_NAME in available_schemes()

    scheme = load_scheme(SCHEME_NAME)

    assert scheme.id == "matskerfi-opinberra-haskola"
    assert scheme.title_is == "Matskerfi opinberra háskóla"
    assert scheme.status == "draft_for_review"
    assert scheme.is_draft is True


def test_icelandic_scheme_cites_both_public_sources():
    urls = {source.url for source in PLUGIN.sources}

    assert urls == {
        "https://fh.hi.is/files/2023-07/matskerfi_opinberra_haskola_des_2013.pdf",
        "https://hi.is/sites/default/files/sverrirg/almennar_leidbeiningar_11.des_2024.pdf",
    }
    assert all(source.reviewed_on for source in PLUGIN.sources)
    assert all(source.published_on for source in PLUGIN.sources)


def test_icelandic_scheme_keeps_original_labels_and_points():
    scheme = load_scheme(SCHEME_NAME)

    assert [section.code for section in scheme.sections] == ["A", "B", "C", "D", "E", "F", "G"]
    assert scheme.sections[0].label_is == "Rannsóknir"
    assert scheme.entry("A1.2").label_is == "Doktorsritgerð"
    assert scheme.entry("A1.2").points.exact == 30
    assert scheme.entry("A6").annual_cap_points == 20
    assert scheme.entry("C7").unit_is == "stig/ári"


def test_icelandic_scheme_marks_uncertain_entries_for_review():
    scheme = load_scheme(SCHEME_NAME)
    flagged = {entry.code for entry in scheme.entries_needing_review()}

    assert {"A10.5", "B1.2", "D5", "D8"} <= flagged
    assert scheme.entry("A10.5").needs_review is True
    assert scheme.entry("A1.1").needs_review is False
    assert scheme.review_notes


def test_classify_uses_a_declared_code_tag():
    record = synthetic_publication(tags=("matskerfi:A4.1",))

    assert reporting_code(record) == "A4.1"

    result = PLUGIN.classify(record)

    assert result["matched"] is True
    assert result["code"] == "A4.1"
    assert result["points"] == {"exact": 20}
    assert result["label_is"].startswith("Grein birt í ISI-tímariti")
    assert "https://fh.hi.is/files/2023-07/matskerfi_opinberra_haskola_des_2013.pdf" in result["source_urls"]


def test_classify_reports_entry_review_notes():
    record = synthetic_publication(extra={"matskerfi_code": "a10.5"})

    result = PLUGIN.classify(record)

    assert result["matched"] is True
    assert result["code"] == "A10.5"
    assert result["needs_review"] is True
    assert any("patent" in note for note in result["review_notes"])


def test_classify_never_guesses_a_code():
    result = PLUGIN.classify(synthetic_publication())

    assert result["matched"] is False
    assert result["code"] is None
    assert result["needs_review"] is True
    assert result["review_notes"] == ["record pub-synthetic declares no matskerfi_code extra "
        "and no matskerfi:<code> tag"]


def test_classify_flags_unknown_codes():
    result = PLUGIN.classify(synthetic_publication(tags=("matskerfi:Z9",)))

    assert result["matched"] is False
    assert result["review_notes"] == ["code Z9 is not defined in scheme matskerfi-opinberra-haskola"]


def test_unknown_plugin_name_is_rejected():
    with pytest.raises(SchemeError, match="unknown reporting scheme 'nope'"):
        get_plugin("nope")
