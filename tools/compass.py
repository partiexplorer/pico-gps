import math

def get_compass_direction(current_lat, current_lon, target_lat, target_lon):
    # Calculate the angle between the current location and the target location
    angle = math.atan2(target_lon - current_lon, target_lat - current_lat)
    # Convert angle to degrees
    angle_degrees = math.degrees(angle)
    # Normalize angle to be between 0 and 360 degrees
    angle_degrees = (angle_degrees + 360) % 360

    # Define compass directions
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    # Calculate the index of the closest compass direction
    idx = round(angle_degrees / 45) % 8
    # Get the compass direction
    compass_direction = directions[idx]

    return compass_direction, angle_degrees

# Example coordinates for current and target locations
current_lat = 37.7749
current_lon = -122.4194
target_lat = 34.0522
target_lon = -118.2437

direction, angle = get_compass_direction(current_lat, current_lon, target_lat, target_lon)
print(f"Compass Direction: {direction}\nAngle: {int(angle)} degrees")
