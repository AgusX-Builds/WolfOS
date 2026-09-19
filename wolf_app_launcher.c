#include <unistd.h>

int main(void) {
    char *args[] = {
        "/usr/local/bin/python3.14",
        "/Users/agustin/WolfOS/wolf_launcher.py",
        NULL
    };

    execv(args[0], args);

    return 1;
}
