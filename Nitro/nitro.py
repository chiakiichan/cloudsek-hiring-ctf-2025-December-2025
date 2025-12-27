#!/usr/bin/env python3
import requests
import base64
import re
import time

BASE_URL = "http://15.206.47.5:9090"

# Session so you keep the same cookies (per-session timer)
session = requests.Session()


def get_random_string() -> str:
    """Fetch /task and pull out the random string from the HTML snippet."""
    resp = session.get(f"{BASE_URL}/task", timeout=3)
    resp.raise_for_status()
    html = resp.text
    m = re.search(r'([A-Za-z0-9+/=]{8,})', html)
    if not m:
        raise ValueError("Could not find random string in /task response")
    return m.group(1)


def build_payload(random_str: str) -> str:
    """Reverse, base64-encode, and wrap as CSK__{{payload}}__2025."""
    reversed_str = random_str[::-1]
    b64 = base64.b64encode(reversed_str.encode()).decode()
    return f"CSK__{b64}__2025"


def submit_answer(payload: str) -> str:
    """POST the raw payload to /submit and return the response body."""
    resp = session.post(f"{BASE_URL}/submit", data=payload, timeout=3)
    resp.raise_for_status()
    return resp.text


def main():
    while True:
        try:
            rnd = get_random_string()
            payload = build_payload(rnd)
            reply = submit_answer(payload)

            print("[*] random:", rnd)
            print("[*] payload:", payload)
            print("[*] response:", reply)

            if "flag" in reply.lower():
                print("[+] Got the flag!")
                break

            time.sleep(0.05)

        except Exception as e:
            print("[!] Error:", e)
            time.sleep(0.2)


if __name__ == "__main__":
    main()
