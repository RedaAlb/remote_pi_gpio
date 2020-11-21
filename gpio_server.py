import socket

import threading
from queue import Queue

import time
import struct

class GPIOServer:
    """ Create a TCP server to control/manipulate GPIO pins on the client (Pi). """

    def __init__(self, host_ip=socket.gethostbyname(socket.gethostname()), port=5000):
        """ Class constructor.

        Args:
            host_ip (str, optional): IP address of the host. Defaults to host local IP.
            port (int, optional): Port for the connection. Defaults to 5000.
        """

        self.host_ip = host_ip
        self.port = port
        self.host = (host_ip, port)

        self.server_on = False

        self.host_print_prefix = "(Host):"
        self.print_sent_commands = False
   
        self.bytes_to_send = 64
        self.bytes_to_recv = 64
        self.add_command_delay = True
        self.delay_between_commands = 0.001

        self.start_server()


    def start_server(self):
        """ Start server on a thread. """

        self.commands = Queue(maxsize=1)

        self.server_t = threading.Thread(target=self.server_thread, name="server_thread", args=((self.commands,)))
        self.server_t.start()


    def server_thread(self, commands):
        """ The server function thread.

        Args:
            commands (Queue): Used to communicate with thread by placing commands in the queue to be sent.
        """

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(self.host)
        self.soc.listen()
        print(self.host_print_prefix, "Socket created.")

        self.server_on = True

        print(self.host_print_prefix, f"Server started and listening on ({self.host_ip}:{self.port})...")

        try:
            self.conn = self.soc.accept()[0]
            client_ip = self.conn.getpeername()[0]
            print(self.host_print_prefix, f"Connection made with {client_ip}")
        except:  # When program finished/exited before connection was made.        
            self.server_on = False
            pass

        while self.server_on:
            if not commands.empty():
                command = commands.get()

                # Ensuring each sent command occupies exactly self.bytes_to_send bytes.
                command_length = len(command)
                remaining_bytes = self.bytes_to_send - command_length

                if remaining_bytes < 0:
                    print(self.host_print_prefix, f"\"{command}\" is over {self.bytes_to_send} bytes, was not sent.")
                    continue

                full_command = command + " " * remaining_bytes
                packed_command = struct.pack(f"{self.bytes_to_send}s", full_command.encode("utf-8"))
                self.conn.send(packed_command)
 

                if self.print_sent_commands:
                    print(self.host_print_prefix, f"Command \"{command}\" sent.")

                if command == "SHUTDOWN":
                    break

                if self.add_command_delay:
                    time.sleep(self.delay_between_commands)


    def close_server(self):
        """ Close the server and thread. """

        self.commands.put("SHUTDOWN")
        self.server_t.join()
        self.server_on = False
        self.soc.close()
        print(self.host_print_prefix, "Server shutdown")


    def send_command(self, command_str):
        """ Put command in the queue to communicate with the server thread to send it.

        Args:
            command_str (str): The command to send.
        """

        self.commands.put(command_str)

    
    def set_mode(self, board):
        """ Set board mode of GPIO pins.

        Args:
            board (str): Board mode, can be "board" or "bcm".
        """

        command = f"GPIO SET_MODE {board}"
        self.send_command(command)


    def setup_gpio(self, pins, pin_type, initial="OFF", pull_up_down=""):
        """ Setup GPIO pin(s) to output or input.

        Args:
            pins (int/list): The GPIO pin number(s) based on the board mode set.
            pin_type (str): Can be "IN" or "OUT".
            initial (str, optional): Initial value for pin(s). Defaults to "OFF".
            pull_up_down (str, optional): Whether to use pull up or down resistor, "UP" or "DOWN". Can be Defaults to "".
        """

        if type(pins) is not list: pins = [pins]

        pins_string = ",".join([str(i) for i in pins])

        if pull_up_down == "":
            command = f"GPIO SETUP_PIN {pins_string} {pin_type} {initial}"
        else:
            command = f"GPIO SETUP_PIN {pins_string} {pin_type} {initial} {pull_up_down}"

        self.send_command(command)


    def set_gpio(self, pins, state):
        """ Change state of GPIO pin(s) to ON or OFF.

        Args:
            pins (int/list): The GPIO pin number(s) based on the board mode set.
            state (str): The new state of the pin(s), "ON" or "OFF".
        """

        if type(pins) is not list: pins = [pins]

        pins_string = ",".join([str(i) for i in pins])

        command = f"GPIO SET_PIN {pins_string} {state}"
        self.send_command(command)
    

    def get_input(self, pin):
        """ Get input of a GPIO pin.

        Args:
            pin (int): The GPIO pin number based on the board mode set.

        Returns:
            str: The input value received from the pin.
        """

        command = f"GPIO GET_INPUT {pin}"
        self.send_command(command)

        data_received = self.conn.recv(self.bytes_to_recv).decode()
        return data_received


    def create_pwm(self, pin, freq, init_duty_cyc):
        """ Create PWM signal for the given pin.

        Args:
            pin (int): The GPIO pin number based on the board mode set.
            freq (int): The frequency of the PWM signal.
            init_duty_cyc (int): The initial duty cycle for the PWM signal (0-100).
        """

        command = f"PWM CREATE {pin} {freq} {init_duty_cyc}"
        self.send_command(command)


    def set_duty_cycle(self, pin, duty_cycle):
        """ Set the duty cycle of the PWM signal for the given pin.

        Args:
            pin (int): The GPIO pin number based on the board mode set.
            duty_cycle (int): The new duty cycle value (0-100).
        """

        command = f"PWM SET {pin} {duty_cycle}"
        self.send_command(command)
