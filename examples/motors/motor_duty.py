import sys
import time
import signal
import logging
from fast_sdk.board_sdk import BoardSDK


MOTOR_1 = 1
MOTOR_SPEED_LOW = 35
MOTOR_SPEED_HIGH = 90
ALL_MOTORS = [(1, 0), (2, 0), (3, 0), (4, 0)]


if sys.version_info.major < 3:
    sys.exit("This program requires Python 3. Please run it with Python 3.")


board = BoardSDK()

# Logger Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

running = True

def stop_program(signum, frame):
    """
    Signal handler to gracefully stop the program.
    """
    global running
    logging.info("Stopping program...")
    running = False
    board.set_motor_duty(ALL_MOTORS)
    logging.info("All motors stopped. Program terminated.")

signal.signal(signal.SIGINT, stop_program)

def main():
    """
    Main function to control the motor.
    """
    logging.info("Starting motor control program...")
    try:
        while running:
            logging.info("Setting motor %d speed to %d", MOTOR_1, MOTOR_SPEED_LOW)
            board.set_motor_duty([(MOTOR_1, MOTOR_SPEED_LOW)])
            time.sleep(0.2)

            logging.info("Setting motor %d speed to %d", MOTOR_1, MOTOR_SPEED_HIGH)
            board.set_motor_duty([(MOTOR_1, MOTOR_SPEED_HIGH)])
            time.sleep(0.2)
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)
    finally:
        board.set_motor_duty(ALL_MOTORS)
        logging.info("Program exited cleanly.")

if __name__ == "__main__":
    print('''
    Official website: https://www.hiwonder.com
    Online mall: https://hiwonder.tmall.com
    ''')
    main()
