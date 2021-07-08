import re
from json import (
    loads as _loads,
    dump,
    dumps
)


__all__ = (
    "load",
    "loads",
    "dump",
    "dumps"
)


regex = re.compile(
    r"(\".*?\"|\'.*?\')|"
    "(/\*.*?[^\".*?]\*/[^.*?\"]|//[^\r\n]*$)",
    re.MULTILINE | re.DOTALL
)


def load(fp, **kw):
    return loads(fp.read(), **kw)


def loads(s, **kw):
    comment_removed = _remove_comments(s)
    return _loads(comment_removed, **kw)


def _remove_comments(string):
    return regex.sub(
        lambda m: m.group(1) if m.group(2) is None else "",
        string
    ).strip()
