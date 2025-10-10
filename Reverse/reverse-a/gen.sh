#!/bin/bash
set -euo pipefail

flag='vsosh{jus7_l00k_insid3}'

b64_flag=$(printf '%s' "$flag" | base64)

png_b64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="

workdir="create"

mkdir "$workdir"

cd "$workdir"

echo "$png_b64" | base64 -d > outer.png

cat > secret_print.c <<'EOF'
#include <stdio.h>
int main(void){
    const char *b64 = "__B64_PLACEHOLDER__";
    printf("Ладно тут флаг: %s\n", b64);
    return 0;
}
EOF

sed -i "s|__B64_PLACEHOLDER__|$b64_flag|" secret_print.c

gcc secret_print.c -o secret_exec -s

zip -j secret.zip secret_exec >/dev/null

cat outer.png secret.zip > challenge.png

