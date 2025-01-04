import sys

import time
import signal

from fast_sdk.board_sdk import BoardSDK

if sys.version_info.major == 2:
    print("Please run this program with python3!")
    sys.exit(0)

board = BoardSDK()

start = True


def Stop(signum, frame):
    global start

    start = False
    print("关闭中...")
    board.set_motor_duty([[1, 0], [2, 0], [3, 0], [4, 0]])  # close all motors


signal.signal(signal.SIGINT, Stop)

if __name__ == "__main__":
    while True:
        board.set_motor_duty([[1, 35]])  # (set motor 1 speed to 35)
        time.sleep(0.2)
        board.set_motor_duty([[1, 90]])  # (set motor 1 speed to 90)
        time.sleep(0.2)

        if not start:
            board.set_motor_duty(
                [[1, 0], [2, 0], [3, 0], [4, 0]]
            )  # (close all motors)
            print("Closed")
            break
