import RPi.GPIO as GPIO
import time

# --- Configuration ---
BUTTON_PIN = 8        # BOARD pin for the button (e.g., physical pin 11)
SERVO_PIN = 18        # BOARD pin for the servo signal (e.g., physical pin 12)
DEBOUNCE_TIME = 0.05  # Debounce time in seconds (e.g., 50 milliseconds)

# Servo PWM frequency
PWM_FREQUENCY = 50 # Hz (Standard for most hobby servos)

# Duty cycles for common SG90 servo angles (adjust if your servo requires slight tuning)
# These values are based on a 20ms period (1000ms / 50Hz = 20ms)
# 0 degrees: ~0.5ms pulse -> (0.5ms / 20ms) * 100 = 2.5% duty cycle
# 90 degrees: ~1.5ms pulse -> (1.5ms / 20ms) * 100 = 7.5% duty cycle
# 180 degrees: ~2.5ms pulse -> (2.5ms / 20ms) * 100 = 12.5% duty cycle
ANGLE_0_DUTY_CYCLE = 8.1
ANGLE_90_DUTY_CYCLE = 2.0

# --- GPIO Setup ---
# Use BOARD pin-numbering scheme (physical pin numbers)
GPIO.setmode(GPIO.BOARD)

# Setup button pin as input with an internal pull-up resistor
# This means the pin will be HIGH when the button is not pressed,
# and LOW when the button is pressed (connecting to GND).
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup servo pin as output
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Initialize PWM on the servo pin with the specified frequency
servo_pwm = GPIO.PWM(SERVO_PIN, PWM_FREQUENCY)

# Start PWM with a 0% duty cycle initially (servo should be off or at default position)
# Or, start at 0 degrees by applying the initial duty cycle
servo_pwm.start(ANGLE_0_DUTY_CYCLE)
servo_pwm.ChangeDutyCycle(0)
print(f"Servo initialized to 0 degrees on BOARD pin {SERVO_PIN}.")

print(f"Waiting for button press on BOARD pin {BUTTON_PIN}...")
print("Press Ctrl+C to exit.")

# --- Debouncing Variables ---
last_button_state = GPIO.LOW  # Assume button is not pressed initially (due to pull-up)
last_debounce_time = 0.0

try:
    while True:
        current_button_state = GPIO.input(BUTTON_PIN)
        current_time = time.time()

        # Check if the button state has changed since the last check
        if current_button_state != last_button_state:
            last_debounce_time = current_time  # Reset the debounce timer

        # Check if enough time has passed for debouncing
        if (current_time - last_debounce_time) > DEBOUNCE_TIME:
            if current_button_state == GPIO.HIGH:
                print("Button Pressed! Moving servo...")

                # Turn servo to 90 degrees
                servo_pwm.ChangeDutyCycle(ANGLE_90_DUTY_CYCLE)
                print("Servo at 90 degrees.")
                time.sleep(2) # Wait for 2 seconds

                # Turn servo back to 0 degrees
                servo_pwm.ChangeDutyCycle(ANGLE_0_DUTY_CYCLE)
                print("Servo at 0 degrees.")
                # Optional: Add a small delay after returning to 0 to allow the servo to settle
                time.sleep(0.5)
                servo_pwm.ChangeDutyCycle(0)

        # Update the last button state for the next iteration
        last_button_state = current_button_state
        time.sleep(0.01) # Small delay to reduce CPU usage and prevent excessive looping

except KeyboardInterrupt:
    print("\nExiting program.")
finally:
    # Stop the PWM signal to the servo
    servo_pwm.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo_pwm.stop()
    # Clean up all GPIO settings, releasing the pins
    GPIO.cleanup()
    print("GPIO cleaned up.")
