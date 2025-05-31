from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import pdfplumber
from io import BytesIO

app = FastAPI()

@app.post("/extract-pdf/")
async def extract_pdf(file: UploadFile):
    contents = await file.read()
    with pdfplumber.open(BytesIO(contents)) as pdf:
        text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
    return JSONResponse(content={"extracted_text": text})
