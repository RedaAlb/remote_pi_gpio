from gpio_client import GPIOClient

host_ip = "192.168.0.17"  # Local IP of your host, will be printed when server is started.

client = GPIOClient(host_ip)
client.listen_for_commands()

