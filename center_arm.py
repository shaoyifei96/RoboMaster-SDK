from robomaster import robot

def center_arm():
    """Centers the robotic arm and returns it to home position (0,0)."""
    try:
        # Initialize the robot
        ep_robot = robot.Robot()
        ep_robot.initialize(conn_type="sta")
        ep_arm = ep_robot.robotic_arm
        
        print("Centering robotic arm...")
        ep_arm.recenter().wait_for_completed()
        print("Arm centered successfully!")
        
    except Exception as e:
        print(f"Error centering arm: {str(e)}")
    finally:
        ep_robot.close()

if __name__ == '__main__':
    center_arm() 