import cv2
import numpy as np
from gpio_server import GPIOServer


# An example of how to use, turning on and off an LED:
# Creating and starting server
pi = GPIOServer()

# Setting board mode
pi.set_mode("board")

# Setting up pin
LED_PIN = 12
pi.setup_gpio(LED_PIN, "OUT")


# Interacting with the pins.

img = np.zeros((200, 200, 1))

while True:
    cv2.imshow("img", img)

    key = cv2.waitKey(1)

    if key == ord("q"): break
    
    elif key == ord("d"):
        pi.set_gpio(LED_PIN, "ON")
    elif key == ord("a"):
        pi.set_gpio(LED_PIN, "OFF")
        
pi.close_server()
cv2.destroyAllWindows()