import struct
import time
import serial

from typing import List, Tuple

from src.utils.utils import checksum_crc8


class BoardSDK:
    """
    Represents a game controller board with functionality to set RGB LEDs and interact with buttons.
    """

    MAGIC_HEADER_1 = 0xAA
    MAGIC_HEADER_2 = 0x55

    def __init__(self, device: str = "/dev/ttyAMA0", baudrate: int = 1000000,
                 timeout: int = 5):
        """
        Initialize the board with a serial connection.

        :param device: Serial port device name.
        :param baudrate: Baud rate for serial communication.
        :param timeout: Timeout in seconds for serial communication.
        """
        self.enable_recv = False
        self.frame = []
        self.recv_count = 0

        try:
            self.port = serial.Serial(None, baudrate=baudrate, timeout=timeout)
            self.port.rts = False
            self.port.dtr = False
            self.port.setPort(device)
            self.port.open()
            time.sleep(0.1)
        except serial.SerialException as e:
            raise RuntimeError(f"Failed to initialize serial port: {e}")

    def set_rgb(self, pixels: List[Tuple[int, int, int, int]]) -> None:
        """
        Set the RGB values for the board's LEDs.

        :param pixels: List of tuples where each tuple contains (index, R, G, B).
        :raises ValueError: If any of the RGB values are out of range.
        """
        data = [0x01, len(pixels)]

        for pixel in pixels:
            if len(pixel) != 4:
                raise ValueError(
                    "Each pixel must be a tuple of (index, R, G, B).")
            index, r, g, b = pixel
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError(
                    f"RGB values must be in the range 0-255. Received: {r}, {g}, {b}")
            data.extend(
                struct.pack("<BBBB", int(index - 1), int(r), int(g), int(b)))

        self.buf_write(11, data)

    def buf_write(self, func: int, data: List[int]) -> None:
        """
        Write a buffer to the serial port.

        :param func: Function code for the operation.
        :param data: Data to send as a list of integers.
        """
        buf = [self.MAGIC_HEADER_1, self.MAGIC_HEADER_2, func, len(data)]
        buf.extend(data)
        buf.append(checksum_crc8(bytes(buf[2:])))
        self.port.write(buf)
