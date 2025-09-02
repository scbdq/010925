#!/usr/bin/env bash
set -euo pipefail
mkdir -p forensic-a/logs
FLAG=$(openssl rand -hex 32 | sed 's/.*/forensic{&}/')
for i in $(seq 1 1500); do
  echo "$(openssl rand -hex 32):$(openssl rand -hex 16)" > forensic-a/log_$(openssl rand -hex 4).txt
done
echo "meta:$(openssl rand -hex 8) $FLAG end" > forensic-a/log_$(openssl rand -hex 4).txt
echo "$FLAG" > forensic-a/.flag