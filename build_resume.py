"""Build the recruiter-facing resume PDF directly from content/resume.json."""

from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfReader

from pdf.components import PdfRenderer, build_contact_markup, build_project, build_role, build_section
from pdf.layout import RESUME_STYLE, make_document, register_fonts


REQUIRED_TEXT = ("Jack Lee", "Ericsson", "University of Galway")


def build_resume(
    content_path: Path = Path("content/resume.json"),
    output_path: Path = Path("output/Jack_Lee_Software_Engineering_Resume.pdf"),
) -> Path:
    """Generate the one-page resume PDF from the JSON content source."""
    try:
        content = json.loads(content_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise RuntimeError(f"Content file not found: {content_path}")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {content_path}: {exc}") from exc

    register_fonts()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    renderer = PdfRenderer(RESUME_STYLE)
    story = build_resume_story(renderer, content)

    document = make_document(
        output_path,
        title=f"{content['name']} - Resume",
        author=content["name"],
        subject="Software Engineering Resume",
        style=RESUME_STYLE,
    )
    document.build(story)
    validate_resume(output_path)
    print(output_path)
    return output_path


def build_resume_story(renderer: PdfRenderer, content: dict):
    story = []
    story.extend(renderer.header(content["name"], build_contact_markup(content)))
    story.append(renderer.summary_paragraph(content["summary"]))

    experience_blocks = [build_role(renderer, role) for role in content["experience"]]
    story.extend(build_section(renderer, "Experience", experience_blocks))

    project_blocks = [build_project(renderer, project) for project in content["projects"]]
    story.extend(build_section(renderer, "Projects", project_blocks))

    story.extend(
        build_section(
            renderer, "Technical Skills", [[renderer.skills(content["skills"])]]
        )
    )

    education = content["education"]
    degree_block = [
        renderer.entry_header(title=education["degree"], dates=education["dates"]),
        renderer.plain(
            education["details"],
            size=RESUME_STYLE.education_size,
            leading=RESUME_STYLE.education_leading,
            space_after=1,
        ),
    ]
    story.extend(build_section(renderer, "Education", [degree_block]))

    secondary = education["secondary"]
    story.append(
        renderer.plain(
            f"{secondary['qualification']} | {secondary['details']}",
            size=RESUME_STYLE.education_size,
            leading=RESUME_STYLE.education_leading,
            space_before=3,
            space_after=1,
        )
    )

    if content.get("other_experience"):
        story.append(
            renderer.plain(
                content["other_experience"],
                size=RESUME_STYLE.education_size,
                leading=RESUME_STYLE.education_leading,
                space_before=3,
            )
        )
    return story


def validate_resume(path: Path) -> None:
    reader = PdfReader(str(path))
    page_count = len(reader.pages)
    if page_count != 1:
        raise RuntimeError(
            f"Resume PDF must be exactly 1 page, generated {page_count} pages: {path}"
        )
    text = "".join(page.extract_text() or "" for page in reader.pages).lower()
    missing = [item for item in REQUIRED_TEXT if item.lower() not in text]
    if missing:
        raise RuntimeError(f"Resume PDF missing expected text {missing}: {path}")
    if _link_annotations(reader) == 0:
        raise RuntimeError(f"Resume PDF contains no clickable links: {path}")


def _link_annotations(reader: PdfReader) -> int:
    count = 0
    for page in reader.pages:
        annots = page.get("/Annots")
        if not annots:
            continue
        for ref in annots:
            annot = ref.get_object()
            action = annot.get("/A")
            if action is not None and action.get("/S") == "/URI":
                count += 1
    return count


if __name__ == "__main__":
    build_resume()