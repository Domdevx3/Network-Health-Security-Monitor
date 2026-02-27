import sqlite3
from datetime import datetime

def init_db():
        conn = sqlite3.connect("network_monitor.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS network_devices (
                mac_address TEXT PRIMARY KEY,
                ip_address TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                alias TEXT,
                vendor TEXT
            )
        """)
        conn.commit()
        conn.close()
        

def get_all_devices():
    conn = sqlite3.connect("network_monitor.db")
    cur = conn.cursor()
    cur.execute("SELECT ip_address, mac_address, 'Saved', 'None', alias, vendor FROM network_devices")
    rows = cur.fetchall()
    conn.close()
    return rows

def save_to_db(ip, mac, hostname, vendor_name):
        conn = None
        try:
            conn = sqlite3.connect("network_monitor.db")
            cur = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            query = """
            INSERT INTO network_devices(mac_address, ip_address, first_seen, last_seen, alias, vendor)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (mac_address)
            DO UPDATE SET
                ip_address = EXCLUDED.ip_address,
                last_seen = EXCLUDED.last_seen,
                vendor = COALESCE(network_devices.vendor, EXCLUDED.vendor)
            """
            
            cur.execute(query, (mac, ip, now, now, hostname, vendor_name))
            cur.execute("SELECT alias, vendor FROM network_devices WHERE mac_address = ?", (mac,))
            result = cur.fetchone()
            
            conn.commit()
            return result if result else("Unknown", "Unknown")
        
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return "Unknown"
        finally:
            if conn:
                conn.close()
        
def update_alias_in_db(mac, new_alias):
        try:
            conn = sqlite3.connect("network_monitor.db")
            cur = conn.cursor()
            cur.execute("UPDATE network_devices SET alias = ? WHERE mac_address = ?", (new_alias, mac))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating alias: {e}")
            
def get_vendor_from_db(mac):
    try:
        conn = sqlite3.connect("network_monitor.db")
        cur = conn.cursor()
        cur.execute("SELECT vendor FROM network_devices WHERE mac_address = ?", (mac,))
        res = cur.fetchone()
        conn.close()
        return res[0] if res and res[0] else None
    except:
        return None
