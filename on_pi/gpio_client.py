import socket
from gpio_utils import GPIOUtils


class GPIOClient:

    def __init__(self, host_ip, port):
        self.host_ip = host_ip
        self.port = port
        self.host = (host_ip, port)

        self.client_print_prefix = "(Client):"

        self.gpio_utils = GPIOUtils()

        self.recv_bytes = 512  # How many bytes to receive.

    def connect_to_server(self):     
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(self.host)
    
    def listen_for_commands(self):
        self.connect_to_server()

        print(self.client_print_prefix, "Waiting for commands...")
        while True:
            commands = self.soc.recv(self.recv_bytes).decode().split("#")  # Splitting needed if sent data accumulates.
            # if commands[0] == "": continue
            if commands[0] == "SHUTDOWN": break


            for command in commands:
                if command == "": continue
                # print(self.client_print_prefix, f"Received \"{command}\"")
                self.process_command(command, self.soc)
        
        self.gpio_utils.cleanup()
        self.soc.close()
        print(self.client_print_prefix, "Server shutdown")
    
    def process_command(self, command, soc):
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
                try:
                    pull_up_down = options[5]
                except IndexError:
                    pass

                self.gpio_utils.setup_gpio(pins, pin_type, initial, pull_up_down)

            elif function == "SET_PIN":
                pins = options[2].split(",")
                state = options[3]
                self.gpio_utils.set_gpio(pins, state)
            elif function == "GET_INPUT":
                pin = options[2]
                input_data = self.gpio_utils.get_input(pin)
                soc.send(str(input_data).encode())

            else:
                print(self.client_print_prefix, "Unkown function received")
        
        else:
            print(self.client_print_prefix, "Unkown main command received.")