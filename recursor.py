import sys
import socket
import time

# Check the number of command-line arguments
if len(sys.argv) != 3:
    print("INVALID ARGUMENTS")
    sys.exit(1)

# Extract the command-line arguments
root_port = int(sys.argv[1])
timeout = float(sys.argv[2])

# Validate the root port range
if not (1024 <= root_port <= 49151):
    print("INVALID PORT NUMBER")
    sys.exit(1)

# Function to query a DNS server and handle timeouts
def query_dns(server, query, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server, port))
            s.send(query.encode())
            response = s.recv(1024).decode()
            return response
    except (ConnectionRefusedError, TimeoutError):
        return None

# Function to resolve a domain
def resolve_domain(domain):
    start_time = time.time()

    # Step 1: Query the root server
    root_response = query_dns("localhost", domain + "\n", root_port)
    if root_response is None:
        print("FAILED TO CONNECT TO ROOT")
        sys.exit(1)

    # Step 2: Extract TLD server port from the root response
    root_response_parts = root_response.strip().split()
    if len(root_response_parts) == 4 and root_response_parts[0] == "resolve":
        try:
            tld_port = int(root_response_parts[3])
        except ValueError:
            print("Invalid port in root response")
            sys.exit(1)
    else:
        print(f"{root_response}")
        sys.exit(1)

    # Step 3: Query the TLD server
    tld_response = query_dns("localhost", ".".join(domain.split('.')[1:]) + "\n", tld_port)
    if tld_response is None:
        print("NXDOMAIN")
        sys.exit(1)

    # Step 4: Extract authoritative server port from the TLD response
    try:
        auth_port = int(tld_response.strip())
    except ValueError:
        print("INVALID TLD RESPONSE")
        sys.exit(1)

    # Step 5: Query the authoritative server
    auth_response = query_dns("localhost", domain + "\n", auth_port)
    if auth_response is None:
        print("NXDOMAIN")
        sys.exit(1)

    # Step 6: Print the resolved port
    print(auth_response.strip())

    elapsed_time = time.time() - start_time

    if elapsed_time > timeout:
        print("TIMEOUT")
        sys.exit(1)

# Main program
while True:
    try:
        user_input = input("Enter a domain (Ctrl-D to exit): ")
        if not user_input:
            break
        resolve_domain(user_input)
    except KeyboardInterrupt:
        break
