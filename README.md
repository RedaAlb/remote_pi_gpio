# Remote Pi GPIO

Control/manipulate Raspberry Pi GPIO pins remotely from the computer.

# Goal

Seamlessly use TCP/UDP connection(s) to control the GPIO pins on the Raspberry Pi from the computer (or any host). This is useful when you are using the Pi as a headless system, you could simply use SSH to run scripts and manipulate the GPIO pins that way, but this limits you on creating GUI applications that interact with the Pi, and I am not a fan of using a virtual viewer/machine...


# How to use

- Place both `on_pi/gpio_client.py` and `on_pi/pi_client.py` on the Pi.
- Run `example.py` on the computer.
    - `numpy` and `opencv` needed, install using `pip install numpy` and `pip install opencv-python`.
- Run `on_pi/pi_client.py` on the Pi.
- Use keys `d` and `a` to turn on and off the LED, and use key `g` to read button input.


# Current to-do

- [ ] Add more functionalities to control/manipulate GPIO pins.
- [ ] Add documentation.
- [x] Establish a fast and reliable connection between the computer and the Pi to send and receive commands from/to computer/pi.
    - [ ] Can still be better, maybe try UDP.
- [x] A way to encode/decode the sent/received messages to control the GPIO pins.
