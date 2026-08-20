"""Reporting plugin for the Icelandic public-universities evaluation scheme.

The scheme is known in Icelandic as *Matskerfi opinberra háskóla* and is used
for *framtal starfa* (annual and baseline evaluation of academic work). Codes,
labels and hints are kept in Icelandic, as published.

Public sources
--------------

- *Matskerfi opinberra háskóla*, December 2013 --
  <https://fh.hi.is/files/2023-07/matskerfi_opinberra_haskola_des_2013.pdf>
  (point scheme)
- *Leiðbeiningar um framtal starfa (ársmat og grunnmat)*, 11 December 2024 --
  <https://hi.is/sites/default/files/sverrirg/almennar_leidbeiningar_11.des_2024.pdf>
  (evidence and entry guidance)

Both documents are linked, never bundled. The exact review date and per-source
roles are recorded in the committed scheme data.

Review status
-------------

The bundled data is ``draft_for_review``. It was transcribed from the public
source documents and reviewed by hand, but the 2024 guidance and the 2013 point
scheme disagree in several places. Those disagreements are recorded as
``review_note`` values on the affected entries instead of being resolved
silently, and are reachable through
:meth:`~academic_profile.reporting.ReportingScheme.entries_needing_review`.
Do not use this data for scoring decisions before a human has resolved the
outstanding notes against the current published rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from academic_profile._records import ProfileRecord
from academic_profile.reporting import ReportingScheme, ReportingSource
from academic_profile.schemes._data import load_scheme_data

SCHEME_NAME = "icelandic-universities"
SCHEME_FILENAME = "matskerfi-opinberra-haskola.json"
CODE_TAG_PREFIX = "matskerfi:"
CODE_EXTRA_KEY = "matskerfi_code"


@lru_cache(maxsize=1)
def load_scheme() -> ReportingScheme:
    """Load and validate the bundled Matskerfi scheme data."""

    return ReportingScheme.from_mapping(load_scheme_data(SCHEME_FILENAME))


def reporting_code(record: ProfileRecord) -> str | None:
    """Return the Matskerfi code declared on a record, if any.

    A record may declare its code either as ``extra["matskerfi_code"]`` or as a
    ``matskerfi:<code>`` tag. Nothing is inferred from titles or venues; the
    scheme requires a deliberate, reviewable classification.
    """

    declared = record.extra.get(CODE_EXTRA_KEY)
    if isinstance(declared, str) and declared.strip():
        return declared.strip()

    for tag in record.tags:
        if tag.lower().startswith(CODE_TAG_PREFIX):
            code = tag[len(CODE_TAG_PREFIX) :].strip()
            if code:
                return code
    return None


@dataclass(frozen=True)
class IcelandicUniversitiesReporting:
    """Public-safe plugin exposing the Matskerfi scheme structure."""

    name: str = SCHEME_NAME

    @property
    def scheme(self) -> ReportingScheme:
        """Return the validated scheme published by this plugin."""

        return load_scheme()

    @property
    def sources(self) -> tuple[ReportingSource, ...]:
        """Return the public source documents behind this scheme."""

        return self.scheme.sources

    def classify(self, record: ProfileRecord) -> dict[str, Any]:
        """Classify a record against the scheme using its declared code.

        The result always states whether human review is still needed: either
        because the record declares no code, because the code is unknown, or
        because the matched entry carries an unresolved interpretation note.
        """

        scheme = self.scheme
        code = reporting_code(record)
        result: dict[str, Any] = {
            "scheme": scheme.id,
            "record_id": record.id,
            "code": code,
            "matched": False,
            "needs_review": True,
            "review_notes": [],
        }

        if code is None:
            result["review_notes"] = [f"record {record.id} declares no {CODE_EXTRA_KEY}"]
            return result

        entry = scheme.entry(code)
        if entry is None:
            result["review_notes"] = [f"code {code} is not defined in scheme {scheme.id}"]
            return result

        review_notes = [] if entry.review_note is None else [entry.review_note]
        if scheme.is_draft:
            review_notes.append(f"scheme {scheme.id} is {scheme.status} and needs human review before scoring")

        result.update(
            {
                "code": entry.code,
                "matched": True,
                "label_is": entry.label_is,
                "points": None if entry.points is None else entry.points.to_dict(),
                "unit_is": entry.unit_is,
                "annual_cap_points": entry.annual_cap_points,
                "evidence_hint_is": entry.evidence_hint_is,
                "description_hint_is": entry.description_hint_is,
                "source_urls": [source.url for source in scheme.sources],
                "needs_review": bool(review_notes),
                "review_notes": review_notes,
            }
        )
        return result


PLUGIN = IcelandicUniversitiesReporting()
