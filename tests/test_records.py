import pytest

from academic_profile import CVSelection, Publication
from academic_profile.publications import group_by_year


def test_publication_requires_stable_id():
    with pytest.raises(ValueError, match="record id"):
        Publication(id=" ", title="Example", authors=("Ada Example",), year=2026)


def test_cv_selection_filters_by_tags():
    selected = Publication(
        id="pub-selected",
        title="Selected publication",
        authors=("Ada Example",),
        year=2026,
        tags=("selected",),
    )
    hidden = Publication(
        id="pub-hidden",
        title="Hidden publication",
        authors=("Ada Example",),
        year=2025,
        tags=("private-draft",),
    )

    selection = CVSelection(include_tags=("selected",), exclude_tags=("private-draft",))

    assert selection.filter([selected, hidden]) == [selected]


def test_group_by_year_sorts_newest_first():
    older = Publication(id="older", title="Older", authors=("Ada Example",), year=2024)
    newer = Publication(id="newer", title="Newer", authors=("Ada Example",), year=2026)

    grouped = group_by_year([older, newer])

    assert list(grouped) == [2026, 2024]
    assert grouped[2026] == [newer]
