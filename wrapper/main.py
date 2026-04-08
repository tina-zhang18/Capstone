import time
import serial
import braille
import tesseract
import cv2
from picamera2 import Picamera2
from braille_uart import BrailleUART

# Initialize the UART helper
# (This opens the port and sets up the nonce tracker)
uart = BrailleUART('/dev/serial0', 9600)

#Taken care of in BrailleUART class
'''
ser = serial.Serial(
    '/dev/serial0',
    9600,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1)
'''

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
    return text

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
    print("System initialized. Waiting for trigger...")

    while True:
        try:
            # Trigger mechanism
            user_input = input("Press ENTER to capture image (or type 'q' to quit): ")
            if user_input.lower() == 'q':
                break

            print("Capturing image...")
            frame = capture()
            
            print("Running OCR...")
            characters_list = translate(frame)
            
            print(f"Sending {len(characters_list)} characters over UART...")
            
            for char in characters_list:            
                
                # Send the character to the helper function.
                # You can pass your specific PWM/Duty values here. 
                # If you leave them blank, it defaults to the values in the class.
                uart.send_char(
                    char, 
                    hiz_duty=30, 
                    hiz_freq=150, 
                    pol_duty=50, 
                    pol_freq=100
                )
                
                # Print to console so you can see what is happening
                print(f"Sent: '{char}'")
                
                # Small delay to allow the physical pins to actuate and user to feel them
                time.sleep(0.5) 

            print("Transmission complete.\n")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    finally:
        # Ensures the serial port is released if you crash or exit the script
        uart.close()
