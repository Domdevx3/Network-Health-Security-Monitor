import requests
import time

    
def get_vendor_api(mac):
    try:
        time.sleep(1.2)
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, headers=headers, timeout=5)
                        
        if response.status_code == 200:
            vendor = response.text
        elif response.status_code == 429:
            vendor = "Rate Limited (Too Fast)"
        elif response.status_code == 404:
            vendor = "Private/Random MAC"
        else:
            vendor = f"Error {response.status_code}"
        return vendor
    except Exception as e:
        return "API Offline"
    
    
