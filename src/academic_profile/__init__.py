"""Public package interface for academic profile data helpers."""

from academic_profile.activities import Activity
from academic_profile.cv import CVSelection
from academic_profile.evidence import Evidence
from academic_profile.projects import Project
from academic_profile.publications import Publication
from academic_profile.reporting import (
    PointValue,
    ReportingPlugin,
    ReportingScheme,
    ReportingSource,
    SchemeEntry,
    SchemeError,
    SchemeSection,
)

__all__ = [
    "Activity",
    "CVSelection",
    "Evidence",
    "PointValue",
    "Project",
    "Publication",
    "ReportingPlugin",
    "ReportingScheme",
    "ReportingSource",
    "SchemeEntry",
    "SchemeError",
    "SchemeSection",
]

__version__ = "0.1.0"
