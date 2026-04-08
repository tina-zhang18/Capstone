import cv2
import pytesseract
import numpy as np
import re
from spellchecker import SpellChecker

# Initialize the spell checker globally so the dictionary only loads once
spell = SpellChecker()
spell.word_frequency.load_words(['stm32', 'uart', 'gpio', 'picamera']) #Test words to add as "valid" spelled words (if needed)

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
            # --- NEW LOGIC: Spell checking ---
            # If the string contains only letters, check it against the dictionary
            if word.isalpha():
                # spell.known() takes a list of words and returns the ones that are valid
                valid_words = spell.known([word.lower()])
                
                if not valid_words:
                    print(f"Discarded non-word: '{word}' (conf: {conf_norm:.2f})")
                    continue # Skip this word completely
            
            # If we made it here, it's either a valid word, a number, or punctuation
            print(f"{word} (conf: {conf_norm:.2f})")
            
            # Break the word into individual characters and add to our buffer
            characters = list(word)
            char_buffer.extend(characters)

    if char_buffer and char_buffer[-1] == ' ':
        char_buffer.pop() # Remove trailing space at the end of a "sentence".

    # Just return the clean array of characters
    return char_buffer
#------------------------------------------------------------------------------------------------------------
