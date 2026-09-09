# Style guide for *Agent Algorithmics*

Adopted 2026-09-09. Every chapter is being brought to this standard.

## Who we are writing for, and in whose voice

The book sits in the *Network Algorithmics* tradition (Varghese): a systems
view, each concept turned into an implementation principle, problem →
mechanism → consequence. That is the **organization**. The **prose register**
is Kleinberg–Tardos (*Algorithm Design*): calm, precise, problem-first,
define-then-argue, "we now show…", worked examples with labelled parts, no
drama. The fifteen-year-old test survives only as a clarity bar — nothing
used before it is defined — not as a tone.

Each section of a definitions chapter ends with an italic *Design
requirement.* sentence: the Varghese principle the definition imposes.

## The voice

**Explain; do not perform.** The reader should finish a section understanding
something they did not understand before, and be able to say *why* it is
true.

**No contrastive phrasing.** This is the most recognisable machine-writing
tic and it is banned: "X is not Y; it is Z", "not merely X but Y", "X, not
Y." as a sentence ending, "It's not about X, it's about Y", one-word
sentences used as a punch ("Architecture decides."). State the positive
claim directly. A plain "rather than" inside a comparison is fine; a
sentence built around a negation for rhetorical effect is not. Check with:

      grep -nE '\b(is|are|was) not\b[^.;]*[;.] (It|That|This|They|The) (is|are)\b'
      grep -nE '\bnot (merely|just|only|simply)\b'
      grep -nE ', not [a-z][^.]*\.$'

Concretely:

1. **Define every term at first use, in the sentence where it appears.**
   "The *context window* — the fixed amount of text a model can read at
   once — fills faster than you expect." Never lean on a word the reader has
   not been given.
2. **Go from the concrete to the abstract, never the reverse.** Start with a
   small example the reader can picture (a ticket-booking assistant, a
   homework helper), show the problem happening, and only then name it and
   generalise.
3. **Connected paragraphs, not fragments.** A paragraph carries a line of
   reasoning: claim, why, consequence. Bullet lists are allowed only when the
   items are genuinely parallel *and* each item is a full explained sentence
   or two. A list of noun phrases is a table of contents, not an explanation.
4. **No aphoristic openers or closers.** Chapters do not begin with a punchy
   one-liner and sections do not end on a mic-drop. If a sentence would work
   as a LinkedIn post, rewrite it as an explanation.
5. **Every number is explained.** When a table shows a figure, the prose
   around it says how the figure was reached and what the reader should take
   from it.
6. **Say what something *is* before saying what it is *not*.** Contrast is
   useful after the positive case is established, not as a substitute for it.
7. **Prefer "because" and "so" to "namely" and "such as".** The book was
   damaged by an automated pass that replaced colons with ", namely",
   ", such as", ", including", or a bare full stop, producing sentences like
   "Strategies include the following." with nothing following. Restore the
   sentence: either use a colon or rewrite so the list is introduced by a
   complete clause.
8. **Fallacies and pitfalls are prose.** The section at the end of each
   chapter is called *Common misunderstandings* and is written as short
   paragraphs — what people believe, why it is tempting, why it is wrong,
   what to do instead. Not `\textbf{Fallacy.}` followed by a fragment.

## Diagrams

Every chapter carries figures. Draw the mechanism, not a decoration:

- a loop, a timeline, a spectrum, a flowchart of decisions, a comparison of
  two runs. TikZ (`\usetikzlibrary{arrows.meta,positioning,shapes.geometric,calc}`
  is loaded in the preamble).
- Every figure has a caption that could stand alone, is referenced from the
  prose (`Figure~\ref{fig:...}`), and is introduced *before* the reader
  reaches it.
- Keep figures to the 6.5in text width; use `\small` text inside nodes.
- **Bold and coloured.** Strokes ≥ 1.1pt, saturated fills, one colour per
  role, using the shared styles in the preamble: `agentbox` (blue),
  `envbox` (orange), `statebox` (purple), `okbox` (green), `warnbox`
  (orange), `badbox` (red), and the matching `bluearr`/`orangearr`/
  `greenarr`/`redarr` arrows. Thin grey line-art is not acceptable.
- **Raster output stays light.** The HTML build renders figures to 160 dpi
  PNG (tens of KB each). Covers are JPEG. Never commit SVG or full-res
  images into the book.

## Mechanics

- `\emph{}` for a term being defined; `\textit{}` for emphasis inside
  running prose; `\textsc{}` for the four gate outcomes.
- Keep the per-chapter `thebibliography` blocks and all existing `\cite`
  keys; every arXiv identifier was verified and the rewrite must not lose
  citations.
- One `\section*{Exercises}` per chapter. One `\section*{Bibliographic
  Notes}`. The order at chapter end is: Summary, Common misunderstandings,
  Exercises, Bibliographic Notes, Bibliography.
- Fragment check before committing a chapter:

      grep -nE ', (namely|such as|including) [A-Z]' main.tex
      grep -nE '(as|include|includes|following|are|is|with|for|via|below|of|from|to)\.$' main.tex
      grep -nE '\\begin\{center\}\.|\}\.\.' main.tex

  The second pattern has legitimate hits ("... and so on." is fine); read
  each one.
