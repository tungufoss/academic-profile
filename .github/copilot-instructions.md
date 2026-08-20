# Copilot Instructions

This repository is a public, reusable Python package for academic profile data processing. Keep suggestions generic, public-safe, and self-contained.

## Repository Boundaries

- Do not introduce personal academic records, private evidence files, credentials, secrets, generated personal CVs, generated website output, or private reporting records.
- Keep reusable package logic separate from any one website, university, Quarto theme, CV design, or local data folder.
- Prefer explicit inputs and outputs over hidden global configuration.
- Keep parsing, validation, reporting, rendering, and plugin concerns separated.

## Review Focus

When reviewing changes, prioritize:

- Package boundaries and reusable architecture.
- Privacy and absence of personal or private data.
- Source citation and ambiguity handling for reporting-scheme rules.
- Tests for parsing, validation, filtering, reporting, and CLI behavior.
- Public API and CLI compatibility.
- Release discipline, documentation, and versioning expectations.
- Plugin safety, including dependency scope, public-safe fixtures, and no secret handling.

For detailed code-review guidance, use `.github/skills/code-review/SKILL.md`.
