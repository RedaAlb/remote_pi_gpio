import socket
from gpio_utils import GPIOUtils
import struct


class GPIOClient:
    """ TCP client to communicate with a host to control Pi GPIO pins remotely. """

    def __init__(self, host_ip, port=5000):
        """ Class constructor

        Args:
            host_ip (str): IP address of the host/server.
            port (int, optional): Port to use for the connection. Defaults to 5000.
        """

        self.host_ip = host_ip
        self.port = port
        self.host = (host_ip, port)

        self.client_print_prefix = "(Client):"

        self.gpio_utils = GPIOUtils()

        self.recv_bytes = 64  # How many bytes to receive.

    def connect_to_server(self):
        """ Create a socket and connect to the host using that socket. """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.host)
    
    def listen_for_commands(self):
        """ Listen for incoming commands from the host and process them to manipulate the GPIO pins. """

        try: 
            self.connect_to_server()

            print(self.client_print_prefix, "Waiting for commands...")
            while True:
                received_bytes = self.socket.recv(self.recv_bytes)
                received_bytes_len = len(received_bytes)
                command = struct.unpack(f"{received_bytes_len}s", received_bytes)[0].decode("utf-8").strip()
                
                # print(self.client_print_prefix, len(received_bytes), len(command), "Received command:", command)

                if command == "SHUTDOWN": break
                elif len(command) == 0: continue
                    
                self.process_command(command, self.socket)
            
            self.shutdown()

        except (KeyboardInterrupt, ConnectionResetError):
            self.shutdown()
    
    def shutdown(self):
        """ Cleanup GPIO and close socket. """

        self.gpio_utils.cleanup()
        self.socket.close()
        print(self.client_print_prefix, "Server shutdown")
    
    def process_command(self, command, socket):
        """ Process commands/strings received from the host to control the GPIO pins.

        Args:
            command (str): The command to process.
            socket (socket): The socket that has the client connection established. Used to send (input) back to host.
        """

        options = command.split(" ")
        main = options[0]
        function = options[1]

        if main == "GPIO":
            if function == "SET_MODE":
                value = options[2]
                self.gpio_utils.set_mode(value)

            elif function == "SETUP_PIN":
                pins = options[2].split(",")
                pin_type = options[3]
                initial = options[4]

                pull_up_down = ""
                try: pull_up_down = options[5]
                except IndexError: pass

                self.gpio_utils.setup_gpio(pins, pin_type, initial, pull_up_down)

            elif function == "SET_PIN":
                pins = options[2].split(",")
                state = options[3]
                self.gpio_utils.set_gpio(pins, state)

            elif function == "GET_INPUT":
                pin = options[2]
                input_data = self.gpio_utils.get_input(pin)
                socket.send(str(input_data).encode())

            else:
                print(self.client_print_prefix, "Unkown GPIO function received")
        
        elif main == "PWM":
            if function == "CREATE":
                pin = options[2]
                freq = options[3]
                init_duty_cyc = options[4]
                self.gpio_utils.create_pwm(pin, freq, init_duty_cyc)

            elif function == "SET":
                pin = options[2]
                duty_cycle = options[3]
                self.gpio_utils.set_duty_cycle(pin, duty_cycle)

            else:
                print(self.client_print_prefix, "Unkown PWM function received")
                
        else:
            print(self.client_print_prefix, "Unkown main command received.")