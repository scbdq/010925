#!/bin/bash

set -e

C_SOURCE_FILE="challenge.cpp"
OBJECT_FILE="challenge.o"
MODIFIED_OBJECT_FILE="challenge_modified.o"
FINAL_EXECUTABLE="challenge"
FLAG_FILE="flag.txt"
SECTION_NAME=".my_secret" 
FLAG="vsosh{sp3c14l_ELF_s3ct10n}"


cat > "${C_SOURCE_FILE}" << EOF
#include <stdio.h>

int main() {
    printf("Флаг не в коде и не в обычных строках.\n");
    return 0;
}
EOF

echo -n "${FLAG}" > "${FLAG_FILE}"

gcc -c "${C_SOURCE_FILE}" -o "${OBJECT_FILE}"

objcopy --add-section "${SECTION_NAME}"="${FLAG_FILE}" "${OBJECT_FILE}" "${MODIFIED_OBJECT_FILE}"

gcc -no-pie -o "${FINAL_EXECUTABLE}" "${MODIFIED_OBJECT_FILE}"

rm "${C_SOURCE_FILE}" "${OBJECT_FILE}" "${MODIFIED_OBJECT_FILE}" "${FLAG_FILE}"

