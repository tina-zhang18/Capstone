import time
import serial
import braille
import tesseract
import cv2
from picamera2 import Picamera2

ser = serial.Serial(
    '/dev/serial0',
    9600,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1)

# Initialize camera ONCE outside the loop (faster, avoids re-init overhead)
picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (1280, 720)})
picam2.configure(config)
picam2.start()
time.sleep(2)  # Let AE/AWB settle on first start

def capture():
    frame = picam2.capture_array()  # numpy array, same as cv2 frame
    if frame is None:
        raise RuntimeError("Failed to capture frame")
    return frame

def translate(image):
    text = tesseract.read_text(image)
    braille_buffer = braille.list_to_braille(text)
    return braille_buffer

"""def capture():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Cannot open Pi Camera")

    # Set resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Capture a single frame
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to capture frame")

    cap.release()

    return frame
"""
def send_uart(val):
    START = 0xAA
    END = 0x55

    val &= 0xFF  

    ser.write(bytes([START, val, END]))

def main(): 
   

    while True:
        try:

            frame = capture()
            cells_list = translate(frame)
            for cell in cells_list:            
                send_uart(cell)
                braille.print_unicode(cell)
                time.sleep(1)

        except Exception as e:
            print("ERROR:", e)

        time.sleep(0.1)  

if __name__ == "__main__":
    main()
