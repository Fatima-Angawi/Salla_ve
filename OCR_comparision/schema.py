def standardize_ocr_result(ocr_result):
    """
    Convert OCR engine output into correctly ordered plain text
    based on bounding box positions (top-to-bottom, left-to-right).
    Works for PaddleOCR, EasyOCR, and Tesseract.
    """

    if not ocr_result:
        return ""

    # If already plain string (e.g., Tesseract)
    if isinstance(ocr_result, str):
        return " ".join(ocr_result.split())

    extracted_items = []

    # -----------------------------
    # PaddleOCR format
    # -----------------------------
    # [[[ [x1,y1],[x2,y2],[x3,y3],[x4,y4] ], (text, conf)], ...]
    for line in ocr_result:
        if isinstance(line, list):
            for item in line:
                if isinstance(item, list) and len(item) == 2:
                    bbox, (text, _) = item
                    x = min(point[0] for point in bbox)
                    y = min(point[1] for point in bbox)
                    extracted_items.append((y, x, text))

    # -----------------------------
    # EasyOCR format
    # -----------------------------
    # [ (bbox, text, confidence), ... ]
    for item in ocr_result:
        if isinstance(item, tuple) and len(item) == 3:
            bbox, text, _ = item
            x = min(point[0] for point in bbox)
            y = min(point[1] for point in bbox)
            extracted_items.append((y, x, text))

    # If nothing extracted via bbox logic, fallback
    if not extracted_items:
        texts = []
        for item in ocr_result:
            texts.append(str(item))
        return " ".join(texts).strip()

    # -----------------------------
    # SORT BY READING ORDER
    # -----------------------------
    extracted_items.sort(key=lambda t: (t[0], t[1]))

    # Join text
    ordered_text = " ".join(text for (_, _, text) in extracted_items)

    return " ".join(ordered_text.split())
