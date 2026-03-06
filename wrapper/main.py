import time
import serial
import braille

ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)

def task_b():
    # your function
    return "B result"

def translate(text_as_list):
    braille_buffer = braille.list_to_braille(text_as_list)
    return braille_buffer

def send_uart(msg):
    ser.write((msg + "\n").encode())

def main():
    while True:
        try:
            a = task_a()
            b = task_b()

            send_uart(a)
            send_uart(b)

        except Exception as e:
            send_uart(f"ERROR: {e}")

        time.sleep(0.1)   # prevents 100% CPU usage

if __name__ == "__main__":
    main()