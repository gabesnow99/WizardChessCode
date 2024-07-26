import matplotlib.pyplot as plt
import numpy as np

# Constants
radius = 3000  # Radius of the circle
center = (0, 0)
points = 10  # Total number of points

# Define the fixed points
fixed_points = [(0,0), (3000,0), (0,3000), (0,0)]

# Calculate the coordinates of the curve points
angles = np.linspace(0, np.pi/2, 8)  # Angles for the curve
curve_points = [(center[0] + radius * np.cos(angle), center[1] + radius * np.sin(angle)) for angle in angles]

# Arrange points in order
coordinates = fixed_points[:2] + curve_points + fixed_points[2:]
print(coordinates)

# Plot the coordinates
plt.figure(figsize=(8,8))
plt.plot(*zip(*coordinates), marker='o', linestyle='-', color='b')

# Label the coordinates
for idx, (x, y) in enumerate(coordinates, start=1):
    plt.text(x, y, f'{idx}', fontsize=12, ha='right')

# Set equal scaling
plt.gca().set_aspect('equal', adjustable='box')

# Set plot limits
plt.xlim(-radius, 2*radius)
plt.ylim(-radius, 2*radius)

# Add grid and labels
plt.grid(True)
plt.title('Plot of Curve with Coordinates')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

plt.show()

