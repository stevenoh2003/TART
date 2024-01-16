import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Sample data points
data_points = np.array([
    [255, 9.2],  # Each sub-array is a point [x, y]
    [200, 8.4],
    [127, 7],
    [100, 6.08],
    [90, 5.79],
    [80, 5.37]
])

# Split the data into x and y components
x = data_points[:, 0].reshape(-1, 1)  # features
y = data_points[:, 1]  # target values

# Create and fit the model
model = LinearRegression()
model.fit(x, y)

# Function to make predictions
def predict_point(x_value):
    return model.predict([[x_value]])[0]

# Predict a specific point (for example, x=4)
x_to_predict = 85
predicted_y = predict_point(x_to_predict)
print(f"Predicted y-value for x={x_to_predict}: {predicted_y}")

# Extrapolate for a range of x-values
x_range = np.linspace(min(x), max(x) + 5, 100).reshape(-1, 1)
y_predicted = model.predict(x_range)

# Plotting
plt.scatter(x, y, color='red', label='Data Points')
plt.plot(x_range, y_predicted, label='Extrapolated Line')
plt.scatter([x_to_predict], [predicted_y], color='blue', label=f'Predicted Point (x={x_to_predict})')
plt.legend()
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Line Extrapolation with Linear Regression')
plt.show()
