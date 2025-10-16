def process_text(string):
    string = string.lower()
    return string

def char_to_braille(char):
    if char.isdigit(): # check if character is a number, if so return the # symbol and the number itself
        if char == "0":
            braille_char = braille_alphabet.get("j")
        else:
            braille_char = braille_alphabet.get(chr(ord(char)+48))
    else:
        braille_char = braille_alphabet.get(char)
    return braille_char

def text_to_braille(string):
    string = process_text(string)
    binary_braille = []
    for char in string:
        if char.isdigit():
            binary_braille.append(char_to_braille("#"))
        binary_braille.append(char_to_braille(char))
    return binary_braille

def print_unicode(list):
    unicode = ""
    for char in list:
        unicode += chr(char+10240)
    print(unicode)
    return

global braille_alphabet
braille_alphabet = {
    "a": 0b000001,
    "b": 0b000011,
    "c": 0b001001,
    "d": 0b011001,
    "e": 0b010001,
    "f": 0b001011,
    "g": 0b011011,
    "h": 0b010011,
    "i": 0b001010,
    "j": 0b011010,
    "k": 0b000101,
    "l": 0b000111,
    "m": 0b001101,
    "n": 0b011101,
    "o": 0b010101,
    "p": 0b001111,
    "q": 0b011111,
    "r": 0b010111,
    "s": 0b001110,
    "t": 0b011110,
    "u": 0b100101,
    "v": 0b100111,
    "w": 0b111010,
    "x": 0b101101,
    "y": 0b111101,
    "z": 0b111001,  
    " ": 0b000000,
    "#": 0b111100,
    ".": 0b011010,
    ",": 0b000010,
    "!": 0b010110,
    "?": 0b100110,
    ":": 0b010010,
    ";": 0b000110,
    "'": 0b000100,
}

text = text_to_braille("where are you? it's almost 6!")
print(text)
print_unicode(text)

