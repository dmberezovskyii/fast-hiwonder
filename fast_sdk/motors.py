import math
from enum import Enum
from typing import Literal, Optional, Tuple

from fast_sdk.board_sdk import BoardSDK

# Constants
RAD_PER_DEG = math.pi / 180


class Direction(Enum):
    FORWARD = "Forward"
    BACKWARD = "Backward"
    LEFT = "Left"
    RIGHT = "Right"
    CURVE = "Curve"


class ControlChassis:
    def __init__(self, a: float = 67.0, b: float = 59.0, wheel_diameter: float = 65.0):
        """
        Initialize the Mecanum chassis with default or custom parameters.

        :param a: Distance from the center to the front or back wheels (mm)
        :param b: Distance from the center to the left or right wheels (mm)
        :param wheel_diameter: Diameter of the wheels (mm)
        """
        self.a = a
        self.b = b
        self.wheel_diameter = wheel_diameter
        self._a_plus_b = a + b  # Precompute constant
        self.velocity = 0.0
        self.direction = 0.0
        self.angular_rate = 0.0
        self.board = BoardSDK()

    def reset_motors(self) -> None:
        """
        Reset the motor velocities to zero.
        """
        self.board.set_motor_duty([(1, 0), (2, 0), (3, 0), (4, 0)])

        # Reset state variables
        self.velocity = 0.0
        self.direction = 0.0
        self.angular_rate = 0.0

    def set_velocity(self, velocity: float, direction: float, angular_rate: float, fake: bool = False) -> None:
        """
        Set the velocity, direction, and angular rate of the chassis using polar coordinates.

        :param velocity: The speed of movement in mm/s.
        :param direction: The moving direction (0-360 degrees).
        :param angular_rate: The speed at which the chassis rotates.
        :param fake: Whether to simulate or actually set the motor velocities.
        """
        if not (0 <= direction <= 360):
            raise ValueError("Direction must be between 0 and 360 degrees.")

        # Pre-calculate cos and sin of direction
        cos_dir = math.cos(direction * RAD_PER_DEG)
        sin_dir = math.sin(direction * RAD_PER_DEG)

        # Calculate velocities for each motor
        vx = velocity * cos_dir
        vy = velocity * sin_dir
        vp = -angular_rate * self._a_plus_b  # Use precomputed constant

        # Motor velocities
        v1 = int(vy + vx - vp)
        v2 = int(vy - vx + vp)
        v3 = int(vy - vx - vp)
        v4 = int(vy + vx + vp)

        if fake:
            return

        # Set motor duties
        self.board.set_motor_duty([(1, -v1), (2, v2), (3, -v3), (4, v4)])

        # Update state only if not fake
        self.velocity = velocity
        self.direction = direction
        self.angular_rate = angular_rate

    def translation(
        self, velocity_x: float, velocity_y: float, fake: bool = False
    ) -> Optional[Tuple[float, float]]:
        """
        Convert linear velocities in the x and y directions into a single velocity and direction.

        :param velocity_x: Velocity in the X direction (mm/s)
        :param velocity_y: Velocity in the Y direction (mm/s)
        :param fake: Whether to simulate or actually set the velocity.
        :return: A tuple (velocity, direction) if fake is True, otherwise None.
        """
        velocity = math.sqrt(velocity_x**2 + velocity_y**2)

        if velocity_x == 0:
            direction = 90 if velocity_y >= 0 else 270  # pi/2 (90deg), (pi * 3)/2 (270deg)
        elif velocity_y == 0:
            direction = 0 if velocity_x > 0 else 180
        else:
            # Calculate the direction angle in degrees using atan2
            direction = math.degrees(math.atan2(velocity_y, velocity_x))

        if fake:
            return velocity, direction
        else:
            self.set_velocity(velocity, direction, 0)
            return None

    def set_direction(
        self, velocity: int = 50, direction: Direction = Direction.FORWARD, fake: bool = False
    ) -> None:
        """
        Set the direction and angular velocity of the chassis, combining linear direction and rotational rate.

        :param velocity: The speed of movement in mm/s.
        :param direction: Direction as an instance of Direction Enum.
        :param fake: If True, the motors won't be actuated (simulation mode).
        """
        # Mapping the direction to corresponding (direction_deg, angular_rate) tuple
        direction_map = {
            Direction.FORWARD: (90, 0),
            Direction.BACKWARD: (270, 0),
            Direction.LEFT: (180, 0),
            Direction.RIGHT: (0, 0),
            Direction.CURVE: (135, 0),
        }

        # Get the corresponding degrees and angular rate for the given direction
        direction_deg, angular_rate = direction_map[direction]
        self.set_velocity(velocity=velocity, direction=direction_deg, angular_rate=angular_rate, fake=fake)