# Network Health & Security Monitor 

A modular network monitoring tool built with Python. It uses ARP scanning to discover devices and features an **Intelligent SQLite Cache** system to identify network card vendors without overusing external APIs.

##  Features
- **ARP Scanning:** Fast device discovery using `Scapy`.
- **Intelligent Cache:** Stores MAC vendors locally in SQLite to speed up subsequent scans.
- **Intruder Detection:** Visually flags unknown or suspicious devices.
- **Alias System:** Assign custom names to your recognized devices.
- **Port Auditing:** Scans common ports (SSH, HTTP, etc.) for each discovered device.

## Requirements
- **Python 3.x**
- **Scapy:** `pip install scapy`
- **Requests:** `pip install requests`
- **Npcap (Windows only):** Required for Scapy to capture packets. [Download here](https://npcap.com/#download).

## How to Use
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the application: `python main.py`.
4. Enter your network range (e.g., `192.168.1.0/24`) and click **Scan Network**.

## Project Structure
- `main.py`: The Tkinter GUI and orchestration logic.
- `database.py`: SQLite persistence and caching logic.
- `network_logic.py`: ARP scanning and port auditing.
- `vendor_lookup.py`: API integration for MAC vendor identification.
