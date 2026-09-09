#!/usr/bin/env python3
"""Replace one chapter's prose in main.tex with a rewritten file.

    python3 splice_chapter.py "Chapter Title" new_chapter.tex

Replaces everything from the ``\\chapter{Chapter Title}`` line up to (not
including) that chapter's ``\\begin{thebibliography}``.  The bibliography
block itself is preserved.  Also runs the contrastive-phrasing and
fragment checks on the new text and prints any hits.
"""
import re
import sys
from pathlib import Path

title, newfile = sys.argv[1], sys.argv[2]
main = Path("main.tex")
src = main.read_text(encoding="utf-8").split("\n")
new = Path(newfile).read_text(encoding="utf-8").rstrip("\n").split("\n")

start = next(i for i, l in enumerate(src) if l.startswith("\\chapter{" + title + "}"))
end = next(i for i, l in enumerate(src) if i > start and l.startswith("\\begin{thebibliography}"))
out = src[:start] + new + [""] + src[end:]
main.write_text("\n".join(out), encoding="utf-8")
print(f"spliced '{title}': replaced lines {start+1}-{end} with {len(new)} lines")

checks = [
    ("contrastive", r"\b(is|are|was|were) not\b[^.;]*[;.] (It|That|This|They|The) (is|are|was)\b"),
    ("not merely", r"\bnot (merely|just|only|simply)\b"),
    (", not Y.", r", not [a-z][^.]*\.$"),
    ("broken colon", r", (namely|such as|including) [A-Z]"),
    ("dangling", r"\b(as|include|includes|following|are|is|with|via|below|from|to)\.$"),
    ("center dot", r"\\begin\{center\}\."),
]
for name, pat in checks:
    hits = [(i + 1, l) for i, l in enumerate(new) if re.search(pat, l)]
    for ln, l in hits[:8]:
        print(f"  [{name}] {ln}: {l[:120]}")
