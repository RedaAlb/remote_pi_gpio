# Remote Pi GPIO

Seamlessly control/manipulate the GPIO pins on a Raspberry Pi from a computer (or any host) remotely.

## How to use


### Example 1 - LED on/off

1. Clone this repo in both the host and the Pi.
2. As an example, connect an LED with a resistor to GPIO pin 12 ("board" numbering).
3. Run `ex1_LED.py` on the computer.
    - `numpy` and `opencv` needed, install using `pip install numpy` and `pip install opencv-python`. Note: This will print your local host IP, take note of it.
4. Run `on_pi/pi_client.py` on the Pi after changing the host_ip to the one printed from previous step.
5. Use the `d` and `a` keys to turn on and off the LED.

<<<<<<< HEAD
=======
- Place both `on_pi/gpio_client.py` and `on_pi/pi_client.py` on the Pi.
- Run `example.py` on the computer.
    - `numpy` and `opencv` needed, install using `pip install numpy` and `pip install opencv-python`.
- Run `on_pi/pi_client.py` on the Pi.
- Use keys `d` and `a` to turn on and off the LED, and use key `g` to read button input.
>>>>>>> 4b2d4ec163ad13186e3ec4b5792fe85705872d82

### Example 2 - RGB LED

1. Clone this repo in both the host and the Pi.
2. Connect the R, G, B pins of the RGB LED to pins 11, 12, 13 respectively, and connect the last pin to any 3v3 pin.
3. Run `ex2_RGB_LED.py` on the computer.
    - `numpy` and `opencv` needed, install using `pip install numpy` and `pip install opencv-python`. Note: This will print your local host ip, take note of it.
4. Run `on_pi/pi_client.py` on the Pi after changing the host_ip to the one printed from previous step.
5. A trackbars window will appear on the host, use it to control each channel of the RGB LED to change the colour.

<<<<<<< HEAD

Please refer to `gpio_server.py` to see all other functions you can use to control the GPIO pins remotely from the host.
=======
- [ ] Add more functionalities to control/manipulate GPIO pins.
- [ ] Add documentation.
- [x] Establish a fast and reliable connection between the computer and the Pi to send and receive commands from/to computer/pi.
    - [ ] Can still be better, maybe try UDP.
- [x] A way to encode/decode the sent/received messages to control the GPIO pins.
>>>>>>> 4b2d4ec163ad13186e3ec4b5792fe85705872d82
