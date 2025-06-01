from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from io import BytesIO
import uvicorn
import os
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PDF Text Extractor API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

@app.get("/")
async def root():
    return {"message": "PDF Text Extractor API is running"}

@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "healthy"}

@app.post("/debug-upload")
async def debug_upload(request: Request, file: UploadFile = None):
    """Debug endpoint to analyze the upload request"""
    try:
        # Log request details
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request URL: {request.url}")
        logger.info(f"Request headers: {dict(request.headers)}")
        
        if not file:
            logger.error("No file provided in request")
            return {
                "error": "No file provided",
                "request_info": {
                    "method": request.method,
                    "url": str(request.url),
                    "headers": dict(request.headers)
                }
            }
        
        # Get file info before reading
        logger.info(f"File filename: {file.filename}")
        logger.info(f"File content_type: {file.content_type}")
        
        # Try to get file size safely
        try:
            contents = await file.read()
            file_size = len(contents)
            logger.info(f"File size: {file_size} bytes")
            
            # Reset file pointer
            await file.seek(0)
            
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            return {
                "error": f"Error reading file: {str(e)}",
                "file_info": {
                    "filename": file.filename,
                    "content_type": file.content_type
                }
            }
        
        return {
            "success": True,
            "file_info": {
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2)
            },
            "validation_checks": {
                "has_filename": bool(file.filename),
                "is_pdf": file.filename.lower().endswith(".pdf") if file.filename else False,
                "size_ok": file_size <= MAX_FILE_SIZE,
                "not_empty": file_size > 0
            }
        }
        
    except Exception as e:
        logger.error(f"Debug upload error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "error": f"Debug error: {str(e)}",
            "traceback": traceback.format_exc()
        }

@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile):
    """Extract text from uploaded PDF file with enhanced debugging"""
    
    try:
        logger.info("=== PDF EXTRACTION REQUEST START ===")
        
        # Check 1: File exists
        if not file:
            logger.error("VALIDATION FAILED: No file provided")
            raise HTTPException(status_code=400, detail="No file provided")
        
        logger.info(f"File received: {file.filename}")
        
        # Check 2: Filename exists
        if not file.filename:
            logger.error("VALIDATION FAILED: No filename provided")
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Check 3: File extension
        if not file.filename.lower().endswith(".pdf"):
            logger.error(f"VALIDATION FAILED: Invalid file type: {file.filename}")
            raise HTTPException(status_code=400, detail=f"Only PDF files are allowed. Received: {file.filename}")
        
        # Check 4: Read file content
        try:
            logger.info("Reading file content...")
            contents = await file.read()
            file_size = len(contents)
            logger.info(f"File size: {file_size} bytes ({file_size / (1024*1024):.2f} MB)")
        except Exception as e:
            logger.error(f"VALIDATION FAILED: Error reading file: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

        # Check 5: File size
        if file_size > MAX_FILE_SIZE:
            logger.error(f"VALIDATION FAILED: File too large: {file_size} bytes")
            raise HTTPException(status_code=413, detail=f"File too large ({file_size} bytes, max {MAX_FILE_SIZE} bytes)")

        # Check 6: File not empty
        if file_size == 0:
            logger.error("VALIDATION FAILED: File is empty")
            raise HTTPException(status_code=400, detail="File is empty")
        
        logger.info("All validations passed, processing PDF...")
        
        # Process PDF
        try:
            with pdfplumber.open(BytesIO(contents)) as pdf:
                if not pdf.pages:
                    logger.error("PDF processing failed: No pages found")
                    raise HTTPException(status_code=400, detail="PDF has no pages")
                    
                logger.info(f"PDF has {len(pdf.pages)} pages")
                extracted_pages = []
                
                for i, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            extracted_pages.append(f"--- Page {i+1} ---\n{page_text}")
                        logger.info(f"Processed page {i+1}")
                    except Exception as e:
                        logger.warning(f"Error processing page {i+1}: {str(e)}")
                
                text = "\n\n".join(extracted_pages)
                
                if not text.strip():
                    logger.warning("No text extracted from PDF")
                    return {
                        "extracted_text": "No text found in the PDF", 
                        "pages_processed": len(pdf.pages),
                        "characters_extracted": 0
                    }
                
                logger.info(f"Successfully extracted {len(text.strip())} characters")
                logger.info("=== PDF EXTRACTION REQUEST END ===")
                
                return {
                    "extracted_text": text.strip(),
                    "pages_processed": len(pdf.pages),
                    "characters_extracted": len(text.strip())
                }
                
        except HTTPException:
            raise  
        except Exception as e:
            logger.error(f"PDF processing error: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
        
    except HTTPException:
        raise  
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")