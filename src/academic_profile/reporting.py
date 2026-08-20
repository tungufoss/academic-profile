"""Boundaries and shared shapes for optional, source-cited reporting plugins.

This module stays scheme-neutral. It describes what every reporting scheme must
publish (sources, review status, a code hierarchy) without encoding the rules of
any one institution. Institution-specific data and rules belong in
:mod:`academic_profile.schemes` or in a separate distribution.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol

from academic_profile._records import ProfileRecord

_ENTRY_POINT_KEYS = {
    "points": "exact",
    "points_min": "minimum",
    "points_max": "maximum",
    "points_default": "default",
}

_ENTRY_KNOWN_KEYS = frozenset(
    {
        "code",
        "label_is",
        "unit_is",
        "annual_cap_points",
        "evidence_hint_is",
        "description_hint_is",
        "source",
        "review_note",
        "children",
        *_ENTRY_POINT_KEYS,
    }
)

_SECTION_KNOWN_KEYS = frozenset({"code", "label_is", "note_is", "source", "review_note", "entries"})


class SchemeError(ValueError):
    """Raised when reporting-scheme data does not match the expected shape."""


@dataclass(frozen=True, kw_only=True)
class ReportingSource:
    """Public source metadata used to implement a reporting scheme."""

    title: str
    url: str
    reviewed_on: str
    published_on: str | None = None
    source_id: str | None = None
    role: str | None = None

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("reporting source title must not be empty")
        if not self.url.strip():
            raise ValueError("reporting source URL must not be empty")
        if not self.reviewed_on.strip():
            raise ValueError("reporting source review date must not be empty")

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> ReportingSource:
        """Build a source record from plain scheme data."""

        for key in ("title", "url", "reviewed_on"):
            if key not in data:
                raise SchemeError(f"reporting source is missing key {key!r}")

        return cls(
            title=str(data["title"]),
            url=str(data["url"]),
            reviewed_on=str(data["reviewed_on"]),
            published_on=_optional_str(data.get("published_on")),
            source_id=_optional_str(data.get("source_id")),
            role=_optional_str(data.get("role")),
        )


@dataclass(frozen=True, kw_only=True)
class PointValue:
    """Points attached to a scheme entry, as a fixed value or as a range."""

    exact: float | None = None
    minimum: float | None = None
    maximum: float | None = None
    default: float | None = None

    def __post_init__(self) -> None:
        if not self.is_specified:
            raise SchemeError("point value must specify at least one of exact/min/max/default")
        if self.exact is not None and (self.minimum is not None or self.maximum is not None):
            raise SchemeError("point value must not mix an exact value with a range")
        if self.minimum is not None and self.maximum is not None and self.minimum > self.maximum:
            raise SchemeError("point value minimum must not exceed its maximum")

    @property
    def is_specified(self) -> bool:
        """Return whether any point information is present."""

        values = (self.exact, self.minimum, self.maximum, self.default)
        return any(value is not None for value in values)

    @property
    def is_range(self) -> bool:
        """Return whether the entry is scored within a range rather than exactly."""

        return self.exact is None

    def to_dict(self) -> dict[str, float]:
        """Return only the point fields that are set."""

        values = {
            "exact": self.exact,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "default": self.default,
        }
        return {key: value for key, value in values.items() if value is not None}


@dataclass(frozen=True, kw_only=True)
class SchemeEntry:
    """A single code in a reporting scheme, such as ``A4.1``.

    Icelandic labels and hints keep their original ``*_is`` names so committed
    scheme data stays close to the wording of the source documents.
    """

    code: str
    label_is: str
    points: PointValue | None = None
    unit_is: str | None = None
    annual_cap_points: float | None = None
    evidence_hint_is: str | None = None
    description_hint_is: str | None = None
    source_ids: tuple[str, ...] = ()
    review_note: str | None = None
    children: tuple[SchemeEntry, ...] = ()
    details: dict[str, Any] = field(default_factory=dict, compare=False, hash=False)

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise SchemeError("scheme entry code must not be empty")
        if not self.label_is.strip():
            raise SchemeError(f"scheme entry {self.code} must keep its Icelandic label")

    @property
    def needs_review(self) -> bool:
        """Return whether this entry carries an unresolved interpretation note."""

        return self.review_note is not None

    def walk(self) -> Iterator[SchemeEntry]:
        """Yield this entry and every descendant, depth first."""

        yield self
        for child in self.children:
            yield from child.walk()

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> SchemeEntry:
        """Build an entry, keeping unmodelled scheme keys in :attr:`details`."""

        for key in ("code", "label_is"):
            if key not in data:
                raise SchemeError(f"scheme entry is missing key {key!r}")

        points = {name: float(data[key]) for key, name in _ENTRY_POINT_KEYS.items() if data.get(key) is not None}
        return cls(
            code=str(data["code"]),
            label_is=str(data["label_is"]),
            points=PointValue(**points) if points else None,
            unit_is=_optional_str(data.get("unit_is")),
            annual_cap_points=_optional_float(data.get("annual_cap_points")),
            evidence_hint_is=_optional_str(data.get("evidence_hint_is")),
            description_hint_is=_optional_str(data.get("description_hint_is")),
            source_ids=_source_ids(data.get("source")),
            review_note=_optional_str(data.get("review_note")),
            children=tuple(SchemeEntry.from_mapping(child) for child in data.get("children", ())),
            details={key: value for key, value in data.items() if key not in _ENTRY_KNOWN_KEYS},
        )


@dataclass(frozen=True, kw_only=True)
class SchemeSection:
    """A top-level scheme section, such as ``A`` for Rannsóknir."""

    code: str
    label_is: str
    note_is: str | None = None
    review_note: str | None = None
    source_ids: tuple[str, ...] = ()
    entries: tuple[SchemeEntry, ...] = ()
    details: dict[str, Any] = field(default_factory=dict, compare=False, hash=False)

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise SchemeError("scheme section code must not be empty")
        if not self.label_is.strip():
            raise SchemeError(f"scheme section {self.code} must keep its Icelandic label")

    def walk(self) -> Iterator[SchemeEntry]:
        """Yield every entry in this section, depth first."""

        for entry in self.entries:
            yield from entry.walk()

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> SchemeSection:
        """Build a section from plain scheme data."""

        for key in ("code", "label_is"):
            if key not in data:
                raise SchemeError(f"scheme section is missing key {key!r}")

        return cls(
            code=str(data["code"]),
            label_is=str(data["label_is"]),
            note_is=_optional_str(data.get("note_is")),
            review_note=_optional_str(data.get("review_note")),
            source_ids=_source_ids(data.get("source")),
            entries=tuple(SchemeEntry.from_mapping(entry) for entry in data.get("entries", ())),
            details={key: value for key, value in data.items() if key not in _SECTION_KNOWN_KEYS},
        )


@dataclass(frozen=True, kw_only=True)
class ReportingScheme:
    """A source-cited reporting scheme described as a hierarchy of codes."""

    id: str
    title_is: str
    reviewed_on: str
    sources: tuple[ReportingSource, ...]
    sections: tuple[SchemeSection, ...]
    status: str = "draft_for_review"
    review_notes: tuple[str, ...] = ()
    rules: dict[str, Any] = field(default_factory=dict, compare=False, hash=False)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise SchemeError("scheme id must not be empty")
        if not self.title_is.strip():
            raise SchemeError("scheme must keep its Icelandic title")
        if not self.reviewed_on.strip():
            raise SchemeError(f"scheme {self.id} must record when its sources were reviewed")
        if not self.sources:
            raise SchemeError(f"scheme {self.id} must cite at least one public source")
        if not self.sections:
            raise SchemeError(f"scheme {self.id} must define at least one section")

        seen: set[str] = set()
        for entry in self.walk():
            if entry.code in seen:
                raise SchemeError(f"scheme {self.id} has duplicate entry code {entry.code}")
            seen.add(entry.code)

        known_source_ids = {source.source_id for source in self.sources if source.source_id}
        for section in self.sections:
            referenced = (*section.source_ids, *(sid for entry in section.walk() for sid in entry.source_ids))
            for source_id in referenced:
                if source_id not in known_source_ids:
                    raise SchemeError(f"scheme {self.id} references unknown source id {source_id!r}")

    @property
    def is_draft(self) -> bool:
        """Return whether the scheme still needs human review before use."""

        return self.status != "reviewed"

    def walk(self) -> Iterator[SchemeEntry]:
        """Yield every entry in every section, depth first."""

        for section in self.sections:
            yield from section.walk()

    def codes(self) -> tuple[str, ...]:
        """Return every entry code in document order."""

        return tuple(entry.code for entry in self.walk())

    def entry(self, code: str) -> SchemeEntry | None:
        """Return the entry with ``code``, or ``None`` when it is unknown."""

        normalized = code.strip().upper()
        for entry in self.walk():
            if entry.code.upper() == normalized:
                return entry
        return None

    def entries_needing_review(self) -> tuple[SchemeEntry, ...]:
        """Return entries whose interpretation is explicitly unresolved."""

        return tuple(entry for entry in self.walk() if entry.needs_review)

    def summary(self) -> dict[str, Any]:
        """Return a small, JSON-serializable overview of the scheme."""

        return {
            "id": self.id,
            "title_is": self.title_is,
            "status": self.status,
            "reviewed_on": self.reviewed_on,
            "sections": len(self.sections),
            "entries": len(self.codes()),
            "entries_needing_review": len(self.entries_needing_review()),
            "sources": [source.url for source in self.sources],
        }

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> ReportingScheme:
        """Validate and build a scheme from plain JSON/YAML-style data."""

        for key in ("id", "title_is", "reviewed_on", "sources", "sections"):
            if key not in data:
                raise SchemeError(f"reporting scheme is missing key {key!r}")

        return cls(
            id=str(data["id"]),
            title_is=str(data["title_is"]),
            reviewed_on=str(data["reviewed_on"]),
            status=str(data.get("status", "draft_for_review")),
            sources=tuple(ReportingSource.from_mapping(source) for source in data["sources"]),
            review_notes=tuple(str(note) for note in data.get("review_notes", ())),
            rules=dict(data.get("rules", {})),
            sections=tuple(SchemeSection.from_mapping(section) for section in data["sections"]),
        )


class ReportingPlugin(Protocol):
    """Interface for scheme-specific reporting packages.

    Reporting implementations should live outside the generic core when they
    encode institution-specific rules. For example, a future Icelandic
    public-universities package can expose this protocol from a separate
    distribution such as ``academic-profile-icelandic-universities``.
    """

    name: str
    sources: tuple[ReportingSource, ...]
    scheme: ReportingScheme

    def classify(self, record: ProfileRecord) -> dict[str, object]:
        """Classify a record for a public reporting scheme."""


def _optional_str(value: Any) -> str | None:
    return None if value is None else str(value)


def _optional_float(value: Any) -> float | None:
    return None if value is None else float(value)


def _source_ids(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Sequence):
        return tuple(str(item) for item in value)
    raise SchemeError(f"source reference must be a string or list, got {type(value).__name__}")
