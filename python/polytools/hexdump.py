# coding: utf-8
import sys
import struct
import string as _string

_PRINTABLE = frozenset(_string.printable) - set('\t\n\r\x0b\x0c')
_HEX_FMT   = {1: '%02x', 2: '%04x', 4: '%08x', 8: '%016x'}


def hexdump(buf, title='', color=6, start=0, remove_dup=True,
            hl_addr=None, hl_val=None, fmt='B'):
    if not buf:
        return
    if isinstance(buf, str):
        buf = buf.encode('latin-1')
    buf = bytes(buf)

    if fmt[0] in '<>!=@':
        endian_pfx, type_char = fmt[0], fmt[1:]
    else:
        endian_pfx, type_char = '=', fmt

    _VALID = {'b', 'B', 'h', 'H', 'i', 'I', 'q', 'Q'}
    if type_char not in _VALID:
        raise ValueError(
            f"invalid fmt {fmt!r}: type must be one of "
            + ', '.join(sorted(_VALID))
            + " (optionally prefixed with < > ! = @)"
        )

    unit   = struct.calcsize('=' + type_char)
    endian = 'little' if endian_pfx == '<' else \
             'big'    if endian_pfx in ('>', '!') else \
             sys.byteorder

    hex_fmt       = _HEX_FMT[unit]
    units_per_row = 16 // unit
    row_bytes     = 16

    hex_col = units_per_row * (unit * 2 + 1)
    box_hex = hex_col + 1
    box_asc = 18

    nbytes      = len(buf)
    addr_digits = max(8, len('%x' % (start + nbytes - 1))) if nbytes else 8
    addr_w      = 2 + addr_digits
    space       = ' ' * (addr_w + 1)

    C   = f'\033[3{color};1m'
    C0  = f'\033[0m\033[3{color}m'
    HL  = f'\033[3{color};41;1m'
    HLV = '\033[31;1m'
    R   = '\033[0m'

    out = []

    if title:
        s      = len(title)
        dlen   = (box_hex - s - 3) // 2
        dlen_r = dlen - (1 - s % 2)
        out.append(f'{space}{C}┌{"─"*dlen}  {title}  {"─"*dlen_r}┬{"─"*box_asc}┐{R}\n')
    else:
        out.append(f'{space}{C}┌{"─"*box_hex}┬{"─"*box_asc}┐{R}\n')

    last_is_dup = False
    mv          = memoryview(buf)

    for i in range(0, nbytes, row_bytes):
        if remove_dup and i != 0 and i + row_bytes < nbytes:
            if (mv[i:i+row_bytes] == mv[i-row_bytes:i] and
                    mv[i:i+row_bytes] == mv[i+row_bytes:i+2*row_bytes]):
                if not last_is_dup:
                    out.append(
                        f'{space[:-2]}{C}* ┆ {C0}'
                        + '⇩' * (box_hex - 2)
                        + f' {C}┆ {C0}'
                        + '⇩' * 16
                        + f' {C}┆{R}\n'
                    )
                last_is_dup = True
                continue
        last_is_dup = False

        parts = []
        for j in range(units_per_row):
            byte_off = i + j * unit
            if byte_off >= nbytes:
                parts.append(' ' * (unit * 2 + 1))
            else:
                chunk = buf[byte_off:byte_off + unit]
                if len(chunk) < unit:
                    chunk += b'\x00' * (unit - len(chunk))
                val = int.from_bytes(chunk, endian)
                h   = hex_fmt % val
                parts.append(f'{HLV}{h}{R} ' if hl_val is not None and val == hl_val else h + ' ')

        asc = []
        for j in range(row_bytes):
            off = i + j
            asc.append((chr(buf[off]) if chr(buf[off]) in _PRINTABLE else '.') if off < nbytes else ' ')

        row_addr  = i + start
        addr_part = (f'{HL}0x{row_addr:0{addr_digits}x}{R}{C} │ {R}' if hl_addr == row_addr
                     else f'{C}0x{row_addr:0{addr_digits}x} │ {R}')

        out.append(f'{addr_part}{"".join(parts)}{C}│ {R}{"".join(asc)} {C}│{R}\n')

    out.append(f'{space}{C}└{"─"*box_hex}┴{"─"*box_asc}┘{R}\n')

    sys.stdout.write(''.join(out))
    sys.stdout.flush()
