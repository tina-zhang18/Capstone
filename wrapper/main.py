import time
import serial
import braille
import tesseract
import cv2


ser = serial.Serial("/dev/serial0", 115200, timeout=1)


def translate(image):
    text = tesseract.read_text(image)
    braille_buffer = braille.list_to_braille(text)
    return braille_buffer

def capture():
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

def send_uart(msg):
    ser.write((msg + "\n").encode())

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