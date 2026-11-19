"""Vercel entry point using the same handler as the local application."""

from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import app as workbench  # noqa: E402

# Deployed source is immutable. Derived index artifacts belong in scratch space.
cache = Path(tempfile.gettempdir()) / "lysis-index"
cache.mkdir(exist_ok=True)
workbench.retrieval.VECTORS_PATH = cache / "lsa_vectors.npy"
workbench.retrieval.VOCAB_PATH = cache / "lsa_vocab.json"
workbench.retrieval.META_PATH = cache / "chunk_meta.json"
workbench.retrieval.MANIFEST_PATH = cache / "lsa_index_manifest.json"


class handler(workbench.Handler):
    """Expose the request handler through Vercel's file-based Python runtime."""
