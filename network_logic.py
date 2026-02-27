import socket 
from scapy.all import ARP, Ether, srp
from concurrent.futures import ThreadPoolExecutor

def scan_single_port(ip, port, svc):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)
    result = s.connect_ex((ip, port))
    s.close()
    return f"{port}({svc})" if result == 0 else None

def scan_ports(ip):
        common_ports = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3389: "RDP"}
        found = []
        with ThreadPoolExecutor(max_workers=len(common_ports)) as executor:
            futures=[executor.submit(scan_single_port, ip, p, s) for p, s in common_ports.items()]
            for future in futures:
                res = future.result()
                if res:
                    found.append(res)
        return ", ".join(found) if found else "None"

def get_device_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname.replace(".lan","").replace(".local","").capitalize()
    except:
        return ""
    
def do_arp_scan(target_range):
    arp_request = ARP(pdst=target_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    answered_list = srp(packet, timeout=2, verbose=False)[0]
    return answered_list
