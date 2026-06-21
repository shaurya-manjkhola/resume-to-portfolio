import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

from core.parser import get_raw_resume_text
from core.generator import generate_portfolio_data
from core.renderer import render_portfolio_html

app = FastAPI(
    title="Resume to Portfolio Agent API",
    description="Backend engine that transforms raw resumes into structured portfolio profiles.",
    version="1.0.0"
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def read_root():
    """
    Serves the landing page.
    """
    return FileResponse("templates/index.html")


@app.post("/api/upload", response_class=HTMLResponse)
async def upload_resume(file: UploadFile = File(...)):
    filename = file.filename.lower()

    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a valid .pdf or .docx file."
        )

    temp_file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"[WEB] Parsing uploaded file: {file.filename}")
        raw_text = get_raw_resume_text(temp_file_path)

        print("[WEB] Triggering Gemini Narrative Pipeline...")
        structured_portfolio = generate_portfolio_data(raw_text)

        print("[WEB] Rendering HTML Portfolio Page...")
        html_content = render_portfolio_html(structured_portfolio)

        return HTMLResponse(content=html_content, status_code=200)

    except Exception as e:
        print(f"[WEB ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"[WEB] Removed temporary file: {temp_file_path}")