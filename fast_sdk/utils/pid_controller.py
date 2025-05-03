class PIDController:
    """
    A class to encapsulate Proportional-Integral-Derivative (PID) control logic.

    PID control is a feedback mechanism widely used in control systems to minimize the error 
    between a desired setpoint and the current process variable. It calculates a correction 
    based on three parameters:
        - Proportional (P): The immediate error.
        - Integral (I): The accumulated error over time.
        - Derivative (D): The rate of change of the error.

    Attributes:
        kp (float): The proportional gain constant.
        ki (float): The integral gain constant.
        kd (float): The derivative gain constant.
        last_error (float): The error from the previous calculation, used for the derivative term.
        integral (float): The running sum of errors, used for the integral term.
    """

    def __init__(self, kp: float, ki: float = 0.0, kd: float = 0.0):
        """
        Initialize the PIDController with the given gain constants.

        :param kp: Proportional gain constant. determines the overall sensitivity to the error
        :param ki: Integral gain constant (default is 0.0). adjusts how the system compensates for long-term errors it shoud be 0 
        :param kd: Derivative gain constant (default is 0.0). determines how the system responds to rapid changes in error, helping to prevent sharp movements
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_error = 0.0
        self.integral = 0.0

    def calculate_correction(self, error: float) -> float:
        """
        Calculate the correction based on the current error.

        The correction is calculated as the sum of three components:
            - Proportional: Proportional to the current error.
            - Integral: Proportional to the accumulated error over time.
            - Derivative: Proportional to the rate of change of the error.

        :param error: The current error value (difference between desired setpoint and actual value).
        :return: Correction value to reduce the error.
        """
        # Proportional term: directly proportional to the current error
        proportional = self.kp * error

        # Integral term: sum of all past errors (accumulated over time)
        self.integral += error
        integral = self.ki * self.integral

        # Derivative term: rate of change of error
        derivative = self.kd * (error - self.last_error)

        # Update last error for the next iteration
        self.last_error = error

        # Compute total correction
        correction = proportional + integral + derivative

        return correction

    def reset(self):
        """
        Reset the integral and last error to zero.

        This can be useful when the PID controller needs to be re-initialized or reused for a new process.
        """
        self.integral = 0.0
        self.last_error = 0.0
