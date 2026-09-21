"""Build-validation tests for the direct JSON-to-PDF pipeline."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from build_cv import build_cv
from build_resume import build_resume

REQUIRED_TEXT = ("Jack Lee", "Ericsson", "University of Galway")


class PdfBuildTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def pdf_path(self, filename: str) -> Path:
        return Path(self.tmp.name) / filename

    def assert_uri_links(self, path: Path) -> None:
        reader = PdfReader(str(path))
        count = 0
        for page in reader.pages:
            annots = page.get("/Annots")
            if not annots:
                continue
            for ref in annots:
                action = ref.get_object().get("/A")
                if action is not None and action.get("/S") == "/URI":
                    count += 1
        self.assertGreater(count, 0, f"{path} should contain clickable links")

    def assert_required_text(self, path: Path) -> None:
        reader = PdfReader(str(path))
        text = "".join(page.extract_text() or "" for page in reader.pages).lower()
        for item in REQUIRED_TEXT:
            self.assertIn(item.lower(), text, f"{item!r} missing from {path}")

    def test_resume_builds_to_single_page(self) -> None:
        path = build_resume(output_path=self.pdf_path("resume.pdf"))
        reader = PdfReader(str(path))
        self.assertEqual(len(reader.pages), 1, "resume must be exactly one page")
        self.assert_required_text(path)
        self.assert_uri_links(path)

    def test_cv_builds_to_two_pages(self) -> None:
        path = build_cv(output_path=self.pdf_path("cv.pdf"))
        reader = PdfReader(str(path))
        self.assertEqual(len(reader.pages), 2, "CV must be exactly two pages")
        self.assert_required_text(path)
        self.assert_uri_links(path)

    def test_resume_output_is_pdf_with_letter_size(self) -> None:
        path = build_resume(output_path=self.pdf_path("resume.pdf"))
        reader = PdfReader(str(path))
        box = reader.pages[0].mediabox
        self.assertAlmostEqual(float(box.width), 612.0, places=1)
        self.assertAlmostEqual(float(box.height), 792.0, places=1)

    def test_cv_output_is_pdf_with_letter_size(self) -> None:
        path = build_cv(output_path=self.pdf_path("cv.pdf"))
        reader = PdfReader(str(path))
        box = reader.pages[0].mediabox
        self.assertAlmostEqual(float(box.width), 612.0, places=1)
        self.assertAlmostEqual(float(box.height), 792.0, places=1)


if __name__ == "__main__":
    unittest.main()