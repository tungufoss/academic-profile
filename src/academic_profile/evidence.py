"""Evidence metadata records without storing private evidence files."""

from __future__ import annotations

from dataclasses import dataclass

from academic_profile._records import ProfileRecord


@dataclass(frozen=True, kw_only=True)
class Evidence(ProfileRecord):
    """Metadata for public, citeable evidence."""

    evidence_type: str
    reviewed_on: str | None = None
    note: str | None = None
