# Agent Instructions

This repository is a public, reusable Python package for academic profile data processing. It is intended to help people maintain structured academic/professional data and reuse it across websites, CVs, publication lists, project pages, evidence tracking, and reporting workflows.

The repository must be safe for public reuse. Do not add private personal data, private evidence files, generated personal CV/site output, or institution-specific confidential material.

## Scope

Keep this repository focused on reusable data and transformation logic:

- Publication parsing, normalization, grouping, filtering, and validation.
- CV selection rules and export-preparation helpers.
- Project, activity, evidence, and reporting data models.
- Validation tools and command-line interfaces.
- Theme-neutral output for tools such as Quarto, for example JSON, YAML, Markdown, or plain HTML fragments when appropriate.
- Optional plugin-style modules for source-cited reporting schemes, provided they remain generic and public-safe.

Do not put these concerns here:

- Personal academic records belonging to one specific site or person.
- Private evidence files, invitations, certificates, correspondence, source PDFs, or unpublished reporting records.
- Quarto theme styling, Bootstrap/SCSS design systems, or presentation templates.
- Generated website output, generated personal CV PDFs, or generated private reports.

## Data and Privacy

- Treat all examples as public. Use synthetic data or clearly public sample records.
- Never copy private records from a user project into tests, examples, docs, fixtures, or snapshots.
- Do not include source documents unless their license and public status are clear. Prefer citing canonical URLs and documenting retrieval/review steps.
- Reporting-scheme data must cite its source documents and mark uncertain interpretations for review.
- Keep test fixtures small and generic.

## Architecture

- Keep the core package independent from any one website, university, theme, or CV design.
- Put institution-specific reporting rules behind plugin/module boundaries.
- Keep parsing/validation logic separate from rendering adapters.
- Prefer typed, documented data structures and stable IDs.
- Avoid hidden global configuration; make inputs and outputs explicit.
- Design command-line tools so they can run in CI without interactive prompts.

## Development Workflow

- Work on branches; do not push feature work directly to `main`.
- Use pull requests and squash merge.
- Delete branches after merge.
- Keep changes small and reviewable.
- Add or update tests for parsing, validation, filtering, reporting, and CLI behavior.
- Update documentation when changing public data shapes or command behavior.
- Tag releases for usable package versions.

## Release Expectations

Before tagging a release:

- Tests should pass.
- Public APIs and CLI behavior should be documented at least briefly.
- Version/release notes should identify breaking changes.
- No private or person-specific data should be present in the repository.