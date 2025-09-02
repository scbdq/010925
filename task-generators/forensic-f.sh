set -euo pipefail
mkdir -p forensic-f/storage
FLAG=$(openssl rand -hex 32 | sed 's/.*/forensic{&}/')
for i in $(seq 1 300); do
  head -c $((128 + RANDOM % 1024)) /dev/urandom > forensic-f/storage/$(openssl rand -hex 6).blob
done
TARGET=forensic-f/storage/$(openssl rand -hex 6).blob
truncate -s 512 "$TARGET"
printf "%s" "$FLAG" | dd of="$TARGET" conv=notrunc bs=1 status=none
chmod 600 "$TARGET"
echo "$FLAG" > forensic-f/.flag