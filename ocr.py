import easyocr
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

_reader = None

def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(["en"], gpu=False)
    return _reader

def preprocess_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")

    max_width = 1600
    if image.width > max_width:
        ratio = max_width / image.width
        new_height = int(image.height * ratio)
        image = image.resize((max_width, new_height))

    image = image.convert("L")
    image = ImageEnhance.Contrast(image).enhance(2.0)
    image = image.filter(ImageFilter.SHARPEN)

    return image

def extract_text(uploaded_file):
    image = preprocess_image(uploaded_file)
    image_array = np.array(image)

    reader = get_reader()
    results = reader.readtext(image_array, detail=0, paragraph=False)

    cleaned_results = []
    for text in results:
        text = text.strip()
        if text:
            cleaned_results.append(text)

    return "\n".join(cleaned_results)