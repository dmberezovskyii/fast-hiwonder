# Documentation for Line Follower with Raspberry Pi

This documentation provides a detailed explanation of how to implement a line-following robot using Raspberry Pi and the `fast_sdk` library. It covers the key components, including the chassis, sensors, PID controller, and the main logic for line-following.

---

## **Overview**

The line-following robot uses infrared sensors to detect the path, a PID controller to calculate corrections, and a chassis control system to drive the motors. The program follows these steps:
1. Reads sensor data.
2. Calculates the error using weights.
3. Computes correction values using the PID controller.
4. Controls motor velocities to adjust the robot's movement.

---

## **Class: LineFollower**

### **Purpose**
Manages the line-following logic and hardware interaction.

### **Initialization**

```python
def __init__(self, chassis: ControlChassis, sensor: InfraredSensors, pid: PIDController, weights: list, base_speed: int):
```

- **Parameters**:
  - `chassis` (ControlChassis): Controls the motors and chassis movement.
  - `sensor` (InfraredSensors): Reads data from infrared sensors.
  - `pid` (PIDController): PID controller for calculating corrections.
  - `weights` (list): Weights to calculate the error from sensor data.
  - `base_speed` (int): Base speed of the robot.

---

### **Key Methods**

#### **`calculate_error(sensor_data: list) -> float`**
Calculates the error based on sensor readings and weights.

- **Input**:
  - `sensor_data`: List of sensor readings.
- **Output**:
  - A float representing the calculated error.

#### **`stop_program(signum, frame)`**
Handles termination signals (e.g., `Ctrl+C`) and stops the motors safely.

#### **`reset_motors()`**
Resets motor velocities to zero.

#### **`follow_line()`**
Main logic for following the line using the PID controller.

- **Steps**:
  1. Reads sensor data.
  2. Calculates error and correction.
  3. Sets motor velocities based on the correction.
  4. Adds a delay to stabilize the loop.

---

## **Class: PIDController**

### **Purpose**
Implements a PID controller for calculating corrections based on error values.

### **Initialization**

```python
def __init__(self, kp: float, ki: float = 0.0, kd: float = 0.0):
```

- **Parameters**:
  - `kp` (float): Proportional gain.
  - `ki` (float): Integral gain.
  - `kd` (float): Derivative gain.

### **How PID Works**

The PID (Proportional-Integral-Derivative) controller is a feedback mechanism widely used in control systems to minimize the error between a desired setpoint and the current process variable. It calculates a correction by combining three components:

---

#### **1. Proportional (P)**
The proportional component reacts to the **current error** between the desired and actual values. It applies a correction that is directly proportional to the error.

- **Formula**:
  \[
  P = K_p \cdot e(t)
  \]
- **Explanation**:
  - \(K_p\): Proportional gain constant, which determines the system's sensitivity to the current error.
  - \(e(t)\): Current error at time \(t\).
- **Effect**:
  - Larger errors result in greater corrections, helping the system respond quickly.
  - However, it may not fully eliminate the error (steady-state error).

---

#### **2. Integral (I)**
The integral component accounts for **past errors** by summing them over time. It helps eliminate persistent errors (steady-state errors) that the proportional component cannot address.

- **Formula**:
  \[
  I = K_i \int e(t) \, dt
  \]
- **Explanation**:
  - \(K_i\): Integral gain constant, which determines how the system compensates for accumulated errors.
  - \(\int e(t) \, dt\): The cumulative sum of errors over time.
- **Effect**:
  - Reduces steady-state errors by accumulating small corrections.
  - Excessive integral action can lead to overshooting and instability.

---

#### **3. Derivative (D)**
The derivative component anticipates **future trends** by observing the rate of change in the error. It applies a correction based on how quickly the error is changing.

- **Formula**:
  \[
  D = K_d \frac{de(t)}{dt}
  \]
- **Explanation**:
  - \(K_d\): Derivative gain constant, which determines the system's response to rapid changes in error.
  - \(\frac{de(t)}{dt}\): The rate of change of the error at time \(t\).
- **Effect**:
  - Smoothes the system's response by dampening rapid changes and preventing overshooting.
  - Helps reduce oscillations and sharp movements.

---

### **Key Methods**

#### **`calculate_correction(error: float) -> float`**
Calculates the correction based on the current error.

- **Input**:
  - `error`: Current error value.
- **Output**:
  - A float representing the correction value.

---

## **Class: ControlChassis**

### **Purpose**
Handles motor controls and manages the movement of the chassis.

### **Initialization**

```python
def __init__(self, a: float = 67.0, b: float = 59.0, wheel_diameter: float = 65.0):
```

- **Parameters**:
  - `a`: Distance from the center to the front/back wheels (mm).
  - `b`: Distance from the center to the left/right wheels (mm).
  - `wheel_diameter`: Diameter of the wheels (mm).

---

### **Key Methods**

#### **`reset_motors()`**
Resets all motor velocities to zero.

#### **`set_velocity(velocity: float, direction: float, angular_rate: float, fake: bool = False)`**
Sets the velocity, direction, and angular rate of the chassis using polar coordinates.

- **Input**:
  - `velocity`: Speed in mm/s.
  - `direction`: Movement direction (0-360 degrees).
  - `angular_rate`: Angular rotation speed.
  - `fake`: If `True`, simulates the velocity without actuating motors.
