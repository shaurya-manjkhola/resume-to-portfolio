# Resume to Portfolio Agent

Upload a resume (PDF or DOCX), pick a visual theme, and get back a complete,
responsive portfolio website — generated from the resume's content, not just
a reformatted copy of it.

## How it works

1. **Parse** — `core/parser.py` extracts raw text from the uploaded PDF or DOCX.
2. **Generate** — `core/generator.py` sends that text to Gemini, which structures
   it into a `PortfolioProfile` (name, headline, bio, experience, projects,
   education, skills) and expands thin bullet points into real narrative —
   without inventing facts that aren't in the resume.
3. **Render** — `core/renderer.py` turns the structured profile into a full
   responsive HTML page, styled according to the theme you picked
   (`aurora`, `terminal`, `sunset`, or `studio`).

## Setup

**Requirements:** Python 3.10+

```bash
git clone git@github.com:shaurya-manjkhola/resume-to-portfolio.git
cd resume-to-portfolio
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

## Running it

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000** in your browser. Pick a theme, upload a resume
(`.pdf` or `.docx`), and submit. The generated portfolio site is returned
directly in the browser.

## Sample input / output

- Sample input resume: `samples/test_resume.pdf`
- To generate a sample output, run the app, upload that resume, and save the
  resulting page (`Ctrl+S` in your browser, or use the "Download Deployable
  Site Code" button on the generated page) as a standalone `.html` file.

## Project structure

```
main.py                 FastAPI app: serves the upload page, handles /api/upload
core/parser.py           PDF/DOCX text extraction
core/schema.py           Pydantic schema the LLM output is forced into
core/generator.py        Gemini call: raw text -> structured PortfolioProfile
core/renderer.py         Structured profile -> full HTML page (3 themes)
templates/index.html     Upload page / theme picker UI
samples/                 Sample resume for local testing
```

## Notes

- Themes: **Aurora** (dark, gradient), **Terminal** (dark, monospace), **Sunset** (light, warm/editorial), **Studio** (light, muted/serif).
- If a resume has no education section, education is simply omitted from the
  generated site rather than shown empty.
- Generation runs Gemini with a fallback chain (`gemini-2.5-flash` →
  `gemini-1.5-flash` → `gemini-1.5-pro`) in case a model is unavailable.