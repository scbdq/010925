#!/usr/bin/env python3
import os

os.makedirs("forensic-i", exist_ok=True)

import secrets

FLAG = "forensic{" + secrets.token_hex(32) + "}"
KEY = 0x55

with open("forensic-i/mystery.bin", "wb") as f:
    f.write(os.urandom(1024))  
    f.write(bytes([b ^ KEY for b in FLAG.encode()]))  
    f.write(os.urandom(512))