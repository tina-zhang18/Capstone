import cv2
import pytesseract
import numpy as np
import re

# If Tesseract is not in PATH (Windows only)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

path = 'Google Drive/My Drive/Capstone 2025/Testing/'

#------------------------------------------------------------------------------------------------------------
def read_text(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT,
        config="--oem 3 --psm 6"
    )

    results = []
    confidences = []
    word_buffer = []

    n = len(data["text"])

    for i in range(n):
        text = data["text"][i].strip()
        conf = float(data["conf"][i])

        if conf < 0 or text == "":
            continue

        conf_norm = conf / 100.0
        confidences.append(conf_norm)

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        bbox = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        results.append((bbox, text, conf_norm))

        # Split words & punctuation (same logic as your EasyOCR version)
        words = re.findall(r'\w+|[^\w\s]', text)
        for word in words:
            print(f"{word} (conf: {conf_norm:.2f})")
            word_buffer.append(word)

    average_conf = np.mean(confidences) if confidences else 0
    print(f"Average confidence across all detected words: {average_conf:.2f}")

    # DRAWING ON IMAGE
    for (bbox, text, prob) in results:
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))

        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        label = f"{text} ({prob:.2f})"
        cv2.putText(
            image,
            label,
            (top_left[0], top_left[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )

    return results, image, word_buffer
#------------------------------------------------------------------------------------------------------------

# DEFINE IMAGE
pathset = path + 'Set 2/'
image = pathset + '2a.png'

# RUN
results, annotated_image, words = read_text(image)
cv2.imshow("Detected Text", annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
