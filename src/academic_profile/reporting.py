"""Boundaries for optional, source-cited reporting plugins."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from academic_profile._records import ProfileRecord


@dataclass(frozen=True, kw_only=True)
class ReportingSource:
    """Public source metadata used to implement a reporting scheme."""

    title: str
    url: str
    reviewed_on: str
    published_on: str | None = None

    def __post_init__(self) -> None:
        if not self.url.strip():
            raise ValueError("reporting source URL must not be empty")
        if not self.reviewed_on.strip():
            raise ValueError("reporting source review date must not be empty")


class ReportingPlugin(Protocol):
    """Interface for scheme-specific reporting packages.

    Reporting implementations should live outside the generic core when they
    encode institution-specific rules. For example, a future Icelandic
    public-universities package can expose this protocol from a separate
    distribution such as ``academic-profile-icelandic-universities``.
    """

    name: str
    sources: tuple[ReportingSource, ...]

    def classify(self, record: ProfileRecord) -> dict[str, object]:
        """Classify a record for a public reporting scheme."""
