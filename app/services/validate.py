from pydantic import ValidationError
from app.models import ReceiptSchema
from .ocr import run_ocr
from .llm import extract_receipt
from app.db.database import save_receipt
from db.crud import update_receipt_parsed, mark_receipt_error

async def run_pipeline(image_path: str, receipt_id: int):
    
    ocr_text = run_ocr(image_path)

    attempts = 0
    while attempts < 2:
        try:
            parsed_json = await extract_receipt(ocr_text)

            valid_data = ReceiptSchema(**parsed_json)

            update_receipt_parsed(receipt_id, ocr_text, valid_data.model_dump())

            return valid_data

        except ValidationError:
            attempts += 1
            if attempts == 2:
                raise Exception("LLM failed to return valid JSON after retry")
            print("Validation Failed. Reattempting")



