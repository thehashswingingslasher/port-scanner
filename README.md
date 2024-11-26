# Port Scanning and OS Detection Script

This Python script performs port scanning and OS detection for a given IP address or hostname. It utilizes `socket`, `scapy`, and `concurrent.futures` for multi-threaded scanning. The results are printed in colored output using the `termcolor` library.

## Prerequisites
Before running the script, make sure you have the required libraries installed:

```bash
pip install termcolor scapy
```

## Script Breakdown

### Import Statements
The script uses the following modules:
- `socket`: For creating TCP connections to ports.
- `termcolor`: For printing colored output to the terminal.
- `scapy.all`: For sending and receiving ICMP packets to detect the operating system.
- `concurrent.futures`: For running port scans concurrently using threads.

### Functions

#### `scan(ipaddress, port)`
This function attempts to connect to a specified IP address and port, checks if the port is open, and attempts to retrieve the service version (if available).

```python
def scan(ipaddress, port):
    print(f"Attempting to connect to {ipaddress}:{port}...")  # Debugging line
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Increase timeout for slower connections
        sock.connect((ipaddress, port))
        print(f"Connected to {ipaddress}:{port}")  # Debugging line
        
        try:
            service_version = sock.recv(1024).decode('utf-8').strip('\n')
        except UnicodeDecodeError:
            service_version = "Unknown Service"
        
        print(colored(f'Port {port} is open', 'green'), end=' ')
        print(colored(f'({service_version})', 'yellow'))
        sock.close()
    except (ConnectionRefusedError, socket.timeout):
        print(f"Failed to connect to {ipaddress}:{port}")  # Debugging line
        pass  # Suppress output for closed ports
```

#### `detect_os(ipaddress)`
This function detects the operating system of the target by sending an ICMP packet and analyzing the TTL (Time to Live) value of the response.

```python
def detect_os(ipaddress):
    print(f"Detecting OS for {ipaddress}...")  # Debugging line
    try:
        response = sr1(IP(dst=ipaddress) / ICMP(), timeout=1, verbose=0)
        if response:
            ttl = response[IP].ttl
            if ttl <= 64:
                os_guess = "Linux/Unix"
            elif ttl == 108:
                os_guess = "Windows 2000"
            elif ttl == 127:
                os_guess = "Windows 9x/NT"
            elif ttl == 128:
                os_guess = "Windows"
            elif ttl == 252:
                os_guess = "Solaris"
            else:
                os_guess = "Unknown OS"

            print(colored(f"[+] OS Detection: TTL={ttl}, Likely OS: {os_guess}", "cyan"))
        else:
            print(colored("[!] OS Detection failed. No response to ICMP request.", "red"))
    except Exception as e:
        print(colored(f"[!] OS Detection error: {str(e)}", "red"))
```

#### `port_scan(ipaddress, ports)`
This function runs the `scan` function for each port in the given range using multiple threads to speed up the scanning process.

```python
def port_scan(ipaddress, ports):
    print(colored(f"\nStarting scan on {ipaddress}...\n", "cyan"))
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan, ipaddress, port) for port in ports]
        for future in as_completed(futures):
            future.result()
```

#### `main()`
The main function orchestrates the port scanning and OS detection. It prompts the user for the target IP/hostname and the ports to scan. The user can specify ports as a range (e.g., `1-1000`), a comma-separated list (e.g., `80,443`), or `all` to scan all ports.

```python
def main():
    target = input('Target IP/Hostname: ').strip()
    ports = input('Ports to scan (e.g., "80,443" or "1-1000" or "all"): ').strip()

    if not target:
        print(colored("Target IP/Hostname cannot be empty. Exiting.", "red"))
        return

    try:
        ipaddress = socket.gethostbyname(target)
    except socket.gaierror:
        print(colored("Invalid hostname or IP address. Exiting.", "red"))
        return

    print(colored(f"\nResolving target: {target} -> {ipaddress}\n", "blue"))

    detect_os(ipaddress)  # Perform OS detection

    if ports.lower() == "all":
        port_range = range(1, 65536)
    elif '-' in ports:
        start, end = map(int, ports.split('-'))
        port_range = range(start, end + 1)
    elif ',' in ports:
        port_range = [int(port) for port in ports.split(',')]
    else:
        port_range = [int(ports)]

    port_scan(ipaddress, port_range)
```

### Running the Script
To run the script, execute it in your terminal:

```bash
python3 port_scan.py
```

You will be prompted for the target IP/hostname and ports to scan.

### Example Output

```
Target IP/Hostname: 192.168.1.1
Ports to scan (e.g., "80,443" or "1-1000" or "all"): 80,443

Resolving target: 192.168.1.1 -> 192.168.1.1

Detecting OS for 192.168.1.1...
[+] OS Detection: TTL=64, Likely OS: Linux/Unix

Starting scan on 192.168.1.1...

Port 80 is open (Apache httpd 2.4.29)
Port 443 is open (OpenSSL)
```

### Notes
- The script uses multi-threading (`ThreadPoolExecutor`) to scan ports concurrently, which makes the scan faster.
- The OS detection is based on TTL values from ICMP responses, which might not always be accurate.
- You can modify the script to scan UDP ports or use more advanced scanning techniques if necessary.

### Troubleshooting
- If the script doesn't detect open ports, ensure there are no firewalls blocking the connections.
- If you encounter permission issues with scanning low-numbered ports, run the script as root or with elevated privileges (e.g., `sudo` on Linux).
