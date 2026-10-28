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
RAW_DEVICE_NEW = "CFE0y/Neafs070CWpn0fgmFoMd6P9nZPyjD/P4VvUObQUlZ0IGU5DzbTf99mlG1A0WBAM4TAxlQWmQqHmbUz0ZDKwIQ/clX37czeZLuip6cS2MuJw3hdaDywSntSrMWkPCSnFwmRmc95E2CDogeGQ5QYGybFyp5KDOjQZDxBqJcf/AA1uKSfTGy3yuULUGZOI9YudukPT1vG6LyRbQOd/kwj3oZSqGPMKAL16fFh9KocutZxpG"

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
    "Content-Type": "application/json; charset=UTF-8",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Access-Control-Allow-Origin": "*",
}

def encode_device_info(info: dict) -> str:
    """Encode the deviceInfo dict to a URL‑safe base64 string."""
    json_str = json.dumps(info, separators=(",", ":"))
    b64 = base64.b64encode(json_str.encode()).decode()
    return urllib.parse.quote_plus(b64)

# ---------------------------------------------------------------------------
# Step 1 – Handshake
# ---------------------------------------------------------------------------
def do_handshake() -> dict:
    payload = {
        "deviceNew": RAW_DEVICE_NEW,
        "deviceName": "Chrome Windows 10",
        "deviceInfo": encode_device_info(DEVICE_INFO_DICT),
    }
    print("[Handshake] Sending payload…")
    resp = requests.post(HANDSHAKE_URL, json=payload, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print("[Handshake] Response:", data)
    if data.get("rc") != 0:
        raise RuntimeError(
            f"Handshake failed – rc={data.get('rc')} rs={data.get('rs')}"
        )
    handshake_payload = data.get("data")
    # The API sometimes returns the `data` field as a JSON string or as an empty list.
    if isinstance(handshake_payload, str):
        try:
            handshake_payload = json.loads(handshake_payload)
        except Exception:
            # If it cannot be parsed, keep the raw string (will be treated as invalid later)
            pass
    # Ensure we always return a dict; if the payload is not a dict (e.g., [] or ""), return empty dict.
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
    print("[Login] Step 1 payload →", payload)
    resp = requests.post(LOGIN_URL, json=payload, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print("[Login] Step 1 response →", data)
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

