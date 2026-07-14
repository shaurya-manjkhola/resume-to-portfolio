from core.schema import PortfolioProfile

def render_portfolio_html(profile: PortfolioProfile, theme: str = "indigo") -> str:
    """
    Accepts a profile and compiles a responsive portfolio website.
    Supports themes: 'indigo' (corporate), 'minimalist' (light), and 'midnight' (dark mode hacker).
    """
    
    # Define our style matrix rules mapping to Tailwind utility classes
    themes = {
        "indigo": {
            "body": "bg-gray-50 text-gray-900",
            "card": "bg-white border-gray-100 shadow-sm",
            "accent_text": "text-indigo-600",
            "accent_bg": "bg-indigo-600 hover:bg-indigo-700 text-white",
            "badge": "bg-indigo-50 text-indigo-700",
            "timeline_border": "border-indigo-500"
        },
        "minimalist": {
            "body": "bg-white text-stone-800 font-serif",
            "card": "bg-stone-50 border-stone-200 shadow-none",
            "accent_text": "text-stone-900 underline decoration-stone-400 decoration-2",
            "accent_bg": "bg-stone-900 hover:bg-stone-800 text-white",
            "badge": "bg-stone-200 text-stone-800 rounded-none",
            "timeline_border": "border-stone-800"
        },
        "midnight": {
            "body": "bg-zinc-950 text-zinc-100 font-mono",
            "card": "bg-zinc-900 border-zinc-800 shadow-xl",
            "accent_text": "text-emerald-400",
            "accent_bg": "bg-emerald-500 hover:bg-emerald-600 text-zinc-950 font-bold",
            "badge": "bg-zinc-800 text-emerald-400 border border-emerald-950",
            "timeline_border": "border-emerald-500"
        }
    }
    
    style = themes.get(theme, themes["indigo"])

    # Build repeating project components dynamically
    project_blocks = ""
    for proj in profile.projects:
        tech_badges = "".join([f"<span class='text-xs font-semibold px-2.5 py-0.5 rounded-full {style['badge']}'>{tech}</span>" for tech in proj.tech_stack])
        github_link = f"<a href='{proj.github_url}' target='_blank' class='text-sm {style['accent_text']} hover:opacity-80 mt-4 inline-block font-medium'>Source Repository →</a>" if proj.github_url else ""
        project_blocks += f"""
        <div class="rounded-xl p-6 border flex flex-col justify-between transition-all {style['card']}">
            <div>
                <h3 class="text-lg font-bold mb-2">{proj.title}</h3>
                <p class="opacity-70 text-sm mb-4 leading-relaxed font-sans">{proj.description}</p>
            </div>
            <div>
                <div class="flex flex-wrap gap-1.5 mb-2">{tech_badges}</div>
                {github_link}
            </div>
        </div>
        """

    # Build repeating timeline components dynamically
    experience_blocks = ""
    for exp in profile.experience:
        highlights_list = "".join([f"<li class='opacity-70 mb-1.5 font-sans text-sm'>• {h}</li>" for h in exp.highlights])
        experience_blocks += f"""
        <div class="mb-8 border-l-2 pl-4 {style['timeline_border']}">
            <div class="flex flex-wrap justify-between items-baseline mb-1">
                <h3 class="text-xl font-bold">{exp.position}</h3>
                <span class="text-xs opacity-60 font-medium">{exp.duration}</span>
            </div>
            <p class="text-sm font-medium mb-3 opacity-80">{exp.company} — <span class="italic text-xs">{exp.location}</span></p>
            <ul class="space-y-1">{highlights_list}</ul>
        </div>
        """

    # Build repeating education components dynamically
    education_blocks = ""
    for edu in profile.education:
        details_html = f"<p class='opacity-60 text-xs mt-1 font-sans italic'>{edu.details}</p>" if edu.details else ""
        education_blocks += f"""
        <div class="mb-6 border-l-2 pl-4 {style['timeline_border']}">
            <div class="flex flex-wrap justify-between items-baseline mb-1">
                <h3 class="text-lg font-bold">{edu.degree}</h3>
                <span class="text-xs opacity-60 font-medium">{edu.duration}</span>
            </div>
            <p class="text-sm font-medium opacity-80">{edu.institution}</p>
            {details_html}
        </div>
        """

    skills_badges = "".join([f"<span class='text-xs font-medium px-3 py-1 rounded-full {style['badge']}'>{skill}</span>" for skill in profile.skills])
    linkedin_html = f"<a href='{profile.linkedin}' target='_blank' class='opacity-60 hover:opacity-100 font-medium transition'>LinkedIn</a>" if profile.linkedin else ""
    github_html = f"<a href='{profile.github}' target='_blank' class='opacity-60 hover:opacity-100 font-medium transition'>GitHub</a>" if profile.github else ""

    # Build the full page template, embedding our Live Exporter HUD bar at the top
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{profile.name} | Portfolio</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="antialiased min-h-screen {style['body']}">
    
    <div id="exportHUD" class="bg-zinc-900 text-white px-6 py-3 flex items-center justify-between font-sans sticky top-0 z-50 border-b border-zinc-800">
        <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <p class="text-xs text-zinc-300">Live Preview Mode — Active Theme: <span class="uppercase font-bold text-white">{theme}</span></p>
        </div>
        <div class="flex items-center gap-3">
            <button onclick="window.print()" class="text-xs bg-zinc-800 hover:bg-zinc-700 text-zinc-200 px-3 py-1.5 rounded-lg transition font-medium">Print PDF</button>
            <button onclick="exportSourceFile()" class="text-xs bg-emerald-500 hover:bg-emerald-600 text-zinc-950 px-4 py-1.5 rounded-lg font-bold transition">Download Deployable Site Code</button>
        </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        <header class="mb-12 text-center md:text-left md:flex md:items-center md:justify-between border-b border-zinc-200/20 pb-8">
            <div>
                <h1 class="text-4xl font-extrabold tracking-tight sm:text-5xl">{profile.name}</h1>
                <p class="mt-3 text-xl font-medium {style['accent_text']}">{profile.headline}</p>
            </div>
            <div class="mt-6 md:mt-0 flex flex-wrap gap-4 justify-center md:justify-end text-sm items-center">
                <a href="mailto:{profile.email}" class="px-4 py-2 rounded-lg font-medium shadow-sm transition {style['accent_bg']}">Contact Me</a>
                {linkedin_html}
                {github_html}
            </div>
        </header>

        <section class="mb-12">
            <h2 class="text-2xl font-bold mb-4 tracking-tight">About Me</h2>
            <p class="text-lg leading-relaxed opacity-80 font-sans">{profile.bio}</p>
        </section>

        <section class="mb-12">
            <h2 class="text-2xl font-bold mb-4 tracking-tight">Technical Skills</h2>
            <div class="flex flex-wrap gap-2">{skills_badges}</div>
        </section>

        <section class="mb-12">
            <h2 class="text-2xl font-bold mb-6 tracking-tight">Featured Production Work</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">{project_blocks}</div>
        </section>

        <section class="mb-12">
            <h2 class="text-2xl font-bold mb-6 tracking-tight">Professional Timeline</h2>
            <div class="space-y-4">{experience_blocks}</div>
        </section>

        {f'''<section class="mb-12">
            <h2 class="text-2xl font-bold mb-6 tracking-tight">Education</h2>
            <div class="space-y-4">{education_blocks}</div>
        </section>''' if profile.education else ''}
    </div>

    <script>
        function exportSourceFile() {{
            // Remove the HUD container before generating code so the output is 100% pure static code files
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
            
            // Bring the HUD back into the visual preview after execution finishes
            document.body.insertBefore(hud, document.body.firstChild);
        }}
    </script>
</body>
</html>
"""
    return html_template