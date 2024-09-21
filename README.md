# Python Reverse Shell with Windows Registry Persistence

## Overview

This project is a **Python-based reverse shell** with **Windows registry persistence**, designed for **malware analysis**, **cybersecurity research**, and **educational purposes**. It demonstrates common techniques used by attackers to gain control of compromised machines, execute arbitrary commands, and maintain persistence across system reboots.

**⚠️ Disclaimer:** This script is for educational and research purposes **only**. Unauthorized use of this code in live environments without permission is illegal. The author is not responsible for any misuse or malicious intent involving this script.

---

## Features

### 🔑 **Reverse Shell**
- Establishes a connection from the victim machine to an attacker's server (using a socket connection).
- Receives and executes shell commands remotely.
- Handles both directory changes (`cd` commands) and standard shell command execution, sending output back to the attacker.

### 🗝️ **Windows Registry Persistence**
- The script adds itself to the Windows Registry under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`.
- This ensures that the script runs every time the system starts, simulating a common persistence technique found in real-world malware.

### ⏳ **Command Execution Loop**
- The reverse shell continuously attempts to connect to the attacker machine until successful.
- Upon connection, it waits to receive commands, execute them, and send the results back.

---

## How It Works

1. **Socket Creation**: The script creates a socket connection to a specified IP and port (configured as `any IP` and `any port` by default). You can modify these settings based on your testing environment.
   
2. **Command Reception & Execution**: After a connection is established, the attacker can send commands. The script executes these commands on the victim machine and returns the output or error back to the attacker.

3. **Persistence Setup**: The script automatically registers itself in the Windows startup registry, ensuring it runs after a system reboot. This is achieved using the `ctypes` library to interact with Windows APIs for registry manipulation.

---

## Setup and Usage

### Prerequisites

- **Python 3.x**
- **Windows OS** (for testing registry persistence)

### Attacker Machine Setup

1. Use a tool like **Netcat** to set up a listener on your attacker machine:
   ```bash
   nc -lvp (port num)
