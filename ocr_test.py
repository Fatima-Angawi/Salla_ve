from PIL import Image, ImageDraw, ImageFont
import os

img_dir = os.path.join('dataset', 'images')
os.makedirs(img_dir, exist_ok=True)
img_path = os.path.join(img_dir, 'test_ocr.png')

# Create a simple test image
W, H = 800, 200
img = Image.new('RGB', (W, H), color=(255, 255, 255))
draw = ImageDraw.Draw(img)
text = "The quick brown fox jumps over the lazy dog"
try:
    font = ImageFont.truetype('arial.ttf', 36)
except Exception:
    font = ImageFont.load_default()
draw.text((20, 70), text, fill=(0, 0, 0), font=font)
img.save(img_path)

print('Test image saved to', img_path)

from OCR_comparision import providers

print('\nRunning PaddleOCR...')
try:
    paddle_res = providers.ocr_provider.ocr_paddle(img_path)
    print('PaddleOCR result (raw):', paddle_res)
except Exception as e:
    print('PaddleOCR error:', e)

print('\nRunning EasyOCR...')
try:
    easy_res = providers.ocr_provider.ocr_easy(img_path)
    print('EasyOCR result (raw):', easy_res)
except Exception as e:
    print('EasyOCR error:', e)

print('\nRunning Tesseract via pytesseract...')
try:
    tess_res = providers.ocr_provider.ocr_tesseract(img_path)
    print('Tesseract result (text):')
    print(tess_res)
except Exception as e:
    print('Tesseract error:', e)
