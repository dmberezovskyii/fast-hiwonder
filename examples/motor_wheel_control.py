import time

from fast_sdk.motors import Motors


# Example Usage: Moving the robot in a square path
def move_in_square(
    mecanum_wheel: Motors, side_length=100, speed=50, angular_rate=30, fake=False
):
    """
    Move the robot in a square path.
    :param mecanum_wheel: Instance of MecanumWheel
    :param side_length: Length of each side of the square in mm
    :param speed: Forward speed in mm/s
    :param angular_rate: Rotation speed in degrees per second
    :param fake: If True, no action is performed (for testing purposes)
    """
    for _ in range(4):  # Move in 4 directions to form a square
        # Move forward
        mecanum_wheel.move_chassis_cartesian(
            speed, 0, fake=fake
        )  # Move along X direction
        time.sleep(side_length / speed)  # Wait for the robot to complete the side

        # Turn 90 degrees (clockwise)
        mecanum_wheel.set_velocity_polar(0, 0, angular_rate, fake=fake)
        time.sleep(90 / angular_rate)  # Wait for the robot to complete the turn

        # Reset the angular rate after turning
        mecanum_wheel.reset_motors()


motors = Motors()

# Move in a square with a side length of 100mm, speed of 50mm/s, and angular rate of 30 degrees/s
move_in_square(motors, side_length=100, speed=50, angular_rate=30, fake=False)
