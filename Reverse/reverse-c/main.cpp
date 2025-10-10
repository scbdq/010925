#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <cstddef>

static const char strings_hint[] = "31337 port";

static const unsigned char XOR_KEY = 0xAA;

static unsigned char obf_data[] = {
    254, 239, 228, 216, 231, 255, 222, 255, 249, 253, 194, 229, 240, 155, 255, 211,
    243, 253, 198, 158, 201, 239, 224, 255, 231, 242, 252, 229, 231, 199, 222, 221,
    249, 196, 201, 147, 250, 251, 151, 151
};
static const size_t obf_len = 40;

void decode(unsigned char *data, size_t len, unsigned char key) {
    for (size_t i = 0; i < len; ++i)
        data[i] ^= key;
}

int main() {
    decode(obf_data, obf_len, XOR_KEY);

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) return 1;

    int opt = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    sockaddr_in addr;
    std::memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(31337);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);

    if (bind(sockfd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        close(sockfd);
        return 1;
    }

    if (listen(sockfd, 1) < 0) {
        close(sockfd);
        return 1;
    }

    while (true) {
        int newsock = accept(sockfd, NULL, NULL);
        if (newsock < 0) break;

        ssize_t sent = 0;
        const unsigned char *ptr = obf_data;
        size_t remaining = obf_len;
        while (remaining > 0) {
            ssize_t n = send(newsock, ptr + sent, remaining, 0);
            if (n <= 0) break;
            sent += n;
            remaining -= (size_t)n;
        }

        close(newsock);
        break;
    }

    close(sockfd);
    return 0;
}
