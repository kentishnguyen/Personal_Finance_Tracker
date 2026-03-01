import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from app.services.validate import run_pipeline
from db.database import init_db


app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/receipts/process")
async def process_receipt(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try: 
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not save File")
    
    try:
        result = await run_pipeline(file_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=422, detail = str(e))
    
@app.on_event("startup")
def startup_event():
    init_db()
