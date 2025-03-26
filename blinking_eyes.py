import time
import random
import os
from pathlib import Path
import openai  # older version of openai
import pygame
from robomaster import robot
from robomaster import led
import subprocess

def get_battery_color(battery_level):
    """Returns RGB values based on battery level
    Green: 100-60%
    Yellow: 60-30%
    Red: 30-0%
    """
    if battery_level >= 60:
        return (0, 255, 0)  # Green
    elif battery_level >= 30:
        return (255, 255, 0)  # Yellow
    else:
        return (255, 0, 0)  # Red

def battery_callback(battery_info, robot_led):
    """Callback function for battery updates
    Updates the left and right armor colors based on battery level
    """
    battery_level = battery_info
    r, g, b = get_battery_color(battery_level)
    robot_led.set_led(comp=led.COMP_BOTTOM_LEFT, r=r, g=g, b=b, effect=led.EFFECT_ON)
    robot_led.set_led(comp=led.COMP_BOTTOM_RIGHT, r=r, g=g, b=b, effect=led.EFFECT_ON)

def say_phrase(phrase):
    """Generate and play text-to-speech audio using OpenAI's TTS API in separate env"""
    try:
        # Call the TTS script in the openai environment
        subprocess.run([
            'conda', 'run', '-n', 'openai', 
            'python', 'tts_service.py', phrase
        ], check=True)
        
        # Play the generated audio using pygame
        # pygame.mixer.init()
        # pygame.mixer.music.load("temp_speech.wav")
        # pygame.mixer.music.play()
        # while pygame.mixer.music.get_busy():
        #     pygame.time.Clock().tick(10)
        # pygame.mixer.quit()
        ep_robot.play_audio(filename="temp_speech.wav").wait_for_completed()

    finally:
        # Clean up
        if os.path.exists("temp_speech.wav"):
            os.remove("temp_speech.wav")

def random_arm_movement(robotic_arm):
    """Make a random arm movement within safe ranges"""
    # Random x movement between -100 and 100mm
    x = random.uniform(-100, 100)
    # Random y movement between 50 and 150mm (keep it in front to avoid hitting the robot)
    y = random.uniform(50, 150)
    # Move the arm
    robotic_arm.move(x=x, y=y).wait_for_completed()
    # Return to home position
    robotic_arm.move(x=0, y=0).wait_for_completed()

# List of Jarvis-style phrases
FUNNY_PHRASES = [
    "At your service, sir.",
    "All systems operational.",
    "Running diagnostics... Everything appears to be functioning within normal parameters.",
    "I am fully charged and ready to assist.",
    "Processing environmental data.",
    "Maintaining optimal performance levels.",
    "Your command is my priority.",
    "I am here to help, sir.",
    "All systems are running at peak efficiency.",
    "Monitoring surroundings for potential threats.",
    "Ready to execute your next command.",
    "I am your AI assistant, how may I be of service?",
    "Maintaining constant vigilance.",
    "All systems are functioning normally.",
    "I am at your disposal, sir."
]

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_led = ep_robot.led
    ep_battery = ep_robot.battery
    ep_chassis = ep_robot.chassis
    ep_arm = ep_robot.robotic_arm

    # Subscribe to battery updates
    ep_battery.sub_battery_info(5, battery_callback, ep_led)

    try:
        while True:
            # Make front and back armor blink like eyes
            # Random interval between 0.5 and 2 seconds
            blink_interval = random.uniform(0.5, 2.0)
            
            # Eyes open (white)
            ep_led.set_led(comp=led.COMP_BOTTOM_FRONT, r=255, g=255, b=255, effect=led.EFFECT_ON)
            ep_led.set_led(comp=led.COMP_BOTTOM_BACK, r=255, g=255, b=255, effect=led.EFFECT_ON)
            
            time.sleep(blink_interval)
            
            # Eyes closed (off) and perform actions
            ep_led.set_led(comp=led.COMP_BOTTOM_FRONT, r=0, g=0, b=0, effect=led.EFFECT_OFF)
            ep_led.set_led(comp=led.COMP_BOTTOM_BACK, r=0, g=0, b=0, effect=led.EFFECT_OFF)
            
            # Say a random funny phrase
            phrase = random.choice(FUNNY_PHRASES)
            say_phrase(phrase)
            
            # Random wiggle angle between 10 and 15 degrees
            wiggle_angle = random.uniform(10, 15)
            # Rotate one way
            ep_chassis.move(x=0, y=0, z=wiggle_angle, z_speed=45).wait_for_completed()
            # Make a random arm movement
            random_arm_movement(ep_arm)
            # Rotate back to center
            ep_chassis.move(x=0, y=0, z=-wiggle_angle, z_speed=45).wait_for_completed()
            
            time.sleep(0.2)  # Brief blink
            
    except KeyboardInterrupt:
        # Unsubscribe from battery updates and turn off all LEDs before exiting
        ep_battery.unsub_battery_info()
        ep_led.set_led(comp=led.COMP_ALL, r=0, g=0, b=0, effect=led.EFFECT_OFF)
        # Return arm to home position before closing
        ep_arm.move(x=0, y=0).wait_for_completed()
        ep_robot.close()
        # Clean up any temporary files
        if os.path.exists("temp_speech.mp3"):
            os.remove("temp_speech.mp3") 