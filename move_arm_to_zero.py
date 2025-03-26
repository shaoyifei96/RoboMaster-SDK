import robomaster
from robomaster import robot
import time
import random
current_x = 0
current_y = 0 
current_position_name = 'RECENTER'
# Position coordinates for key locations (x, y in mm)
POSITIONS = {
    'FRONT_LOW': (155, -96),      # Front position, lower height
    'FRONT_HIGH': (173, 144),     # Front position, higher height
    'FAR_REACH': (200, -46),      # Maximum forward reach
    'STOW_LOOK_UP': (85, 157),    # Side position, higher height
    'STOW_LOOK_FORWARD': (74, 57), # Side position, middle height
    'RECENTER': (0, 0)
}
def convert_to_signed(value, bits=32):
    """Convert an unsigned integer to signed representation."""
    if value >= 2**(bits - 1):
        value -= 2**bits
    return value

def sub_data_handler(sub_info):
    global current_x, current_y
    try:
        # Convert to signed integers if needed
        x, y = sub_info
        current_x = convert_to_signed(x)
        current_y = convert_to_signed(y)
        # print(f"Raw position data: {sub_info}")
        # print(f"Processed position - x: {current_x}, y: {current_y}")
    except Exception as e:
        print(f"Error processing position data: {e}")

def move_to_target(ep_arm):
    global current_x, current_y, current_position_name
    try:
        # Cycle through all positions continuously
        while True:
            # Randomly select a position
            position_name = random.choice(list(POSITIONS.keys()))
            target_x, target_y = POSITIONS[position_name]
            print(f"Moving to {position_name} position ({target_x}, {target_y})...")
            # For FRONT_LOW position, go to FAR_REACH first
            if position_name != current_position_name:
                # If we're currently in FRONT_LOW and moving to a different position,
                # we need to go through FAR_REACH first
                if current_position_name == 'FRONT_LOW' and position_name != 'FRONT_LOW':
                    print("Moving to FAR_REACH first to safely exit FRONT_LOW position...")
                    far_x, far_y = POSITIONS['FAR_REACH']
                    ep_arm.moveto(x=far_x, y=far_y).wait_for_completed()
                
                # If moving to FRONT_LOW, go through FAR_REACH first
                elif position_name == 'FRONT_LOW':
                    print("Moving to FAR_REACH first...")
                    far_x, far_y = POSITIONS['FAR_REACH'] 
                    ep_arm.moveto(x=far_x, y=far_y).wait_for_completed()

                # Move to the target position
                if position_name == 'RECENTER':
                    ep_arm.recenter().wait_for_completed()
                else:
                    ep_arm.moveto(x=target_x, y=target_y).wait_for_completed()
            
            current_position_name = position_name
            # Wait 1 second before next movement
            # time.sleep(1)
            print("Movement completed!")
    except Exception as e:
        print(f"Error during movement: {e}")

def main():
    ep_robot = None
    try:
        # Initialize the robot
        ep_robot = robot.Robot()
        ep_robot.initialize(conn_type="sta")

        # Get the robotic arm instance
        ep_arm = ep_robot.robotic_arm

        # Subscribe to position updates
        print("Subscribing to position updates...")
        ep_arm.sub_position(freq=5, callback=sub_data_handler)
        time.sleep(1)  # Give some time to get initial position

        # Move to target position
        move_to_target(ep_arm)

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    finally:
        if ep_robot:
            # Cleanup
            try:
                ep_arm.unsub_position()
                ep_robot.close()
            except:
                pass

if __name__ == '__main__':
    main() 