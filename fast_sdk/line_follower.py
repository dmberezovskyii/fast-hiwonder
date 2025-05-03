import time
import signal
import logging
from fast_sdk.motors import ControlChassis
from fast_sdk.infra_red import InfraredSensors
from fast_sdk.utils.pid_controller import PIDController


class LineFollower:
    """
    A class to manage line-following logic and hardware interaction.
    """
    def __init__(self, chassis: ControlChassis, sensor: InfraredSensors, pid: PIDController, weights: list, base_speed: int):
        self.chassis = chassis
        self.sensor = sensor
        self.pid = pid
        self.weights = weights
        self.base_speed = base_speed
        self.running = True

        # Register signal handler
        signal.signal(signal.SIGINT, self.stop_program)

    def calculate_error(self, sensor_data: list) -> float:
        """
        Calculate the error based on sensor data and weights.
        :param sensor_data: List of sensor readings.
        :return: Calculated error.
        """
        return sum(w * s for w, s in zip(self.weights, sensor_data))

    def stop_program(self, signum, frame):
        """
        Signal handler to gracefully stop the program.
        """
        logging.info("Stopping program...")
        self.running = False
        self.reset_motors()
        logging.info("All motors stopped. Program terminated.")

    def reset_motors(self):
        """
        Gracefully reset all motors.
        """
        self.chassis.reset_motors()

    def follow_line(self):
        """
        Main logic for following a line using PID control.
        """
        logging.info("Starting line-following program...")

        try:
            while self.running:
                # Read sensor data
                sensor_data = self.sensor.read_sensor_data()
                logging.info(
                    "Sensor Readings -> Sensor1: %d, Sensor2: %d, Sensor3: %d, Sensor4: %d",
                    *sensor_data
                )

                # Calculate error and correction
                error = self.calculate_error(sensor_data)
                correction = self.pid.calculate_correction(error)

                # Calculate velocity, direction, and angular rate
                velocity = self.base_speed
                direction = (90 + correction) % 360  # Ensure direction is within 0-360 degrees
                angular_rate = correction * 0.5  # Optional: adjust rotation rate based on correction

                # Apply motor velocities using set_velocity
                self.chassis.set_velocity(velocity, direction, angular_rate, fake=False)

                # Add a small delay
                time.sleep(0.1)

        except Exception as e:
            logging.error("An error occurred: %s", e, exc_info=True)
        finally:
            self.reset_motors()
            logging.info("Program exited cleanly.")