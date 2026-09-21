"""Shared layout constants, font registration, and document styles for PDFs.

This module is the single source of truth for typography, colours, margins,
and style configuration used by both the resume and the CV.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

FONT_DIR = Path(__file__).resolve().parent / "fonts"

FONT_REGULAR = "LiberationSans"
FONT_BOLD = "LiberationSans-Bold"
FONT_ITALIC = "LiberationSans-Italic"
FONT_BOLD_ITALIC = "LiberationSans-BoldItalic"

FONT_FILES = {
    FONT_REGULAR: "LiberationSans-Regular.ttf",
    FONT_BOLD: "LiberationSans-Bold.ttf",
    FONT_ITALIC: "LiberationSans-Italic.ttf",
    FONT_BOLD_ITALIC: "LiberationSans-BoldItalic.ttf",
}

INK = colors.HexColor("#111827")
MUTED = colors.HexColor("#4B5563")
RULE = colors.HexColor("#1F4E79")

INK_HEX = "#111827"
MUTED_HEX = "#4B5563"
RULE_HEX = "#1F4E79"

PAGE_SIZE = LETTER
PAGE_WIDTH, PAGE_HEIGHT = PAGE_SIZE

RESUME_MARGINS = {
    "top": 0.62 * inch,
    "bottom": 0.62 * inch,
    "left": 0.72 * inch,
    "right": 0.72 * inch,
}

CV_MARGINS = {
    "top": 0.70 * inch,
    "bottom": 0.58 * inch,
    "left": 0.68 * inch,
    "right": 0.68 * inch,
}

_fonts_registered = False


def register_fonts() -> None:
    """Register Liberation Sans once for the whole process.

    Raises if a required font file is missing so builds fail loudly instead
    of silently falling back to a font with different metrics.
    """
    global _fonts_registered
    if _fonts_registered:
        return
    for font_name, file_name in FONT_FILES.items():
        font_path = FONT_DIR / file_name
        if not font_path.exists():
            raise RuntimeError(f"Required font file missing: {font_path}")
        pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
    pdfmetrics.registerFontFamily(
        FONT_REGULAR,
        normal=FONT_REGULAR,
        bold=FONT_BOLD,
        italic=FONT_ITALIC,
        boldItalic=FONT_BOLD_ITALIC,
    )
    _fonts_registered = True


def make_document(output_path, *, title, author, subject, style):
    """Build a BaseDocTemplate with a zero-padding frame so the margins are exact.

    ReportLab's default Frame adds a 6pt internal padding on every side, which
    would silently shrink the text area. Zero padding reproduces the margins
    the DOCX template used.
    """
    margins = style.margins
    frame = Frame(
        margins["left"],
        margins["bottom"],
        PAGE_WIDTH - margins["left"] - margins["right"],
        PAGE_HEIGHT - margins["top"] - margins["bottom"],
        id="Body",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    document = BaseDocTemplate(
        str(output_path),
        pagesize=PAGE_SIZE,
        title=title,
        author=author,
        subject=subject,
    )
    document.addPageTemplates([PageTemplate(id="Main", frames=[frame])])
    return document


@dataclass(frozen=True)
class DocumentStyle:
    """Explicit style configuration for one document type.

    Using a frozen dataclass avoids the global-size mutation pattern the old
    CV builder relied on and prevents state leaking between builds.
    """

    name_size: float
    name_leading: float
    name_space_after: float

    contact_size: float
    contact_leading: float
    contact_space_before: float
    contact_space_after: float

    body_size: float
    body_leading: float

    bullet_size: float
    bullet_leading: float
    bullet_space_after: float
    bullet_indent: float
    bullet_text_indent: float

    entry_size: float
    entry_leading: float
    entry_space_before: float
    entry_space_after: float

    date_size: float

    section_size: float
    section_leading: float
    section_space_before: float
    section_space_after: float

    summary_size: float
    summary_leading: float
    summary_space_after: float

    skills_size: float
    skills_leading: float
    skills_space_after: float

    education_size: float
    education_leading: float
    education_space_after: float

    note_size: float
    note_leading: float
    note_space_before: float

    margins: dict
    date_col_padding: float


RESUME_STYLE = DocumentStyle(
    name_size=19,
    name_leading=22.0,
    name_space_after=1,
    contact_size=8.8,
    contact_leading=11.0,
    contact_space_before=0,
    contact_space_after=5.5,
    body_size=9.2,
    body_leading=11.1,
    bullet_size=9.2,
    bullet_leading=11.1,
    bullet_space_after=2.5,
    bullet_indent=9,
    bullet_text_indent=18,
    entry_size=9.7,
    entry_leading=11.3,
    entry_space_before=5,
    entry_space_after=1.6,
    date_size=9.2,
    section_size=10.2,
    section_leading=12.0,
    section_space_before=8.5,
    section_space_after=4,
    summary_size=9.4,
    summary_leading=11.0,
    summary_space_after=2,
    skills_size=9.15,
    skills_leading=10.8,
    skills_space_after=0,
    education_size=9.15,
    education_leading=10.6,
    education_space_after=1,
    note_size=9.0,
    note_leading=10.5,
    note_space_before=1.5,
    margins=RESUME_MARGINS,
    date_col_padding=1,
)

CV_STYLE = DocumentStyle(
    name_size=19,
    name_leading=22.0,
    name_space_after=1,
    contact_size=8.8,
    contact_leading=11.0,
    contact_space_before=0,
    contact_space_after=7,
    body_size=9.75,
    body_leading=11.7,
    bullet_size=9.75,
    bullet_leading=11.7,
    bullet_space_after=3.2,
    bullet_indent=9,
    bullet_text_indent=18,
    entry_size=10.2,
    entry_leading=11.9,
    entry_space_before=6,
    entry_space_after=2,
    date_size=9.55,
    section_size=10.9,
    section_leading=12.6,
    section_space_before=13.5,
    section_space_after=5.5,
    summary_size=9.9,
    summary_leading=11.8,
    summary_space_after=5,
    skills_size=10.15,
    skills_leading=13.2,
    skills_space_after=2.5,
    education_size=10.15,
    education_leading=12.9,
    education_space_after=4.5,
    note_size=9.55,
    note_leading=11.0,
    note_space_before=1.5,
    margins=CV_MARGINS,
    date_col_padding=1,
)