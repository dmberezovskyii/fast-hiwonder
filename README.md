
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)

# Fast Wonder SDK

The **Fast Wonder SDK** is a Python library that facilitates communication with the **Hiwonder TurboPi controller**. It provides easy-to-use functions for controlling various peripherals such as RGB LEDs, buzzers, infrared sensors, and more, while ensuring reliable communication with checksum validation using CRC-8.

## Features

- **Control RGB LEDs**: Easily control the colors of RGB LEDs using indexed tuples.
- **Control BUZZER**: Simple API to control the buzzer.
- **Control Infrared Sensors**: Interface with infrared sensors to detect obstacles or follow lines.
- **Reliable Communication**: Ensures data integrity with CRC-8 checksum validation for communication.
- **Configurable Serial Communication**: Adjust serial communication parameters such as baud rate, timeout, etc.

## Installation

To get started with Fast Wonder SDK, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dmberezovskyii/fast-hiwonder.git


## Usage
1. **Infra red sensors**
   ``` python
   from fast_hi_wonder import InfraredSensors

   # Initialize the sensor with the default I2C address and bus
   sensors = InfraredSensors()
   
   # Read sensor data
   sensor_states = sensors.read_sensor_data()
   
   # Process sensor states
   for i, state in enumerate(sensor_states):
       print(f"Sensor {i+1} is {'active' if state else 'inactive'}")

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-personal-page.svg)](https://stand-with-ukraine.pp.ua)
