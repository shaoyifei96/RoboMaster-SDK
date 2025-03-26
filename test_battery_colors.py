import time
from robomaster import robot
from robomaster import led
from blinking_eyes import get_battery_color

def test_battery_levels():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    ep_led = ep_robot.led

    # Test battery levels: 100%, 75%, 45%, 15%
    test_levels = [100, 75, 45, 15]
    
    try:
        print("Testing battery level colors...")
        print("Green: 100-60%")
        print("Yellow: 60-30%")
        print("Red: 30-0%")
        print("\nPress Ctrl+C to exit")
        
        while True:
            for level in test_levels:
                print(f"\nTesting battery level: {level}%")
                r, g, b = get_battery_color(level)
                print(f"LED color: {'Green' if g == 255 and r == 0 else 'Yellow' if r == 255 and g == 255 else 'Red'}")
                
                # Set both left and right armor to the battery color
                ep_led.set_led(comp=led.COMP_BOTTOM_LEFT, r=r, g=g, b=b, effect=led.EFFECT_ON)
                ep_led.set_led(comp=led.COMP_BOTTOM_RIGHT, r=r, g=g, b=b, effect=led.EFFECT_ON)
                
                # Wait 3 seconds before next level
                time.sleep(3)
                
    except KeyboardInterrupt:
        print("\nTest completed. Cleaning up...")
        ep_led.set_led(comp=led.COMP_ALL, r=0, g=0, b=0, effect=led.EFFECT_OFF)
        ep_robot.close()

if __name__ == '__main__':
    test_battery_levels() 