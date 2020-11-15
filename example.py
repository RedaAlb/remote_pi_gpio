import socket
import cv2
import numpy as np
from gpio_server import GPIOServer


# An example of how to use, turning on and off an LED and getting button input:
host_ip = socket.gethostbyname(socket.gethostname())
port = 5000


# Starting server
pi = GPIOServer(host_ip, port)
pi.start_server()

# Setting board mode
pi.set_mode("board")

# Setting up pins
LED_PIN = 12
BUTTON_PIN = 8

pi.setup_gpio(LED_PIN, "OUT")
pi.setup_gpio(BUTTON_PIN, "IN", pull_up_down="UP")

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
    elif key == ord("g"):
        button = pi.get_input(BUTTON_PIN)
        print("Button state:", button)

pi.close_server()
cv2.destroyAllWindows()