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

# Function to validate a "single" configuration file
def validate_single_config(single_file):
    try:
        with open(single_file, "r") as file:
            lines = file.readlines()
            if len(lines) > 0:
                # The first line contains the port number
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

# Validate the "master" configuration file
if not validate_master_config(master_file):
    print("invalid master")
    sys.exit(1)

# Validate the directory for "single" files
if not os.path.exists(single_files_dir) or not os.path.isdir(single_files_dir):
    print("singles io error")
    sys.exit(1)

# Compare the "master" file with "single" files
def compare_files(master_file, single_files_dir):
    with open(master_file, "r") as master_file:
        master_lines = master_file.readlines()
        for single_filename in os.listdir(single_files_dir):
            single_file = os.path.join(single_files_dir, single_filename)
            if validate_single_config(single_file):
                with open(single_file, "r") as single_file:
                    single_lines = single_file.readlines()
                    if master_lines != single_lines:
                        print("neq")
                        return
            else:
                print("invalid single")
                sys.exit(1)
    print("eq")

# Perform the comparison
compare_files(master_file, single_files_dir)
