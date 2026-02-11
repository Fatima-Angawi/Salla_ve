from PIL import Image, ImageDraw, ImageFont
import os

img_dir = os.path.join('dataset', 'images')
os.makedirs(img_dir, exist_ok=True)
img_path = os.path.join(img_dir, 'test_ocr_arabic.png')

# Create a test image with Arabic text
W, H = 800, 200
img = Image.new('RGB', (W, H), color=(255, 255, 255))
draw = ImageDraw.Draw(img)
text = "مرحبا بك في نظام التحقق"  # "Welcome to the verification system" in Arabic
try:
    # Try to load an Arabic font; if not available, use default
    font = ImageFont.truetype('arial.ttf', 36)
except Exception:
    font = ImageFont.load_default()

# For RTL text (Arabic), PIL may need special handling
draw.text((20, 70), text, fill=(0, 0, 0), font=font)
img.save(img_path)

print('Test image (Arabic) saved to', img_path)

from OCR_comparision import providers

print('\nRunning PaddleOCR on Arabic text...')
try:
    paddle_res = providers.ocr_provider.ocr_paddle(img_path)
    print('PaddleOCR result (raw):', paddle_res[:100] if isinstance(paddle_res, str) else str(paddle_res)[:100])
except Exception as e:
    print('PaddleOCR error:', e)

print('\nRunning EasyOCR on Arabic text...')
try:
    easy_res = providers.ocr_provider.ocr_easy(img_path)
    print('EasyOCR result (raw):', easy_res[:2] if isinstance(easy_res, list) else str(easy_res)[:100])
except Exception as e:
    print('EasyOCR error:', e)

print('\nRunning Tesseract on Arabic text...')
try:
    tess_res = providers.ocr_provider.ocr_tesseract(img_path)
    print('Tesseract result (text):')
    print(tess_res)
except Exception as e:
    print('Tesseract error:', e)

# Test extract_text_from_img
print('\n--- Testing extract_text_from_img on Arabic ---')
try:
    from OCR_comparision.providers import extract_text_from_img
    results = extract_text_from_img(img_path)
    for provider, text in results.items():
        print(f'{provider}: {text[:50]}...' if len(str(text)) > 50 else f'{provider}: {text}')
except Exception as e:
    print('Error in extract_text_from_img:', e)
