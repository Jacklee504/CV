"""Build both documents (resume and CV) as direct PDFs."""

from __future__ import annotations

import build_cv
import build_resume


def build_documents():
    """Generate both PDF outputs by importing and calling the builders directly."""
    build_resume.build_resume()
    build_cv.build_cv()


if __name__ == "__main__":
    build_documents()