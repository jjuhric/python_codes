import RPi.GPIO as GPIO
import time

# Define GPIO pin for servo
servo_pin = 18  # Example - Use the pin you connected to

# Set up GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set up the GPIO pin as output
GPIO.setup(servo_pin, GPIO.OUT)

# Create a PWM object
servo = GPIO.PWM(servo_pin, 50)  # 50Hz PWM frequency

# Start the PWM
servo.start(0)  # Start at 0 duty cycle (servo at 0 degrees)
print ("Waiting for 1 second")
time.sleep(1)


angle = 0.0
def findTheDutyCycle(angle):
  return (angle/18.0) + 2.0 if angle >= 0 else 0

while angle >= 0:
  angle = float(input("What angle do you want?: "));
  duty = findTheDutyCycle(angle)
  servo.ChangeDutyCycle(duty)
  print("Duty: " + str(duty))
  print("Angle: " + str(angle)) if angle >= 0 else print("Exit command entered")

  time.sleep(0.25)
  servo.ChangeDutyCycle(0)
  time.sleep(0.25)

print("Turning back to 0 degrees")
servo.ChangeDutyCycle(2)
time.sleep(1)
servo.ChangeDutyCycle(0)

servo.stop()
GPIO.cleanup()
print("Everything is cleaned up")
