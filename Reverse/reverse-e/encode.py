#!/usr/bin/env python3

import sys
import base64

def rol(b, r):
    r %= 8
    return ((b << r) | (b >> (8 - r))) & 0xFF

def lcg32(x):
    return (1103515245 * x + 12345) & 0xFFFFFFFF

def keystream_byte(i):
    v = lcg32(i ^ 0xC0FFEE)
    return (v >> 16) & 0xFF

def make_permutation(n):
    perm = list(range(n))
    state = (n * 0x9E3779B1) & 0xFFFFFFFF
    for i in range(n - 1, 0, -1):
        state = lcg32(state)
        j = state % (i + 1)
        perm[i], perm[j] = perm[j], perm[i]
    return perm

def encode(flag: str) -> str:
    bs = flag.encode('utf-8')
    n = len(bs)

    layer1 = [ (b + keystream_byte(i)) & 0xFF for i, b in enumerate(bs) ]

    layer2 = [ rol(v, (i * 7 + 3) % 8) for i, v in enumerate(layer1) ]

    layer3 = [ v ^ ((i * 31 + 77) & 0xFF) for i, v in enumerate(layer2) ]

    perm = make_permutation(n)
    out = [0] * n
    for i, v in enumerate(layer3):
        out[perm[i]] = v

    return base64.b64encode(bytes(out)).decode('ascii')

def main():
    if len(sys.argv) >= 2:
        flag = sys.argv[1]
    else:
        flag = sys.stdin.read().strip()
    if not flag:
        return
    encoded_str = encode(flag)
    print(encoded_str)

if __name__ == "__main__":
    main()
