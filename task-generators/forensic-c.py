#!/usr/bin/env python3
from scapy.all import *
import secrets, random, time, os

OUTPUT_PCAP = "forensic-с.pcap"
FLAG = "forensic{" + secrets.token_hex(32) + "}"
CORE = FLAG[9:-1]
BITS = [i % 2 for i in range(64)]

packets = []
src, dst = "10.0.0.1", "10.0.0.2"

for _ in range(40000):
    p = IP(src=src, dst=dst)/UDP(sport=random.randint(1024,65535), dport=12345)/Raw(load=os.urandom(random.randint(20,60)))
    p.time = time.time()
    packets.append(p)

for idx in range(64):
    bit_id = BITS[idx] & 1
    bit_seq = (BITS[idx] ^ 1) & 1
    ip_id = bit_id
    pkt = IP(src=src, dst=dst, id=ip_id)/TCP(sport=10000+idx, dport=80, seq=bit_seq, flags="A")/Raw(load=f"b{idx}:{bit_id}:{bit_seq}".encode())
    pkt.time = time.time() + (idx+1)*0.01
    packets.append(pkt)

wrpcap(OUTPUT_PCAP, packets)
with open(".flag-c", "w") as f: f.write(FLAG)