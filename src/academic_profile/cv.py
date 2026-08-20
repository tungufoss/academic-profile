"""Selection helpers for CV and profile exports."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeVar

from academic_profile._records import ProfileRecord


class RecordFilter(Protocol):
    """Callable boundary for custom CV filtering rules."""

    def __call__(self, record: ProfileRecord) -> bool: ...


TRecord = TypeVar("TRecord", bound=ProfileRecord)


@dataclass(frozen=True, kw_only=True)
class CVSelection:
    """Simple, explicit selection criteria for export-ready profile records."""

    include_tags: tuple[str, ...] = ()
    exclude_tags: tuple[str, ...] = ()

    def includes(self, record: ProfileRecord) -> bool:
        """Return whether a record matches the selection criteria."""

        tags = set(record.tags)
        if self.include_tags and not tags.intersection(self.include_tags):
            return False
        if tags.intersection(self.exclude_tags):
            return False
        return True

    def filter(self, records: list[TRecord] | tuple[TRecord, ...]) -> list[TRecord]:
        """Return records that match this selection."""

        return [record for record in records if self.includes(record)]
