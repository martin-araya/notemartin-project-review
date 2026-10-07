/* F06y: command_dispatch.c - tabla de handlers y dispatch. */
#include "fxemb/command_dispatch.h"

#include <errno.h>
#include <stddef.h>
#include <string.h>

/* Handlers concretos. Los tests los llaman via dispatch_cmd. */
static int cmd_read(int argc, char** argv) {
    (void)argc; (void)argv;
    return 0;
}

static int cmd_write(int argc, char** argv) {
    (void)argc; (void)argv;
    return 0;
}

static int cmd_reset(int argc, char** argv) {
    (void)argc; (void)argv;
    return 0;
}

static int cmd_status(int argc, char** argv) {
    (void)argc; (void)argv;
    return 0;
}

/* E03: tabla de punteros a funcion. La trampa es que parece una lookup
 * O(1) por nombre pero el dispatch_cmd() itera linealmente. */
const cmd_dispatch_t cmd_table[] = {
    { "READ",   cmd_read,   "Lee un sensor" },
    { "WRITE",  cmd_write,  "Escribe un valor" },
    { "RESET",  cmd_reset,  "Soft reset del firmware" },
    { "STATUS", cmd_status, "Imprime estado del sistema" },
};
const int cmd_table_size = (int)(sizeof(cmd_table) / sizeof(cmd_table[0]));

int dispatch_cmd(const char* name, int argc, char** argv) {
    /* trampa E03: lookup O(n) lineal en lugar de O(1) hash. */
    for (int i = 0; i < cmd_table_size; ++i) {
        if (strcmp(cmd_table[i].cmd_name, name) == 0) {
            return cmd_table[i].handler(argc, argv);
        }
    }
    return -EINVAL;
}
