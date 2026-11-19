# LYSIS Research Desk

A local workbench for phage literature research and descriptive nucleotide analysis. The interface uses a quiet, editorial layout with warm neutrals, readable typography and clear source attribution.

## Live application

Open [lysisdesk.vercel.app](https://lysisdesk.vercel.app). Hosting details and the pending custom-domain configuration are documented in [DEPLOYMENT.md](DEPLOYMENT.md).

## Start on this Mac

Double-click **Launch.command**, keep the terminal open, then visit **http://127.0.0.1:8765**. Press **Control+C** in the terminal to stop.

Or run:

```sh
cd ~/Desktop/LYSIS
uv sync --locked
uv run --locked app.py
```

Python 3.10 or later and NumPy are required. `uv.lock` pins the environment. On first setup an internet connection is needed to install dependencies. Search and sequence analysis then run locally.

Without uv:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

## Windows

Double-click `Run_LYSIS.bat`, or run `py -m pip install -r requirements.txt` followed by `py app.py`. Windows execution has not been verified on this Mac.

## Research workflows

- **Literature search:** hybrid LSA and lexical retrieval, relevance scores, year and subject filters, configurable result count, source links and record details.
- **Paper library:** browse the 19-record starter corpus, compare two to four papers and export CSV, JSON, BibTeX or RIS references.
- **Reading list:** save papers and personal notes in browser local storage, with a JSON backup export. Keep the same browser and local address to access saved notes.
- **Evidence brief:** compile attributed corpus notes with citations and download Markdown.
- **FASTA review:** inspect format, IUPAC symbols, lengths, nucleotide composition, ambiguity and N50.
- **Sequence analysis:** reverse complement, k-mer frequencies and exploratory ORF candidates.
- **Translation:** standard-code six-frame translation with FASTA amino-acid export.
- **Motif search:** overlapping IUPAC motif matches in both orientations with 1-based coordinates.
- **Corpus and methods:** structural metadata audit and retrieval-method documentation.

All sequence tools accept pasted input. ORF coordinates on the negative strand refer to the reverse-complement sequence. Motif coordinates refer to the original supplied sequence; ambiguous motif symbols match canonical sequence bases, but ambiguous input bases are not expanded.

## Verification

```sh
uv run --locked python -m unittest discover -s tests -v
uv run --locked python evaluate_retrieval.py
ruff check .
ruff format --check .
shellcheck Launch.command
```

The restored application has 21 regression tests covering the live HTTP API, search, source details, comparison, briefs, FASTA, translation, motifs, validation and corpus integrity. Browser verification is recorded in [VALIDATION_REPORT.md](VALIDATION_REPORT.md).

The five-query retrieval smoke evaluation reproduces Precision@5 of 0.64 and Hit@5 of 1.00. These are project-team relevance judgments on a small starter corpus, not independent performance estimates.

## Recovery and source history

The source was recovered on 19 November 2026 from locally stored WhatsApp project attachments. Twenty files matched the supplied SHA-256 manifest byte for byte. Original attachment names were restored by matching their content hashes. `RECOVERY.json` records the recovery evidence without personal chat content.

The original web page, two test files and detailed test log were unavailable. The web interface and regression suite in this repository are new implementations. The recovered Python source was formatted and unused code removed. The initial Git commit preserves the exact recovered source before those changes.

Original documentation and its original manifest are retained in `docs/original/`. Their historical claims, including the original 62-test result, are not claims about this restoration. The root `SHA256_MANIFEST.json` describes the current working files.

## Scope

Educational research support. This application does not provide treatment recommendations, phage-host prediction, validated annotation, MedCPT inference, full-text ingestion or generated scientific synthesis. The 19-record corpus is distinct from the larger project survey catalogue. Inspect original publications before relying on their findings. Do not enter patient-identifiable information.

The desktop launcher binds to `127.0.0.1`. The web edition sends search and sequence inputs to the hosted application for processing. Reading notes stay in browser storage. Publication links open external sites when clicked. No visitor account or API key is needed.
