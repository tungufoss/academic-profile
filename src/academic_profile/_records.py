"""Shared record helpers for public academic profile data."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, kw_only=True)
class ProfileRecord:
    """Base value object for stable, source-aware profile records."""

    id: str
    title: str
    tags: tuple[str, ...] = ()
    source_urls: tuple[str, ...] = ()
    extra: dict[str, Any] = field(default_factory=dict, compare=False, hash=False)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("record id must not be empty")
        if not self.title.strip():
            raise ValueError("record title must not be empty")
        if any(not tag.strip() for tag in self.tags):
            raise ValueError("record tags must not be empty")
        if any(not url.strip() for url in self.source_urls):
            raise ValueError("source URLs must not be empty")

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dictionary suitable for JSON/YAML serialization."""

        return asdict(self)
