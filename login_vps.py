#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VPS Login & OTP helper script
---------------------------------
This script demonstrates the full handshake → login → OTP flow for the
VPS API (bgapi.vps.com.vn). It includes robust error handling and prints
useful debug information.

Usage:
    python login_vps.py
    # The script will prompt for the OTP code.

Make sure to replace the placeholder values for `raw_device_new` and
`device_info` with the actual values you receive from the VPS client.
"""

import json
import base64
import urllib.parse
import requests
from typing import Dict
import sys

# ---------------------------------------------------------------------------
# Configuration (replace with your real values)
# ---------------------------------------------------------------------------
BASE_URL = "https://bgapi.vps.com.vn"
HANDSHAKE_URL = f"{BASE_URL}/handler/core.vpbs"
LOGIN_URL = f"{BASE_URL}/handler/core_check.login"

# ---- Device information ----------------------------------------------------
# The raw `deviceNew` string you received from the VPS client (very long).
RAW_DEVICE_NEW = "SWyBp0tYbPcK2cehnzGtgxJn6TJXiemsNW6BduP9JUKLD9zXsor2X6R8GovcQrokGoFt6gdwZU5 bSGBBLKdLDwzL3MC01ZH1PUw2VY0/5T54llsG87KpzWqvr7Dpdqsndsf1aX6c JMwx4EQ8nRelELk/qAtKVAeGeXewx5oqiWgsGQgDt3XdaQ4FH5KzQgeeUdyVlCNWi5Yw0YlxVW0wTpG1rTkI6rsZ2616YiV6QyOfYnHGKoUw=="

# DeviceInfo is a JSON object that must be base64‑encoded and URL‑encoded.
DEVICE_INFO_DICT = {
    "type": "web",
    "source": "Priceboard",
    "version": "1.8.0",
    "model": "Chrome Windows 10",
    "deviceOS": "",
    "geoLocation": "",
}

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
HEADERS = {
    "content-type": "application/json; charset=UTF-8",
    "accept": "*/*",
    "origin": "https://banggia.vps.com.vn",
    "referer": "https://banggia.vps.com.vn/",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"156\", \"Google Chrome\";v=\"156\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
}

# Session to keep cookies and reuse headers
session = requests.Session()
session.headers.update(HEADERS)
# Warm‑up request to obtain any initial cookies the server may set
try:
    session.get(BASE_URL, timeout=5)
except Exception as e:
    print("[Info] Warm‑up request failed (ignored):", e)

# Session to keep cookies and reuse headers


def encode_device_info(info: dict) -> str:
    """Encode the deviceInfo dict to a plain base64 string (no URL‑encoding)."""
    json_str = json.dumps(info, separators=(",", ":"))
    return base64.b64encode(json_str.encode()).decode()

# ---------------------------------------------------------------------------
# Step 1 – Handshake
# ---------------------------------------------------------------------------
def do_handshake() -> dict:
    global RAW_DEVICE_NEW
    while True:
        payload = {
            "deviceNew": RAW_DEVICE_NEW,  # raw token from DevTools, no extra encoding
            "deviceName": "Chrome Windows 10",
            "deviceInfo": encode_device_info(DEVICE_INFO_DICT),
        }
        # Print payload as JSON for debugging
        print("[Handshake] Payload (JSON):", json.dumps(payload, indent=2))
        print("[Handshake] Headers:", HEADERS)
        resp = session.post(HANDSHAKE_URL, json=payload, timeout=60)
        resp.raise_for_status()
        raw_text = resp.text
        print("[Handshake] Raw response text:", raw_text)
        try:
            data = resp.json()
        except Exception:
            print("[Error] Response is not JSON. Exiting.")
            sys.exit(1)
        print("[Handshake] Response:", data)
        if data.get("rc") != 0:
            raise RuntimeError(f"Handshake failed – rc={data.get('rc')} rs={data.get('rs')}")
        # Detect invalid session or empty data
        if data.get("rs") == "FOException.InvalidSessionException" or not data.get("data"):
            new_token = input("Handshake failed - enter new deviceNew token: ").strip()
            if not new_token:
                sys.exit("No token provided - exiting.")
            RAW_DEVICE_NEW = new_token
            continue  # retry with new token
        handshake_payload = data.get("data")
        if isinstance(handshake_payload, str):
            try:
                handshake_payload = json.loads(handshake_payload)
            except Exception:
                pass
        if not isinstance(handshake_payload, dict):
            handshake_payload = {}
        return handshake_payload

# ---------------------------------------------------------------------------
# Step 2 – Login (step 1)
# ---------------------------------------------------------------------------
def login_step1(handshake: dict, user: str, pwd_hash: str) -> dict:
    payload = {
        "user": user,
        "pass": pwd_hash,
        "channel": "I",
        "language": "vi",
        "cmd": "Web.sCheckLogin",
        "p5": "",
        "p6": "",
        "p7": 1,
        "deviceNew": handshake["deviceNew"],
        "deviceName": "Chrome Windows 10",
        "deviceInfo": handshake["deviceInfo"],
        "sessionId": handshake["sessionId"],
    }
    # Detailed request logging for login step 1
    print("[Login] URL:", LOGIN_URL)
    print("[Login] Method: POST")
    print("[Login] Payload:", json.dumps(payload, indent=2))
    print("[Login] Headers:", HEADERS)
    # Use form‑encoded payload as the server expects
    login_headers = HEADERS.copy()
    login_headers["content-type"] = "application/x-www-form-urlencoded"
    resp = session.post(LOGIN_URL, data=payload, headers=login_headers, timeout=60)
    print("[Login] Response status code:", resp.status_code)
    print("[Login] Response headers:", dict(resp.headers))
    resp.raise_for_status()
    raw_text = resp.text
    print("[Login] Raw response text:", raw_text)
    data = resp.json()
    print("[Login] Response:", data)
    return data

# ---------------------------------------------------------------------------
# Step 3 – OTP (step 2)
# ---------------------------------------------------------------------------
def login_otp(handshake: dict, otp_code: str) -> dict:
    payload = {
        "user": handshake.get("user", ""),  # optional – some APIs require it again
        "pass": handshake.get("pass", ""),
        "cmd": "Web.sCheckLoginOTP",
        "otp": otp_code,
        "p5": "",
        "p6": "",
        "p7": 1,
        "deviceNew": handshake["deviceNew"],
        "deviceInfo": handshake["deviceInfo"],
        "sessionId": handshake["sessionId"],
    }
    print("[OTP] Sending payload →", payload)
    resp = requests.post(LOGIN_URL, json=payload, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print("[OTP] Response →", data)
    return data

# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Replace these with your actual credentials
    USERNAME = "P91708"
    PASSWORD_HASH = "e4b57d46a8053ddb7341ee6e6b35924c"

    # 1️⃣ Handshake
    handshake_data = do_handshake()
    # Verify that we obtained a valid sessionId
    if not isinstance(handshake_data, dict) or not handshake_data.get("sessionId"):
        sys.exit("❌ Handshake succeeded but no valid sessionId was returned. Cannot continue.")
    print("[Info] Handshake succeeded – sessionId:", handshake_data.get("sessionId"))

    # 2️⃣ Login step 1
    login_res = login_step1(handshake_data, USERNAME, PASSWORD_HASH)
    if login_res.get("rc") != 0:
        sys.exit(f"❌ Login step 1 failed – rc={login_res.get('rc')} rs={login_res.get('rs')}")
    print("[Info] Login step 1 succeeded.")

    # 3️⃣ OTP – ask user for the code
    otp = input("Enter OTP code: ").strip()
    otp_res = login_otp(handshake_data, otp)
    if otp_res.get("rc") == 0:
        print("✅ Login successful!")
    else:
        print(f"❌ OTP failed – rc={otp_res.get('rc')} rs={otp_res.get('rs')}")

