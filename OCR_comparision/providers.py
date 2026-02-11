'''
paddleocr --- IGNORE ---
easyocr --- IGNORE ---
tesseract --- IGNORE ---
aws --- IGNORE ---
'''
from paddleocr import PaddleOCR
from easyocr import Reader
import pytesseract
import shutil
import os
import sys

from schema import standardize_ocr_result

# Auto-detect Tesseract executable and configure pytesseract.
# Prefer PATH lookup, then common default install locations.
_tess_path = shutil.which('tesseract')
if not _tess_path:
    _default_paths = [
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
    ]
    for p in _default_paths:
        if os.path.exists(p):
            _tess_path = p
            break

if _tess_path:
    pytesseract.pytesseract.tesseract_cmd = _tess_path


class OCRProvider:
    def __init__(self):

        # EasyOCR يدعم العربية والإنجليزية
        self.easy_ocr = Reader(['ar', 'en'])
        # Tesseract
        self.tesseract_ocr = pytesseract

    def ocr_easy(self, image_path):
        return self.easy_ocr.readtext(image_path)

    def ocr_tesseract(self, image_path):
        return self.tesseract_ocr.image_to_string(image_path, lang='ara+eng')
    
ocr_provider = OCRProvider()
def extract_text_from_img(img_path):
    """
    Run all configured OCR providers on `img_path` and return standardized text.
    """
    #paddle_result = ocr_provider.ocr_paddle(img_path)
    easy_result = ocr_provider.ocr_easy(img_path)
    tesseract_result = ocr_provider.ocr_tesseract(img_path)

    #paddle_text = standardize_ocr_result(paddle_result)
    easy_text = standardize_ocr_result(easy_result)
    tesseract_text = standardize_ocr_result(tesseract_result)

    return {
        #"PaddleOCR": paddle_text,
        "EasyOCR": easy_text,
        "Tesseract": tesseract_text,
    }
"""
        # PaddleOCR v3.x
        try:
            self.paddle_ocr = PaddleOCR(lang='ar') 
        except Exception as e:
            print(f"⚠️ PaddleOCR initialization failed: {e}")
            self.paddle_ocr = None

    def ocr_paddle(self, image_path):
        result = self.paddle_ocr.predict(image_path)
        return result
"""