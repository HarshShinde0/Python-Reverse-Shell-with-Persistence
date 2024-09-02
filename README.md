# Reverse Shell Script with Persistence

## Disclaimer

This code should only be used in a legal and ethical manner. Always obtain explicit permission before testing any system. Misuse of this code can lead to serious legal consequences.

## How It Works

### Reverse Shell

- **Connection:** The script connects to the attacker's machine and awaits commands.
- **Execution:** It executes commands on the victim’s machine and sends the output back to the attacker.

### Persistence Mechanism

- **File Copy:** The script copies itself to the Windows startup folder (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`) under a new name (`updater.exe`).
- **Registry Entry:** It adds a registry entry under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` to ensure the script runs every time the user logs in.

### Reconnection Attempts

- If the initial connection to the server fails, the script waits for 10 seconds and tries again to re-establish the reverse shell.

## Ethical Considerations

- **Testing:** Use this script only in a controlled environment where you have explicit permission from the system owner.
- **Mitigation:** To prevent such attacks, monitor and restrict access to startup folders and registry keys. Use antivirus software, enable strict firewall rules, and educate users about the risks of running untrusted software.

## Mitigation Steps

1. **Remove the Registry Key:**
   - Go to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` and delete the entry created by the script (WindowsUpdater).

2. **Delete the Startup File:**
   - Navigate to the startup folder (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`) and delete the `updater.exe` file.

3. **Use Antivirus Software:**
   - Ensure that antivirus software is up to date and can detect and remove such scripts.

## Steps to Use the Script

### 1. Prepare the Attacker's Machine

- **Set Up a Listener:** On your machine (the attacker's machine), set up a listener to wait for the connection from the target machine.

  ```bash
  nc -lvp 4444
  ```

  - `-lvp` options stand for listening, verbose output, and port, respectively.
  - `4444` is the port number. Ensure it matches the port number specified in the script.

### 2. Modify the Script

- **Edit the Script:** Open the Python script in a text editor. Replace `SERVER_IP` with the IP address of your machine (the attacker's machine) and `SERVER_PORT` with the port number specified in the Netcat command.

  ```python
  SERVER_IP = "192.168.1.10"  # Replace with your attacker's IP address
  SERVER_PORT = 4444           # Replace with your chosen port number
  ```

- **Save the Script:** Save the script as `reverse_shell.py` or any preferred name.

### 3. Transfer the Script to the Target Machine

- **Copy the Script:** Transfer `reverse_shell.py` to the target Windows machine using USB drives, email (within ethical guidelines), or other file-sharing methods.

### 4. Execute the Script on the Target Machine

- **Run the Script:** On the target machine, open a command prompt or terminal. Navigate to the script's directory and run it using Python:

  ```bash
  python reverse_shell.py
  ```

- **Persistence:** The script will copy itself to the startup folder and create a registry key to ensure it runs every time the user logs in. It will then attempt to connect back to your attacker's machine.

### 5. Interact with the Target Machine

- **Connection Established:** If successful, the reverse shell will connect back to your attacker's machine where Netcat is listening. You should see a connection established message in your terminal.

- **Execute Commands:** You can now execute commands on the target machine from your Netcat terminal. For example, run `dir` to list files or `ipconfig` to check network configurations.

- **Exit:** To end the reverse shell session, type `exit` in the Netcat terminal. This will terminate the connection and stop the shell.

## Important Notes

- **Security & Legal Considerations:** Ensure you have explicit permission to perform this test. Unauthorized use of this script is illegal.
- **Use:** This script is for educational purposes, ethical hacking, and penetration testing within legal boundaries. Never deploy such tools on systems you do not own or have explicit authorization to test.
- **Detection & Mitigation:** After testing, remove the persistence mechanism by deleting the startup file (`updater.exe`) and removing the registry key (`WindowsUpdater`) to avoid leaving the system compromised. Educate users and administrators about the risks and signs of such attacks.
