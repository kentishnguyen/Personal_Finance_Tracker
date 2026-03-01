from pydantic import ValidationError
from app.models import ReceiptSchema
from .ocr import run_ocr
from .llm import extract_receipt
from app.db.crud import update_receipt_parsed, mark_receipt_error

async def run_pipeline(image_path: str, receipt_id: int):
    
    ocr_text = run_ocr(image_path)

    attempts = 0
    while attempts < 2:
        try:
            parsed_json = await extract_receipt(ocr_text)

            valid_data = ReceiptSchema(**parsed_json)

            update_receipt_parsed(receipt_id, ocr_text, valid_data.model_dump())

            return ocr_text, valid_data.model_dump()

        except (ValidationError, Exception) as e:
            attempts += 1
            print(f"Attempt {attempts} failed: {e}")
            
            if attempts == 2:
                mark_receipt_error(receipt_id, ocr_text)
                raise Exception("LLM failed to produce valid data after retries.")


