# Agent Instructions

This repository is a public, reusable Python package for academic profile data processing. It is intended to help people maintain structured academic or professional data and reuse it across websites, CVs, publication lists, project pages, evidence tracking, and source-cited reporting workflows.

Keep all work self-contained and safe for public release. Do not refer to, copy from, or depend on private website repositories, private refactors, local personal data folders, or unpublished reporting records.

## Scope

Keep this repository focused on reusable data and transformation logic:

- Publication parsing, normalization, grouping, filtering, and validation.
- CV selection rules and export-preparation helpers.
- Project, activity, evidence, affiliation, service, teaching, and reporting data models.
- Validation tools and command-line interfaces.
- Theme-neutral output such as JSON, YAML, Markdown, or plain HTML fragments when appropriate.
- Optional plugin-style modules for source-cited reporting schemes, provided they remain generic and public-safe.

Do not put these concerns here:

- Personal academic records belonging to one specific site or person.
- Private evidence files, invitations, certificates, correspondence, source PDFs, or unpublished reporting records.
- Quarto theme styling, Bootstrap/SCSS design systems, presentation templates, or institution-specific website design.
- Generated website output, generated personal CV PDFs, or generated private reports.
- Data, implementation notes, or issue context copied from a private repository.

## Data and Privacy

- Treat all examples as public. Use synthetic data or clearly public sample records.
- Never copy private records from a user project into tests, examples, docs, fixtures, or snapshots.
- Do not include source documents unless their license and public status are clear. Prefer citing canonical URLs and documenting retrieval or review steps.
- Reporting-scheme data must cite its source documents and mark uncertain interpretations for human review.
- Keep test fixtures small and generic.

## Architecture

- Keep the core package independent from any one website, university, theme, or CV design.
- Put institution-specific reporting rules behind plugin or module boundaries.
- Keep parsing, validation, reporting, and rendering adapters separated.
- Prefer typed, documented data structures and stable IDs.
- Avoid hidden global configuration; make inputs and outputs explicit.
- Design command-line tools so they can run in CI without interactive prompts.

## Development Workflow

- Work on branches; do not push feature work directly to `main`.
- Use pull requests and squash merge.
- Delete branches after merge when no longer needed.
- Keep changes small and reviewable.
- Add or update tests for parsing, validation, filtering, reporting, and CLI behavior.
- Update documentation when changing public data shapes, plugin boundaries, or command behavior.
- Tag releases for usable package versions.

## Reporting Schemes

Reporting scheme modules must be public-safe and source-cited. Each plugin should document canonical public source URLs, source dates or review dates, direct source requirements, project interpretations, and ambiguous rules requiring human review.

The Icelandic public-universities plugin (`academic_profile.schemes.icelandic_universities`) is bundled and documented in `docs/reporting-schemes.md`. Its scheme data is `draft_for_review`. Verify the current public source documents before changing rules, keep Icelandic labels as published, and record unresolved differences between sources as `review_note` values instead of resolving them silently.

## Release Expectations

Before tagging a release:

- Tests should pass.
- Public APIs and CLI behavior should be documented at least briefly.
- Version or release notes should identify breaking changes.
- No private or person-specific data should be present in the repository.
