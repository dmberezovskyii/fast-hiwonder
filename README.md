
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
2. **Mecanum wheels**
   ## Polar Coordinates

In polar coordinates, we describe a point (or movement) in space using two parameters:

- **Radius (r)**: The distance from the origin (0,0) to the point.
- **Angle (θ)**: The direction of the point relative to the X-axis (horizontal axis) in degrees or radians.

In the case of your mechanism:

- **Velocity**: The distance the robot moves per unit of time.
- **Direction**: The angle at which the robot is moving, measured from the X-axis.

## Trigonometry and Coordinate Transformation

To control the robot's movement, we break the velocity down into two components — **vx** and **vy**:

- **vx**: The velocity component along the X-axis (horizontal axis).
- **vy**: The velocity component along the Y-axis (vertical axis).

To calculate these components, we use trigonometric functions:

- **vx** (component along the X-axis) is calculated using the cosine of the direction angle:
  \[
  vx = \text{velocity} \times \cos(\text{direction})
  \]

- **vy** (component along the Y-axis) is calculated using the sine of the direction angle:
  \[
  vy = \text{velocity} \times \sin(\text{direction})
  \]

### Example

If the robot needs to move at a speed of 100 mm/s in the direction of 30 degrees (from the X-axis):

- \( vx = 100 \times \cos(30^\circ) \)
- \( vy = 100 \times \sin(30^\circ) \)


   ``` python
   chassis = MecanumChassis()

    # Move forward at 100 mm/s in the direction of 0 degrees (forward along the X-axis)
    chassis.set_velocity(100, 0, 0)

    # Rotate the chassis at an angular rate of 30 degrees per second
    chassis.set_velocity(100, 0, 30)

    # Translate the chassis based on Cartesian coordinates (e.g., moving diagonally)
    chassis.translation(50, 50)

    # Stop all motors and reset movement attributes
    chassis.reset_motors()
   ``` 
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-personal-page.svg)](https://stand-with-ukraine.pp.ua)
