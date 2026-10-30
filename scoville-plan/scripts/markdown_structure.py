"""Mask fenced code while preserving character offsets and line endings."""
from __future__ import annotations

import re


FRONTMATTER_ENTRY_RE = re.compile(r"([a-z_]+): (\S.*)\Z")
STEP_LINE_RE = re.compile(r"([1-9][0-9]*)\. (.+)\Z")


class PlanSectionsError(ValueError):
    def __init__(self, message: str, line: int, code: str = 'PLAN_SECTION_BOUNDARY_INVALID'):
        super().__init__(message)
        self.line = line
        self.code = code


def plan_sections(text: str) -> dict[str, tuple[int, int]]:
    """Return exact section spans; whitespace is not a structural boundary."""
    masked = mask_fenced_code(text)
    headings = list(re.finditer(r'^(#{1,6}) ([^\n]+)$', masked, re.MULTILINE))
    def fail(message, offset=0, code='PLAN_SECTION_BOUNDARY_INVALID'):
        raise PlanSectionsError(message, text.count('\n', 0, offset) + 1, code)
    titles = [h for h in headings if h[1] == '#']
    if len(titles) != 1 or not titles[0][2].strip() or masked[:titles[0].start()].strip():
        fail('Use one H1 title before the Plan sections; preserve authored content.')
    roots = [h for h in headings if h[1] == '##']
    if [h[2] for h in roots] != ['Goal', 'Non-goals', 'Work items']:
        fail('Use Goal, Non-goals and Work items exactly once in that order.', roots[0].start() if roots else titles[0].end())
    if text[titles[0].end():roots[0].start()].strip():
        fail('Move text between the title and Goal into its owning section.', titles[0].end())
    spans = {}
    for index, heading in enumerate(roots):
        end = roots[index + 1].start() if index + 1 < len(roots) else len(text)
        if heading[2] != 'Work items' and not text[heading.end():end].strip():
            fail('Restore the known content of the empty section; do not invent it.', heading.start())
        spans[heading[2]] = (heading.start(), end)
    work_start = roots[-1].end()
    work_headings = [h for h in headings if h.start() >= work_start]
    if not work_headings:
        fail('Restore at least one authored Work Item; do not invent project scope.', work_start, 'WORK_ITEM_MISSING')
    if text[work_start:work_headings[0].start()].strip():
        fail('Work items must begin with a canonical ### W-NNN block; move unowned text into its item.', work_start, 'WORK_BOUNDARY_INVALID')
    for heading in work_headings:
        if heading[1] != '###' or not re.fullmatch(r'W-[0-9]{3} .+', heading[2]):
            fail('Use canonical ### W-NNN item headings; place literal examples in code fences.', heading.start(), 'WORK_BOUNDARY_INVALID')
    return spans


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
