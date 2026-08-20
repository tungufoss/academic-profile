"""Project records for academic profile data."""

from __future__ import annotations

from dataclasses import dataclass

from academic_profile._records import ProfileRecord


@dataclass(frozen=True, kw_only=True)
class Project(ProfileRecord):
    """A public-safe project record."""

    role: str | None = None
    start_year: int | None = None
    end_year: int | None = None
