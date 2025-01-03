import smbus2


class InfraredSensors:
    """
    A class to interface with infrared sensors over I2C.

    The sensors can be used to detect obstacles or follow lines by reading the
    sensor data, which returns a list of boolean values for each sensor state.
    """

    def __init__(self, address=0x78, bus=1):
        """
        Initializes the InfraredSensors class.

        :param address: I2C address of the sensor (default 0x78). Use `scan_i2c_bus()` to check your address.
        :param bus: I2C bus number (default 1). This is the most common bus on modern boards such as Raspberry Pi,
                    usually connected to the SCL (Clock) and SDA (Data) pins.
        """
        self.address = address
        self.bus = smbus2.SMBus(bus)

    def scan_i2c_bus(self):
        """
        Scans the I2C bus for available devices and prints their addresses.

        This method can be used to confirm the I2C address of the sensor.
        """
        try:
            devices = []
            for address in range(0, 128):
                try:
                    self.bus.read_byte(address)
                    devices.append(hex(address))
                except IOError:
                    pass
            print(f"Found devices at: {', '.join(devices)}")
            return devices
        except Exception as e:
            print(f"Error scanning I2C bus: {e}")
            return []

    def read_sensor_data(self, register=0x01):
        """
        Reads data from the sensor and returns the sensor states as booleans.

        :param register: The register address to read from (default 0x01).
        :return: List of booleans representing the state of each sensor.
        """
        try:
            value = self.bus.read_byte_data(self.address, register)
            # Dynamically calculate the bit masks for the sensor states
            return [(value & (1 << i)) > 0 for i in range(4)]  # Assumes 4 sensors
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            return [False] * 4


# Example usage:
# sensors = InfraredSensors()
# sensors.scan_i2c_bus()  # Scan and print available I2C devices
# sensor_data = sensors.read_sensor_data()  # Read sensor data
# print(sensor_data)
