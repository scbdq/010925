#!/usr/bin/env python3
import secrets
import random
import time
import hashlib
import os
from scapy.all import *

OUTPUT_PCAP = "forensic-h.pcap"

FLAG = "forensic{" + secrets.token_hex(32) + "}"
CORE = FLAG[9:-1]
SEGMENTS = [CORE[i:i+16] for i in range(0, len(CORE), 16)]
SEGMENTS = SEGMENTS[:4]

DNS_DOMAIN = "forensictest.lab"

DNS_SRC, DNS_DST = "198.51.100.10", "203.0.113.53"
HTTP_SRC, HTTP_DST = "198.51.100.20", "203.0.113.50"
ICMP_SRC, ICMP_DST = "198.51.100.25", "203.0.113.80"
FTP_SRC, FTP_DST = "203.0.113.60", "203.0.113.70"
TLS_SRC, TLS_DST = "198.51.100.30", "203.0.113.90"

packets = []

for i, seg in enumerate(SEGMENTS):
    qname = f"seg{i+1}.{i}.{DNS_DOMAIN}"
    dns_q = DNS(rd=1, qd=DNSQR(qname=qname, qtype='TXT'))
    dns_r = DNSRR(rrname=qname, type='TXT', rdata=seg)
    p = IP(src=DNS_SRC, dst=DNS_DST)/UDP(sport=10000+i, dport=53)/dns_q
    p2 = IP(src=DNS_DST, dst=DNS_SRC)/UDP(sport=53, dport=10000+i)/DNS(id=dns_q.id, qr=1, aa=1, qd=dns_q.qd, an=[dns_r])
    p.time = 1609459200 + i*300
    p2.time = p.time + 0.001
    packets.extend([p, p2])

for i, seg in enumerate(SEGMENTS):
    client = f"10.0.0.{i+2}"
    sport = 40000 + i

    syn = IP(src=client, dst=HTTP_DST)/TCP(sport=sport, dport=80, flags="S")
    synack = IP(src=HTTP_DST, dst=client)/TCP(sport=80, dport=sport, flags="SA", seq=2000, ack=1001)
    ack = IP(src=client, dst=HTTP_DST)/TCP(sport=sport, dport=80, flags="A", seq=1001, ack=2001)
    http_resp = (
        "HTTP/1.1 200 OK\r\n"
        f"X-Flag-Segment: {seg}\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"segment-{i+1}\r\n"
    )
    resp = IP(src=HTTP_DST, dst=client)/TCP(sport=80, dport=sport, flags="A", seq=2001, ack=1001)/Raw(load=http_resp)
    t0 = 1609459200 + 2*i*0.5
    syn.time = t0
    synack.time = syn.time + 0.01
    ack.time = synack.time + 0.01
    resp.time = ack.time + 0.01
    packets.extend([syn, synack, ack, resp])

for i, seg in enumerate(SEGMENTS):
    p = IP(src=ICMP_SRC, dst=ICMP_DST)/ICMP()/Raw(load=seg.encode())
    p.time = 1609459200 + 4 + i*0.7
    packets.append(p)

for i, seg in enumerate(SEGMENTS):
    client_ip = "203.0.113.60"
    server_ip = "203.0.113.70"
    sport = 50000 + i

    syn = IP(src=client_ip, dst=server_ip)/TCP(sport=sport, dport=21, flags="S")
    synack = IP(src=server_ip, dst=client_ip)/TCP(sport=21, dport=sport, flags="SA", seq=2000, ack=1001+i)
    ack = IP(src=client_ip, dst=server_ip)/TCP(sport=sport, dport=21, flags="A", seq=1001+i, ack=2001+i)
    retr = IP(src=client_ip, dst=server_ip)/TCP(sport=sport, dport=21, flags="A", seq=1002+i, ack=2002+i)/Raw(load=f"RETR forensic_seg{i+1}.txt\r\n")
    syn.time = 1609459200 + 6 + i*0.9
    synack.time = syn.time + 0.02
    ack.time = synack.time + 0.02
    retr.time = ack.time + 0.02
    packets.extend([syn, synack, ack, retr])

hash16 = hashlib.sha256(FLAG.encode()).hexdigest()[:16]
tls_payload = f"TLS ClientHello... SNI:{hash16} ... END".encode()
tls_pkt = IP(src=TLS_SRC, dst=TLS_DST)/TCP(sport=65001, dport=443, flags="A")/Raw(load=tls_payload)
tls_pkt.time = 1609459200 + 10
packets.append(tls_pkt)

for j in range(2000):
    u = IP(src=f"198.51.100.{random.randint(1,254)}", dst=f"203.0.113.{random.randint(1,254)}")\
        /UDP(sport=random.randint(1024,65535), dport=random.randint(1024,65535))/Raw(load=os.urandom(random.randint(20, 120)))
    u.time = 1609459200 + 20 + j*0.01
    packets.append(u)

wrpcap(OUTPUT_PCAP, packets)

with open(".flag-h", "w") as f:
    f.write(FLAG)