import time
import serial
import braille
import tesseract
from picamera2 import Picamera2
import time

ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)
picam = Picamera2()

def translate(image):
    text = tesseract.read_text(image)
    braille_buffer = braille.list_to_braille(text)
    return braille_buffer

def send_uart(msg):
    ser.write((msg + "\n").encode())

def main(): 
    picam.start()
    time.sleep(2)  # allow camera to adjust

    while True:
        try:

            frame = picam.capture_array()
            cells_list = translate(frame)
            for cell in cells_list:            
                send_uart(cell)
                braille.print_unicode(cell)
                time.sleep(1)

        except Exception as e:
            send_uart(f"ERROR: {e}")

        time.sleep(0.1)  

if __name__ == "__main__":
    main()