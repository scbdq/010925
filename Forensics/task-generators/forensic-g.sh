set -euo pipefail
mkdir -p forensic-g
FLAG=$(openssl rand -hex 32 | sed 's/.*/forensic{&}/')
echo "$FLAG" > forensic-g/secret.txt
gzip -c forensic-g/secret.txt > forensic-g/secret.txt.gz
xxd -p forensic-g/secret.txt.gz > forensic-g/dump.hex
rm -f forensic-g/secret.txt.gz forensic-g/secret.txt
echo "$FLAG" > forensic-g/.flag