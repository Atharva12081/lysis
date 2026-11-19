# LYSIS restoration verification

Verification date: 19 November 2026. Host: macOS, Python 3.12, locked NumPy environment.

## Source recovery

20 of 24 files matched the original manifest. The unavailable original files were `static/index.html`, `tests/test_app.py`, `tests/test_retrieval.py` and `test_results.txt`. The interface and regression suite were rebuilt. Original documentation is archived under `docs/original/`; the initial Git commit retains exact recovered source.

## Automated checks

- 21 regression tests pass, including real HTTP requests to a temporary local server.
- Python lint, formatting and bytecode compilation pass.
- Mac launcher shell lint and formatting pass.
- Retrieval smoke evaluation reproduces mean Precision@5 0.64, Hit@5 1.00 and MRR@5 1.00 across five project-team-labelled queries.

## Browser checks

Verified the user journey from interface through the local API to corpus records and rendered results:

- Literature search produces ranked papers and original publication links.
- Reading-list notes persist after reload in the same browser.
- Two-paper comparison displays attributed notes and source links.
- Evidence brief renders five source records.
- FASTA review, reverse complement and ORF analysis render results.
- Six-frame translation renders six amino-acid sequences.
- Motif scanning renders match coordinates.
- Corpus audit passes for all 19 records.

All four reference formats were downloaded and inspected. CSV and JSON each contain 19 records. BibTeX uses separated author fields and RIS includes author tags. The Mac launcher successfully starts the server. The desktop WCAG A/AA audit reports 0 violations and 0 incomplete checks; mobile has no horizontal document overflow. Offscreen mobile navigation items were manually reviewed after an automated contrast check could not inspect them.

Desktop and mobile layouts were inspected. The interface has no em dashes, gradients, bright accent colours or external font dependencies.

## Limits

Windows launch has not been executed on macOS. This does not independently validate scientific statements in the supplied corpus. The original 62-test suite was not recovered and is not claimed to have passed in this repository.
