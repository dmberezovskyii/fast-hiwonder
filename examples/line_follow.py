import sys
import logging
from fast_sdk.motors import ControlChassis
from fast_sdk.infra_red import InfraredSensors
from fast_sdk.line_follower import LineFollower
from fast_sdk.utils.pid_controller import PIDController


def setup_logger() -> None:
    """Setup the logger configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


if __name__ == "__main__":
    print('''
    ----------------------------------------------------------
    Official Website: https://www.hiwonder.com
    Online Mall: https://hiwonder.tmall.com
    ----------------------------------------------------------
    ''')


    setup_logger()

    # Initialize components
    chassis = ControlChassis()
    sensor = InfraredSensors()
    pid = PIDController(kp=0.9, kd=0.3)  # Customize Kp, Ki, and Kd values
    weights = [-5, -1, 1, 5]  # Adjust weights based on sensor placement
    base_speed = 30  # Base speed for the chassis

    # Create LineFollower instance
    line_follower = LineFollower(chassis, sensor, pid, weights, base_speed)

    # Start line-following
    line_follower.follow_line()