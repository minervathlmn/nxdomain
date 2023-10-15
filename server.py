import sys
import socket

# Check the number of command-line arguments
if len(sys.argv) != 2:
    print("INVALID ARGUMENTS")
    sys.exit(1)

# Extract the configuration file path from the command-line argument
config_file = sys.argv[1]

# Initialize a dictionary to store hostname to port mappings
hostname_to_port = {}

# Load the configuration from the file
try:
    with open(config_file, "r") as file:
        lines = file.readlines()
        # The first line contains the port number the server occupies
        server_port = int(lines[0].strip())
        # Read the rest of the lines to populate the hostname_to_port dictionary
        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) == 2:
                hostname, port = parts
                hostname_to_port[hostname] = int(port)
except (FileNotFoundError, PermissionError, ValueError):
    print("INVALID CONFIGURATION")
    sys.exit(1)

# Create a buffer to store incomplete messages
buffer = ""

# Function to handle the ADD command
def handle_add_command(command, connection):
    # Extract HOSTNAME and PORT from the command
    parts = command.split()
    if len(parts) == 3:
        _, hostname, port = parts
        if hostname.isalnum() and port.isdigit():
            port = int(port)
            hostname_to_port[hostname] = port
            connection.send(f"OK\n".encode())
        else:
            connection.send("INVALID\n".encode())
    else:
        connection.send("INVALID\n".encode())

# Function to handle the DEL command
def handle_del_command(command, connection):
    # Extract HOSTNAME from the command
    parts = command.split()
    if len(parts) == 2:
        _, hostname = parts
        if hostname in hostname_to_port:
            del hostname_to_port[hostname]
            connection.send(f"OK\n".encode())
        else:
            connection.send("INVALID\n".encode())
    else:
        connection.send("INVALID\n".encode())

# Function to handle the EXIT command
def handle_exit_command(connection):
    connection.send(f"Goodbye\n".encode())
    connection.close()
    sys.exit(0)

# Function to resolve a hostname to a port and log the result
def resolve_hostname(hostname, connection):
    if hostname in hostname_to_port:
        port = hostname_to_port[hostname]
        connection.send(f"resolve {hostname} to {port}\n".encode())
        print(f"resolve {hostname} to {port}")
    else:
        connection.send("resolve NXDOMAIN\n".encode())
        print(f"resolve {hostname} to NXDOMAIN")

# Main server loop
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(("localhost", server_port))
    server_socket.listen()

    print(f"Server is listening on port {server_port}")

    while True:
        try:
            connection, address = server_socket.accept()
            data = connection.recv(1024).decode()
            if not data:
                break

            # Handle incomplete messages and accumulate them in the buffer
            buffer += data
            if '\n' not in buffer:
                continue

            # Split the complete messages in the buffer
            messages = buffer.split('\n')
            # The last element in messages may be an incomplete message
            buffer = messages[-1]
            messages = messages[:-1]

            # Process complete messages
            for message in messages:
                if message.startswith('!ADD'):
                    handle_add_command(message, connection)
                elif message.startswith('!DEL'):
                    handle_del_command(message, connection)
                elif message == '!EXIT':
                    handle_exit_command(connection)
                else:
                    resolve_hostname(message, connection)
        except KeyboardInterrupt:
            sys.exit(0)
