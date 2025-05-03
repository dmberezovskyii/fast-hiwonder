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

The PID controller adjusts the system's behavior by combining three components:

1. **Proportional (P):**
   - Reacts to the current error.
   - Formula:
     \[
     P = K_p \cdot e(t)
     \]
     Where:
     - \(K_p\): Proportional gain.
     - \(e(t)\): Current error.

2. **Integral (I):**
   - Reacts to the accumulated error over time.
   - Formula:
     \[
     I = K_i \int e(t) dt
     \]
     Where:
     - \(K_i\): Integral gain.

3. **Derivative (D):**
   - Reacts to the rate of change of the error.
   - Formula:
     \[
     D = K_d \frac{de(t)}{dt}
     \]
     Where:
     - \(K_d\): Derivative gain.

**Output Correction**:
\[
u(t) = P + I + D = K_p \cdot e(t) + K_i \cdot \int e(t) dt + K_d \cdot \frac{de(t)}{dt}
\]

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
