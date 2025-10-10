
#!/usr/bin/env python3

import base64

encoded = "wL0Zo/MYMC8lw7ddjC9Ci9D4pdz+92g="

def rol(b, r):
    r %= 8
    return ((b << r) | (b >> (8 - r))) & 0xFF

def ror(b, r):
    r %= 8
    return ((b >> r) | (b << (8 - r))) & 0xFF

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

def decode(encoded_str):
    data = list(base64.b64decode(encoded_str))
    n = len(data)

    perm = make_permutation(n)
    layer3 = [0] * n
    for i in range(n):
        layer3[i] = data[perm[i]]

    layer2 = [ v ^ ((i * 31 + 77) & 0xFF) for i, v in enumerate(layer3) ]

    layer1 = [ ror(v, (i * 7 + 3) % 8) for i, v in enumerate(layer2) ]

    bs = bytearray((v - keystream_byte(i)) & 0xFF for i, v in enumerate(layer1))

    return bs.decode('utf-8')

if __name__ == "__main__":
    flag = decode(encoded)
    print("Recovered flag:", flag)
