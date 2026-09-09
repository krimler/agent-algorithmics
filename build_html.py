#!/usr/bin/env python3
"""Build the HTML edition of *Agent Algorithmics* from main.tex.

One HTML page per chapter, plain year-2000 markup, SEO metadata, TikZ
figures and algorithm blocks rendered to lightweight PNG.  Requires pandoc, pdflatex
and pdftoppm (poppler) on PATH.

    python3 build_html.py            # writes ./docs/ (GitHub Pages source)
    BOOK_BASE_URL=https://example.com/book python3 build_html.py
"""
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "main.tex"
OUT = ROOT / "docs"   # served by GitHub Pages from the docs/ folder
FIG = OUT / "figures"
TMP = ROOT / ".buildtmp" / "html"
BASE_URL = os.environ.get("BOOK_BASE_URL", "https://krimler.github.io/agent-algorithmics").rstrip("/")

BOOK_TITLE = "Agent Algorithmics"
SUBTITLE = "Principles for Cost, Reliability, and Safety in Tool-Using AI Systems"
AUTHOR = "Madhava Gaikwad"
YEAR = "2026"

# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def slugify(s):
    s = re.sub(r"\\[a-zA-Z]+\*?(\{[^}]*\})?", "", s)
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s


def balanced(text, start):
    """Return index just past the brace group starting at text[start] == '{'."""
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced braces")


def arg(text, cmd, pos=0):
    """First brace argument of \\cmd found at or after pos."""
    m = re.compile(r"\\" + cmd + r"\*?\s*\{").search(text, pos)
    if not m:
        return None, None
    end = balanced(text, m.end() - 1)
    return text[m.end():end - 1], (m.start(), end)


def tex_to_text(tex):
    """Crude plain text from a LaTeX fragment (for meta descriptions)."""
    t = re.sub(r"\\(emph|textit|textbf|texttt|textsc)\{([^}]*)\}", r"\2", tex)
    t = re.sub(r"~?\\(ref|cite)\{[^}]*\}", "", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", "", t)
    t = t.replace("``", '"').replace("''", '"').replace("---", "—").replace("--", "–")
    t = re.sub(r"[{}$]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout[-3000:] + r.stderr[-3000:])
        raise SystemExit(f"command failed: {' '.join(str(c) for c in cmd)}")
    return r.stdout


# --------------------------------------------------------------------------
# Read source, split preamble/body, collect figure styles
# --------------------------------------------------------------------------

tex = SRC.read_text(encoding="utf-8")
pre, body = tex.split("\\begin{document}", 1)
body = body.split("\\end{document}", 1)[0]

tikzlibs = "\n".join(re.findall(r"\\usetikzlibrary\{[^}]*\}", pre) +
                     re.findall(r"\\definecolor\{[^}]*\}\{[^}]*\}\{[^}]*\}", pre))
_, span = arg(pre, "tikzset")
tikzset = pre[span[0]:span[1]] if span else ""

FIG_PREAMBLE = r"""
\usepackage{amsmath,amssymb}
\usepackage[T1]{fontenc}
\usepackage{XCharter}
\usepackage[charter,vvarbb,scaled=1.03]{newtxmath}
\usepackage[scaled=0.96]{inter}
\usepackage[scaled=0.92]{zi4}
\usepackage{tikz}
""" + tikzlibs + "\n" + tikzset + "\n"

# --------------------------------------------------------------------------
# Split body into chapters
# --------------------------------------------------------------------------

heads = list(re.finditer(r"^\\(part|chapter)(\*?)\{([^}]*)\}", body, re.M))
chapters = []
current_part = None
part_no = 0
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
for i, m in enumerate(heads):
    kind, star, title = m.group(1), m.group(2), m.group(3)
    end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
    if kind == "part":
        part_no += 1
        current_part = f"Part {ROMAN[part_no - 1]}: {title}"
        continue
    if title.strip() == "Index":
        continue
    chunk = body[m.end():end]
    label = re.match(r"\s*\\label\{([^}]*)\}", chunk)
    chapters.append({
        "title": title,
        "starred": star == "*",
        "part": current_part,
        "label": label.group(1) if label else None,
        "tex": chunk,
    })

num = 0
for ch in chapters:
    if ch["starred"]:
        ch["number"] = None
        ch["file"] = slugify(ch["title"]) + ".html"
    else:
        num += 1
        ch["number"] = num
        ch["file"] = f"{num:02d}-{slugify(ch['title'])}.html"

# --------------------------------------------------------------------------
# Numbering pass: sections, figures, algorithms; label map
# --------------------------------------------------------------------------

labels = {}  # label -> (file, display)
for ch in chapters:
    t = ch["tex"]
    if ch["label"]:
        labels[ch["label"]] = (ch["file"], str(ch["number"]))
    sec = sub = 0
    n = ch["number"]
    fig = alg = 0
    out = []
    pos = 0
    pat = re.compile(
        r"\\(section|subsection|subsubsection)(\*?)\{|\\begin\{(figure|algorithm)\}", re.M)
    for m in pat.finditer(t):
        if m.start() < pos:
            continue
        if m.group(1):
            kind, star = m.group(1), m.group(2)
            end = balanced(t, m.end() - 1)
            title = t[m.end():end - 1]
            if star or n is None:
                disp = ""
            elif kind == "section":
                sec += 1; sub = 0
                disp = f"{n}.{sec} "
            elif kind == "subsection":
                sub += 1
                disp = f"{n}.{sec}.{sub} "
            else:
                disp = ""
            lab = re.match(r"\s*\\label\{([^}]*)\}", t[end:])
            if lab:
                labels[lab.group(1)] = (ch["file"], disp.strip())
            out.append(t[pos:m.start()])
            out.append(f"\\{kind}{star}{{{disp}{title}}}")
            pos = end
        else:
            env = m.group(3)
            close = t.find(f"\\end{{{env}}}", m.end())
            block = t[m.start():close]
            lab = re.search(r"\\label\{([^}]*)\}", block)
            if env == "figure":
                fig += 1
                disp = f"{n}.{fig}"
            else:
                alg += 1
                disp = f"{n}.{alg}"
            if lab:
                labels[lab.group(1)] = (ch["file"], disp)
    out.append(t[pos:])
    ch["tex"] = "".join(out)

# --------------------------------------------------------------------------
# Render TikZ figures and algorithms to SVG
# --------------------------------------------------------------------------

FIG.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)


def render_png(name, doc):
    h = hashlib.sha1(doc.encode()).hexdigest()[:10]
    png = FIG / f"{name}-{h}.png"
    if png.exists():
        return png.name
    for old in FIG.glob(f"{name}-*.png"):
        old.unlink()
    texf = TMP / f"{name}.tex"
    texf.write_text(doc, encoding="utf-8")
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
         "-output-directory", str(TMP), str(texf)])
    # 300 dpi for sharpness on high-density screens, then palette-quantised
    # (figures are flat colour) so each file stays in the tens of kilobytes.
    run(["pdftoppm", "-png", "-r", "300", "-singlefile", str(TMP / f"{name}.pdf"),
         str(png.with_suffix(""))])
    venv_py = ROOT / ".venv" / "bin" / "python"
    if venv_py.exists():
        run([str(venv_py), "-c",
             "import sys; from PIL import Image; im=Image.open(sys.argv[1]).convert('RGB');"
             "im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)"
             ".save(sys.argv[1], optimize=True)", str(png)])
    return png.name


def figure_doc(tikz):
    return ("\\documentclass[tikz,border=4pt]{standalone}\n" + FIG_PREAMBLE +
            "\\begin{document}\n" + tikz + "\n\\end{document}\n")


def algorithm_doc(caption, algorithmic, number):
    return ("\\documentclass[varwidth=6.3in,border=6pt]{standalone}\n" + FIG_PREAMBLE +
            "\\usepackage{algpseudocode}\n"
            "\\begin{document}\\small\n"
            f"\\noindent\\textbf{{Algorithm {number}}} {caption}\\par\\medskip\n"
            "\\hrule\\smallskip\n" + algorithmic + "\n\\smallskip\\hrule\n"
            "\\end{document}\n")


def replace_figures(ch):
    t = ch["tex"]
    stem = ch["file"].rsplit(".", 1)[0]
    fig_no = alg_no = 0
    out = []
    pos = 0
    for m in re.finditer(r"\\begin\{(figure|algorithm)\}", t):
        if m.start() < pos:
            continue
        env = m.group(1)
        close = t.find(f"\\end{{{env}}}", m.end()) + len(f"\\end{{{env}}}")
        block = t[m.start():close]
        caption, _ = arg(block, "caption")
        caption = caption or ""
        lab = re.search(r"\\label\{([^}]*)\}", block)
        labtex = f"\\label{{{lab.group(1)}}}" if lab else ""
        if env == "figure":
            fig_no += 1
            tm = re.search(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", block, re.S)
            if not tm:
                continue
            svg = render_png(f"{stem}-fig{fig_no}", figure_doc(tm.group(0)))
            rep = (f"\\begin{{figure}}\\centering\\includegraphics{{figures/{svg}}}"
                   f"\\caption{{\\textbf{{Figure {ch['number']}.{fig_no}.}} {caption}}}{labtex}\\end{{figure}}")
        else:
            alg_no += 1
            am = re.search(r"\\begin\{algorithmic\}.*?\\end\{algorithmic\}", block, re.S)
            svg = render_png(f"{stem}-alg{alg_no}",
                             algorithm_doc(caption, am.group(0), f"{ch['number']}.{alg_no}"))
            rep = (f"\\begin{{figure}}\\centering\\includegraphics{{figures/{svg}}}"
                   f"{labtex}\\end{{figure}}")
        out.append(t[pos:m.start()])
        out.append(rep)
        pos = close
    out.append(t[pos:])
    ch["tex"] = "".join(out)


# --------------------------------------------------------------------------
# Per-chapter LaTeX preprocessing for pandoc
# --------------------------------------------------------------------------

def preprocess(ch):
    t = ch["tex"]

    # bibliography: number items, give them anchors
    bib = {}
    def bibrepl(m):
        inner = m.group(1)
        items = re.split(r"\\bibitem\{([^}]*)\}", inner)
        parts = []
        for k in range(1, len(items), 2):
            key, txt = items[k], items[k + 1]
            n = len(bib) + 1
            bib[key] = n
            txt = txt.replace("\\newblock", " ")
            parts.append(f"\\item \\hypertarget{{ref-{key}}}{{}}{txt.strip()}")
        return "\\begin{enumerate}\n" + "\n".join(parts) + "\n\\end{enumerate}\n"
    t = re.sub(r"\\begin\{thebibliography\}\{[^}]*\}(.*?)\\end\{thebibliography\}",
               bibrepl, t, flags=re.S)
    ch["bib"] = bib

    # citations -> [n] links
    def citerepl(m):
        keys = [k.strip() for k in m.group(1).split(",")]
        links = []
        for k in keys:
            if k in bib:
                links.append(f"\\href{{#ref-{k}}}{{{bib[k]}}}")
            else:
                sys.stderr.write(f"warning: {ch['file']}: cite {k} not in chapter bibliography\n")
                links.append(k)
        return "[" + ", ".join(links) + "]"
    t = re.sub(r"\\cite\{([^}]*)\}", citerepl, t)

    # cross references
    def refrepl(m):
        key = m.group(1)
        if key in labels:
            f, disp = labels[key]
            target = ("" if f == ch["file"] else f) + "#" + key
            return f"\\href{{{target}}}{{{disp or '?'}}}"
        sys.stderr.write(f"warning: {ch['file']}: unresolved ref {key}\n")
        return "??"
    t = re.sub(r"\\ref\{([^}]*)\}", refrepl, t)

    # size groups around verbatim blocks
    t = re.sub(r"\{\\(?:footnotesize|scriptsize|small)\s*(?:\{\\(?:footnotesize|scriptsize|small)\s*)?"
               r"(\\begin\{verbatim\}.*?\\end\{verbatim\})\s*\}\}?", r"\1", t, flags=re.S)
    t = t.replace("\\checkmark", "✓")
    t = re.sub(r"\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}", "", t)
    t = re.sub(r"\\vspace\{[^}]*\}", "", t)
    t = re.sub(r"\\(problem|model|mechanism|consequence|evaluation)\b(?![a-zA-Z])",
               lambda m: f"\\paragraph{{{m.group(1).capitalize()}.}}", t)
    return t


# --------------------------------------------------------------------------
# HTML template
# --------------------------------------------------------------------------

CSS = """\
body { font-family: Georgia, "Times New Roman", serif; font-size: 17px; line-height: 1.5;
       color: #111; background: #fff; margin: 0; padding: 0 1em; }
#page { max-width: 44em; margin: 0 auto; }
#top, #bottom { font-family: Verdana, Arial, sans-serif; font-size: 13px; color: #444;
       border-bottom: 1px solid #999; padding: 0.6em 0; }
#bottom { border-bottom: none; border-top: 1px solid #999; margin-top: 3em; }
#top a, #bottom a { color: #00e; }
#top .book { font-weight: bold; }
h1 { font-size: 1.9em; margin: 1.2em 0 0.3em; line-height: 1.2; }
h1 .part { display: block; font-size: 0.55em; font-weight: normal; color: #555;
       letter-spacing: 0.04em; text-transform: uppercase; }
h2 { font-size: 1.35em; margin-top: 2em; border-bottom: 1px solid #ccc; padding-bottom: 0.15em; }
h3 { font-size: 1.1em; margin-top: 1.6em; }
h4, h5 { font-size: 1em; margin: 1.2em 0 0.4em; }
h5 { font-style: italic; font-weight: normal; }
a { color: #00e; }  a:visited { color: #551a8b; }
p { margin: 0 0 1em; text-align: left; }
figure { margin: 1.5em 0; text-align: center; }
figure img { width: 88%; max-width: 100%; height: auto; }
figcaption { font-size: 0.9em; color: #333; text-align: left; margin-top: 0.6em; }
table { border-collapse: collapse; margin: 1.2em auto; font-size: 0.95em; }
th, td { padding: 0.25em 0.8em; text-align: left; vertical-align: top; }
thead th { border-bottom: 1px solid #333; }
tbody { border-bottom: 1px solid #333; }
pre { background: #f4f4f4; border: 1px solid #ddd; padding: 0.7em 1em; overflow-x: auto;
      font-size: 0.85em; line-height: 1.35; }
code { font-family: "Courier New", Courier, monospace; }
blockquote { margin: 1em 2em; }
ol.toc, ul.toc { list-style: none; padding-left: 0; }
ul.toc li { margin: 0.3em 0; }
ul.toc li.part { margin-top: 1.4em; font-family: Verdana, Arial, sans-serif; font-size: 0.85em;
      text-transform: uppercase; letter-spacing: 0.05em; color: #555; }
.enumerate-bib { font-size: 0.7em; }
.enumerate-bib li { margin-bottom: 0.35em; line-height: 1.35; }
hr { border: 0; border-top: 1px solid #999; }
.smallcaps { font-variant: small-caps; }
"""

MATHJAX = ('<script id="MathJax-script" async '
           'src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>')


def page(title, desc, body_html, prev, nxt, canonical, extra_head="", jsonld=None):
    nav = []
    if prev:
        nav.append(f'<a href="{prev[0]}" rel="prev">&laquo; {html.escape(prev[1])}</a>')
    nav.append('<a href="index.html">Contents</a>')
    if nxt:
        nav.append(f'<a href="{nxt[0]}" rel="next">{html.escape(nxt[1])} &raquo;</a>')
    navs = " &nbsp;|&nbsp; ".join(nav)
    canon = f'<link rel="canonical" href="{canonical}">' if canonical else ""
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="{AUTHOR}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="book">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
{('<meta property="og:url" content="' + canonical + '">') if canonical else ''}
{canon}
<link rel="stylesheet" href="style.css">
{ld}
{extra_head}
</head>
<body>
<div id="page">
<div id="top"><span class="book"><a href="index.html">{BOOK_TITLE}</a></span> &mdash; {html.escape(SUBTITLE)}<br>{navs}</div>
{body_html}
<div id="bottom">{navs}<br>&copy; {YEAR} {AUTHOR}. Also available as a <a href="agent-algorithmics.pdf">PDF</a>.</div>
</div>
{MATHJAX}
</body>
</html>
"""


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

if OUT.exists():
    for f in OUT.glob("*.html"):
        f.unlink()
OUT.mkdir(exist_ok=True)
(OUT / "style.css").write_text(CSS, encoding="utf-8")

for ch in chapters:
    replace_figures(ch)

for i, ch in enumerate(chapters):
    t = preprocess(ch)
    r = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "html5", "--mathjax", "--wrap=none",
         "--top-level-division=chapter"],
        input=t, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit(f"pandoc failed on {ch['file']}")
    inner = r.stdout
    # pandoc emits sections as h1 (the \chapter line was stripped); shift down one level
    for lvl in (5, 4, 3, 2, 1):
        inner = re.sub(rf"<(/?)h{lvl}\b", rf"<\g<1>h{lvl + 1}", inner)
    # drop the empty paragraph holding the chapter label (the h1 carries the id)
    inner = re.sub(r'<p><span id="[^"]*" data-label="[^"]*"></span></p>\s*', "", inner, count=1)
    # bibliography enumerate gets a class for styling
    inner = re.sub(r'<ol[^>]*>(\s*<li><span id="ref-)', r'<ol class="enumerate-bib">\1', inner, count=1)

    heading = html.escape(tex_to_text(ch["title"]))
    if ch["number"]:
        h1 = f'<h1><span class="part">{html.escape(ch["part"] or "")}</span>Chapter {ch["number"]}. {heading}</h1>'
        title = f"Chapter {ch['number']}: {tex_to_text(ch['title'])} — {BOOK_TITLE}"
    else:
        h1 = f"<h1>{heading}</h1>"
        title = f"{tex_to_text(ch['title'])} — {BOOK_TITLE}"
    if ch["label"]:
        h1 = h1.replace("<h1>", f'<h1 id="{ch["label"]}">', 1)

    desc = SUBTITLE
    for pm in re.finditer(r"<p>(.*?)</p>", inner, re.S):
        cand = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", pm.group(1)))).strip()
        if len(cand) > 40:
            desc = cand
            break
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0] + "…"

    prev = (chapters[i - 1]["file"], tex_to_text(chapters[i - 1]["title"])) if i > 0 else None
    nxt = (chapters[i + 1]["file"], tex_to_text(chapters[i + 1]["title"])) if i + 1 < len(chapters) else None
    canonical = f"{BASE_URL}/{ch['file']}" if BASE_URL else ""
    jsonld = {
        "@context": "https://schema.org", "@type": "Chapter",
        "name": tex_to_text(ch["title"]), "author": {"@type": "Person", "name": AUTHOR},
        "isPartOf": {"@type": "Book", "name": BOOK_TITLE, "author": {"@type": "Person", "name": AUTHOR}},
        "position": ch["number"] or 0,
    }
    if canonical:
        jsonld["url"] = canonical
    (OUT / ch["file"]).write_text(page(title, desc, h1 + inner, prev, nxt, canonical, jsonld=jsonld),
                                  encoding="utf-8")

# index / contents page
items = []
last_part = None
for ch in chapters:
    if ch["part"] and ch["part"] != last_part:
        items.append(f'<li class="part">{html.escape(ch["part"])}</li>')
        last_part = ch["part"]
    label = f"{ch['number']}. " if ch["number"] else ""
    items.append(f'<li><a href="{ch["file"]}">{label}{html.escape(tex_to_text(ch["title"]))}</a></li>')
toc = f"""<h1>{BOOK_TITLE}<span class="part" style="text-transform:none;letter-spacing:0">{html.escape(SUBTITLE)}</span></h1>
<p><i>{AUTHOR}</i></p>
<p>A textbook on building agents that stay within budget, take back what they
can, refuse what they must, and leave a trace you can audit. Language models
appear as components; the subject is the control structure around them.
Also available as a single <a href="agent-algorithmics.pdf">PDF</a>.</p>
<h2>Contents</h2>
<ul class="toc">
{chr(10).join(items)}
</ul>
"""
index_ld = {"@context": "https://schema.org", "@type": "Book", "name": BOOK_TITLE,
            "alternativeHeadline": SUBTITLE, "author": {"@type": "Person", "name": AUTHOR},
            "inLanguage": "en", "datePublished": YEAR}
if BASE_URL:
    index_ld["url"] = BASE_URL + "/"
(OUT / "index.html").write_text(
    page(f"{BOOK_TITLE} — {SUBTITLE}", f"{BOOK_TITLE}: {SUBTITLE}. A textbook by {AUTHOR}.",
         toc, None, (chapters[0]["file"], tex_to_text(chapters[0]["title"])),
         BASE_URL + "/" if BASE_URL else "", jsonld=index_ld),
    encoding="utf-8")

# sitemap, robots, PDF copy
urls = [BASE_URL + "/"] + [f"{BASE_URL}/{c['file']}" for c in chapters] if BASE_URL else []
if urls:
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{html.escape(u)}</loc></url>\n" for u in urls) + "</urlset>\n",
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
else:
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n")
pdf = ROOT / "main.pdf"
if pdf.exists():
    shutil.copy(pdf, OUT / "agent-algorithmics.pdf")

print(f"wrote {len(chapters)} chapter pages to {OUT}/")
