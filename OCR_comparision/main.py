import os
# هذه الأسطر يجب أن تكون في القمة تماماً
os.environ['FLAGS_use_onednn'] = '0'
os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'

import sys
# أحياناً نحتاج إضافة المسار لضمان عدم وجود تداخل في الـ Modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from providers import OCRProvider, extract_text_from_img
# ... بقية الكود
from metrics import calculate_error_rates

"""
عندي 3 صور لوثائق رسميه ابغا اجرب 3 محركات OCR عليهم (PaddleOCR, EasyOCR, Tesseract) وبعدين اقارن النتائج مع النصوص الحقيقية (ground truth) باستخدام مقاييس WER و CER.


"""
image_dir = "dataset/images"
ground_truth_dir = "dataset/ground_truth"

for image_file in os.listdir(image_dir):
    if not image_file.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    image_path = os.path.join(image_dir, image_file)
    txt_path = os.path.join(ground_truth_dir, os.path.splitext(image_file)[0] + ".txt")

    ground_truth = open(txt_path, "r", encoding="utf-8").read()
    ocr_texts = extract_text_from_img(image_path)

    print(f"\nResults for {image_file}:")
    for ocr_name, text in ocr_texts.items():
        metrics = calculate_error_rates(ground_truth, text)
        print(f"{ocr_name} -> CER: {metrics['CER']:.2%}, WER: {metrics['WER']:.2%}")
