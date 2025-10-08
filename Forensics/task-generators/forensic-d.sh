#!/usr/bin/env bash
set -euo pipefail
mkdir -p forensic-d
FLAG=$(openssl rand -hex 32 | sed 's/.*/forensic{&}/')
FILE=forensic-d/report.txt
rm -f "$FILE"
for i in $(seq 1 80); do
  echo "SECTION-$(openssl rand -hex 4)" >> "$FILE"
  for j in $(seq 1 10); do
    echo "$(openssl rand -hex 48)" >> "$FILE"
  done
  echo "END-$(openssl rand -hex 4)" >> "$FILE"
done
echo "BEGIN-$(openssl rand -hex 6)" >> "$FILE"
echo "$(openssl rand -hex 40)" >> "$FILE"
echo "$FLAG" >> "$FILE"
echo "$(openssl rand -hex 32)" >> "$FILE"
echo "FIN-$(openssl rand -hex 6)" >> "$FILE"
echo "$FLAG" > forensic-d/.flag