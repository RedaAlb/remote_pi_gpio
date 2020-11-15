from gpio_client import GPIOClient

host_ip = "192.168.0.17"  # Local IP of your computer, will be printed when server is started.
port = 5000  # Needs to be the same port specified on the computer.

pc = GPIOClient(host_ip, port)

try:
    pc.listen_for_commands()
except KeyboardInterrupt:
    print("Done")