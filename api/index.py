import os
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from io import BytesIO

app = FastAPI()

# Allow CORS (if frontend is on a different URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing only!
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Render free tier has a 10MB file limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/extract-pdf/")
async def extract_pdf(file: UploadFile):
    # Check file size
    file.file.seek(0, 2)  # Move to end of file
    file_size = file.file.tell()  # Get size in bytes
    file.file.seek(0)  # Reset cursor
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large (max 10MB)")
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files allowed")

    try:
        contents = await file.read()
        with pdfplumber.open(BytesIO(contents)) as pdf:
            text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
        return {"extracted_text": text.strip()}
    except Exception as e:
        raise HTTPException(500, f"Error processing PDF: {str(e)}")