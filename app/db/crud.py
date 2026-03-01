# this is a data access layer
# handles all the CRUD operations
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.db.database import get_db_connection

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
# this should be called right after saving the upload
# this creates the image path and timestamp only (like an empty record ready when a user uploads a file)
def create_receipt_row(image_path: str) -> int:
    
    with get_db_connection() as conn:
        cur = conn.execute(
            "INSERT INTO receipts (image_path, status, created_at) VALUES (?, 'uploaded', ?)",
            (image_path, _now_iso()),
        )
        conn.commit()
        return int(cur.lastrowid) #id of the empty record row --> so that we can update it once the AI finishes reading the receipt

# this is the save receipt function
# this adds store_name, purchase date, total, parsed json objects
def update_receipt_parsed(receipt_id: int, raw_ocr_text: str, parsed: Dict[str, Any]) -> None:
    
    store_name = parsed.get("store_name")
    purchase_date = parsed.get("purchase_date") 
    total = parsed.get("total")
    parsed_json_str = json.dumps(parsed, ensure_ascii=False) #this converts a dict into a string --> to be stored in a single database column (parsed_json column)

    with get_db_connection() as conn:
        conn.execute(
            """
            UPDATE receipts
            SET raw_ocr_text = ?,
                parsed_json = ?,
                store_name = ?,
                purchase_date = ?,
                total = ?,
        
                status = 'parsed'
            WHERE id = ?
            """,
            (raw_ocr_text, parsed_json_str, store_name, purchase_date, total, receipt_id),
        )
        conn.commit()

#handle error when pipeline (the AI) fails to read the image
def mark_receipt_error(receipt_id: int, raw_ocr_text: Optional[str] = None) -> None:
   
    with get_db_connection() as conn:
        conn.execute(
            """
            UPDATE receipts
            SET status = 'error',
                raw_ocr_text = COALESCE(?, raw_ocr_text)
            WHERE id = ?
            """,
            (raw_ocr_text, receipt_id),
        )
        conn.commit()

#Used by GET /api/receipts
#lists max 50 receipts
def list_receipts(limit: int = 50) -> List[dict]:
    
    with get_db_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, store_name, purchase_date, total, status, created_at
            FROM receipts
            ORDER BY datetime(created_at) DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]

#Used by GET /api/receipts/{id}
#just to get/pull a single receipt to view
def get_receipt(receipt_id: int) -> Optional[dict]:
    
    with get_db_connection() as conn:
        row = conn.execute("SELECT * FROM receipts WHERE id = ?", (receipt_id,)).fetchone()
    if not row:
        return None
    d = dict(row)
    if d.get("parsed_json"):
        try:
            d["parsed_json"] = json.loads(d["parsed_json"])
        except json.JSONDecodeError:
            pass
    return d

def summary(period: str = "week") -> dict:
   
    if period not in ("week", "month"):
        raise ValueError("period must be 'week' or 'month'")

    date_expr = "COALESCE(purchase_date, substr(created_at, 1, 10))"

    if period == "week":
        group_expr = f"date({date_expr}, '-' || ((cast(strftime('%w',{date_expr}) as integer) + 6) % 7) || ' days')"
    else:
        group_expr = f"date({date_expr}, 'start of month')"

    with get_db_connection() as conn:
        rows = conn.execute(
            f"""
            SELECT
              {group_expr} AS period_start,
              COUNT(*) AS receipt_count,
              SUM(COALESCE(total, 0)) AS total_spend
            FROM receipts
            WHERE status = 'parsed'
            GROUP BY period_start
            ORDER BY period_start DESC
            LIMIT 12
            """
        ).fetchall()

    return {
        "period": period,
        "groups": [dict(r) for r in rows]
    }