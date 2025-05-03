class PIDController:
    """
    A class to encapsulate PID control logic.
    """
    def __init__(self, kp: float, ki: float = 0.0, kd: float = 0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_error = 0
        self.integral = 0

    def calculate_correction(self, error: float) -> float:
        """
        Calculate the correction based on the current error.
        :param error: The current error value.
        :return: Correction value.
        """
        # Proportional term
        proportional = self.kp * error

        # Integral term
        self.integral += error
        integral = self.ki * self.integral

        # Derivative term
        derivative = self.kd * (error - self.last_error)

        # Update last error
        self.last_error = error

        # Compute total correction
        correction = proportional + integral + derivative
        return correction
