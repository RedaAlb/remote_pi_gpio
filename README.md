# Remote Pi GPIO

Control/manipulate Raspberry Pi GPIO pins remotely from the computer.

# Goal

Seamlessly use TCP/UDP connection(s) to control the GPIO pins on the Raspberry Pi from the computer (or any host). This is useful when you are using the Pi as a headless system, you could simply use SSH to run scripts and manipulate the GPIO pins that way, but this limits you on creating GUI applications that interact with the Pi, and I am not a fan of using a virtual viewer/machine...

The end result should allow for a user to write such statements on the computer:

```python
# Setting up pins
pi.setup_gpio_pin(12, "OUT")  # Which would be the same as doing GPIO.setup(12, GPIO.OUT) on the Pi.

# Controlling the pins
pi.set_gpio_pin(12, 1)  # GPIO.output(12, GPIO.HIGH) on the Pi.
pi.set_gpio_pin(12, 0)  # GPIO.output(12, GPIO.LOW) on the Pi.
```

Including all the rest of key GPIO manipulations needed, board configuration, getting GPIO inputs, PWM, and much more.


# Current to-do

- [ ] Establish a fast and reliable connection between the computer and the Pi to send and receive commands from/to computer/pi.
- [ ] A way to encode/decode the sent/received messages to control the GPIO pins.