import socket
import threading
from queue import Queue
import time

class GPIOServer:

    def __init__(self, host_ip, port):
        self.host_ip = host_ip
        self.port = port
        self.host = (host_ip, port)

        self.server_on = False
        self.print_sent_commands = False

        self.host_print_prefix = "(Host):"
        # print(self.host_print_prefix, f"{self.host_ip}:{self.port}")

        self.bytes_to_recv = 512
        self.add_command_delay = True
        self.delay_between_commands = 0.001


    def start_server(self):
        self.commands = Queue(maxsize=1)

        self.server_t = threading.Thread(target=self.server_thread, name="server_thread", args=((self.commands,)))
        self.server_t.start()
        
    def create_socket(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(self.host)
        self.soc.listen()

        print(self.host_print_prefix, "Socket created.")

    def server_thread(self, commands):
        self.create_socket()

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
                self.conn.send(command.encode())

                if self.print_sent_commands:
                    print(self.host_print_prefix, f"Command \"{command}\" sent.")

                if command == "SHUTDOWN":
                    break

                if self.add_command_delay:
                    time.sleep(self.delay_between_commands)



    def close_server(self):
        self.commands.put("SHUTDOWN")
        self.server_t.join()
        self.server_on = False
        self.soc.close()
        print(self.host_print_prefix, "Server shutdown")

    def send_command(self, command_str):
        self.commands.put(command_str)
    
    def set_mode(self, board):
        command = f"#GPIO SET_MODE {board}"
        self.send_command(command)

    def setup_gpio(self, pins, pin_type, initial="OFF", pull_up_down=""):
        if type(pins) is not list: pins = [pins]

        pins_string = ",".join([str(i) for i in pins])

        if pull_up_down == "":
            command = f"#GPIO SETUP_PIN {pins_string} {pin_type} {initial}"
        else:
            command = f"#GPIO SETUP_PIN {pins_string} {pin_type} {initial} {pull_up_down}"
        self.send_command(command)

    def set_gpio(self, pins, state):
        if type(pins) is not list: pins = [pins]

        pins_string = ",".join([str(i) for i in pins])

        command = f"#GPIO SET_PIN {pins_string} {state}"
        self.send_command(command)
    
    def get_input(self, pin):

        command = f"#GPIO GET_INPUT {pin}"
        self.send_command(command)

        data_received = self.conn.recv(self.bytes_to_recv).decode()
        return data_received



