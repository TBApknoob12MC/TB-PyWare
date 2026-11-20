"""Safe, static word completion for the editor; never evaluates user code."""
import builtins
import keyword
import re

_WORD = re.compile(r'\b[A-Za-z_][A-Za-z_0-9]*\b')


def complete(source, prefix):
    if not prefix or not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', prefix):
        return []
    words = set(keyword.kwlist) | set(dir(builtins)) | set(_WORD.findall(source))
    return sorted(word for word in words if word.startswith(prefix) and word != prefix)
