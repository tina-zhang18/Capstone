def process_text(string):
    string = string.lower()
    return string

def char_to_braile(char):
    
    return braille_alphabet.get(char)

def text_to_braille(string):
    string = process_text(string)
    binary_braille = []
    for i in string:
        binary_braille.append(char_to_braile(i))
    return binary_braille

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
    " ": 0b000000  
}

# braille_alphabet = {
#     "a": b"000001",
#     "b": b"000011",
#     "c": b"001001",
#     "d": b"011001",
#     "e": b"010001",
#     "f": b"001011",
#     "g": b"011011",
#     "h": b"010011",
#     "i": b"001010",
#     "j": b"011010",
#     "k": b"000101",
#     "l": b"000111",
#     "m": b"001101",
#     "n": b"011101",
#     "o": b"010101",
#     "p": b"001111",
#     "q": b"011111",
#     "r": b"010111",
#     "s": b"001110",
#     "t": b"011110",
#     "u": b"100101",
#     "v": b"100111",
#     "w": b"111010",
#     "x": b"101101",
#     "y": b"111101",
#     "z": b"111001",    
# }

print(text_to_braille("cat and dog"))