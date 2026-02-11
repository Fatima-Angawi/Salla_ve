import sys
from jiwer import wer, cer


def normalize(text: str) -> str:
    return " ".join(text.lower().split())

def calculate_error_rates(ground_truth: str, ocr_output: str):
    """
    Calculate Word Error Rate (WER) and Character Error Rate (CER)
    between ground truth text and OCR output.
    """
    # Basic input validation
    if not isinstance(ground_truth, str) or not isinstance(ocr_output, str):
        raise TypeError("Both inputs must be strings.")

    # Strip leading/trailing spaces
    ground_truth = normalize(ground_truth.strip())
    ocr_output = normalize(ocr_output.strip())

    # Handle empty cases
    if not ground_truth and not ocr_output:
        return {"WER": 0.0, "CER": 0.0}
    if not ground_truth:
        return {"WER": 1.0, "CER": 1.0}

    # Calculate metrics
    word_error_rate = wer(ground_truth, ocr_output)
    char_error_rate = cer(ground_truth, ocr_output)

    return {"WER": word_error_rate, "CER": char_error_rate}



