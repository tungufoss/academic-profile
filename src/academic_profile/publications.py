"""Publication records and lightweight grouping helpers."""

from __future__ import annotations

from dataclasses import dataclass

from academic_profile._records import ProfileRecord


@dataclass(frozen=True, kw_only=True)
class Publication(ProfileRecord):
    """A normalized publication record."""

    authors: tuple[str, ...]
    year: int
    venue: str | None = None
    doi: str | None = None


def group_by_year(publications: list[Publication] | tuple[Publication, ...]) -> dict[int, list[Publication]]:
    """Group publications by year, newest year first."""

    grouped: dict[int, list[Publication]] = {}
    for publication in publications:
        grouped.setdefault(publication.year, []).append(publication)
    return dict(sorted(grouped.items(), reverse=True))
