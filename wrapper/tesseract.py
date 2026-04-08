import cv2
import pytesseract
import numpy as np
import re


#------------------------------------------------------------------------------------------------------------
def read_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT,
        config="--oem 3 --psm 6"
    )

    confidences = []
    char_buffer = []

    n = len(data["text"])

    for i in range(n):
        text = data["text"][i].strip()
        conf = float(data["conf"][i])

        if conf < 40 or text == "":
            continue

        conf_norm = conf / 100.0
        confidences.append(conf_norm)

        # Split words & punctuation
        words = re.findall(r'\w+|[^\w\s]', text)
        for word in words:
            print(f"{word} (conf: {conf_norm:.2f})")
            
            # Break the word into individual characters and add to our buffer
            characters = list(word)
            char_buffer.extend(characters)
            
        char_buffer.append(' ') # Add a space after each block

    if char_buffer and char_buffer[-1] == ' ':
        char_buffer.pop() # Remove trailing space at the end of a "sentence".

    # Just return the clean array of characters
    return char_buffer
#------------------------------------------------------------------------------------------------------------
