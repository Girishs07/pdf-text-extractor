import io
from fastapi import FastAPI, File, UploadFile, HTTPException
import pdfplumber

app = FastAPI()

@app.post("/extract-pdf/")
async def extract_pdf(file: UploadFile = File(...)):
    print("Received content type:", file.content_type)  # 👈 For debugging

    # ✅ Relaxed check to allow more content-type variations
    if "pdf" not in (file.content_type or ""):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        contents = await file.read()
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n\n"
        return {"extracted_text": text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting PDF: {str(e)}")

