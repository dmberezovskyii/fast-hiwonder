import math
from typing import Literal

from fast_sdk.board_sdk import BoardSDK


# Pre-calculate common constants
RAD_PER_DEG = math.pi / 180

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
        self.velocity = 0
        self.direction = 0
        self.angular_rate = 0
        self.board = BoardSDK()

    def reset_motors(self) -> None:
        """
        Reset the motor velocities to zero.
        """
        self.board.set_motor_duty([(1, 0), (2, 0), (3, 0), (4, 0)])

        # Reset state variables
        self.velocity = 0
        self.direction = 0
        self.angular_rate = 0

    def set_velocity(self, velocity: float, direction: float, angular_rate: float, fake: bool = False) -> None:
        """
        Set the velocity, direction, and angular rate of the chassis using polar coordinates.

        :param velocity: The speed of movement in mm/s.
        :param direction: The moving direction (0-360 degrees).
        :param angular_rate: The speed at which the chassis rotates.
        :param fake: Whether to simulate or actually set the motor velocities.
        """
        # Pre-calculate cos and sin of direction
        cos_dir = math.cos(direction * RAD_PER_DEG)
        sin_dir = math.sin(direction * RAD_PER_DEG)

        # Calculate velocities for each motor
        vx = velocity * cos_dir
        vy = velocity * sin_dir
        vp = -angular_rate * (self.a + self.b)

        # Motor velocities
        v1 = int(vy + vx - vp)
        v2 = int(vy - vx + vp)
        v3 = int(vy - vx - vp)
        v4 = int(vy + vx + vp)

        if fake:
            return

        # Set motor duties
        self.board.set_motor_duty([(1, -v1), (2, v2), (3, -v3), (4, v4)])

        # Update state
        self.velocity = velocity
        self.direction = direction
        self.angular_rate = angular_rate

    def translation(self, velocity_x: float, velocity_y: float, fake: bool = False) -> tuple[float, int | float] | None:
        """
        Convert linear velocities in the x and y directions into a single velocity and direction.

        :param velocity_x: Velocity in the X direction (mm/s)
        :param velocity_y: Velocity in the Y direction (mm/s)
        :param fake: Whether to simulate or actually set the velocity.
        :return: A tuple (velocity, direction) if fake is True, otherwise sets the actual velocity.
        """
        velocity = math.sqrt(velocity_x ** 2 + velocity_y ** 2)

        if velocity_x == 0:
            direction = 90 if velocity_y >= 0 else 270  # pi/2 (90deg), (pi * 3)/2 (270deg)
        elif velocity_y == 0:
            direction = 0 if velocity_x > 0 else 180
        else:
            # Calculate the direction angle in degrees using atan2
            direction = math.atan2(velocity_y, velocity_x) * 180 / math.pi

        if fake:
            return velocity, direction
        else:
            return self.set_velocity(velocity, direction, 0)

    def set_direction(self, velocity: int = 50,
                      direction: Literal["Forward", "Backward", "Left", "Right", "Curve"] = "Forward",
                      fake: bool = False) -> None:
        """
        Set the direction and angular velocity of the chassis, combining linear direction and rotational rate.
        :param velocity:
        :param direction: Direction in one of ["Forward", "Backward", "Left", "Right", "Curve"].
        :param fake: If True, the motors won't be actuated (simulation mode).
        """
        # Mapping the direction string to corresponding (direction_deg, angular_rate) tuple
        direction_map = {
            "Forward": (90, 0),
            "Backward": (0, 0),
            "Left": (180, 0),
            "Right": (360, 0),
            "Curve": (135, 0) # (324,0)
        }

        # Check if the provided direction is valid
        if direction not in direction_map:
            raise ValueError(
                f"Invalid direction: {direction}. Choose from 'Forward', 'Backward', 'Left', 'Right', 'Curve'.")

        # Get the corresponding degrees and angular rate for the given direction
        direction_deg, angular_rate = direction_map[direction]
        self.set_velocity(velocity=velocity, direction=direction_deg, angular_rate=angular_rate, fake=fake)