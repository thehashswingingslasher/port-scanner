# Port Scanner with Service Version Detection

## Overview

This Python script is designed to perform a network port scan on a specified target IP address or domain. It checks for open ports and attempts to retrieve the service version running on those ports. The script uses color-coded output to help quickly identify port status:
- **Green:** Port is open and a service version was successfully detected.
- **Red:** Port is closed.

## Requirements

1. **Python 3.x** - Make sure you have Python 3 installed on your system.
2. **`termcolor` library** - Used to color the output. You can install it using the following command:
   ```bash
   pip install termcolor
Here’s a full markdown file for your port scanner script with detailed explanations and usage instructions:

```markdown
# Port Scanner with Service Version Detection

## Overview

This Python script is designed to perform a network port scan on a specified target IP address or domain. It checks for open ports and attempts to retrieve the service version running on those ports. The script uses color-coded output to help quickly identify port status:
- **Green:** Port is open and a service version was successfully detected.
- **Red:** Port is closed.

## Requirements

1. **Python 3.x** - Make sure you have Python 3 installed on your system.
2. **`termcolor` library** - Used to color the output. You can install it using the following command:
   ```bash
   pip install termcolor
   ```

## How the Script Works

1. **Input**: You need to specify the target IP address or domain and the ports to scan.
   - You can input a single port number, a comma-separated list of port numbers, or a range of ports.
2. **Output**: The script will output the status of each port:
   - **Green** if the port is open and a service version is detected.
   - **Red** if the port is closed.
   - If the port is open, it will also display the service version (if detected).

## Script Usage

### Running the Script

Run the following command in your terminal:

```bash
python port_scanner.py
```

### Input Options

You will be prompted to enter:
- **Target IP or domain** (e.g., `192.168.1.1`)
- **Ports to scan**: This can be:
  - A single port number (e.g., `80`).
  - A comma-separated list of port numbers (e.g., `80,443,8080`).
  - A range of ports (e.g., `20-80`).

### Example 1: Single Port Scan
Prompt:
```bash
Target: 192.168.1.1
Port: 80
```
Output:
```
Port 80 is open    Apache/2.4.29 (Ubuntu)
```

### Example 2: Multiple Port Scan (Comma-separated list)
Prompt:
```bash
Target: 192.168.1.1
Port: 80,443,8080
```
Output:
```
Port 80 is open    Apache/2.4.29 (Ubuntu)
Port 443 is closed
Port 8080 is open    Jetty/9.4.31.v20200723
```

### Example 3: Port Range Scan
Prompt:
```bash
Target: 192.168.1.1
Port: 20-80
```
Output:
```
Port 20 is closed
Port 21 is open    vsftpd 3.0.3
Port 22 is open    OpenSSH 7.6 (Ubuntu)
Port 80 is open    Apache/2.4.29 (Ubuntu)
```

## Code Explanation

Here’s a breakdown of the script (`port_scanner.py`):

### Code:
```python
import socket
from termcolor import colored

def scan(ipaddress, port):
    try:
        # Create a socket object
        sock = socket.socket()
        sock.connect((ipaddress, port))
        service_version = sock.recv(1024)
        service_version = service_version.decode('utf-8').strip('\n')
        port_state = f'Port {str(port)} is open'
        print(colored(port_state, 'green'), end='    ')
        print(service_version)
        print(f'Port {str(port)} is open')
    except ConnectionRefusedError:
        print(colored(f'Port {str(port)} is closed', 'red'))
    except UnicodeDecodeError:
        print(colored(f'Port {str(port)} is open', 'green'))

# Prompt the user for input
target = input('Target: ')
ports = input('Port: ')

# Check if the ports input is a comma-separated list
if ',' in ports:
    port_list = ports.split(',')
    for port in port_list:
        scan(target, int(port))
# Check if the ports input is a range
elif '-' in ports:
    port_range = ports.split('-')
    start = int(port_range[0])
    end = int(port_range[1])
    for port in range(start, end + 1):
        scan(target, port)
# If neither, assume a single port number
else:
    scan(target, int(ports))
```

### Script Explanation:
1. **`socket` library** is used to create a socket and attempt a connection to the specified IP and port.
2. **`termcolor`** is used to format output messages with colors for readability.
3. **`ConnectionRefusedError`** is caught if the connection attempt is refused.
4. **`UnicodeDecodeError`** is caught if there's an issue decoding data received from the port (e.g., a simple "open" port with no detected service version).
