import struct
import time
import serial

from typing import List, Tuple

from fast_sdk.utils.check_sum import checksum_crc8
from fast_sdk.utils.functions import Functions


class BoardSDK:
    """
    Represents a controller board with functionality to set RGB LEDs and buzzer with buttons.
    """

    MAGIC_HEADER_1 = 0xAA
    MAGIC_HEADER_2 = 0x55

    def __init__(
        self, device: str = "/dev/ttyAMA0", baudrate: int = 1000000, timeout: int = 5
    ):
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
                raise ValueError("Each pixel must be a tuple of (index, R, G, B).")
            index, r, g, b = pixel
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError(
                    f"RGB values must be in the range 0-255. Received: {r}, {g}, {b}"
                )
            data.extend(struct.pack("<BBBB", int(index - 1), int(r), int(g), int(b)))

        self.buf_write(Functions.FUNC_RGB.value, data)

    def set_led(
        self, on_time: float, off_time: float, repeat: int = 1, led_id: int = 1
    ) -> None:
        """
        Control the LED with specified on/off timings and repetitions.

        :param on_time: Time in seconds the LED stays on (must be > 0).
        :param off_time: Time in seconds the LED stays off (must be >= 0).
        :param repeat: Number of times the LED blinks (must be >= 1).
        :param led_id: LED ID to control (must be in range 1-255).
        :raises ValueError: If any parameter is out of the expected range.
        """
        if on_time <= 0:
            raise ValueError(f"on_time must be greater than 0. Received: {on_time}")
        if off_time < 0:
            raise ValueError(
                f"off_time must be greater than or equal to 0. Received: {off_time}"
            )
        if repeat < 1:
            raise ValueError(f"repeat must be at least 1. Received: {repeat}")
        if not (1 <= led_id <= 255):
            raise ValueError(
                f"led_id must be in the range 1-255. Received: {led_id}"
            )

        on_time_ms = int(on_time * 1000)
        off_time_ms = int(off_time * 1000)
        data = struct.pack("<BHHH", led_id, on_time_ms, off_time_ms, repeat)

        self.buf_write(Functions.FUNC_LED.value, data)

    def set_buzzer(
        self, freq: int, on_time: float, off_time: float, repeat: int = 1
    ) -> None:
        """
        Control the buzzer with specified frequency, on/off timings, and repetitions.

        :param freq: Frequency of the buzzer in Hz (must be > 0).
        :param on_time: Time in seconds the buzzer stays on (must be > 0).
        :param off_time: Time in seconds the buzzer stays off (must be >= 0).
        :param repeat: Number of times the buzzer activates (must be >= 1).
        :raises ValueError: If any parameter is out of the expected range.
        """
        if freq <= 0:
            raise ValueError(f"freq must be greater than 0. Received: {freq}")
        if on_time <= 0:
            raise ValueError(f"on_time must be greater than 0. Received: {on_time}")
        if off_time < 0:
            raise ValueError(
                f"off_time must be greater than or equal to 0. Received: {off_time}"
            )
        if repeat < 1:
            raise ValueError(f"repeat must be at least 1. Received: {repeat}")

        on_time_ms = int(on_time * 1000)
        off_time_ms = int(off_time * 1000)
        data = struct.pack("<HHHH", freq, on_time_ms, off_time_ms, repeat)

        self.buf_write(Functions.FUNC_BUZZER.value, data)

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
