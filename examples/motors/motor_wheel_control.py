import sys
import time
import signal
from fast_sdk.motors import ControlChassis


# Ensure Python 3 is used
if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)


chassis = ControlChassis()

start = True

# Function to handle graceful shutdown on receiving SIGINT
def stop_program(signum, frame):
    global start
    start = False
    print('Shutting down...')
    chassis.set_velocity(0, 0, 0)  # Reset all motors gracefully


signal.signal(signal.SIGINT, stop_program)


if __name__ == '__main__':
    print('''
    ----------------------------------------------------------
    Official Website: https://www.hiwonder.com
    Online Mall: https://hiwonder.tmall.com
    ----------------------------------------------------------
    ''')


    try:
        while start:
            # Control the chassis movement - Right direction example
            chassis.set_direction(velocity=50, direction="Right")
            time.sleep(1)

    except Exception as e:
        print(f"Error occurred: {e}")
        chassis.set_velocity(0, 0, 0)  # Ensure motors are stopped in case of an error
    finally:
        chassis.set_velocity(0, 0, 0)
