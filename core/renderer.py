from core.schema import PortfolioProfile


THEMES = {
    # ---------- DARK 1: gradient hero + side facts card (inspired by dark analytics-style portfolios) ----------
    "aurora": {
        "label": "Aurora",
        "mode": "dark",
        "google_fonts": "family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600",
        "font_disp": "'Space Grotesk','Inter',sans-serif",
        "font_body": "'Inter',sans-serif",
        "bg": "#0B0E1A", "surface": "#121628", "surface2": "#171C33",
        "ink": "#F3F2FF", "ink_soft": "#B4B1DA", "ink_faint": "#6E6B96",
        "line": "#242A48",
        "accent": "#8B7CF6", "accent2": "#34D8B0",
        "radius": "16px",
        "split_hero": True, "numbered": False, "gradient_text": True, "avatar": False,
    },
    # ---------- DARK 2: monospace, numbered sections, lime accent (inspired by brutalist dev portfolios) ----------
    "terminal": {
        "label": "Terminal",
        "mode": "dark",
        "google_fonts": "family=JetBrains+Mono:wght@400;500;700",
        "font_disp": "'JetBrains Mono',monospace",
        "font_body": "'JetBrains Mono',monospace",
        "bg": "#0A0A0A", "surface": "#121212", "surface2": "#171717",
        "ink": "#F2F2F0", "ink_soft": "#9A9A96", "ink_faint": "#5C5C58",
        "line": "#2A2A28",
        "accent": "#D6FF3F", "accent2": "#7DFFE0",
        "radius": "6px",
        "split_hero": False, "numbered": True, "gradient_text": False, "avatar": False,
    },
    # ---------- LIGHT 1: warm, editorial, coral accent (inspired by warm creative portfolios) ----------
    "sunset": {
        "label": "Sunset",
        "mode": "light",
        "google_fonts": "family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600",
        "font_disp": "'Poppins','Inter',sans-serif",
        "font_body": "'Inter',sans-serif",
        "bg": "#FBF3EE", "surface": "#FFFFFF", "surface2": "#FFF7F2",
        "ink": "#2B2320", "ink_soft": "#7A6E67", "ink_faint": "#B5A89F",
        "line": "#F0DED2",
        "accent": "#E1573C", "accent2": "#F2A65A",
        "radius": "18px",
        "split_hero": False, "numbered": False, "gradient_text": False, "avatar": True,
    },
    # ---------- LIGHT 2: muted, graphite, minimal serif (inspired by studio/agency portfolios) ----------
    "studio": {
        "label": "Studio",
        "mode": "light",
        "google_fonts": "family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600",
        "font_disp": "'Fraunces','Inter',serif",
        "font_body": "'Inter',sans-serif",
        "bg": "#F3F2EF", "surface": "#FFFFFF", "surface2": "#FAFAF8",
        "ink": "#201F1C", "ink_soft": "#69675F", "ink_faint": "#A6A399",
        "line": "#E4E1DA",
        "accent": "#9C6B3F", "accent2": "#5F6B5A",
        "radius": "4px",
        "split_hero": False, "numbered": False, "gradient_text": False, "avatar": True,
    },
}


def _initials(name: str) -> str:
    parts = [p for p in name.strip().split() if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][0].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def render_portfolio_html(profile: PortfolioProfile, theme: str = "aurora") -> str:
    """
    Accepts a profile and compiles a complete, responsive portfolio website.
    Supports 4 visually distinct themes: 'aurora' and 'terminal' (dark),
    'sunset' and 'studio' (light).
    """
    t = THEMES.get(theme, THEMES["aurora"])

    def esc(s):
        return s if s else ""

    # ---- Skill badges ----
    skills_html = "".join(f'<span class="badge">{s}</span>' for s in profile.skills)

    # ---- Projects ----
    accent_cycle = [t["accent"], t["accent2"]]
    project_blocks = ""
    for i, proj in enumerate(profile.projects):
        stripe = accent_cycle[i % 2]
        tech_badges = "".join(f'<span class="badge sm">{tech}</span>' for tech in proj.tech_stack)
        github_link = (
            f'<a href="{proj.github_url}" target="_blank" class="proj-link">Source →</a>'
            if proj.github_url else ""
        )
        label = f'<span class="proj-num">{i + 1:02d}</span>' if t["numbered"] else ""
        project_blocks += f"""
        <div class="card proj-card" style="--stripe:{stripe}">
            <div class="proj-head">{label}<h3>{proj.title}</h3></div>
            <p class="proj-desc">{proj.description}</p>
            <div class="proj-foot">
                <div class="badge-row">{tech_badges}</div>
                {github_link}
            </div>
        </div>
        """

    # ---- Experience timeline ----
    experience_blocks = ""
    for exp in profile.experience:
        highlights = "".join(f"<li>{h}</li>" for h in exp.highlights)
        experience_blocks += f"""
        <div class="timeline-item">
            <div class="timeline-row">
                <h3>{exp.position}</h3>
                <span class="meta">{exp.duration}</span>
            </div>
            <p class="sub">{exp.company} · {exp.location}</p>
            <ul class="highlights">{highlights}</ul>
        </div>
        """

    # ---- Education timeline ----
    education_blocks = ""
    for edu in profile.education:
        details = f'<p class="edu-detail">{edu.details}</p>' if edu.details else ""
        education_blocks += f"""
        <div class="timeline-item">
            <div class="timeline-row">
                <h3>{edu.degree}</h3>
                <span class="meta">{edu.duration}</span>
            </div>
            <p class="sub">{edu.institution}</p>
            {details}
        </div>
        """

    # ---- Certifications (only rendered when present on the resume) ----
    certification_blocks = ""
    for cert in profile.certifications:
        date_html = f'<span class="meta">{cert.date}</span>' if cert.date else ""
        certification_blocks += f"""
        <div class="timeline-item">
            <div class="timeline-row">
                <h3>{cert.name}</h3>
                {date_html}
            </div>
            <p class="sub">{cert.issuer}</p>
        </div>
        """

    # ---- Volunteer work (only rendered when present on the resume) ----
    volunteer_blocks = ""
    for vol in profile.volunteer_work:
        desc_html = f'<p class="edu-detail">{vol.description}</p>' if vol.description else ""
        volunteer_blocks += f"""
        <div class="timeline-item">
            <div class="timeline-row">
                <h3>{vol.role}</h3>
                <span class="meta">{vol.duration}</span>
            </div>
            <p class="sub">{vol.organization}</p>
            {desc_html}
        </div>
        """

    linkedin_html = f'<a href="{profile.linkedin}" target="_blank" class="link">LinkedIn</a>' if profile.linkedin else ""
    github_html = f'<a href="{profile.github}" target="_blank" class="link">GitHub</a>' if profile.github else ""

    # ---- Section eyebrow helper (numbered vs plain) ----
    def eyebrow(idx, text):
        if t["numbered"]:
            return f'<div class="eyebrow"><span class="idx">{idx:02d}</span> — {text.upper()}</div>'
        return f'<div class="eyebrow">{text.upper()}</div>'

    # ---- Hero ----
    name_html = (
        f'<span class="grad">{profile.name}</span>' if t["gradient_text"] else profile.name
    )
    avatar_html = (
        f'<div class="avatar">{_initials(profile.name)}</div>' if t["avatar"] else ""
    )

    if t["split_hero"]:
        top_skills = " · ".join(profile.skills[:3]) if profile.skills else ""
        first_edu = profile.education[0] if profile.education else None
        hero_html = f"""
        <section class="hero split">
            <div class="hero-main">
                {eyebrow(0, "Portfolio")}
                <h1>{name_html}</h1>
                <p class="headline">{profile.headline}</p>
                <p class="bio">{profile.bio}</p>
                <div class="cta-row">
                    <a href="mailto:{profile.email}" class="btn-primary">Contact me</a>
                    {linkedin_html}
                    {github_html}
                </div>
            </div>
            <div class="facts-card">
                {f'<div class="fact"><span class="fact-label">Degree</span><span class="fact-value">{first_edu.degree}</span></div>' if first_edu else ""}
                {f'<div class="fact"><span class="fact-label">Institution</span><span class="fact-value">{first_edu.institution}</span></div>' if first_edu else ""}
                <div class="fact"><span class="fact-label">Projects</span><span class="fact-value">{len(profile.projects)}</span></div>
                <div class="fact"><span class="fact-label">Focus</span><span class="fact-value">{top_skills}</span></div>
            </div>
        </section>
        """
    else:
        hero_html = f"""
        <section class="hero">
            {avatar_html}
            {eyebrow(0, "Portfolio")}
            <h1>{name_html}</h1>
            <p class="headline">{profile.headline}</p>
            <p class="bio">{profile.bio}</p>
            <div class="cta-row">
                <a href="mailto:{profile.email}" class="btn-primary">Contact me</a>
                {linkedin_html}
                {github_html}
            </div>
        </section>
        """

    education_section = f"""
    <section class="block">
        {eyebrow(4, "Education")}
        <h2>Education</h2>
        <div class="timeline">{education_blocks}</div>
    </section>
    """ if profile.education else ""

    certifications_section = f"""
    <section class="block">
        {eyebrow(5, "Certifications")}
        <h2>Certifications</h2>
        <div class="timeline">{certification_blocks}</div>
    </section>
    """ if profile.certifications else ""

    volunteer_section = f"""
    <section class="block">
        {eyebrow(6, "Volunteer work")}
        <h2>Volunteer work</h2>
        <div class="timeline">{volunteer_blocks}</div>
    </section>
    """ if profile.volunteer_work else ""

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{profile.name} | Portfolio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?{t['google_fonts']}&display=swap" rel="stylesheet">
<style>
  :root{{
    --bg:{t['bg']}; --surface:{t['surface']}; --surface2:{t['surface2']};
    --ink:{t['ink']}; --ink-soft:{t['ink_soft']}; --ink-faint:{t['ink_faint']};
    --line:{t['line']}; --accent:{t['accent']}; --accent2:{t['accent2']};
    --radius:{t['radius']};
    --font-disp:{t['font_disp']}; --font-body:{t['font_body']};
  }}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-body);line-height:1.6}}
  h1,h2,h3{{font-family:var(--font-disp);letter-spacing:-.02em;margin:0}}
  a{{color:inherit}}
  .wrap{{max-width:880px;margin:0 auto;padding:0 24px}}

  #exportHUD{{position:sticky;top:0;z-index:50;background:var(--surface2);border-bottom:1px solid var(--line);
    display:flex;align-items:center;justify-content:space-between;padding:12px 24px;font-family:var(--font-body)}}
  #exportHUD .status{{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--ink-soft)}}
  #exportHUD .dot{{width:7px;height:7px;border-radius:50%;background:var(--accent)}}
  #exportHUD button{{font-size:12px;font-weight:600;border:1px solid var(--line);background:var(--surface);
    color:var(--ink);padding:8px 14px;border-radius:8px;cursor:pointer;margin-left:8px;font-family:var(--font-body)}}
  #exportHUD button.primary{{background:var(--accent);color:{"#0A0A0A" if t['mode']=='dark' else '#FFFFFF'};border:none}}

  .eyebrow{{font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-bottom:14px}}
  .eyebrow .idx{{color:var(--ink-faint);margin-right:4px}}

  .hero{{padding:64px 0 40px}}
  .hero h1{{font-size:42px;font-weight:700;margin-bottom:10px}}
  .hero .grad{{background:linear-gradient(100deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent}}
  .headline{{font-size:18px;color:var(--ink-soft);font-weight:500;margin:0 0 16px}}
  .bio{{font-size:15px;color:var(--ink-soft);max-width:560px;margin:0 0 24px}}
  .cta-row{{display:flex;gap:18px;align-items:center;flex-wrap:wrap}}
  .btn-primary{{background:var(--accent);color:{"#0A0A0A" if t['mode']=='dark' else '#FFFFFF'};font-weight:600;
    padding:12px 22px;border-radius:calc(var(--radius) - 4px);text-decoration:none;font-size:14px}}
  .link{{font-size:14px;font-weight:500;color:var(--ink-soft);text-decoration:none}}
  .link:hover{{color:var(--accent)}}
  .avatar{{width:56px;height:56px;border-radius:50%;background:var(--accent);color:{"#0A0A0A" if t['mode']=='dark' else '#FFFFFF'};
    display:flex;align-items:center;justify-content:center;font-family:var(--font-disp);font-weight:600;font-size:18px;margin-bottom:18px}}

  .hero.split{{display:grid;grid-template-columns:1.5fr 1fr;gap:32px;align-items:start}}
  @media(max-width:720px){{.hero.split{{grid-template-columns:1fr}}}}
  .facts-card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:22px;margin-top:10px}}
  .fact{{display:flex;flex-direction:column;gap:2px;padding:12px 0;border-bottom:1px solid var(--line)}}
  .fact:last-child{{border-bottom:none;padding-bottom:0}}
  .fact-label{{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-faint)}}
  .fact-value{{font-size:14px;font-weight:600}}

  .block{{padding:36px 0}}
  .block h2{{font-size:24px;font-weight:700;margin-bottom:18px}}

  .badge-row{{display:flex;flex-wrap:wrap;gap:8px}}
  .badge{{font-size:12px;font-weight:500;padding:6px 13px;border-radius:100px;background:var(--surface2);
    border:1px solid var(--line);color:var(--ink-soft)}}
  .badge.sm{{padding:3px 9px;font-size:11px}}

  .grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
  @media(max-width:640px){{.grid{{grid-template-columns:1fr}}}}
  .card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:22px;
    transition:transform .15s,border-color .15s}}
  .card:hover{{transform:translateY(-2px);border-color:var(--accent)}}
  .proj-card{{border-top:3px solid var(--stripe);display:flex;flex-direction:column;justify-content:space-between}}
  .proj-head{{display:flex;align-items:baseline;gap:10px;margin-bottom:8px}}
  .proj-num{{font-size:12px;color:var(--ink-faint);font-weight:600}}
  .proj-head h3{{font-size:17px;font-weight:600}}
  .proj-desc{{font-size:13.5px;color:var(--ink-soft);margin-bottom:16px}}
  .proj-foot{{display:flex;flex-direction:column;gap:10px}}
  .proj-link{{font-size:13px;font-weight:600;color:var(--accent);text-decoration:none}}

  .timeline{{display:flex;flex-direction:column;gap:26px}}
  .timeline-item{{border-left:2px solid var(--accent);padding-left:18px}}
  .timeline-row{{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px}}
  .timeline-row h3{{font-size:17px;font-weight:600}}
  .meta{{font-size:12px;color:var(--ink-faint);font-weight:500;white-space:nowrap}}
  .sub{{font-size:13.5px;color:var(--ink-soft);margin:4px 0 10px}}
  .highlights{{margin:0;padding-left:18px;font-size:13.5px;color:var(--ink-soft)}}
  .highlights li{{margin-bottom:5px}}
  .edu-detail{{font-size:12.5px;color:var(--ink-faint);font-style:italic;margin:4px 0 0}}

  footer{{padding:40px 0 60px;font-size:12px;color:var(--ink-faint);border-top:1px solid var(--line);margin-top:20px;text-align:center}}
</style>
</head>
<body>

<div id="exportHUD">
    <div class="status"><span class="dot"></span>Live preview · {t['label']} theme</div>
    <div>
        <button onclick="window.print()">Print PDF</button>
        <button class="primary" onclick="exportSourceFile()">Download site</button>
    </div>
</div>

<div class="wrap">
    {hero_html}

    <section class="block">
        {eyebrow(1, "Skills")}
        <h2>Technical skills</h2>
        <div class="badge-row">{skills_html}</div>
    </section>

    <section class="block">
        {eyebrow(2, "Selected work")}
        <h2>Projects</h2>
        <div class="grid">{project_blocks}</div>
    </section>

    <section class="block">
        {eyebrow(3, "Experience")}
        <h2>Where I've worked</h2>
        <div class="timeline">{experience_blocks}</div>
    </section>

    {education_section}

    {certifications_section}

    {volunteer_section}

    <footer>Generated portfolio · {profile.name}</footer>
</div>

<script>
    function exportSourceFile() {{
        const hud = document.getElementById("exportHUD");
        if (hud) hud.remove();
        const rawHtml = document.documentElement.outerHTML;
        const blob = new Blob([rawHtml], {{ type: "text/html" }});
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "index.html";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        document.body.insertBefore(hud, document.body.firstChild);
    }}
</script>
</body>
</html>
"""
    return html_template