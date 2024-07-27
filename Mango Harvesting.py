import time
import random
import matplotlib.pyplot as plt
import numpy as np

# Function to simulate depth measurement (in meters)
def measure_distance():
    # Simulate depth measurement between 0.2 meters and 3.0 meters
    return random.uniform(0.2, 3)

# Function to draw the mango
def draw_mango(ax, position):
    mango_radius = 0.2
    mango_circle = plt.Circle(position, mango_radius, color='orange', fill=True)
    ax.add_patch(mango_circle)
    
    # Adding the stem to the mango
    stem_length = 0.25
    stem_position = (position[0], position[1] + mango_radius)
    ax.plot([stem_position[0], stem_position[0]], 
            [stem_position[1], stem_position[1] + stem_length], 
            'saddlebrown', lw=4)

# Function to simulate extending the actuator
def extend_actuator(duration, distance, ax, mango_position):
    print(f"Simulating extending actuator for {duration:.2f} seconds...")
    steps = int(duration * 10)  # More steps for smoother animation
    for step in range(steps):
        ax.clear()
        ax.set_xlim(0, 5)
        ax.set_ylim(-1, 1)
        current_distance = distance * (step / steps)
        ax.plot([0, current_distance], [0, 0], 'r-', lw=6)
        ax.plot(current_distance, 0, 'ro', markersize=12)
        # Visualize the cutting mechanism as part of the manipulator
        draw_cutting_mechanism(ax, current_distance, 0.4, 0.2, "open")
        draw_mango(ax, mango_position)
        
        ax.set_title(f"Extending Actuator: {current_distance:.2f} meters")
        plt.pause(0.1)
    print("Actuator extended.")

# Function to simulate retracting the actuator
def retract_actuator(duration, distance, ax):
    print(f"Simulating retracting actuator for {duration:.2f} seconds...")
    steps = int(duration * 10)  # More steps for smoother animation
    for step in range(steps):
        ax.clear()
        ax.set_xlim(0, 5)
        ax.set_ylim(-1, 1)
        current_distance = distance * (1 - step / steps)
        ax.plot([0, current_distance], [0, 0], 'r-', lw=6)
        ax.plot(current_distance, 0, 'ro', markersize=12)
        # Visualize the cutting mechanism as part of the manipulator
        draw_cutting_mechanism(ax, current_distance, 0.4, 0.2, "closed")
        draw_mango(ax, (current_distance + 0.2, -0.4))
        ax.set_title(f"Retracting Actuator: {current_distance:.2f} meters")
        plt.pause(0.1)
    print("Actuator retracted.")

# Function to draw the cutting mechanism
def draw_cutting_mechanism(ax, x, width, height, state):
    if state == "open":
        ax.plot([x + width / 2, x + width], [0, height / 2], 'b-', lw=6)
        ax.plot([x + width / 2, x + width], [0, -height / 2], 'b-', lw=6)
        ax.plot([x, x + width], [height / 2 , height / 2], 'b-', lw=6)
        ax.plot([x, x + width], [-height / 2, -height / 2], 'b-', lw=6)
    elif state == "closed":
        ax.plot([x, x + width / 2], [height / 2, 0], 'b-', lw=6)
        ax.plot([x, x + width / 2], [-height / 2, 0], 'b-', lw=6)
        ax.plot([x + width / 2, x + width], [0, height / 2], 'b-', lw=6)
        ax.plot([x + width / 2, x + width], [0, -height / 2], 'b-', lw=6)

# Function to simulate cutting action
def operate_cutting_mechanism(action, distance, ax, mango_position):
    print(f"Simulating cutting mechanism {action}...")
    steps = 20  # Number of steps for smoother animation
    for step in range(steps):
        ax.clear()
        ax.set_xlim(0, 5)
        ax.set_ylim(-1, 1)
        ax.plot([0, distance], [0, 0], 'r-', lw=6)
        ax.plot(distance, 0, 'ro', markersize=12)
        
        if action == "close":
            draw_cutting_mechanism(ax, distance, 0.4 * (1 - step/2 / steps), 0.2, "closed")
        elif action == "open":
            draw_cutting_mechanism(ax, distance, 0.4 * (step / steps), 0.2, "open")
        draw_mango(ax, mango_position)
        
        ax.set_title(f"Cutting Mechanism {action.capitalize()}")
        plt.pause(0.05)
    print(f"Cutting mechanism {action} completed.")

def main():
    fig, ax = plt.subplots()
    fig.show()

    try:
        # Simulate measuring distance
        distance = measure_distance()
        mango_position = (distance + 0.2, -0.4)
        if distance is not None:
            print(f"Measured Distance: {distance:.2f} meters")

            # Constants for actuator control
            speed_meters_per_second = 0.1  # Example speed of actuator in meters per second

            # Calculate time required to cover the measured distance
            time_seconds = distance / speed_meters_per_second

            print(f"Time required to cover {distance:.2f} meters: {time_seconds:.2f} seconds")

            # Simulate extending the actuator
            extend_actuator(time_seconds, distance, ax, mango_position)

            # Simulate closing the cutting mechanism
            operate_cutting_mechanism("close", distance, ax, mango_position)

            # Simulate some action after extending (e.g., cutting)
            print("Performing some action after extending...")

            # Simulate retracting the actuator
            retract_actuator(time_seconds, distance, ax)

            # Simulate opening the cutting mechanism
            operate_cutting_mechanism("open", 0.1, ax, mango_position)

            # Simulate some action after retracting (e.g., releasing)
            print("Performing some action after retracting...")
        
        else:
            print("Failed to measure distance.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up resources if needed (not necessary in this simulation)
        pass

if __name__ == "__main__":
    main()
