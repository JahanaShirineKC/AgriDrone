import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon
import math

# Function to generate random pests data
def generate_random_pests(num_pests, leaf_shape):
    pest_data = []
    for _ in range(num_pests):
        centroid = (np.random.randint(0, leaf_shape[0]), np.random.randint(0, leaf_shape[1]))
        area = np.random.randint(10, 100)  # Random area for each pest
        pest_data.append({
            'centroid': centroid,
            'area': area
        })
    return pest_data

# Function to draw a leaf shape
def draw_leaf(ax, leaf_shape):
    leaf_points = np.array([
        [0.5 * leaf_shape[0], 0],  # Top point
        [leaf_shape[0], 0.25 * leaf_shape[1]],  # Right point
        [0.75 * leaf_shape[0], leaf_shape[1]],  # Bottom right
        [0.25 * leaf_shape[0], leaf_shape[1]],  # Bottom left
        [0, 0.25 * leaf_shape[1]],  # Left point
    ])
    leaf_polygon = Polygon(leaf_points, closed=True, color='green', alpha=0.3)
    ax.add_patch(leaf_polygon)

# Function to check if a point is inside the leaf
def is_inside_leaf(point, leaf_shape):
    leaf_points = np.array([
        [0.5 * leaf_shape[0], 0],
        [leaf_shape[0], 0.25 * leaf_shape[1]],
        [0.75 * leaf_shape[0], leaf_shape[1]],
        [0.25 * leaf_shape[0], leaf_shape[1]],
        [0, 0.25 * leaf_shape[1]],
    ])
    polygon = Polygon(leaf_points, closed=True)
    return polygon.contains_point(point)

# Function to calculate the angle and diameter of spray
def calculate_spray_parameters(drone_position, pest_position, spray_radius):
    distance = np.sqrt((drone_position[0] - pest_position[0])**2 + (drone_position[1] - pest_position[1])**2)
    angle = np.degrees(np.arctan2(pest_position[1] - drone_position[1], pest_position[0] - drone_position[0]))
    diameter = 2 * spray_radius  # Diameter of the spray coverage
    return distance, angle, diameter

# Set up animation
def animate(i, pest_data, ax, leaf_shape, drone, spray_radius, sprayed_area):
    ax.clear()
    
    # Draw leaf
    draw_leaf(ax, leaf_shape)
    
    # Update drone position
    if i < len(pest_data):
        centroid = pest_data[i]['centroid']
        distance, angle, diameter = calculate_spray_parameters(drone.center, centroid, spray_radius)
        drone.set_center(centroid)
        # Draw spray area with dynamic diameter
        spray_circle = plt.Circle(centroid, diameter / 2, color='blue', alpha=0.5)  # Use diameter / 2 for radius
        ax.add_patch(spray_circle)
        sprayed_area.append(spray_circle)
        
        # Display parameters
        ax.text(10, leaf_shape[1] - 30, f'Pest {i+1}', color='black', fontsize=12)
        ax.text(10, leaf_shape[1] - 60, f'Distance: {distance:.2f}', color='black', fontsize=12)
        ax.text(10, leaf_shape[1] - 90, f'Angle: {angle:.2f}°', color='black', fontsize=12)
        ax.text(10, leaf_shape[1] - 120, f'Diameter: {diameter:.2f}', color='black', fontsize=12)

    # Draw pests
    for pest in pest_data:
        centroid = pest['centroid']
        ax.plot(centroid[0], centroid[1], 'go')
    
    # Draw sprayed areas
    for area in sprayed_area:
        ax.add_patch(area)

    ax.set_xlim(0, leaf_shape[0])
    ax.set_ylim(0, leaf_shape[1])
    ax.set_aspect('equal')
    ax.axis('off')


# Define parameters
leaf_shape = (500, 300)  # Size of the leaf (width x height)
num_pests = 10  # Number of pests
spray_radius = 30  # Radius of spray coverage in pixels

# Generate random pests data
pest_data = generate_random_pests(num_pests, leaf_shape)

# Filter pests inside the leaf
pest_data = [pest for pest in pest_data if is_inside_leaf(pest['centroid'], leaf_shape)]

# Calculate distances from the drone (fixed at the center of the leaf for simplicity)
drone_position = (leaf_shape[0] / 2, leaf_shape[1] / 2)
for pest in pest_data:
    pest['distance'] = np.sqrt((drone_position[0] - pest['centroid'][0])**2 + (drone_position[1] - pest['centroid'][1])**2)

# Sort pests by distance from the drone (maximum to minimum)
pest_data.sort(key=lambda p: p['distance'], reverse=True)

# Calculate total pest area
total_pest_area = sum(pest['area'] for pest in pest_data)

# Calculate adjustment
spray_rate = np.pi * spray_radius**2  # Effective spray coverage area in pixels^2
num_adjustments = total_pest_area / spray_rate

# Define the movement of threaded shaft per adjustment
movement_per_adjustment = 5  # Example movement in mm per adjustment

# Calculate the total required movement of the threaded shaft
total_movement = num_adjustments * movement_per_adjustment

# Print results
print(f'Total Pest Area: {total_pest_area:.2f} square pixels')
print(f'Number of Adjustments Required: {num_adjustments:.2f}')
print(f'Total Movement Required for Threaded Shaft: {total_movement:.2f} mm')

# Set up plot for animation
fig, ax = plt.subplots(figsize=(10, 6))
drone = plt.Circle((0, 0), 5, color='cyan', fill=True)  # Drone representation
sprayed_area = []

# Create animation
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=len(pest_data)+1,
    fargs=(pest_data, ax, leaf_shape, drone, spray_radius, sprayed_area),
    interval=1000,
    repeat=False
)

plt.show()
