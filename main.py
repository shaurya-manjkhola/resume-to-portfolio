import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse

# Import backbone modules and the new multi-theme renderer
from core.parser import get_raw_resume_text
from core.generator import generate_portfolio_data
from core.renderer import render_portfolio_html

app = FastAPI(
    title="Resume to Portfolio Agent API",
    description="Backend engine that transforms raw resumes into structured portfolio profiles with multi-theme support.",
    version="2.0.0"
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def read_root():
    """
    Serves the interactive landing page where users pick themes and upload files.
    """
    return FileResponse("templates/index.html")


@app.post("/api/upload", response_class=HTMLResponse)
async def upload_resume(
    file: UploadFile = File(...),
    theme: str = Form("indigo")  # Captures the user's explicit theme framework selection click
):
    """
    Accepts a resume file and theme metadata selection, processes it through 
    the parsing and Gemini execution engine, and outputs optimized HTML code layouts.
    """
    filename = file.filename.lower()

    # Defensive validation: Check file type extension before writing to disk
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a valid .pdf or .docx file."
        )

    # Generate a secure path to temporarily store the uploaded file
    temp_file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Save the uploaded file stream onto the local disk
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Execute Backbone Move #1: Ingestion & Parsing
        print(f"[WEB] Parsing uploaded file: {file.filename}")
        raw_text = get_raw_resume_text(temp_file_path)

        # Execute Backbone Move #2: AI Narrative Generation & Structured Output
        print("[WEB] Triggering Gemini Narrative Pipeline...")
        structured_portfolio = generate_portfolio_data(raw_text)

        # Pass the extracted profile object AND the selected template style to our theme engine
        print(f"[WEB] Rendering HTML Portfolio Page with theme framework: {theme}...")
        html_content = render_portfolio_html(structured_portfolio, theme=theme)

        # Return raw string wrapped inside FastAPI's HTMLResponse handler
        return HTMLResponse(content=html_content, status_code=200)

    except Exception as e:
        print(f"[WEB ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # DEFENSIVE HYGIENE: Always delete the temporary file after processing to prevent disk leaks
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"[WEB] Removed temporary file: {temp_file_path}")