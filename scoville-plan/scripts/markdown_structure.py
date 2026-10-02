"""Mask fenced code while preserving character offsets and line endings."""
from __future__ import annotations

import re


def mask_fenced_code(text: str) -> str:
    """Leave structural prose intact; replace fence lines and contents with spaces."""
    fence_char = ""
    fence_length = 0
    output: list[str] = []
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        if fence_char:
            closing = re.fullmatch(r" {0,3}(" + re.escape(fence_char) + r"{" + str(fence_length) + r",})[ \t]*", body)
            output.append("".join(char if char in "\r\n" else " " for char in line))
            if closing:
                fence_char = ""
            continue
        opening = re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", body)
        if opening and not (opening.group(1)[0] == "`" and "`" in opening.group(2)):
            fence_char = opening.group(1)[0]
            fence_length = len(opening.group(1))
            output.append("".join(char if char in "\r\n" else " " for char in line))
        else:
            output.append(line)
    return "".join(output)
