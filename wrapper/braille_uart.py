import serial

class BrailleUART:
    # Standard grade-1 braille mapping from your UI
    BRAILLE_MAP = {
        ' ': 0b000000,
        'a': 0b000001, 'b': 0b000011, 'c': 0b001001, 'd': 0b011001, 'e': 0b010001,
        'f': 0b001011, 'g': 0b011011, 'h': 0b010011, 'i': 0b001010, 'j': 0b011010,
        'k': 0b000101, 'l': 0b000111, 'm': 0b001101, 'n': 0b011101, 'o': 0b010101,
        'p': 0b001111, 'q': 0b011111, 'r': 0b010111, 's': 0b001110, 't': 0b011110,
        'u': 0b100101, 'v': 0b100111, 'w': 0b111010, 'x': 0b101101, 'y': 0b111101,
        'z': 0b110101
    }

    def __init__(self, port='/dev/serial0', baud=9600):
        """Initialize the serial connection and state."""
        self.ser = serial.Serial(
            port, 
            baud, 
            bytesize=8, 
            parity='N', 
            stopbits=1, 
            timeout=1
        )
        self.nonce = 0 # Rolling tracking number for packets

    def _char_to_packet_byte(self, ch):
        """Looks up the 6-bit braille code and shifts it to bits [6:1]."""
        cell6 = self.BRAILLE_MAP.get(ch, 0b000000) # Defaults to space if unknown
        return (cell6 & 0x3F) << 1

    def send_char(self, char, hiz_duty=30, hiz_freq=150, pol_duty=50, pol_freq=100):
        """Constructs the 10-byte packet, sends it, and waits for ACK."""
        
        braille_byte = self._char_to_packet_byte(char)

        # Split 16-bit frequencies into High and Low bytes
        hiz_freq_h = (hiz_freq >> 8) & 0xFF
        hiz_freq_l = hiz_freq & 0xFF
        pol_freq_h = (pol_freq >> 8) & 0xFF
        pol_freq_l = pol_freq & 0xFF

        # Construct the 10-byte raw binary packet
        packet = bytearray([
            0xAA,           # CMD Start Byte
            braille_byte,   
            hiz_duty,
            hiz_freq_h,
            hiz_freq_l,
            pol_duty,
            pol_freq_h,
            pol_freq_l,
            self.nonce,     
            0x55            # End Byte
        ])

        # Send packet
        self.ser.write(packet)
        self.ser.flush()

        # Wait for the 5-byte ACK
        self._wait_for_ack()

        # Increment nonce for the next packet, wrap at 255
        self.nonce = (self.nonce + 1) & 0xFF

    def _wait_for_ack(self):
        """Reads the ACK and prints warnings if communication fails."""
        ack = self.ser.read(5)

        if len(ack) == 5:
            if ack[0] == 0x06:
                status = ack[2]
                frame_ok = bool(status & 0x08)
                
                if not frame_ok:
                    print(f"WARNING: MCU reported Frame Error. Raw ACK: {[hex(b) for b in ack]}")
            else:
                print("WARNING: Received packet was not an ACK (first byte not 0x06).")
        else:
            print("ERROR: UART Timeout! No ACK received from STM32.")

    def close(self):
        """Safely close the serial port."""
        if self.ser.is_open:
            self.ser.close()