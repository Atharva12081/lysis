"""Regression checks for the recovered API and research workflows."""

import contextlib
import io
import json
import threading
import unittest
from http.client import HTTPConnection

import app
import build_embeddings as retrieval


class WorkbenchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()):
            app.ensure_index()
        cls.server = app.ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def request(self, route, body=None, raw=None):
        connection = HTTPConnection("127.0.0.1", self.port, timeout=10)
        try:
            method = "POST" if body is not None or raw is not None else "GET"
            payload = json.dumps(body) if raw is None and body is not None else raw
            connection.request(
                method, route, payload, {"Content-Type": "application/json"}
            )
            response = connection.getresponse()
            content = response.read().decode()
            data = (
                json.loads(content)
                if "application/json" in response.getheader("Content-Type", "")
                else content
            )
            return response.status, data
        finally:
            connection.close()

    def test_homepage_is_complete(self):
        status, html = self.request("/")
        self.assertEqual(status, 200)
        self.assertIn("Literature search", html)
        self.assertIn("FASTA review", html)
        self.assertNotIn("\u2014", html)

    def test_health_and_corpus(self):
        status, data = self.request("/api/health")
        self.assertEqual(status, 200)
        self.assertTrue(data["ok"])
        self.assertEqual(data["records"], 19)
        self.assertEqual(data["index_dimension"], 18)

    def test_library_and_detail(self):
        _, data = self.request("/api/papers")
        self.assertEqual(data["count"], 19)
        _, paper = self.request("/api/paper?id=P001")
        self.assertEqual(paper["paper_id"], "P001")
        self.assertTrue(paper["text"])
        self.assertEqual(self.request("/api/paper?id=missing")[0], 404)

    def test_library_filter(self):
        _, data = self.request("/api/papers?q=medcpt")
        self.assertGreater(data["count"], 0)
        self.assertLess(data["count"], 19)

    def test_search_ranking(self):
        status, data = self.request(
            "/api/search", {"query": "MedCPT biomedical retrieval", "k": 5}
        )
        self.assertEqual(status, 200)
        self.assertEqual(data["count"], 5)
        self.assertIn(data["results"][0]["paper_id"], {"P006", "P007"})
        scores = [row["score"] for row in data["results"]]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_unknown_search_is_empty(self):
        _, data = self.request("/api/search", {"query": "qzxwvvvzzzzz", "k": 5})
        self.assertEqual(data["results"], [])

    def test_search_validation(self):
        for body in (
            {"query": ""},
            {"query": "phage", "k": 0},
            {"query": "phage", "k": 21},
            {"query": "a" * 1001},
        ):
            with self.subTest(body=body):
                self.assertEqual(self.request("/api/search", body)[0], 400)

    def test_compare(self):
        status, data = self.request("/api/compare", {"paper_ids": ["P001", "P002"]})
        self.assertEqual(status, 200)
        self.assertEqual([p["paper_id"] for p in data["papers"]], ["P001", "P002"])
        self.assertTrue(all(p["text"] for p in data["papers"]))

    def test_compare_validation(self):
        for ids in (["P001"], ["P001", "P001"], ["P001", "missing"]):
            with self.subTest(ids=ids):
                self.assertEqual(
                    self.request("/api/compare", {"paper_ids": ids})[0], 400
                )

    def test_evidence_brief_has_attributed_sources(self):
        status, data = self.request(
            "/api/brief", {"query": "Pseudomonas phage antibiotic", "k": 3}
        )
        self.assertEqual(status, 200)
        self.assertEqual(len(data["records"]), 3)
        self.assertTrue(
            all(
                r["research_note"] and r["citation"] and r["source_url"]
                for r in data["records"]
            )
        )

    def test_corpus_audit(self):
        status, data = self.request("/api/audit")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "pass")
        self.assertEqual(data["unique_dois"], 19)

    def test_fasta_statistics(self):
        _, data = self.request("/api/fasta", {"fasta": ">one\nACGTNN\n>two\nGGCC"})
        self.assertTrue(data["valid"])
        self.assertEqual(data["summary"]["total_length"], 10)
        self.assertEqual(data["summary"]["n50"], 6)
        self.assertEqual(data["records"][0]["ambiguous_count"], 2)
        self.assertEqual(data["records"][1]["gc_percent"], 100)

    def test_fasta_invalid(self):
        for fasta in ("", "ACGT", ">empty", ">invalid\nACGTZ"):
            with self.subTest(fasta=fasta):
                _, data = self.request("/api/fasta", {"fasta": fasta})
                self.assertFalse(data["valid"])
                self.assertTrue(data["errors"])

    def test_reverse_complement_and_kmers(self):
        _, data = self.request("/api/sequence-analysis", {"sequence": "AACGTT", "k": 2})
        self.assertEqual(data["reverse_complement"], "AACGTT")
        self.assertEqual(sum(x["count"] for x in data["top_kmers"]), 5)

    def test_orf_candidate(self):
        sequence = "ATG" + "GCT" * 30 + "TAA"
        _, data = self.request("/api/sequence-analysis", {"sequence": sequence, "k": 3})
        candidate = next(r for r in data["orf_candidates"] if r["strand"] == "+")
        self.assertEqual(candidate["length_nt"], 96)
        self.assertEqual(candidate["start_1based"], 1)

    def test_translation(self):
        _, data = self.request("/api/translate", {"sequence": "ATGGCTNNNTAA"})
        self.assertEqual(len(data["frames"]), 6)
        self.assertEqual(data["frames"][0]["amino_acids"], "MAX*")
        self.assertEqual(data["frames"][0]["ambiguous_codons"], 1)

    def test_motif_overlap_and_reverse_strand(self):
        _, data = self.request(
            "/api/motif-scan", {"sequence": "AAAAATTT", "motif": "AAA"}
        )
        self.assertEqual(data["hit_count"], 4)
        self.assertEqual([h["start_1based"] for h in data["hits"]], [1, 2, 3, 6])
        self.assertEqual(data["hits"][-1]["strand"], "-")

    def test_degenerate_motif(self):
        _, data = self.request(
            "/api/motif-scan", {"sequence": "GAATC", "motif": "GANTC"}
        )
        self.assertTrue(any(h["start_1based"] == 1 for h in data["hits"]))

    def test_sequence_validation(self):
        for route, body in (
            ("/api/translate", {"sequence": "ACGTZ"}),
            ("/api/sequence-analysis", {"sequence": "ATG", "k": 7}),
            ("/api/motif-scan", {"sequence": "ATG", "motif": "Z"}),
        ):
            with self.subTest(route=route):
                self.assertEqual(self.request(route, body)[0], 400)

    def test_malformed_requests(self):
        self.assertEqual(self.request("/api/search", raw="{")[0], 400)
        self.assertEqual(self.request("/api/search", raw="[]")[0], 400)
        self.assertEqual(self.request("/missing")[0], 404)

    def test_index_is_reproducibly_current(self):
        self.assertTrue(retrieval.index_is_current())
        manifest = json.loads(retrieval.MANIFEST_PATH.read_text())
        self.assertEqual(
            manifest["corpus_sha256"], retrieval.sha256_file(app.CORPUS_PATH)
        )


if __name__ == "__main__":
    unittest.main()
