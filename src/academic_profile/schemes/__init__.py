"""Optional, source-cited reporting-scheme plugins bundled with the package.

Each plugin here stays public-safe: it ships scheme structure and public source
citations only, never personal records, private evidence or source documents.
Plugins are looked up by name so private sites can consume them as ordinary
package data instead of copying scheme rules into their own repositories.
"""

from __future__ import annotations

from academic_profile.reporting import ReportingPlugin, ReportingScheme, SchemeError
from academic_profile.schemes import icelandic_universities
from academic_profile.schemes._data import load_scheme_data

_PLUGINS: dict[str, ReportingPlugin] = {
    icelandic_universities.PLUGIN.name: icelandic_universities.PLUGIN,
}

__all__ = [
    "available_schemes",
    "get_plugin",
    "icelandic_universities",
    "load_scheme",
    "load_scheme_data",
]


def available_schemes() -> tuple[str, ...]:
    """Return the names of the reporting plugins shipped with this package."""

    return tuple(sorted(_PLUGINS))


def get_plugin(name: str) -> ReportingPlugin:
    """Return the bundled reporting plugin registered under ``name``."""

    try:
        return _PLUGINS[name]
    except KeyError:
        known = ", ".join(available_schemes()) or "none"
        raise SchemeError(f"unknown reporting scheme {name!r}; available: {known}") from None


def load_scheme(name: str) -> ReportingScheme:
    """Load and validate the scheme published by a bundled plugin."""

    return get_plugin(name).scheme
