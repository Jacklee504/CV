"""Reusable ReportLab flowable components shared by the resume and CV builders.

JSON content is never read here; these functions only turn already-loaded
content plus a DocumentStyle into story flowables.
"""

from __future__ import annotations

from typing import List, Optional

from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, Table, TableStyle
from xml.sax.saxutils import escape

from .layout import (
    FONT_BOLD,
    FONT_BOLD_ITALIC,
    FONT_ITALIC,
    FONT_REGULAR,
    INK,
    MUTED,
    MUTED_HEX,
    PAGE_WIDTH,
    RULE,
    DocumentStyle,
)


def _markup(text: str) -> str:
    return escape(text)


class PdfRenderer:
    """Holds a DocumentStyle and the ParagraphStyle instances derived from it."""

    def __init__(self, style: DocumentStyle):
        self.style = style
        left = style.margins["left"]
        right = style.margins["right"]
        self.content_width = PAGE_WIDTH - left - right

        self.bullet_ps = ParagraphStyle(
            "bullet",
            fontName=FONT_REGULAR,
            fontSize=style.bullet_size,
            leading=style.bullet_leading,
            textColor=INK,
            leftIndent=style.bullet_text_indent,
            bulletIndent=style.bullet_indent,
            spaceBefore=0,
            spaceAfter=style.bullet_space_after,
            bulletFontName=FONT_REGULAR,
            bulletFontSize=style.bullet_size,
        )

        self.name_ps = ParagraphStyle(
            "name",
            fontName=FONT_BOLD,
            fontSize=style.name_size,
            leading=style.name_leading,
            textColor=INK,
            alignment=TA_CENTER,
            spaceBefore=0,
            spaceAfter=style.name_space_after,
        )

        self.contact_ps = ParagraphStyle(
            "contact",
            fontName=FONT_REGULAR,
            fontSize=style.contact_size,
            leading=style.contact_leading,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=style.contact_space_before,
            spaceAfter=style.contact_space_after,
        )

        self.section_ps = ParagraphStyle(
            "section",
            fontName=FONT_BOLD,
            fontSize=style.section_size,
            leading=style.section_leading,
            textColor=RULE,
            spaceBefore=style.section_space_before,
            spaceAfter=style.section_space_after,
        )

        self.entry_left_ps = ParagraphStyle(
            "entry_left",
            fontName=FONT_REGULAR,
            fontSize=style.entry_size,
            leading=style.entry_leading,
            textColor=INK,
            spaceBefore=style.entry_space_before,
            spaceAfter=style.entry_space_after,
        )

        self.entry_date_ps = ParagraphStyle(
            "entry_date",
            fontName=FONT_BOLD,
            fontSize=style.date_size,
            leading=style.entry_leading,
            textColor=MUTED,
            alignment=TA_RIGHT,
            spaceBefore=style.entry_space_before,
            spaceAfter=style.entry_space_after,
        )

        self.summary_ps = ParagraphStyle(
            "summary",
            fontName=FONT_REGULAR,
            fontSize=style.summary_size,
            leading=style.summary_leading,
            textColor=INK,
            spaceBefore=0,
            spaceAfter=style.summary_space_after,
        )

        self.skills_ps = ParagraphStyle(
            "skills",
            fontName=FONT_REGULAR,
            fontSize=style.skills_size,
            leading=style.skills_leading,
            textColor=INK,
            spaceBefore=0,
            spaceAfter=style.skills_space_after,
        )

        self.education_ps = ParagraphStyle(
            "education",
            fontName=FONT_REGULAR,
            fontSize=style.education_size,
            leading=style.education_leading,
            textColor=INK,
            spaceBefore=0,
            spaceAfter=style.education_space_after,
        )

        self.note_ps = ParagraphStyle(
            "note",
            fontName=FONT_ITALIC,
            fontSize=style.note_size,
            leading=style.note_leading,
            textColor=MUTED,
            spaceBefore=style.note_space_before,
            spaceAfter=0,
        )

    def header(self, name: str, contact_markup: str) -> List:
        return [
            Paragraph(_markup(name.upper()), self.name_ps),
            Paragraph(contact_markup, self.contact_ps),
            HRFlowable(
                width="100%",
                thickness=0.9,
                color=RULE,
                spaceBefore=1,
                spaceAfter=0,
            ),
        ]

    def section_heading(self, title: str) -> Paragraph:
        return Paragraph(_markup(title.upper()), self.section_ps)

    def entry_header(
        self,
        *,
        title: str,
        detail: Optional[str] = None,
        dates: Optional[str] = None,
        detail_italic: bool = False,
        title_url: Optional[str] = None,
        space_before: Optional[float] = None,
    ) -> object:
        left_text = f"<b>{_markup(title)}</b>"
        if title_url:
            url = escape(str(title_url))
            left_text = f'<a href="{url}">{left_text}</a>'
        if detail:
            detail_text = _markup(detail)
            if detail_italic:
                detail_text = f"<i>{detail_text}</i>"
            left_text += f'<font color="{MUTED_HEX}"> | {detail_text}</font>'
        left_style = self.entry_left_ps
        date_style = self.entry_date_ps
        if space_before is not None:
            left_style = ParagraphStyle(
                "entry_left_variant", parent=self.entry_left_ps, spaceBefore=space_before
            )
            date_style = ParagraphStyle(
                "entry_date_variant", parent=self.entry_date_ps, spaceBefore=space_before
            )
        left = Paragraph(left_text, left_style)

        if not dates:
            return left

        date_text = _markup(dates)
        date_width = stringWidth(date_text, FONT_BOLD, self.style.date_size)
        date_width += self.style.date_col_padding
        left_width = max(self.content_width - date_width, 1)
        table = Table(
            [[left, Paragraph(date_text, date_style)]],
            colWidths=[left_width, date_width],
            hAlign="LEFT",
        )
        table.setStyle(
            TableStyle(
                [
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        return table

    def summary_paragraph(self, text: str) -> Paragraph:
        return Paragraph(_markup(text), self.summary_ps)

    def bullet(self, text: str, *, space_after: Optional[float] = None) -> Paragraph:
        if space_after is None:
            style = self.bullet_ps
        else:
            style = ParagraphStyle(
                "bullet_variant", parent=self.bullet_ps, spaceAfter=space_after
            )
        return Paragraph(_markup(text), style, bulletText="\u2022")

    def skills(self, skills) -> Paragraph:
        lines = []
        for index, (label, value) in enumerate(skills):
            line = f"<b>{_markup(label)}:</b> {_markup(value)}"
            if index < len(skills) - 1:
                line += "<br/>"
            lines.append(line)
        return Paragraph("".join(lines), self.skills_ps)

    def education_line(self, text: str, *, space_before: float = 0) -> Paragraph:
        style = ParagraphStyle(
            "education_variant",
            parent=self.education_ps,
            spaceBefore=space_before,
        )
        return Paragraph(_markup(text), style)

    def note_paragraph(self, text: str) -> Paragraph:
        return Paragraph(_markup(text), self.note_ps)

    def plain(
        self,
        text: str,
        *,
        size: float,
        leading: float,
        space_before: float = 0,
        space_after: float = 0,
        bold: bool = False,
        italic: bool = False,
        color=INK,
        markup: bool = False,
    ) -> Paragraph:
        font = FONT_REGULAR
        if bold and italic:
            font = FONT_BOLD_ITALIC
        elif bold:
            font = FONT_BOLD
        elif italic:
            font = FONT_ITALIC
        style = ParagraphStyle(
            "plain_variant",
            fontName=font,
            fontSize=size,
            leading=leading,
            textColor=color,
            spaceBefore=space_before,
            spaceAfter=space_after,
        )
        content = text if markup else _markup(text)
        return Paragraph(content, style)


def build_contact_markup(content: dict) -> str:
    """Render the centred contact line markup used in the resume/cv header."""
    parts = [_markup(f"{content['location']}  |  Email: ")]
    parts.append(_link(content["email"], f"mailto:{content['email']}"))
    for link in content["links"]:
        parts.append(_markup("  |  "))
        parts.append(_markup(f"{link['label']}: "))
        parts.append(_link(link["username"], link["url"]))
    return "".join(parts)


def _link(text: str, url: str) -> str:
    return f'<a href="{escape(url)}">{escape(text)}</a>'


def build_role(renderer: PdfRenderer, role: dict) -> List:
    detail = f"{role['organisation']}, {role['location']}"
    flowables = [
        renderer.entry_header(title=role["title"], detail=detail, dates=role["dates"])
    ]
    for item in role["bullets"]:
        flowables.append(renderer.bullet(item))
    note = role.get("note")
    if note:
        flowables.append(renderer.note_paragraph(note))
    return flowables


def build_project(
    renderer: PdfRenderer,
    project: dict,
    *,
    with_context: bool = False,
) -> List:
    detail = project["context"] if with_context else project["technologies"]
    flowables = [
        renderer.entry_header(
            title=project["title"],
            detail=detail,
            detail_italic=True,
            title_url=project.get("url"),
            space_before=3,
        )
    ]
    if with_context:
        flowables.append(
            renderer.plain(
                project["technologies"],
                size=8.7,
                leading=10.2,
                italic=True,
                color=MUTED,
                space_after=0.5,
            )
        )
    for item in project["bullets"]:
        flowables.append(renderer.bullet(item, space_after=0))
    return flowables


def build_section(renderer: PdfRenderer, title: str, blocks: List[List]) -> List:
    """Section heading kept with its first block to avoid orphaned headings."""
    heading = renderer.section_heading(title)
    if not blocks:
        return [heading]
    return [KeepTogether([heading] + list(blocks[0]))] + [
        KeepTogether(list(block)) for block in blocks[1:]
    ]
