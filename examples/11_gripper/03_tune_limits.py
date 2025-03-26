import time
import robomaster
from robomaster import robot

def sub_data_handler(sub_info):
    status = sub_info
    print(f"Gripper status: {status}")

def test_gripper_power(ep_gripper, power_level, direction="open"):
    print(f"\nTesting {direction} with power level {power_level}")
    if direction == "open":
        ep_gripper.open(power=power_level)
    else:
        ep_gripper.close(power=power_level)
    time.sleep(2)
    ep_gripper.pause()

def main():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    
    ep_gripper = ep_robot.gripper
    
    # Subscribe to gripper status
    ep_gripper.sub_status(freq=5, callback=sub_data_handler)
    
    # Test different power levels for opening
    print("\nTesting opening with different power levels...")
    power_levels = [25, 50, 75, 100]
    for power in power_levels:
        test_gripper_power(ep_gripper, power, "open")
        time.sleep(1)
    
    # Test different power levels for closing
    print("\nTesting closing with different power levels...")
    for power in power_levels:
        test_gripper_power(ep_gripper, power, "close")
        time.sleep(1)
    
    # Test fine control with small power increments
    print("\nTesting fine control with small power increments...")
    fine_power_levels = [30, 40, 50, 60, 70]
    for power in fine_power_levels:
        test_gripper_power(ep_gripper, power, "open")
        time.sleep(1)
        test_gripper_power(ep_gripper, power, "close")
        time.sleep(1)
    
    # Unsubscribe and close
    ep_gripper.unsub_status()
    ep_robot.close()

if __name__ == '__main__':
    main() 