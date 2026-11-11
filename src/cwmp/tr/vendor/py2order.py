"""Python 3 port of HoneyThing: reproduce the iteration order of Python 2.7 dicts.

The original ran on Python 2.7, where HTTP response headers (tornado) and XML
attributes (xmlwitch) came out in dict hash order. This module lets the Python 3
port emit them in exactly the same order, so that responses stay byte-identical.
"""

_M64 = (1 << 64) - 1


def _py2_str_hash(s):
    """Hash of a byte string in CPython 2.7 (64-bit, no -R randomisation)."""
    if isinstance(s, str):
        s = s.encode('latin-1', 'replace')
    if not s:
        return 0
    x = (s[0] << 7) & _M64
    for c in s:
        x = ((1000003 * x) & _M64) ^ c
    x ^= len(s)
    if x == _M64:  # -1 is reserved for errors
        x = _M64 - 1
    return x


def _py2_slot(table, mask, h):
    i = h & mask
    if table[i] is None:
        return i
    perturb = h
    while True:
        i = ((i << 2) + i + perturb + 1) & _M64
        if table[i & mask] is None:
            return i & mask
        perturb >>= 5


def py2_dict_order(keys):
    """Iteration order of a CPython 2.7 dict whose str keys were inserted in this order."""
    size, table, used = 8, [None] * 8, 0
    for k in keys:
        h = _py2_str_hash(k)
        table[_py2_slot(table, size - 1, h)] = (k, h)
        used += 1
        if used * 3 >= size * 2:
            newsize = 8
            while newsize <= 4 * used:
                newsize <<= 1
            old = [e for e in table if e is not None]
            size, table = newsize, [None] * newsize
            for key, hh in old:
                table[_py2_slot(table, size - 1, hh)] = (key, hh)
    return [e[0] for e in table if e is not None]


def py2_items(d, hops=1):
    """Items of d in Python 2.7 order (hops: number of dict-to-dict copies)."""
    keys = list(d.keys())
    for _ in range(hops):
        keys = py2_dict_order(keys)
    return [(k, d[k]) for k in keys]
