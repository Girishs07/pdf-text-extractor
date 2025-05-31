import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
import pdfplumber

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/extract-pdf/")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, "File must be a PDF")
    
    try:
        
        contents = await file.read()
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            text = "\n\n".join(
                page.extract_text() or ""  
                for page in pdf.pages
            )
        return {"extracted_text": text.strip()}
    except pdfplumber.PDFSyntaxError:
        raise HTTPException(400, "Invalid PDF file")
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")