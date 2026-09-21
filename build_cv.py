"""Build the full CV PDF directly from content/cv.json."""

from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfReader

from pdf.components import (
    PdfRenderer,
    build_contact_markup,
    build_project,
    build_role,
    build_section,
)
from pdf.layout import CV_STYLE, make_document, register_fonts


REQUIRED_TEXT = ("Jack Lee", "Ericsson", "University of Galway")


def build_cv(
    content_path: Path = Path("content/cv.json"),
    output_path: Path = Path("output/Jack_Lee_CV.pdf"),
) -> Path:
    """Generate the two-page CV PDF from the JSON content source."""
    try:
        content = json.loads(content_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise RuntimeError(f"Content file not found: {content_path}")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {content_path}: {exc}") from exc

    register_fonts()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    renderer = PdfRenderer(CV_STYLE)
    story = build_cv_story(renderer, content)

    document = make_document(
        output_path,
        title=f"{content['name']} - Curriculum Vitae",
        author=content["name"],
        subject="Curriculum Vitae",
        style=CV_STYLE,
    )
    document.build(story)
    validate_cv(output_path)
    print(output_path)
    return output_path


def build_cv_story(renderer: PdfRenderer, content: dict):
    story = []
    story.extend(renderer.header(content["name"], build_contact_markup(content)))

    story.extend(
        build_section(
            renderer, "Profile", [[renderer.summary_paragraph(content["profile"])]]
        )
    )

    experience_blocks = [build_role(renderer, role) for role in content["experience"]]
    story.extend(build_section(renderer, "Professional Experience", experience_blocks))

    story.extend(
        build_section(
            renderer, "Technical Skills", [[renderer.skills(content["skills"])]]
        )
    )

    project_blocks = [
        build_project(renderer, project, with_context=True)
        for project in content["projects"]
    ]
    story.extend(build_section(renderer, "Selected Projects", project_blocks))

    story.extend(build_section(renderer, "Education", build_education(renderer, content["education"])))

    additional_blocks = [
        add_additional_entry(renderer, entry, index, len(content["additional_experience"]))
        for index, entry in enumerate(content["additional_experience"])
    ]
    story.extend(build_section(renderer, "Additional Experience", additional_blocks))

    activity_blocks = [
        [
            renderer.plain(
                activity,
                size=CV_STYLE.education_size,
                leading=CV_STYLE.education_leading,
                space_after=3 if index < len(content["activities"]) - 1 else 0,
            )
        ]
        for index, activity in enumerate(content["activities"])
    ]
    story.extend(build_section(renderer, "Activities & Interests", activity_blocks))
    return story


def build_education(renderer: PdfRenderer, education: dict):
    blocks = []
    details = [education["institution"]] + list(education["details"])
    degree_block = [
        renderer.entry_header(title=education["degree"], dates=education["dates"])
    ]
    degree_block.extend(
        renderer.plain(
            detail,
            size=CV_STYLE.education_size,
            leading=CV_STYLE.education_leading,
            space_after=6 if index == len(details) - 1 else 0,
        )
        for index, detail in enumerate(details)
    )
    blocks.append(degree_block)

    secondary = education["secondary"]
    blocks.append(
        [
            renderer.entry_header(
                title=secondary["qualification"],
                dates=secondary["dates"],
            ),
            renderer.plain(
                secondary["institution"],
                size=CV_STYLE.education_size,
                leading=CV_STYLE.education_leading,
            ),
            renderer.plain(
                secondary["details"],
                size=CV_STYLE.education_size,
                leading=CV_STYLE.education_leading,
            ),
        ]
    )
    return blocks


def add_additional_entry(renderer: PdfRenderer, entry: dict, index: int, total: int):
    detail = f"{entry['organisation']}, {entry['location']}"
    block = [
        renderer.entry_header(title=entry["title"], detail=detail, dates=entry["dates"])
    ]
    for item in entry["bullets"]:
        block.append(renderer.bullet(item))
    block.append(
        renderer.plain(
            entry["note"],
            size=CV_STYLE.education_size,
            leading=CV_STYLE.education_leading,
            space_after=4 if index < total - 1 else 0,
        )
    )
    return block


def validate_cv(path: Path) -> None:
    reader = PdfReader(str(path))
    page_count = len(reader.pages)
    if page_count != 2:
        raise RuntimeError(f"CV PDF must be exactly 2 pages, generated {page_count} pages: {path}")
    text = "".join(page.extract_text() or "" for page in reader.pages).lower()
    missing = [item for item in REQUIRED_TEXT if item.lower() not in text]
    if missing:
        raise RuntimeError(f"CV PDF missing expected text {missing}: {path}")
    link_count = sum(
        len(_uri_annotations(page)) for page in reader.pages
    )
    if link_count == 0:
        raise RuntimeError(f"CV PDF contains no clickable links: {path}")


def _uri_annotations(page) -> list:
    annots = page.get("/Annots")
    if not annots:
        return []
    links = []
    for ref in annots:
        annot = ref.get_object()
        action = annot.get("/A")
        if action is not None and action.get("/S") == "/URI":
            links.append(action.get("/URI"))
    return links


if __name__ == "__main__":
    build_cv()
