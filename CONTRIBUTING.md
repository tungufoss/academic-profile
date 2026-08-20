# Contributing

Thank you for helping improve `academic-profile`. This repository is a public, reusable Python package, so contributions should keep the project generic, documented, testable, and safe to publish.

## Workflow

- Work on a branch, not directly on `main`.
- Open a pull request for review.
- Keep changes focused and reviewable.
- Use squash merge for completed pull requests.
- Delete merged branches when they are no longer needed.
- Tag releases only when the package is in a usable, documented state.

## Development Standards

- Prefer small, typed, well-documented data structures.
- Keep inputs and outputs explicit.
- Keep parsing, validation, reporting, and rendering concerns separated.
- Make command-line behavior suitable for CI and non-interactive use.
- Avoid adding broad dependencies unless they clearly reduce implementation or maintenance risk.

## Tests

Add or update tests when changing behavior, especially for:

- Publication parsing and normalization.
- CV selection and export-preparation logic.
- Project, activity, evidence, and reporting data models.
- Validation rules and error messages.
- Reporting scheme classification or scoring behavior.
- Command-line interfaces.

Tests should use synthetic fixtures or clearly public sample data. Keep fixtures small enough to review easily.

## Documentation

Update documentation when changing:

- Public data shapes.
- Command-line behavior.
- Plugin boundaries or entry points.
- Reporting scheme interpretation.
- Privacy or repository-boundary expectations.

Documentation for reporting schemes must identify the source documents used and make clear which behavior is directly required by a source and which behavior is project interpretation.

## Privacy and Public Data Rules

Do not commit:

- Personal academic records from a private site or local data folder.
- Private evidence files, certificates, invitations, correspondence, or unpublished source documents.
- Generated personal CVs, generated website output, or generated private reports.
- Private reporting records or institution-specific confidential material.
- Quarto theme styling, Bootstrap/SCSS design systems, or presentation templates.

Examples, fixtures, and snapshots should be synthetic unless the data is clearly public and appropriate to redistribute.

## Reporting Scheme Plugins

Reporting scheme modules are welcome when they are generic, public-safe, and source-cited. A plugin should:

- Keep scheme-specific logic outside the core package.
- Cite canonical public source URLs.
- Record source publication dates or review dates.
- Flag ambiguous interpretations for human review.
- Avoid bundling source PDFs unless redistribution rights are clear.

## Releases

Before tagging a release:

- Run the test suite.
- Confirm documentation describes public APIs and command-line behavior.
- Review the repository for private or person-specific data.
- Note breaking changes in release notes.
- Use a version tag that matches the package metadata.
