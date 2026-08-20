"""Activity records such as teaching, service, talks, and outreach."""

from __future__ import annotations

from dataclasses import dataclass

from academic_profile._records import ProfileRecord


@dataclass(frozen=True, kw_only=True)
class Activity(ProfileRecord):
    """A public-safe activity record."""

    kind: str
    year: int | None = None
    organization: str | None = None
