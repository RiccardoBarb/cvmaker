import sys
import yaml

def esc(text: str) -> str:
    """Escape special LaTeX characters."""
    if not isinstance(text, str):
        text = str(text)
    for char, escaped in [
        ("&",  r"\&"),
        ("%",  r"\%"),
        ("$",  r"\$"),
        ("#",  r"\#"),
        ("_",  r"\_"),
        ("~",  r"\textasciitilde{}"),
        ("^",  r"\textasciicircum{}"),
    ]:
        text = text.replace(char, escaped)
    return text


def build_skill_tags(tags: list) -> str:
    return "\n\t\t".join(f"\\chartlabel{{{esc(t)}}}" for t in tags)


def build_skill_tools(tools: list) -> str:
    lines = []
    for t in tools:
        cat = esc(t["category"])
        items = esc(t["items"])
        lines.append(f"    \\skill{{}}{{\\textbf{{{cat}:}} \\emph{{{items}}}}}")
    return "\n".join(lines)


def build_transferable_skills(skills: list) -> str:
    lines = []
    for s in skills:
        name = esc(s["name"])
        desc = esc(s["description"].strip())
        lines.append(
            f"\t\t\\skill{{}}{{\\textbf{{{name}:}}\\emph{{\\slightlylarger{{\\\\{{{desc}}}}}}}}}"
        )
    return "\n".join(lines)


def build_work_experience(experience: list) -> str:
    lines = []
    for job in experience:
        company = job["company"]
        url = job.get("url")
        location = esc(job.get("location", ""))
        period = esc(str(job.get("period", "")))

        # Company name, linked if url provided
        if isinstance(url, str):
            company_tex = f"\\href{{{url}}}{{{esc(company)}}}"
        elif isinstance(url, list):
            parts = company.split(" / ")
            company_tex = " / ".join(
                f"\\href{{{u}}}{{{esc(p)}}}"
                for u, p in zip(url, parts)
            )
        else:
            company_tex = esc(company)

        lines.append(
            f"    \\cvitem{{\\textbf{{\\Large{{{company_tex}}}}}"
            f"\\hspace{{0.5em}}\\slightlylarger{{({period})}}"
            f"\\hspace{{0.5em}}}}{{\\slightlylarger{{{location}}}}}{{}}{{}}",
        )

        for role in job.get("roles", []):
            title = esc(role["title"])
            rperiod = esc(str(role.get("period", "")))
            summary = esc(role.get("summary", ""))
            highlights = role.get("highlights", [])

            items_tex = "\n".join(
                f"        \\item \\textbf{{{esc(h['name'])}:}} {esc(h['description'].strip())}"
                for h in highlights
            )

            lines.append(
                f"    \\cvitem{{\\Large{{{title}}}\\hspace{{0.5em}}"
                f"\\slightlylarger{{({rperiod})}}}}{{}}",
            )
            lines.append(f"    {{\\\\[-0.5em]\\slightlylarger{{\\emph{{{summary}}}}}")
            lines.append(r"    \addtolength{\leftmargini}{-1.3em}")
            lines.append(r"    \begin{itemize}")
            lines.append(r"        \setlength\itemsep{-0.1em}")
            lines.append(r"        \setlength\topsep{-0.1em}")
            lines.append(items_tex)
            lines.append(r"    \end{itemize}}")

    return "\n".join(lines)


def build_education(education: list) -> str:
    lines = []
    for entry in education:
        degree = esc(entry["degree"])
        institution = esc(entry["institution"])
        lines.append(
            f"   \\cvitem{{\\textbf{{\\large{{{degree}}}}}}}{{\\normalsize{{{institution}}}}}{{}}"
        )
    return "\n".join(lines)


def main():
    yaml_path     = sys.argv[1] if len(sys.argv) > 1 else "template.yml"
    template_path = sys.argv[2] if len(sys.argv) > 2 else "template.tex"
    output_path   = "cv.tex"

    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    with open(template_path, encoding="utf-8") as f:
        tex = f.read()

    p = data["personal"]
    ts = data.get("technical_skills", {})

    replacements = {
        "<<NAME>>":              esc(p["name"]),
        "<<ROLE>>":              esc(p["role"]),
        "<<PHONE>>":             esc(str(p.get("phone", ""))),
        "<<EMAIL>>":             esc(p.get("email", "")),
        "<<LINKEDIN>>":          esc(p.get("linkedin", "")),
        "<<GITHUB>>":            esc(p.get("github", "")),
        "<<SKILL_TAGS>>":        build_skill_tags(ts.get("tags", [])),
        "<<SKILL_TOOLS>>":       build_skill_tools(ts.get("tools", [])),
        "<<TRANSFERABLE_SKILLS>>": build_transferable_skills(data.get("transferable_skills", [])),
        "<<WORK_EXPERIENCE>>":   build_work_experience(data.get("experience", [])),
        "<<EDUCATION>>":         build_education(data.get("education", [])),
    }

    for placeholder, value in replacements.items():
        tex = tex.replace(placeholder, value)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tex)

    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()