# Reporting Schemes

`academic-profile` supports public reporting schemes through optional plugin-style modules under `academic_profile.schemes`. Reporting plugins are generic, source-cited, and separate from personal records or private reporting submissions.

## Source-Citation Requirements

Each reporting scheme plugin should document:

- Canonical public source URLs.
- Source publication dates and the date the source was reviewed for implementation.
- Which rules are direct requirements from the source.
- Which rules are implementation interpretations.
- Known ambiguities, local practices, or rules that require human review.

Source documents are linked instead of bundled. No source PDFs are committed to this repository.

## Plugin Boundary

The core package stays scheme-neutral. `academic_profile.reporting` defines the shared shapes:

- `ReportingSource` -- one cited public document, with `url`, `published_on` and `reviewed_on`.
- `PointValue` -- an exact point value or a `minimum`/`maximum` range.
- `SchemeEntry` -- one code such as `A4.1`, with its Icelandic label, points, unit, annual cap, evidence and description hints, `review_note`, and nested `children`. Keys that the model does not cover (citation tiers, grant tiers, and similar) are preserved verbatim under `details`.
- `SchemeSection` -- a top-level section such as `A`.
- `ReportingScheme` -- the validated scheme, with `codes()`, `entry(code)`, `entries_needing_review()` and `summary()`.
- `ReportingPlugin` -- the protocol a scheme plugin implements (`name`, `sources`, `scheme`, `classify`).

`ReportingScheme.from_mapping` raises `SchemeError` when scheme data is malformed: missing keys, missing Icelandic labels, duplicate codes, unresolvable source ids, or contradictory point values. Scheme data is plain JSON, so the package needs no extra dependencies.

Institution-specific rules live in a plugin module (here) or in a separate distribution that depends on `academic-profile`. Private sites consume a scheme as an ordinary package dependency and keep their own records out of this repository.

## Icelandic Public-Universities Scheme (`icelandic-universities`)

- Module: `academic_profile.schemes.icelandic_universities`
- Data: `src/academic_profile/schemes/data/matskerfi-opinberra-haskola.json`
- Scheme id: `matskerfi-opinberra-haskola`
- Status: `draft_for_review`
- Sources reviewed on: 2026-08-20

The scheme is *Matskerfi opinberra háskóla*, used for *framtal starfa* (ársmat and grunnmat). Codes, labels and hints are kept in Icelandic exactly as published; English labels should only be added after a separate review pass.

### Sources

| Source id | Document | Published | URL | Role |
| --- | --- | --- | --- | --- |
| `matskerfi-2013` | Matskerfi opinberra háskóla | 2013-12 | <https://fh.hi.is/files/2023-07/matskerfi_opinberra_haskola_des_2013.pdf> | Point scheme |
| `almennar-leidbeiningar-2024` | Leiðbeiningar um framtal starfa (ársmat og grunnmat) | 2024-12-11 | <https://hi.is/sites/default/files/sverrirg/almennar_leidbeiningar_11.des_2024.pdf> | Evidence and entry guidance |

### Direct source requirements vs. interpretation

Direct from the sources:

- Section and entry codes, Icelandic labels, point values and ranges, annual caps, units, and the evidence/description hints.
- The multi-author division formula and the rule that no points are awarded before a satisfactory *framtal* has been submitted (`rules` in the scheme data).

Interpretation made by this package:

- The scheme is expressed as a code tree with `points` / `points_min` / `points_max` fields. The sources are prose and tables; the tree shape is this project's modelling choice.
- `classify()` never infers a code from a title, venue or record type. A record must declare its code, either as `extra["matskerfi_code"]` or as a `matskerfi:<code>` tag. Anything else is reported as `matched: false` and `needs_review: true`.
- No scoring, aggregation, or annual-total computation is implemented. Point data is exposed for human use only, because several rules are still unresolved (below).

### Open questions for human review

The bundled data is a reviewed transcription, not authoritative structured truth. The 2024 guidance is newer than the 2013 point scheme and disagrees with it in places. Those disagreements are recorded as `review_note` values rather than resolved silently, and can be listed with:

```bash
academic-profile schemes icelandic-universities --review-notes
```

The main open questions are:

- **A10.1 / A10.2** -- the 2024 guidance relabels A10.1 and narrows A10.2 to research software with an associated peer-reviewed A4 article.
- **A10.5 (Einkaleyfi)** -- the two sources give different point splits for patent applications and grants.
- **A10.7 (Nýsköpun í listum)** -- Appendix II subcodes are transcribed as a draft and need specialist review.
- **A11 (Tilvitnanir)** -- 2013 names ISI databases; 2024 refers to Web of Science or Scopus.
- **A6.1** -- possible higher assessment for very large conferences.
- **B1.2, B3.5, B4** -- teaching entries whose current point handling or code assignment differs between the sources; B3.5 has no transcribed point value.
- **D5-D8** -- the 2013 numbering differs from the 2024 guidance, where D5 is *Vísindamiðlun*, D6 is *Sprotafyrirtæki og nytjaleyfissamningar*, and D7 is *Styrkir frá öðrum en samkeppnissjóðum*.
- **F, G** -- section labels and *Frávik* handling come from the 2024 guidance only.

Because `status` is `draft_for_review`, every successful `classify()` result also carries a review note saying so. Resolving the notes and setting `status` to `reviewed` is a deliberate human step.

### Refreshing the data

1. Download both source documents from the URLs above into a local, git-ignored folder. Do not commit them.
2. Extract text and tables locally and compare the changed passages against `matskerfi-opinberra-haskola.json`.
3. Update the affected entries, the per-source `reviewed_on` dates, the top-level `reviewed_on`, and the `review_notes`.
4. Run `python -m pytest` and `academic-profile schemes --review-notes`.

## CLI

```bash
academic-profile schemes                                   # list and validate every bundled scheme
academic-profile schemes icelandic-universities            # summarize one scheme
academic-profile schemes icelandic-universities --review-notes
```

The command prints JSON and exits non-zero when scheme data fails validation, so it can be used as a CI check.
