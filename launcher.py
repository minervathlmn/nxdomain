import sys
import os

# Check the number of command-line arguments
if len(sys.argv) != 3:
    print("INVALID ARGUMENTS")
    sys.exit(1)

# Extract the paths of the "master" configuration file and the directory for "single" files
master_file = sys.argv[1]
single_files_dir = sys.argv[2]

# Function to validate the "master" configuration file
def validate_master_config(master_file):
    try:
        with open(master_file, "r") as file:
            lines = file.readlines()
            if len(lines) > 0:
                # The first line contains the port number of the root server
                root_port = lines[0].strip()
                if not root_port.isdigit():
                    return False
                for line in lines[1:]:
                    parts = line.strip().split(',')
                    if len(parts) != 2:
                        return False
            else:
                return False
    except (FileNotFoundError, PermissionError):
        return False
    return True

# Function to create a "single" configuration file
def create_single_config_file(single_file, domain, port):
    with open(single_file, "w") as file:
        file.write(f"{port}\n{domain},{port}\n")

# Validate the "master" configuration file
if not validate_master_config(master_file):
    print("INVALID MASTER")
    sys.exit(1)

# Create the directory for "single" configuration files if it does not exist
try:
    os.makedirs(single_files_dir, exist_ok=True)
except (PermissionError, OSError):
    print("NON-WRITABLE SINGLE DIR")
    sys.exit(1)

# Read the "master" configuration file and generate "single" configuration files
with open(master_file, "r") as file:
    lines = file.readlines()
    root_port = lines[0].strip()
    for line in lines[1:]:
        parts = line.strip().split(',')
        if len(parts) == 2:
            domain, port = parts
            single_file = os.path.join(single_files_dir, f"{domain}.conf")
            create_single_config_file(single_file, domain, port)

print(f"Single configuration files generated in {single_files_dir}")
