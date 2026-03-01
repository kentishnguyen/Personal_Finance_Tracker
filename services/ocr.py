import cv2
import pytesseract

def run_ocr(image_path: str) -> str:
    """
    Runs Preprocessing + Tesseract OCR.
    Returns extracted text.
    """
    # Get image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Process image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resize = cv2.resize(gray, None, fx=2, fy=2)
    _, thresh = cv2.threshold(resize, 150, 255, cv2.THRESH_BINARY)
    
    # Extract the text
    text = pytesseract.image_to_string(thresh);
    return text.strip()
