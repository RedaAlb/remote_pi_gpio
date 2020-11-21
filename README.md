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


### Example 2 - RGB LED

1. Clone this repo in both the host and the Pi.
2. Connect the R, G, B pins of the RGB LED to pins 11, 12, 13 respectively, and connect the last pin to any 3v3 pin.
3. Run `ex2_RGB_LED.py` on the computer.
    - `numpy` and `opencv` needed, install using `pip install numpy` and `pip install opencv-python`. Note: This will print your local host ip, take note of it.
4. Run `on_pi/pi_client.py` on the Pi after changing the host_ip to the one printed from previous step.
5. A trackbars window will appear on the host, use it to control each channel of the RGB LED to change the colour.


Please refer to `gpio_server.py` to see all other functions you can use to control the GPIO pins remotely from the host.