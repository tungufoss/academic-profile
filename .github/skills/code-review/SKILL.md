# Code Review Skill

Use this skill when reviewing pull requests, commits, or proposed changes for `academic-profile`.

`academic-profile` is a public, reusable Python package for academic profile data processing. It may support publications, CV data preparation, projects, activities, evidence metadata, validation, command-line tools, theme-neutral rendering, and optional source-cited reporting-scheme plugins.

## Review Posture

Start with concrete risks and actionable findings. Prefer file- and line-specific comments when possible. Distinguish blocking correctness, privacy, or public-release issues from follow-up improvements.

Keep all review advice self-contained and public-safe. Do not rely on private repositories, private academic records, local user folders, unpublished reporting material, credentials, MCP settings, or secrets.

## Package Boundaries

Check that changes preserve the reusable package boundary:

- Core code is independent from any one person, website, university, Quarto theme, CV design, or reporting submission.
- Personal data, generated website output, generated personal CVs, private reports, source PDFs, invitations, certificates, correspondence, and unpublished institutional records are not added.
- Parsing, validation, reporting, rendering, CLI, and plugin logic remain separated.
- Reporting-scheme logic lives behind clear module or plugin boundaries instead of leaking into core profile models.
- Inputs and outputs are explicit; hidden global configuration, local absolute paths, and environment-specific defaults are avoided.

## Privacy and Public Safety

Treat every committed file as public. Review for:

- Real names, employment histories, publication lists, private evidence metadata, file paths, emails, account IDs, access tokens, API keys, MCP server names, plugin credentials, or copied private issue context.
- Fixtures, snapshots, examples, and docs that should be synthetic unless the source is clearly public and redistributable.
- Bundled source documents whose license or public status is unclear. Prefer canonical URLs and review notes over committed PDFs.
- Error messages, logs, snapshots, and test baselines that might expose private paths or record contents.

Block the change if it introduces private or person-specific data that is not clearly public sample data.

## Reporting-Scheme Citations

Reporting scheme support must be source-cited and human-reviewable:

- Cite canonical public source URLs for each implemented scheme.
- Record source publication dates when available and the date the source was reviewed for implementation.
- Separate direct source requirements from project interpretations.
- Flag ambiguous rules, locally variable practices, and judgment calls for human review.
- Avoid implementing rules from memory, private notes, or unstated institutional practice.
- Keep source-citation docs updated when scheme behavior changes.

If a reporting rule affects scoring, classification, eligibility, or required evidence, require a source citation or an explicit "needs human review" marker.

## Tests

Expect tests for behavior changes, especially:

- Publication parsing, normalization, grouping, filtering, and validation.
- CV selection and export-preparation logic.
- Project, activity, evidence, affiliation, service, teaching, and reporting models.
- Reporting scheme classification, scoring, ambiguity flags, and citation metadata.
- CLI argument parsing, exit codes, non-interactive CI behavior, and error messages.
- Backward-compatible behavior for public data shapes or documented outputs.

Fixtures should be small, synthetic, and easy to inspect. Tests should not depend on network access, private files, local absolute paths, or user-specific environment variables.

## API and CLI Behavior

Review public interfaces carefully:

- Public APIs should use stable, typed data structures where practical.
- CLI commands should be deterministic, scriptable, and suitable for CI without interactive prompts.
- Inputs, outputs, errors, and exit codes should be documented when behavior is public or user-facing.
- Breaking changes should be deliberate, documented, and reflected in release notes or versioning plans.
- Validation failures should be precise enough for users to fix data without exposing private content.

## Release Discipline

For release-facing changes, check that:

- Documentation describes new public APIs, CLI commands, data shapes, or plugin boundaries.
- Version metadata and release notes are updated when appropriate.
- Breaking changes are called out plainly.
- Tests pass or the PR explains any remaining test gaps.
- The repository remains safe to publish before tagging a release.

Prefer small, squash-merge-friendly changes with clear PR descriptions.

## Plugin Safety

Optional plugins and plugin-style modules must remain safe and generic:

- Plugins must not require private data, private credentials, MCP secrets, or local user configuration to import or test.
- Optional dependencies should be narrowly scoped and justified.
- Plugin boundaries should prevent institution-specific reporting rules from coupling tightly to the core package.
- Plugin fixtures and examples should be synthetic or clearly public and redistributable.
- Network calls should be avoided in tests unless explicitly mocked.
- Any source document retrieval or review process should be documented without bundling restricted material.

## Review Output

When writing a review, lead with findings ordered by severity. For each finding, include:

- The concrete risk.
- The affected file or behavior.
- The expected safer behavior.
- The smallest practical fix or test to add.

If no issues are found, say that clearly and note any residual risk, such as unrun tests or source documents that still need human verification.
