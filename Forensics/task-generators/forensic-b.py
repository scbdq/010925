#!/usr/bin/env python3
from scapy.all import *
import secrets, random, time

OUTPUT_PCAP = "forensic-b.pcap"
FLAG = "forensic{" + secrets.token_hex(32) + "}"
segments = [FLAG[9+i*16:9+(i+1)*16] for i in range(4)]
pkts = []
src, dst = "10.0.0.1", "10.0.0.2"

def smb_like_transaction(cmd, payload, sport, dport=445):
    return IP(src=src, dst=dst)/TCP(sport=sport, dport=dport, flags="PA")/Raw(load=(cmd + ":" + payload).encode())

for i in range(25000):
    b = IP(src=src, dst=dst)/TCP(sport=1000+i, dport=445, flags="S")
    b.time = time.time() + i*0.002
    pkts.append(b)
    s = IP(src=dst, dst=src)/TCP(sport=445, dport=1000+i, flags="SA", seq=1000+i, ack=2000+i)
    s.time = b.time + 0.001
    pkts.append(s)
    a = IP(src=src, dst=dst)/TCP(sport=1000+i, dport=445, flags="A", seq=1001+i, ack=2001+i)
    a.time = s.time + 0.001
    pkts.append(a)

for idx, seg in enumerate(segments):
    sport = 20000 + idx
    filename = f"file_seg{idx+1}.bin"
    pkts.append(smb_like_transaction("SMB_COM_TRANSACTION2", f"FILENAME={filename};SEG={seg}", sport))
    content = f"SEGMENT={seg}".encode()
    pkts.append(IP(src=src, dst=dst)/TCP(sport=sport, dport=445, flags="PA")/Raw(load=content))

wrpcap(OUTPUT_PCAP, pkts)
with open(".flag-b", "w") as f: f.write(FLAG)