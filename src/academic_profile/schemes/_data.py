"""Access helpers for scheme data files shipped as package data."""

from __future__ import annotations

import json
from collections.abc import Mapping
from importlib import resources
from typing import Any


def load_scheme_data(filename: str) -> Mapping[str, Any]:
    """Load raw scheme data shipped under ``academic_profile/schemes/data``."""

    source = resources.files("academic_profile.schemes").joinpath("data", filename)
    return json.loads(source.read_text(encoding="utf-8"))
