import time
from robomaster import robot

def print_position(sub_info):
    pos_x, pos_y = sub_info
    print(f"Arm position - X: {pos_x}mm, Y: {pos_y}mm")

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    ep_arm = ep_robot.robotic_arm
    
    # Subscribe to position updates
    ep_arm.sub_position(freq=5, callback=print_position)
    
    try:
        print("\nMoving to home position...")
        ep_arm.recenter().wait_for_completed()
        time.sleep(1)
        
        print("\nDemonstrating relative movements:")
        # Move forward 50mm
        print("Moving forward 50mm...")
        ep_arm.move(x=50, y=0).wait_for_completed()
        time.sleep(1)
        
        # Move up 30mm
        print("Moving up 30mm...")
        ep_arm.move(x=0, y=30).wait_for_completed()
        time.sleep(1)
        
        print("\nDemonstrating absolute position:")
        # Move to a specific position
        print("Moving to position (100, 50)...")
        ep_arm.moveto(x=100, y=50).wait_for_completed()
        time.sleep(1)
        
        # Return to home position
        print("\nReturning to home position...")
        ep_arm.recenter().wait_for_completed()
        
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    finally:
        # Unsubscribe from position updates and close connection
        ep_arm.unsub_position()
        ep_robot.close() 