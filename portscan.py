import socket
from termcolor import colored
from scapy.all import IP, ICMP, sr1
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def port_scan(ipaddress, ports):
    print(colored(f"\nStarting scan on {ipaddress}...\n", "cyan"))
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan, ipaddress, port) for port in ports]
        for future in as_completed(futures):
            future.result()

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

if __name__ == "__main__":
    main()
