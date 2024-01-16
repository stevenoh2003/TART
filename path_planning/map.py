import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

# PWM to Voltage data points
pwm_voltage_data = np.array([
    [255, 9.2],
    [200, 8.4],
    [127, 7],
    [100, 6.08],
    [90, 5.79],
    [80, 5.37]
])

# Voltage to RPM data points
voltage_rpm_data = np.array([
    [6, 250],
    [4.5, 185],
    [3, 120]
])

# Fit a polynomial regression for PWM to Voltage
pwm = pwm_voltage_data[:, 0].reshape(-1, 1)
voltage_from_pwm = pwm_voltage_data[:, 1]
poly_pwm_to_voltage = PolynomialFeatures(degree=2)
pwm_poly = poly_pwm_to_voltage.fit_transform(pwm)
model_pwm_to_voltage = LinearRegression()
model_pwm_to_voltage.fit(pwm_poly, voltage_from_pwm)

# Fit a polynomial regression for Voltage to RPM
voltage = voltage_rpm_data[:, 0].reshape(-1, 1)
rpm = voltage_rpm_data[:, 1]
poly_voltage_to_rpm = PolynomialFeatures(degree=2)
voltage_poly = poly_voltage_to_rpm.fit_transform(voltage)
model_voltage_to_rpm = LinearRegression()
model_voltage_to_rpm.fit(voltage_poly, rpm)

# Function to predict RPM from PWM
def predict_rpm_from_pwm(pwm_value):
    # Convert PWM to Voltage
    pwm_poly = poly_pwm_to_voltage.transform([[pwm_value]])
    predicted_voltage = model_pwm_to_voltage.predict(pwm_poly)[0]
    
    # Convert Voltage to RPM
    voltage_poly = poly_voltage_to_rpm.transform([[predicted_voltage]])
    predicted_rpm = model_voltage_to_rpm.predict(voltage_poly)[0]
    
    return predicted_rpm


# test_pwm = 100
# predicted_rpm = predict_rpm_from_pwm(test_pwm)
# print(f"Predicted RPM for PWM={test_pwm}: {predicted_rpm}")



def inverse_kinematics_mecanum(Vx, Vy, omega, l, w, r):

    FL = (1/r) * (Vx - Vy - (l + w) * omega)  # Front Left Wheel
    FR = (1/r) * (Vx + Vy + (l + w) * omega)  # Front Right Wheel
    RL = (1/r) * (Vx + Vy - (l + w) * omega)  # Rear Left Wheel
    RR = (1/r) * (Vx - Vy + (l + w) * omega)  # Rear Right Wheel

    return FL, FR, RL, RR

def rpm_to_rad_s(rpm):
    return rpm * (2 * np.pi / 60)

def are_about_the_same(a, b, tolerance=3):
    return abs(a - b) <= tolerance

Vx = 1.0
Vy = 0.0
omega = 0.0
l = 0.09  
w = 0.09  
r = 0.03

print("Vx: ", Vx)
print("Vy: ", Vy)
print("Omega: ", omega)

wheel_speeds = inverse_kinematics_mecanum(Vx, Vy, omega, l, w, r)
print(wheel_speeds)

pwm_list = []
for j in wheel_speeds:
    match_found = False
    for i in range(1, 255):
        rpm_current = predict_rpm_from_pwm(i)
        
        rad_per_s_current = rpm_to_rad_s(rpm_current)

        if are_about_the_same(rad_per_s_current, j):
            pwm_list.append(i)
            match_found = True
            break

    # If no match is found for a particular wheel speed, append a placeholder or handle it
    if not match_found:
        pwm_list.append(0)  # or some other placeholder value

print(pwm_list)



