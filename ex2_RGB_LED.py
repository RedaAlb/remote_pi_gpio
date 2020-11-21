import cv2
import numpy as np

from gpio_server import GPIOServer


# An example of how to use, controlling an RGB LED.

# Creating and starting server
pi = GPIOServer()

# Setting board mode
pi.set_mode("board")

# Setting up pins
R_PIN = 11  # Red pin
G_PIN = 12  # Green pin
B_PIN = 13  # Blue pin

PINS = [R_PIN, G_PIN, B_PIN]

FREQ = 100           # PWM frequency
INIT_DUTY_CYC = 100  # Initial PWM duty cycle

# Used to convert between 0-255 and 100-0 scales.
RGB_RANGE = [0, 255]
DCYCLE_RANGE = [100, 0]

pi.setup_gpio(PINS, "OUT")

pi.create_pwm(R_PIN, FREQ, INIT_DUTY_CYC)
pi.create_pwm(G_PIN, FREQ, INIT_DUTY_CYC)
pi.create_pwm(B_PIN, FREQ, INIT_DUTY_CYC)


# Interacting with the pins.

window_name = "Trackbars"
cv2.namedWindow(window_name)


def nothing(x): pass

# Trackbars to change the colour.
cv2.createTrackbar("R", window_name, 0, 255, nothing)
cv2.createTrackbar("G", window_name, 0, 255, nothing)
cv2.createTrackbar("B", window_name, 0, 255, nothing)

img = np.zeros((400, 400, 3), np.uint8)

while True:

    # Getting trackbar values.
    r = cv2.getTrackbarPos("R", window_name)
    g = cv2.getTrackbarPos("G", window_name)
    b = cv2.getTrackbarPos("B", window_name)

    # Updating the PWM duty cycle for each pin.
    pi.set_duty_cycle(R_PIN, int(np.interp(r, RGB_RANGE, DCYCLE_RANGE)))
    pi.set_duty_cycle(G_PIN, int(np.interp(g, RGB_RANGE, DCYCLE_RANGE)))
    pi.set_duty_cycle(B_PIN, int(np.interp(b, RGB_RANGE, DCYCLE_RANGE)))

    # Updating image with current selected colour.
    img[:] = [b, g, r]
    cv2.imshow(window_name, img)

    key = cv2.waitKey(1)
    if key == ord("q"): break
    
    
pi.close_server()
cv2.destroyAllWindows()