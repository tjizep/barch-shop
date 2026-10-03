#!/usr/bin/env python3
"""Write app/commands.json - the RESP console's command list - out of the command
reference that docs/index.html carries as `const CMDS={...}`.

Usage: make_commands.py path/to/barch/docs/index.html
The reference is in the barch repository (github.com/tjizep/barch), so point this at
a checkout of it. Run it again when the reference changes; the page reads whatever
this last wrote, and app/commands.json is checked in, so the shop runs without it.
"""
import html, json, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2:
    sys.exit("usage: make_commands.py path/to/barch/docs/index.html")
src = sys.argv[1]
text = open(src, encoding="utf-8").read()
start = text.index("const CMDS=") + len("const CMDS=")
cmds, _ = json.JSONDecoder().raw_decode(text[start:])

def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

out = []
for name, c in sorted(cmds.items()):
    if c.get("asy"):
        continue                    # KEYS, VALUES, RANGE: a script may not call them
    out.append({
        "name": name,
        "family": plain(c.get("family")),
        "syntax": plain(c.get("syntax")),
        "summary": plain(c.get("summary")),
        "example": c.get("example") or "",
        "dangerous": bool(c.get("dangerous")),
        "write": "write" in (c.get("cats") or []),
    })
dst = os.path.join(here, "app", "commands.json")
with open(dst, "w", encoding="utf-8") as f:
    json.dump(out, f, separators=(",", ":"))
print("wrote %d commands to %s" % (len(out), dst))
