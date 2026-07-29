from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.shared import Inches, Pt, RGBColor


OUT = Path("output/Jack_Lee_Software_Engineering_Resume.docx")
INK = "111827"
MUTED = "4B5563"
RULE = "1F4E79"


def set_cell_margins(*_args, **_kwargs):
    # Intentionally unused: this resume uses no tables for layout.
    pass


def set_font(run, name="Arial", size=None, bold=None, color=None, italic=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def add_hyperlink(paragraph, text, url, color=MUTED):
    """Add a visible external hyperlink while preserving the resume's muted contact styling."""
    relationship_id = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship_id)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), "Arial")
    fonts.set(qn("w:hAnsi"), "Arial")
    rPr.append(fonts)
    color_element = OxmlElement("w:color")
    color_element.set(qn("w:val"), color)
    rPr.append(color_element)
    font_size = OxmlElement("w:sz")
    font_size.set(qn("w:val"), "18")
    rPr.append(font_size)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "none")
    rPr.append(underline)
    run.append(rPr)
    text_element = OxmlElement("w:t")
    text_element.text = text
    run.append(text_element)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def set_paragraph_spacing(paragraph, before=0, after=0, line=1.0):
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = line


def set_keep(paragraph, keep_with_next=False, keep_together=False):
    pPr = paragraph._p.get_or_add_pPr()
    if keep_with_next:
        pPr.append(OxmlElement("w:keepNext"))
    if keep_together:
        pPr.append(OxmlElement("w:keepLines"))


def add_bottom_border(paragraph, color=RULE, size="8", space="4"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:space"), space)
    bottom.set(qn("w:color"), color)
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_custom_bullet_numbering(document):
    numbering = document.part.numbering_part.element
    abstract_id = 73
    num_id = 73

    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(abstract_id))
    multi_level = OxmlElement("w:multiLevelType")
    multi_level.set(qn("w:val"), "singleLevel")
    abstract.append(multi_level)
    level = OxmlElement("w:lvl")
    level.set(qn("w:ilvl"), "0")
    start = OxmlElement("w:start")
    start.set(qn("w:val"), "1")
    level.append(start)
    num_fmt = OxmlElement("w:numFmt")
    num_fmt.set(qn("w:val"), "bullet")
    level.append(num_fmt)
    lvl_text = OxmlElement("w:lvlText")
    lvl_text.set(qn("w:val"), "•")
    level.append(lvl_text)
    lvl_jc = OxmlElement("w:lvlJc")
    lvl_jc.set(qn("w:val"), "left")
    level.append(lvl_jc)
    pPr = OxmlElement("w:pPr")
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "num")
    tab.set(qn("w:pos"), "360")
    tabs.append(tab)
    pPr.append(tabs)
    ind = OxmlElement("w:ind")
    ind.set(qn("w:left"), "360")
    ind.set(qn("w:hanging"), "180")
    pPr.append(ind)
    level.append(pPr)
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), "Arial")
    rFonts.set(qn("w:hAnsi"), "Arial")
    rPr.append(rFonts)
    level.append(rPr)
    abstract.append(level)
    numbering.append(abstract)

    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(num_id))
    abs_ref = OxmlElement("w:abstractNumId")
    abs_ref.set(qn("w:val"), str(abstract_id))
    num.append(abs_ref)
    numbering.append(num)
    return num_id


def add_bullet(paragraph, num_id, text):
    pPr = paragraph._p.get_or_add_pPr()
    numPr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    numId = OxmlElement("w:numId")
    numId.set(qn("w:val"), str(num_id))
    numPr.append(ilvl)
    numPr.append(numId)
    pPr.append(numPr)
    run = paragraph.add_run(text)
    set_font(run, size=9.25, color=INK)
    set_paragraph_spacing(paragraph, after=2.2, line=1.05)
    set_keep(paragraph, keep_together=True)


def add_section(document, title):
    p = document.add_paragraph()
    p.style = "Resume Section"
    p.add_run(title.upper())
    return p


def add_role(document, title, employer, location, dates, num_id, bullets):
    p = document.add_paragraph()
    p.style = "Role"
    p.paragraph_format.tab_stops.add_tab_stop(Inches(6.48), WD_TAB_ALIGNMENT.RIGHT)
    r = p.add_run(title)
    set_font(r, size=9.7, bold=True, color=INK)
    r = p.add_run(f" | {employer}, {location}")
    set_font(r, size=9.7, color=INK)
    p.add_run("\t")
    r = p.add_run(dates)
    set_font(r, size=9.1, bold=True, color=MUTED)
    set_paragraph_spacing(p, before=3, after=1.2, line=1.0)
    set_keep(p, keep_with_next=True, keep_together=True)
    for item in bullets:
        bullet = document.add_paragraph()
        bullet.style = "Resume Body"
        add_bullet(bullet, num_id, item)


def add_project(document, title, technologies, num_id, bullets):
    p = document.add_paragraph()
    p.style = "Project"
    r = p.add_run(title)
    set_font(r, size=9.7, bold=True, color=INK)
    r = p.add_run(f" | {technologies}")
    set_font(r, size=9.3, italic=True, color=MUTED)
    set_paragraph_spacing(p, before=3, after=1.2, line=1.0)
    set_keep(p, keep_with_next=True, keep_together=True)
    for item in bullets:
        bullet = document.add_paragraph()
        bullet.style = "Resume Body"
        add_bullet(bullet, num_id, item)


def add_project_group(document, title):
    p = document.add_paragraph()
    p.style = "Resume Body"
    set_paragraph_spacing(p, before=3, after=0.5, line=1.0)
    r = p.add_run(title.upper())
    set_font(r, size=8.4, bold=True, color=MUTED)
    set_keep(p, keep_with_next=True, keep_together=True)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.62)
    section.bottom_margin = Inches(0.62)
    section.left_margin = Inches(0.72)
    section.right_margin = Inches(0.72)
    section.header_distance = Inches(0.3)
    section.footer_distance = Inches(0.3)

    styles = document.styles
    normal = styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    normal.font.size = Pt(9.2)
    normal.font.color.rgb = RGBColor.from_string(INK)

    for name, base in [("Resume Body", "Normal"), ("Role", "Normal"), ("Project", "Normal"), ("Resume Section", "Normal")]:
        style = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        style.base_style = styles[base]

    section_style = styles["Resume Section"]
    section_style.font.name = "Arial"
    section_style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    section_style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    section_style.font.size = Pt(10.2)
    section_style.font.bold = True
    section_style.font.color.rgb = RGBColor.from_string(RULE)
    section_style.paragraph_format.space_before = Pt(8)
    section_style.paragraph_format.space_after = Pt(2.5)

    num_id = add_custom_bullet_numbering(document)

    # Header: name and contact information. The location is intentionally city/region only.
    name = document.add_paragraph()
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(name, after=1, line=1.0)
    r = name.add_run("JACK LEE")
    set_font(r, size=19, bold=True, color=INK)

    contact = document.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(contact, after=5, line=1.0)
    add_bottom_border(contact)
    r = contact.add_run("Roscommon, Ireland  |  ")
    set_font(r, size=8.8, color=MUTED)
    add_hyperlink(contact, "jack@jack-lee.dev", "mailto:jack@jack-lee.dev")
    r = contact.add_run("  |  ")
    set_font(r, size=8.8, color=MUTED)
    add_hyperlink(contact, "linkedin.com/in/jack-lee12", "https://www.linkedin.com/in/jack-lee12")
    r = contact.add_run("  |  ")
    set_font(r, size=8.8, color=MUTED)
    add_hyperlink(contact, "github.com/JackLee504", "https://github.com/JackLee504")

    summary = document.add_paragraph()
    summary.style = "Resume Body"
    set_paragraph_spacing(summary, after=2, line=1.07)
    r = summary.add_run("Software engineering student and Ericsson intern with hands-on experience in Python CI tooling, "
                        "Jenkins and Spinnaker pipelines, cloud-native delivery workflows, and responsive client web development.")
    set_font(r, size=9.4, color=INK)

    add_section(document, "Experience")
    add_role(
        document, "Software Engineer Intern", "Ericsson", "Athlone, Ireland", "Jan 2026–Present", num_id,
        [
            "Moved from a broader support role into a central CI/CD pipeline team supporting build, test, and deployment workflows for cloud-native services.",
            "Independently decomposed a 2,000+ line Python CI component into shared and executor-specific modules across 14 modules, adding parameterisation, unit tests, and lint compliance.",
            "Develop and maintain Jenkins/Groovy and Spinnaker pipeline changes for configurable build and packaging workflows, including verification stages and test-flow improvements.",
            "Investigate build and infrastructure issues across Kubernetes, Docker, and pipeline integrations, collaborating through Gerrit review, Jira, and technical documentation.",
        ],
    )
    add_role(
        document, "Web Developer Intern", "Ossark", "Athlone, Ireland", "May 2025–Aug 2025", num_id,
        [
            "Built and refined responsive client websites using PHP and SCSS, with attention to usability and accessibility across devices.",
            "Contributed to full-stack projects with the team, helping deliver robust applications and client-facing web features.",
            "Resolved defects and optimized site performance to support smooth, reliable user experiences.",
        ],
    )
    add_role(
        document, "Cashier & Customer Service Representative", "Casey's Londis", "Roscommon, Ireland", "May 2024–Mar 2026", num_id,
        [
            "Handle high-volume transactions accurately and resolve customer issues promptly, demonstrating attention to detail and clear communication.",
            "Prioritize tasks and coordinate with teammates to maintain efficient checkout flow in a fast-paced setting.",
        ],
    )

    add_section(document, "Projects")
    add_project_group(document, "Independent Projects")
    add_project(
        document, "Deal Ledger", "Hugo, Python, GitHub Actions, Cloudflare Workers, DNS", num_id,
        [
            "Built a responsive Hugo affiliate deal-discovery site with localised interfaces and market-specific routing across English, German, Dutch, and French.",
            "Automated Amazon candidate review, listing and price validation, builds, SEO checks, alert emails, domain/DNS configuration, and Cloudflare routing with Python and GitHub Actions.",
        ],
    )
    add_project(
        document, "Multi-Broker Paper Trading Platform", "Python, APIs, SQLite, testing, observability", num_id,
        [
            "Built a modular Python paper-trading platform for FX, CFDs, and US equities, separating strategy, execution, risk, market data, journaling, and dashboards.",
            "Integrated IG, Capital.com, and Alpaca paper/demo workflows with SQLite journaling, risk checks, and automated tests.",
        ],
    )
    add_project_group(document, "University Coursework Projects")
    add_project(
        document, "Car Racing Application", "Gameplay logic, leaderboards, performance", num_id,
        [
            "Developed a racing application where users compete against bots or race for fastest-lap leaderboard rankings.",
            "Designed core gameplay and lap-time ranking mechanics with responsive interaction and reliable score handling.",
        ],
    )
    add_project(
        document, "Data Structures & Algorithmic Games", "Algorithms, persistence, game logic", num_id,
        [
            "Built a savable Binary Tree item-guessing game, Alien Invaders, and a persistence-backed A* pathfinding game.",
            "Applied data structures, algorithms, and AI/pathfinding patterns in interactive game systems.",
        ],
    )

    add_section(document, "Education")
    edu = document.add_paragraph()
    edu.style = "Role"
    edu.paragraph_format.tab_stops.add_tab_stop(Inches(6.48), WD_TAB_ALIGNMENT.RIGHT)
    r = edu.add_run("BSc (Hons) Computer Science & Information Technology")
    set_font(r, size=9.7, bold=True, color=INK)
    edu.add_run("\t")
    r = edu.add_run("Expected 2027")
    set_font(r, size=9.1, bold=True, color=MUTED)
    set_paragraph_spacing(edu, before=2, after=0, line=1.0)
    set_keep(edu, keep_with_next=True, keep_together=True)
    details = document.add_paragraph()
    details.style = "Resume Body"
    r = details.add_run("University of Galway | Expected First-Class Honours (1.1) | Relevant coursework: Database Systems, Algorithms & Data Structures, Software Engineering, Networks & Data Communications")
    set_font(r, size=9.15, color=INK)
    set_paragraph_spacing(details, after=1, line=1.03)

    school = document.add_paragraph()
    school.style = "Resume Body"
    r = school.add_run("Scoil Mhuire, Strokestown, Co. Roscommon | Leaving Certificate: 520 points (2023)")
    set_font(r, size=9.15, color=INK)
    set_paragraph_spacing(school, after=1, line=1.03)

    add_section(document, "Technical Skills")
    skills = document.add_paragraph()
    skills.style = "Resume Body"
    set_paragraph_spacing(skills, after=0, line=1.05)
    for label, value in [
        ("Languages & Scripting: ", "Python, Groovy, Bash, Java, C, SQL, JavaScript, PHP, HTML/CSS/SCSS, R"),
        ("CI/CD & Cloud-Native: ", "Jenkins, Spinnaker, Docker, Kubernetes, Helm/Helmfile, Maven, Artifactory, Nexus"),
        ("Testing & Data: ", "unit testing, pylint, pytest, pytest-cov, Bandit, pandas, NumPy"),
        ("Practices: ", "CI/CD, code review, incident investigation, root-cause analysis, Agile delivery, responsive web development"),
    ]:
        r = skills.add_run(label)
        set_font(r, size=9.15, bold=True, color=INK)
        r = skills.add_run(value)
        set_font(r, size=9.15, color=INK)
        if label != "Practices: ":
            skills.add_run("\n")
    document.core_properties.title = "Jack Lee — Resume"
    document.core_properties.author = "Jack Lee"
    document.core_properties.subject = "Software Engineering Resume"
    document.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
