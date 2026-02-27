import tkinter as tk
from tkinter import ttk
import threading        
import database as db
import network_logic as net
import vendor_lookup as ven



class NetworkHealthMonitor:
    def __init__(self, root):
        self.root = root 
        self.root.title("Network Health & Security Monitor")
        self.root.geometry("1200x600") 
        
        self.header = tk.Label(root, text="Network Device Discovery & Port Audit", font=("Arial", 14, "bold"))
        self.header.pack(pady=15)
        
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Target Range:").grid(row=0, column=0, padx=5)
        self.range_entry = tk.Entry(control_frame)
        self.range_entry.insert(0, "192.168.1.0/24")
        self.range_entry.grid(row=0, column=1, padx=5)
        
        self.scan_button = tk.Button(control_frame, text="Scan Network", command=self.start_scan_thread, bg="#2c3e50", fg="black")
        self.scan_button.grid(row=0, column=2, padx=10)
    
        self.tree = ttk.Treeview(root, columns=("IP", "MAC", "Status", "Ports", "Alias", "Vendor"), show="headings")
        self.tree.tag_configure("intruder", foreground = "red", font=("Arial", 0, "bold"))
        self.tree.heading("IP", text="IP Address")
        self.tree.heading("MAC", text="MAC Address")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Ports", text="Open Ports")
        self.tree.heading("Alias", text="Device Alias") 
        self.tree.heading("Vendor", text="Device Vendor") 
        self.tree.column("Alias", width=150)
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        self.tree.bind("<Double-1>", self.on_double_click)
        db.init_db()
        self.load_data()

    
        
    def start_scan_thread(self):
        target = self.range_entry.get()
        self.scan_button.config(state="disabled")
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        thread = threading.Thread(target=self.run_network_scan, args=(target,))
        thread.daemon = True
        thread.start()

    def run_network_scan(self, target_range):
        try:
            answered_list = net.do_arp_scan(target_range)
            
            for sent, received in answered_list:
                current_ip = received.psrc
                current_mac = received.hwsrc
                vendor = db.get_vendor_from_db(current_mac)
                
                if not vendor or vendor in ["Unknown", "Api Offline"]:
                    vendor = ven.get_vendor_api(current_mac)
                    
                if vendor is None: vendor = "Unknown"
                
                
                hostname_raw = net.get_device_hostname(current_ip)
                
                res_db = db.save_to_db(current_ip, current_mac, hostname_raw, vendor)
                final_alias = res_db[0]
                final_vendor = res_db[1]
                
                
                status = "Active"
                row_tag = ""
                if (not final_alias or final_alias == "Unknown") and ("Unknown" in final_vendor or "Private" in final_vendor):
                    status = "INTRUDER?"
                    row_tag = "intruder"
                
                display_name = final_alias if final_alias not in [None, "Unknown", "Null"] else (hostname_raw or "Generic Device")
                open_ports = net.scan_ports(current_ip)
                
                self.root.after(0, lambda i=current_ip, m=current_mac, s=status, p=open_ports, d=display_name, v=final_vendor, t=row_tag: self.tree.insert("", "end", values=(i, m, s, p, d, v), tags=(t,)))
           
        except Exception as e:
            print(f"Scan Error: {e}")
            
        finally:
            self.root.after(0, lambda: self.scan_button.config(state="normal"))
            
    
    def on_double_click(self, event):
        item_id = self.tree.selection()[0]
        item_values = self.tree.item(item_id, "values")
        mac = item_values[1]
        
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Device Alias")
        edit_win.geometry("300x150")
        
        tk.Label(edit_win, text=f"New Alias for {mac}: ").pack(pady=10)
        new_alias_entry = tk.Entry(edit_win)
        new_alias_entry.pack(pady=5)
        
        def save_alias():
            new_name = new_alias_entry.get()
            if new_name:
                db.update_alias_in_db(mac, new_name)
                self.tree.set(item_id, 4, new_name)
                edit_win.destroy()
                
        tk.Button(edit_win, text="Save", command=save_alias).pack(pady=10)
        
    
    def load_data(self):
        try:
            rows = db.get_all_devices()
            
            for row in rows:
                #row[0]=IP, row[1]=MAC, row[2]=Alias, row[3]=Vendor
                self.tree.insert("", "end", values=(row[0], row[1], "Saved", "Scan to check", row[2], row[3]))
        except Exception as e:
            print(f"Error al cargar: {e}")
            
                
if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkHealthMonitor(root)
    root.mainloop()