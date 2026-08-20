# Reporting Schemes

`academic-profile` may support public reporting schemes through optional plugin-style modules. Reporting plugins should be generic, source-cited, and separate from personal records or private reporting submissions.

## Source-Citation Requirements

Each reporting scheme plugin should document:

- Canonical public source URLs.
- Source publication dates and the date the source was reviewed for implementation.
- Which rules are direct requirements from the source.
- Which rules are implementation interpretations.
- Known ambiguities, local practices, or rules that require human review.

Source documents should be linked instead of bundled unless their license and redistribution status are clear.

## Icelandic Public-Universities Scheme References

Future work may include a plugin for Icelandic public-university or Matskerfi reporting. Initial public references are:

- Almennar leidbeiningar, 11 December 2024: <https://hi.is/sites/default/files/sverrirg/almennar_leidbeiningar_11.des_2024.pdf>
- Matskerfi opinberra haskola, December 2013: <https://fh.hi.is/files/2023-07/matskerfi_opinberra_haskola_des_2013.pdf>

These references are starting points only. Any implementation should review the current public sources, cite the exact reviewed documents, and flag uncertain interpretations for human review.

## Suggested Plugin Boundary

Icelandic public-universities reporting should remain outside the generic core package unless a rule is clearly reusable across reporting schemes. A future plugin can:

- Depend on `academic-profile`.
- Implement `academic_profile.reporting.ReportingPlugin`.
- Publish its source list as `ReportingSource` records.
- Keep synthetic fixtures in its own test suite.
- Return plain dictionaries or typed records that can later be rendered by separate reporting/export adapters.

This keeps `academic_profile` useful for generic publications, CV selections, projects, activities, and evidence metadata while allowing public, source-cited reporting rules to evolve independently.
