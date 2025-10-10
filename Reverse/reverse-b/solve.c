#include <stdio.h>

int main(void) {
    char s[18];

    __asm__ volatile(
        "movl $7, %%eax;\n\t"
        "imull $17, %%eax;\n\t"
        "subl $1, %%eax;\n\t"
        "movb %%al, 0(%0);\n\t"

        "movl $12, %%eax;\n\t"
        "imull $10, %%eax;\n\t"
        "subl $5, %%eax;\n\t"
        "movb %%al, 1(%0);\n\t"

        "movl $37, %%eax;\n\t"
        "imull $3, %%eax;\n\t"
        "movb %%al, 2(%0);\n\t"

        "movl $300, %%eax;\n\t"
        "shrl $1, %%eax;\n\t"
        "subl $35, %%eax;\n\t"
        "movb %%al, 3(%0);\n\t"

        "movl $13, %%eax;\n\t"
        "shll $3, %%eax;\n\t"
        "movb %%al, 4(%0);\n\t"

        "movl $41, %%eax;\n\t"
        "imull $3, %%eax;\n\t"
        "movb %%al, 5(%0);\n\t"

        "movl $15, %%eax;\n\t"
        "imull $7, %%eax;\n\t"
        "movb %%al, 6(%0);\n\t"

        "movl $400, %%eax;\n\t"
        "shrl $2, %%eax;\n\t"
        "subl $5, %%eax;\n\t"
        "movb %%al, 7(%0);\n\t"

        "movl $27, %%eax;\n\t"
        "imull $4, %%eax;\n\t"
        "movb %%al, 8(%0);\n\t"

        "movl $6, %%eax;\n\t"
        "shll $3, %%eax;\n\t"
        "movb %%al, 9(%0);\n\t"

        "movl $7, %%eax;\n\t"
        "imull $17, %%eax;\n\t"
        "subl $1, %%eax;\n\t"
        "movb %%al, 10(%0);\n\t"

        "movl $17, %%eax;\n\t"
        "imull $3, %%eax;\n\t"
        "movb %%al, 11(%0);\n\t"

        "movl $20, %%eax;\n\t"
        "imull $5, %%eax;\n\t"
        "subl $5, %%eax;\n\t"
        "movb %%al, 12(%0);\n\t"

        "movl $13, %%eax;\n\t"
        "imull $4, %%eax;\n\t"
        "movb %%al, 13(%0);\n\t"

        "movl $230, %%eax;\n\t"
        "shrl $1, %%eax;\n\t"
        "movb %%al, 14(%0);\n\t"

        "movl $11, %%eax;\n\t"
        "imull $10, %%eax;\n\t"
        "subl $1, %%eax;\n\t"
        "movb %%al, 15(%0);\n\t"

        "movl $250, %%eax;\n\t"
        "shrl $1, %%eax;\n\t"
        "movb %%al, 16(%0);\n\t"

        "movb $0, 17(%0);\n\t"
        :
        : "r"(s)
        : "rax", "rbx", "rcx", "rdx", "memory"
    );

    puts(s);
    return 0;
}
