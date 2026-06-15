from rapidfuzz import fuzz
import re

GOVERNMENT_WARNING_REQUIRED = (
    "GOVERNMENT WARNING: "
    "According to the Surgeon General, women should not drink alcoholic beverages "
    "during pregnancy because of the risk of birth defects. "
    "Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, "
    "and may cause health problems."
)

def normalize_text(text):
    return re.sub(r"[^a-z0-9%./ ]", "", text.lower()).strip()

def fuzzy_check(expected, extracted_text, threshold=80):
    if not expected:
        return {
            "status": "Not Provided",
            "score": 0,
            "note": "No expected value entered."
        }

    expected_clean = normalize_text(expected)
    extracted_clean = normalize_text(extracted_text)

    score = fuzz.partial_ratio(expected_clean, extracted_clean)

    if score >= 90:
        status = "PASS"
    elif score >= threshold:
        status = "REVIEW"
    else:
        status = "FAIL"

    return {
        "status": status,
        "score": round(score, 1),
        "note": f"Matched at {round(score, 1)}% confidence."
    }

def check_government_warning(extracted_text):
    extracted_clean = normalize_text(extracted_text)
    warning_clean = normalize_text(GOVERNMENT_WARNING_REQUIRED)

    score = fuzz.partial_ratio(warning_clean, extracted_clean)

    if score >= 90:
        status = "PASS"
    elif score >= 75:
        status = "REVIEW"
    else:
        status = "FAIL"

    return {
        "status": status,
        "score": round(score, 1),
        "note": "Checks for required government health warning text."
    }

def verify_label(expected_data, extracted_text):
    results = {}

    results["Brand Name"] = fuzzy_check(expected_data.get("brand_name"), extracted_text)
    results["Class/Type"] = fuzzy_check(expected_data.get("class_type"), extracted_text)
    results["Alcohol Content"] = fuzzy_check(expected_data.get("alcohol_content"), extracted_text)
    results["Net Contents"] = fuzzy_check(expected_data.get("net_contents"), extracted_text)
    results["Government Warning"] = check_government_warning(extracted_text)

    return results