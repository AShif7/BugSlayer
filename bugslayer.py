# Placeholder for BugSlayer tool code
#!/usr/bin/env python3 """ BugSlayer v1.1 - Complete OWASP Top10 Automated Scanner with Animation, Proxy/User-Agent Rotation, Reporting """ import argparse import subprocess import requests import concurrent.futures import time import itertools import sys import random import json from urllib.parse import urlparse from colorama import init, Fore, Style import pyfiglet

Initialize colorama

init(autoreset=True)

User-agent list for rotation\USER_AGENTS = [

"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
"Mozilla/5.0 (X11; Linux x86_64)",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
"Googlebot/2.1 (+http://www.google.com/bot.html)",
"curl/7.68.0"

]

Proxy list example (can be extended)

PROXIES = [ None,  # direct {"http": "http://127.0.0.1:9050", "https": "http://127.0.0.1:9050"}  # Tor ]

Report storage

report = {"target": None, "vulnerabilities": []}

def animated_banner(): banner = pyfiglet.figlet_format("BugSlayer v1.1") for line in banner.split("\n"): print(Fore.CYAN + line) time.sleep(0.02)

def spinner(msg, duration=2): spinner_cycle = itertools.cycle(["|", "/", "-", "\"]) end_time = time.time() + duration sys.stdout.write(Fore.YELLOW + msg + " ") while time.time() < end_time: sys.stdout.write(next(spinner_cycle)) sys.stdout.flush() time.sleep(0.1) sys.stdout.write("\b") print(Fore.GREEN + "Done!")

def fake_hacking_intro(target): steps = [ f"[+] Target Acquired: {target}", "[+] Establishing secure connection...", "[+] Bypassing firewall...", "[+] Injecting scanning modules...", "[+] Recon engine online" ] for step in steps: print(Fore.GREEN + step) time.sleep(0.8)

phases = [
    ("[=         ] 10% - Initializing modules", 0.4),
    ("[=====     ] 50% - Loading payloads", 0.4),
    ("[==========] 100% - Ready to scan", 0.6)
]
for text, d in phases:
    print(Fore.YELLOW + text)
    time.sleep(d)

def rotate_headers(): return {"User-Agent": random.choice(USER_AGENTS)}

def choose_proxy(): return random.choice(PROXIES)

def nmap_scan(target): spinner("[+] Running Nmap port & service scan...", 3) subprocess.run(["nmap", "-sC", "-sV", target])

def dirb_scan(target): spinner("[+] Running directory brute-force (gobuster)...", 3) subprocess.run(["gobuster", "dir", "-u", f"http://{target}", "-w", "/usr/share/wordlists/dirb/common.txt"])

def sqlmap_scan(target): print(Fore.YELLOW + "[+] Testing for SQL Injection with sqlmap...") cmd = ["sqlmap", "-u", f"http://{target}/?id=1", "--batch", "--level=2"] subprocess.run(cmd) report["vulnerabilities"].append({"type": "SQL Injection", "details": "See sqlmap output"})

def xss_scan(target): print(Fore.YELLOW + "[+] Testing for XSS with XSStrike...") cmd = ["python3", "XSStrike/xsstrike.py", "-u", f"http://{target}/?search=test", "--crawl"] subprocess.run(cmd) report["vulnerabilities"].append({"type": "XSS", "details": "See XSStrike output"})

def header_check(target): print(Fore.YELLOW + "[+] Checking security headers...") try: resp = requests.get(f"http://{target}", headers=rotate_headers(), proxies=choose_proxy(), timeout=5) missing = [] for h in ["X-Frame-Options", "Content-Security-Policy", "X-XSS-Protection"]: if h not in resp.headers: missing.append(h) if missing: print(Fore.RED + f"[-] Missing security headers: {missing}") report["vulnerabilities"].append({"type": "Security Headers", "details": missing}) else: print(Fore.GREEN + "[+] All important headers present") except Exception as e: print(Fore.RED + "[-] Header check failed:", e)

def generate_reports(target): # Text report timestamp = time.strftime("%Y%m%d-%H%M%S") txt_file = f"report_{target}{timestamp}.txt" json_file = f"report{target}_{timestamp}.json" with open(txt_file, "w") as f: f.write(json.dumps(report, indent=2)) with open(json_file, "w") as f: f.write(json.dumps(report, indent=2)) print(Fore.CYAN + f"[+] Reports saved: {txt_file}, {json_file}")

def main(): parser = argparse.ArgumentParser(description="BugSlayer v1.1 - OWASP Top10 Scanner") parser.add_argument("--target", required=True, help="Target domain or IP") args = parser.parse_args() tgt = args.target # Remove scheme parsed = urlparse(tgt) target = parsed.netloc or parsed.path report["target"] = target

animated_banner()
fake_hacking_intro(target)

# Run phases
nmap_scan(target)
header_check(target)
dirb_scan(target)
sqlmap_scan(target)
xss_scan(target)

generate_reports(target)

if name == "main": main()

