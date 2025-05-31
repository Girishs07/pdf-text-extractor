from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from io import BytesIO
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 100 * 1024 * 1024  

@app.post("/extract-pdf/")
async def extract_pdf(file: UploadFile):
    file.file.seek(0, 2)  # Move to end of file
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large (max 100MB)")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files allowed")

    try:
        contents = await file.read()
        with pdfplumber.open(BytesIO(contents)) as pdf:
            text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
        return {"extracted_text": text.strip()}
    except Exception as e:
        raise HTTPException(500, f"Error processing PDF: {str(e)}")

handler = Mangum(app)
