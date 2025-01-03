import math
from fast_sdk.board_sdk import BoardSDK


class Motors:
    # Default params
    DEFAULT_A = 67  # mm
    DEFAULT_B = 59  # mm
    DEFAULT_WHEEL_DIAMETER = 65  # mm

    # Motor IDs
    MOTOR_IDS = [1, 2, 3, 4]

    def __init__(self, a=DEFAULT_A, b=DEFAULT_B, wheel_diameter=DEFAULT_WHEEL_DIAMETER):
        self.a = a
        self.b = b
        self.wheel_diameter = wheel_diameter
        self.velocity = 0
        self.direction = 0
        self.angular_rate = 0
        self.board = BoardSDK()
        self.rad_per_deg = math.pi / 180

    def reset_motors(self):
        """Stop all motors and reset movement attributes."""
        self.board.set_motor_duty([(motor_id, 0) for motor_id in self.MOTOR_IDS])
        self.velocity = 0
        self.direction = 0
        self.angular_rate = 0

    def set_velocity_polar(self, velocity, direction, angular_rate, fake=False):
        """
        Use polar coordinates to control movement.
        :param velocity: mm/s how fast its moving
        :param direction: moving direction in degrees (0-360).
        :param angular_rate: Rotation speed of the chassis.
        :param fake: If True, no action is performed.
        """
        # Normalize direction to 0–360 degrees
        direction %= 360

        # Calculate velocity components
        vx = velocity * math.cos(direction * self.rad_per_deg)
        vy = velocity * math.sin(direction * self.rad_per_deg)
        vp = -angular_rate * (self.a + self.b)

        # Motor duty cycle calculations
        motor_speeds = [
            (1, -int(vy + vx - vp)),  # Motor 1
            (2, int(vy - vx + vp)),   # Motor 2
            (3, -int(vy - vx - vp)),  # Motor 3
            (4, int(vy + vx + vp))    # Motor 4
        ]

        # Apply motor duties if not in fake mode
        if not fake:
            self.board.set_motor_duty(motor_speeds)

        # Update current state
        self.velocity = velocity
        self.direction = direction
        self.angular_rate = angular_rate

    def move_chassis_cartesian(self, velocity_x, velocity_y, fake=False):
        """
        Move the chassis based on Cartesian coordinates.
        :param velocity_x: Velocity in the X direction.
        :param velocity_y: Velocity in the Y direction.
        :param fake: If True, no action is performed.
        """
        # Calculate velocity magnitude and direction
        velocity = math.hypot(velocity_x, velocity_y)
        direction = math.degrees(math.atan2(velocity_y, velocity_x)) % 360

        if fake:
            return velocity, direction
        self.set_velocity_polar(velocity, direction, 0)
