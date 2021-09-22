#include "dbg.h"

#define REMOVE_DUP

void hexdump(const void *data, int size, char *name, uint64_t start)
{
	unsigned char *p = (unsigned char *)data;
	int n, l, i, s, dashlen;
	uint8_t last_is_dup;

	char line[512] = {0};

	sprintf(line, "\033[36m                   ┌");
	if (name != NULL && strlen(name) > 0)
	{
		s = strlen(name);
		dashlen = (46 - s) / 2;
		for (i = 0; i < dashlen; i++)
		{
			strncat(line, "─", sizeof(line) - strlen(line) - 1);
		}
		strncat(line, "  ", sizeof(line) - strlen(line) - 1);
		strncat(line, "\033[1m", sizeof(line) - strlen(line) - 1);
		strncat(line, name, sizeof(line) - strlen(line) - 1);
		strncat(line, "\033[0m\033[36m", sizeof(line) - strlen(line) - 1);
		strncat(line, "  ", sizeof(line) - strlen(line) - 1);
		for (i = 0; i < (dashlen - (1 - s % 2)); i++)
		{
			strncat(line, "─", sizeof(line) - strlen(line) - 1);
		}
	}
	else
	{
		for (i = 0; i < 49; i++)
		{
			strncat(line, "─", sizeof(line) - strlen(line) - 1);
		}
	}
	strncat(line, "┬", sizeof(line) - strlen(line) - 1);
	for (i = 0; i < 18; i++)
	{
		strncat(line, "─", sizeof(line) - strlen(line) - 1);
	}
	strncat(line, "┐\033[0m\n", sizeof(line) - strlen(line) - 1);
	printf("%s", line);

	last_is_dup = 0;
	for (n = 0; n < size; n += 16)
	{
#ifdef REMOVE_DUP
		if(n!=0 && (n+16)<size) {
			if(!memcmp(&p[n], &p[n-16], 16) && ((n+16)<size && !memcmp(&p[n], &p[n+16], 16))) {
				if(!last_is_dup) {
					sprintf(line, "\033[36m                 * ┆ \033[0m\033[36m");
					for (i = 0; i < 47; i++)
					{
						strncat(line, "⇩", sizeof(line) - strlen(line) - 1);
					}
					strncat(line, " \033[0m\033[36m┆\033[0m\033[36m ", sizeof(line) - strlen(line) - 1);
					for (i = 0; i < 16; i++)
					{
						strncat(line, "⇩", sizeof(line) - strlen(line) - 1);
					}
					strncat(line, "\033[0m\033[36m ┆\033[0m\n", sizeof(line) - strlen(line) - 1);
					printf("%s", line);
				}
				last_is_dup=1;
				continue;
			}else{
				last_is_dup=0;
			}
		}
#endif
		sprintf(line, "\033[36m0x%016lx │ \033[0m\033[1m", (n + start));
		for (l = n; l < n + 16; l++)
		{
			if (l < size)
			{
				sprintf(line, "%s%02x ", line, p[l]);
			}
			else
			{
				strncat(line, "   ", sizeof(line) - strlen(line) - 1);
			}
		}
		strncat(line, "\033[0m\033[36m│\033[0m\033[1m ", sizeof(line) - strlen(line) - 1);
		for (l = n; l < n + 16; l++)
		{
			if (l < size)
			{
				if (isprint(p[l]) == 0)
				{
					strncat(line, ".", sizeof(line) - strlen(line) - 1);
				}
				else
				{
					sprintf(line, "%s%c", line, p[l]);
				}
			}
			else
			{
				strncat(line, " ", sizeof(line) - strlen(line) - 1);
			}
		}
		strncat(line, "\033[0m\033[36m │\033[0m\n", sizeof(line) - strlen(line) - 1);
		printf("%s", line);
	}
	sprintf(line, "\033[36m                   └");
	for (i = 0; i < 49; i++)
	{
		strncat(line, "─", sizeof(line) - strlen(line) - 1);
	}
	strncat(line, "┴", sizeof(line) - strlen(line) - 1);
	for (i = 0; i < 18; i++)
	{
		strncat(line, "─", sizeof(line) - strlen(line) - 1);
	}
	strncat(line, "┘\033[0m\n", sizeof(line) - strlen(line) - 1);
	printf("%s", line);
	fflush(stdout);
}