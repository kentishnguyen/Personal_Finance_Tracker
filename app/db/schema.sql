CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT NOT NULL,
    raw_ocr_text TEXT,
    parsed_json TEXT,

    store_name TEXT NOT NULL,
    purchase_date TEXT,
    tax REAL DEFAULT 0.0, 
    total REAL NOT NULL,
    
    status TEXT NOT NULL DEFAULT 'uploaded',  -- uploaded/parsed/error
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
)

CREATE INDEX IF NOT EXISTS idx_receipts_created_at ON receipts(created_at);
CREATE INDEX IF NOT EXISTS idx_receipts_purchase_date ON receipts(purchase_date);
