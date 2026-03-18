#include "dbg.h"

#include <inttypes.h>

#define REMOVE_DUP

#define CYAN    "\033[36m"
#define BOLD    "\033[1m"
#define RESET   "\033[0m"

#define BOX_H   "─"
#define BOX_V   "│"
#define BOX_TL  "┌"
#define BOX_TR  "┐"
#define BOX_BL  "└"
#define BOX_BR  "┘"
#define BOX_TM  "┬"
#define BOX_BM  "┴"
#define BOX_DUP "⇩"

static int bcat(char *buf, int size, int off, const char *s)
{
    while (*s && off < size - 1)
        buf[off++] = *s++;
    buf[off] = '\0';
    return off;
}

static int bcatn(char *buf, int size, int off, const char *s, int n)
{
    for (int i = 0; i < n; i++)
        off = bcat(buf, size, off, s);
    return off;
}

void hexdump(const void *data, int size, const char *name, uint64_t start)
{
    const unsigned char *p = (const unsigned char *)data;
    char line[512];
    int  off;
    int  last_is_dup = 0;

    // Header
    off = bcat(line, sizeof(line), 0, CYAN "                   " BOX_TL);
    if (name && *name) {
        int s       = (int)strlen(name);
        int dashlen = (46 - s) / 2;
        off = bcatn(line, sizeof(line), off, BOX_H, dashlen);
        off = bcat (line, sizeof(line), off, "  " BOLD);
        off = bcat (line, sizeof(line), off, name);
        off = bcat (line, sizeof(line), off, RESET CYAN "  ");
        off = bcatn(line, sizeof(line), off, BOX_H, dashlen - (1 - s % 2));
    } else {
        off = bcatn(line, sizeof(line), off, BOX_H, 49);
    }
    off = bcat (line, sizeof(line), off, BOX_TM);
    off = bcatn(line, sizeof(line), off, BOX_H, 18);
    off = bcat (line, sizeof(line), off, BOX_TR RESET "\n");
    fwrite(line, 1, (size_t)off, stdout);

    // Raws
    for (int n = 0; n < size; n += 16) {

#ifdef REMOVE_DUP
        if (n != 0 && (n + 16) < size
            && !memcmp(&p[n], &p[n - 16], 16)
            && !memcmp(&p[n], &p[n + 16], 16))
        {
            if (!last_is_dup) {
                off = bcat (line, sizeof(line), 0,  CYAN "                 * " BOX_V " " RESET CYAN);
                off = bcatn(line, sizeof(line), off, BOX_DUP, 47);
                off = bcat (line, sizeof(line), off, " " RESET CYAN BOX_V RESET CYAN " ");
                off = bcatn(line, sizeof(line), off, BOX_DUP, 16);
                off = bcat (line, sizeof(line), off, RESET CYAN " " BOX_V RESET "\n");
                fwrite(line, 1, (size_t)off, stdout);
            }
            last_is_dup = 1;
            continue;
        }
        last_is_dup = 0;
#endif

        off = snprintf(line, sizeof(line),
                       CYAN "0x%016" PRIx64 " " BOX_V " " RESET BOLD,
                       (uint64_t)n + start);
        if (off < 0) off = 0;

        for (int l = n; l < n + 16; l++) {
            if (l < size) {
                int r = snprintf(line + off, sizeof(line) - (size_t)off, "%02x ", p[l]);
                if (r > 0) off += r;
            } else {
                off = bcat(line, sizeof(line), off, "   ");
            }
        }

        off = bcat(line, sizeof(line), off, RESET CYAN BOX_V RESET BOLD " ");

        for (int l = n; l < n + 16; l++) {
            char c = (l < size) ? (isprint((unsigned char)p[l]) ? (char)p[l] : '.') : ' ';
            if (off < (int)sizeof(line) - 1)
                line[off++] = c;
        }
        line[off] = '\0';

        off = bcat(line, sizeof(line), off, RESET CYAN " " BOX_V RESET "\n");
        fwrite(line, 1, (size_t)off, stdout);
    }

    // footer
    off = bcat (line, sizeof(line), 0,   CYAN "                   " BOX_BL);
    off = bcatn(line, sizeof(line), off, BOX_H, 49);
    off = bcat (line, sizeof(line), off, BOX_BM);
    off = bcatn(line, sizeof(line), off, BOX_H, 18);
    off = bcat (line, sizeof(line), off, BOX_BR RESET "\n");
    fwrite(line, 1, (size_t)off, stdout);

    fflush(stdout);
}
