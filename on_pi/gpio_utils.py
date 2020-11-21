import RPi.GPIO as g

class GPIOUtils:
    """ Provides utility functions to control/manipulate Pi GPIO pins. """

    def __init__(self):

        self.print_prefix = "(GPIO):"

        self.pwm = {}  # Keeps track of PWM objects (value) for each GPIO pin (key).


    def set_mode(self,  board="board"):
        """ Set board mode of the Pi GPIO pins.

        Args:
            board (str, optional): GPIO board mode, can be "board" or "bcm". Defaults to "board".
        """

        if board.lower() == "board":
            g.setmode(g.BOARD)
            print(self.print_prefix, "Board type set to \"board\"")
        elif board.lower() == "bcm":
            g.setmode(g.BCM)
            print(self.print_prefix, "Board type set to \"BCM\"")
        else:
            print(self.print_prefix, "Board type not set, wrong board name given, can only be \"board\" or \"BCM\".")

    
    def setup_gpio(self, pins, pin_mode, initial="OFF", pull_up_down=""):
        """ Setup a GPIO pin as input or output with initial value and pull up or down resistor.

        Args:
            pins (int/list): The GPIO pin number(s) based on the board mode set.
            pin_mode (str): The mode to be set for the pin(s), can be "IN" or "OUT".
            initial (str, optional): Initial state of the pin(s), "ON" or "OFF". Defaults to "OFF".
            pull_up_down (str, optional): Whether to use a pull up or down resistor, can be "UP" or "DOWN". Defaults to "".
        """
        
        # TODO: This function needs to be cleaned up and done more elegantly.

        if type(pins) is not list: pins = [pins]

        if initial == "OFF": initial = 0
        elif initial == "ON": initial = 1
        else:
            initial = 0
            print(self.print_prefix, f"Wrong initial value given for pin(s) {pins}, OFF initial value is used instead.")

        for pin in pins:
            pin = int(pin)

            if pin_mode == "OUT":
                error = ""
                if pull_up_down == "":
                    g.setup(pin, g.OUT, initial=initial)
                elif pull_up_down == "UP":
                    g.setup(pin, g.OUT, initial=initial, pull_up_down=g.PUD_UP)
                elif pull_up_down == "DOWN":
                    g.setup(pin, g.OUT, initial=initial, pull_up_down=g.PUD_DOWN)
                else:
                    print(self.print_prefix, f"Wrong pull up down keyword received for pin {pin}.")
                    error = " WAS NOT"
                print(self.print_prefix, f"Pin {pin}{error} set to OUT")

            elif pin_mode == "IN":
                error = ""
                if pull_up_down == "":
                    g.setup(pin, g.IN)
                elif pull_up_down == "UP":
                    g.setup(pin, g.IN, pull_up_down=g.PUD_UP)
                elif pull_up_down == "DOWN":
                    g.setup(pin, g.IN, pull_up_down=g.PUD_DOWN)
                else:
                    print(self.print_prefix, f"Wrong pull up down keyword received for pin {pin}.")
                    error = " WAS NOT"

                print(self.print_prefix, f"Pin {pin}{error} set to IN")
            else:
                print(self.print_prefix, "Wrong pin mode, can only be OUT or IN.")


    def set_gpio(self, pins, state):
        """ Turn on or off GPIO pin(s).

        Args:
            pins (int/list): The GPIO pin number(s) based on the board mode set.
            state (str): The new state for the pin(s), "ON" or "OFF".
        """

        if type(pins) is not list: pins = [pins]

        for pin in pins:
            pin = int(pin)
            if state == "ON":
                g.output(pin, 1)
                print(self.print_prefix, f"Pin {pin} turned on")
            elif state == "OFF":
                g.output(pin, 0)
                print(self.print_prefix, f"Pin {pin} turned off")
            else:
                print(self.print_prefix, "Wrong GPIO state given, can only be ON or OFF.")

    
    def get_input(self, pin):
        """ Return the input value of the given GPIO pin.

        Args:
            pin (int): The GPIO pin number based on the board mode set.

        Returns:
            int: The input value for the given GPIO pin.
        """
        
        return g.input(int(pin))


    def create_pwm(self, pin, freq, init_duty_cyc):
        """ Create a Pulse-width modulation (PWM) signal and store it in self.pwm.

        Args:
            pin (int): The GPIO pin number based on the board mode set.
            freq (int): Frequency of the PWM signal.
            init_duty_cyc (int): The initial duty cycle for the PWM signal.

        Returns:
            int: The pin number the PWM was created for.
        """

        pin = int(pin)
        pwm = g.PWM(pin, int(freq))
        pwm.start(int(init_duty_cyc))
        self.pwm[pin] = pwm  # To keep track of for remote gpio.
        print(self.print_prefix, f"PWM created and started for pin {pin}, with freq={freq}, duty cycle={init_duty_cyc}")
        return pin
    
    
    def set_duty_cycle(self, pin, new_duty_cyc):
        """ Set a new duty cycle for the given pin PWM signal.

        Args:
            pin (int): The GPIO pin number based on the board mode set.
            new_duty_cyc (int): The new duty cycle for the PWM signal.
        """

        pwm = self.pwm[int(pin)]
        pwm.ChangeDutyCycle(int(new_duty_cyc))

        # print(self.print_prefix, f"PWM for pin {pin} set to {new_duty_cyc}")


    def cleanup(self):
        """ Stop all PWM signals created and cleanup GPIO. """

        for _, pwm in self.pwm.items():
            pwm.stop()
        
        g.cleanup()
        print(self.print_prefix, "GPIO cleaned up")