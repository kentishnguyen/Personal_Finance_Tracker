# Finvoice — Personal AI Finance Tracker

Finvoice is an AI-powered expense tracking app that extracts receipt data from images and organizes spending history and summaries.

## Features

- OCR-based receipt text extraction with Tesseract
- AI-powered structured parsing with Gemini
- Receipt history view with status tracking
- Weekly/monthly spending summary from stored receipts

## Roadmap (Planned)

- Simple Summary enhancements for clearer weekly/monthly budgeting insights
- Automatic budgeting suggestions based on receipt spending patterns

## Tech Stack

- Backend: FastAPI
- OCR: Tesseract + OpenCV
- AI parsing: Gemini (`google-generativeai`)
- Database: SQLite
- Frontend: HTML/CSS/JavaScript (served as static files)

## Project Structure

```text
personal-finance-tracker/
├── app/
│   ├── main.py              # FastAPI app and API endpoints
│   ├── models.py            # Pydantic receipt schemas
│   ├── db/
│   │   ├── database.py      # DB connection and initialization
│   │   ├── crud.py          # Receipt CRUD + summary queries
│   │   └── schema.sql       # SQLite schema
│   └── services/
│       ├── ocr.py           # OCR pipeline (OpenCV + Tesseract)
│       ├── llm.py           # Gemini extraction prompt/call
│       └── validate.py      # Validation + retry pipeline
├── static/
│   ├── index.html           # UI
│   ├── app.js               # Client API calls and rendering
│   └── styles.css           # Styling
├── testsamples/             # Sample receipt assets
├── uploads/                 # Uploaded receipt images
├── requirements.txt
└── README.md
```

## API Endpoints

- `POST /api/receipts/process` — upload and process a receipt image
- `GET /api/receipts` — list recent receipts
- `GET /api/receipts/{receipt_id}` — fetch a specific receipt record
- `GET /api/receipts/summary?period=week|month` — spending summary

## Example Parsed Receipt JSON

```json
{
	"store_name": "Costco",
	"date": "2026-02-26",
	"tax": 3.75,
	"total": 54.74,
	"items": [
		{
			"name": "Bananas",
			"quantity": 1,
			"price": 2.99
		}
	]
}
```

## Quick Start

### 1) Clone

```bash
git clone https://github.com/kentishnguyen/personal-finance-tracker.git
cd personal-finance-tracker
```

### 2) Install system dependency (Tesseract)

#### Ubuntu / WSL

```bash
sudo apt update
sudo apt install -y tesseract-ocr
```

#### Windows

Install from: https://github.com/tesseract-ocr/tesseract

### 3) Create virtual environment and install Python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4) Configure Gemini key

Set your API key as an environment variable:

```bash
export GEMINI_API_KEY="your_key_here"
```

### 5) Run the app

```bash
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000`

## Notes

- Keep receipts flat and well-lit for best OCR accuracy.
- The app stores receipt data in `receipts.db` (created automatically).
- Uploaded images are saved in `uploads/`.

## Security Reminder

If an API key was posted publicly during collaboration, rotate it immediately and replace it with a new key.