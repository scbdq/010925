#!/usr/bin/env bash
set -euo pipefail
mkdir -p forensic-e/layer1
FLAG=$(openssl rand -hex 32 | sed 's/.*/forensic{&}/')
for i in $(seq 1 80); do
  head -c 48 /dev/urandom > forensic-e/layer1/$(openssl rand -hex 6).txt
done
echo -n "$FLAG" | base64 > forensic-e/layer1/hidden.b64
tar -C forensic-e -czf forensic-e/pack1.tgz layer1
mkdir -p forensic-e/wrapper
cp forensic-e/pack1.tgz forensic-e/wrapper/
for i in $(seq 1 40); do
  dd if=/dev/urandom bs=256 count=1 of=forensic-e/wrapper/$(openssl rand -hex 5).bin 2>/dev/null
done
tar -C forensic-e/wrapper -czf forensic-e/wrapping.tgz .
echo "$FLAG" > forensic-e/.flag