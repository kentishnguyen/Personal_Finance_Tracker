import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile, HTTPException
from app.services.validate import run_pipeline
from app.db.database import init_db
from app.db.crud import create_receipt_row, update_receipt_parsed, mark_receipt_error, list_receipts, get_receipt, summary


app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/receipts/process")
async def process_receipt(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file to disk
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    receipt_id = create_receipt_row(file_path)
    try:
        raw_ocr, parsed_data = await run_pipeline(file_path, receipt_id)
        return {"id": receipt_id, "status": "success", "data": parsed_data}

    except Exception as e:
        mark_receipt_error(receipt_id, str(e))
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/api/receipts")
def get_receipts(limit: int = 50):
    return list_receipts(limit=limit)


@app.get("/api/receipts/summary")
def get_summary(period: str = "week"):
    try:
        return summary(period=period)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/receipts/{receipt_id}")
def get_single_receipt(receipt_id: int):
    receipt = get_receipt(receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt


@app.on_event("startup")
def startup_event():
    init_db()

app.mount("/", StaticFiles(directory="static", html=True), name="static")
