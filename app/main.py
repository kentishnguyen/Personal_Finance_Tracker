import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile, HTTPException
from app.services.validate import run_pipeline
from db.database import init_db
from db.crud import create_receipt_row, update_receipt_parsed, mark_receipt_error


app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/receipts/process")
async def process_receipt(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    receipt_id = create_receipt_row(file_path)
    try: 
        raw_ocr, parsed_data = await run_pipeline(file_path)
        update_receipt_parsed(receipt_id, raw_ocr, parsed_data)
        return {"id": receipt_id, "status": "success", "data": parsed_data}
    

    except Exception as e:
        mark_receipt_error(receipt_id, str(e))
        raise HTTPException(status_code=422, detail=str(e))
    
    
    
@app.on_event("startup")
def startup_event():
    init_db()

app.mount("/", StaticFiles(directory="static", html=true), name="static")
