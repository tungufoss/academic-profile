# academic-profile

`academic-profile` is a public Python package for processing structured academic profile data. The package is intended to support reusable workflows around publications, CVs, projects, activities, evidence tracking, and source-cited reporting.

This repository is deliberately generic. It must not contain personal academic records, private evidence files, generated personal CVs, generated website output, private reporting records, or Quarto theme styling.

## Status

This project is in early public setup. The repository now contains an installable package skeleton with placeholder public APIs, a CLI, tests, and CI. Public APIs, command-line tools, and plugin entry points may change until a versioned release says otherwise.

## Installation

For local development:

```bash
python -m pip install -e ".[test]"
python -m pytest
academic-profile doctor
```

The import package name is `academic_profile`.

## Scope

The package may include reusable logic for:

- Parsing, normalizing, grouping, filtering, and validating publication records.
- Preparing CV data selections and export-ready profile data.
- Modeling projects, activities, evidence, affiliations, service, teaching, and related academic profile records.
- Checking data quality and producing theme-neutral outputs such as JSON, YAML, Markdown, or plain HTML fragments.
- Supporting public, source-cited reporting schemes through plugin-style modules.

## Non-Goals

This repository is not a personal website, private archive, reporting submission, or visual theme package. Do not use it for:

- Personal records belonging to one specific person or site.
- Private evidence files, correspondence, invitations, certificates, source PDFs, or unpublished institutional records.
- Generated personal CV PDFs, generated website output, or private reporting outputs.
- Quarto themes, Bootstrap/SCSS styling, presentation templates, or institution-specific web design.
- Data copied from private repositories or local folders.

## Architecture

The intended package shape is:

- `academic_profile.publications` for publication records and grouping helpers.
- `academic_profile.cv` for explicit CV/profile selection helpers.
- `academic_profile.projects`, `academic_profile.activities`, and `academic_profile.evidence` for public-safe record metadata.
- `academic_profile.reporting` for reporting source metadata and plugin protocols.
- `academic_profile.cli` for command-line tools that can run in CI without interactive prompts.

Core package code should remain independent from any one website, university, theme, or CV design. Reporting-specific logic belongs behind module or plugin boundaries so the generic profile model remains reusable.

## CLI

The current CLI is intentionally small:

```bash
academic-profile doctor
```

It verifies that the package is installed and prints a machine-readable status object. Future commands should keep inputs and outputs explicit and avoid interactive prompts by default.

## Reporting Scheme Policy

Reporting scheme modules must be source-cited and public-safe. Each scheme should:

- Cite public source documents by canonical URL.
- Record the publication date or access/review date used for implementation decisions.
- Distinguish direct source requirements from project interpretation.
- Mark ambiguous rules or locally variable practices for human review.
- Keep fixtures synthetic or clearly public.

Future work may include a plugin for Icelandic public-university reporting schemes. That code should live outside the core package, for example as a separate distribution named `academic-profile-icelandic-universities`, and implement the protocol in `academic_profile.reporting`. Initial public source references for that work are tracked in [docs/reporting-schemes.md](docs/reporting-schemes.md).

## Development

Contributions should be made on branches and reviewed through pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md) for workflow, testing, documentation, privacy, and release expectations.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
