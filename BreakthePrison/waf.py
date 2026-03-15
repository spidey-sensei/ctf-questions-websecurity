import re

BLOCKED_KEYWORDS = [
    'or', 'union', 'select', 'insert', 'delete', 'update',
    'drop', 'sleep', 'benchmark'
]

BLOCKED_CHARS = [
    '--', '/*', '*/', ';'
]

def waf_check(inp):
    s = inp.lower()

    # Block obvious SQL keywords
    for kw in BLOCKED_KEYWORDS:
        if re.search(rf'\\b{kw}\\b', s):
            return False

    # Block comments & statement chaining
    for ch in BLOCKED_CHARS:
        if ch in s:
            return False

    # Block numbers (forces string logic)
    if any(c.isdigit() for c in s):
        return False

    # Length-based suspicion
    if len(s) > 40:
        return False

    return True