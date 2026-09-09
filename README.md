# Agent Algorithmics

**Principles for Cost, Reliability, and Safety in Tool-Using AI Systems**

Madhava Gaikwad

<p align="center">
  <a href="https://krimler.github.io/agent-algorithmics/"><img src="docs/cover-front.jpg" alt="Front cover of Agent Algorithmics" width="360"></a>
</p>

Read the book online at **[krimler.github.io/agent-algorithmics](https://krimler.github.io/agent-algorithmics/)**, one page per chapter, or download the **[PDF](docs/agent-algorithmics.pdf)** (304 pages).

## What the book is about

An agent is a program that keeps state across interactions, chooses among actions, spends real resources, and changes systems that other people depend on. Some of what it does cannot be undone. This book treats such programs as algorithmic objects and develops the control structure they need: budgets that live in the state rather than in a configuration file, gates that decide whether an action may commit, speculation that can be discarded completely, memory whose write and delete paths are tested, capabilities that bound what a tool call may reach, and traces from which cost, safety, and reliability can be read after the fact.

Language models appear throughout as components, in the way a database or a network appears in a systems book: useful, unreliable in characterized ways, and never the whole system. The book does not contain prompt engineering advice, a tour of frameworks, or a recipe for training models. When a cost problem, a control problem, or an alignment problem comes up, it is treated as a systems problem, because that is where the fix lives.

The title follows Varghese's *Network Algorithmics*. Each concept is stated as an implementation principle, and each chapter works from a concrete problem to the mechanism that solves it and the consequence for the design. The prose aims for the register of an algorithms textbook: definitions first, then the argument, then the worked example.

## Who it is for

Engineers and researchers who build, deploy, and operate agents in systems that other people rely on. Comfort with algorithms, systems design, and probability is assumed. Background in distributed systems, control theory, or reinforcement learning helps in places and is required nowhere; every term is defined where it first appears, and Chapter 2 supplies the mathematics the later chapters use.

## Contents

**Part I: Foundations**

1. Terms and Operational Definitions
2. Mathematical Foundations
3. A Short History of Agents, Control, and Commitment
4. Formal Semantics, Types, and Contracts
5. Cost Models and Critical Paths
6. Budget-Aware Policies and Horizon Estimation

**Part II: Control and Commitment**

7. Action Selection Under Budgets
8. Speculation, Parallelism, and Commit Protocols
9. Risk-Aware Gates: Verification, Abstention, Refusal
10. Memory, State, and Forgetting
11. Retrieval and Evidence Management
12. Capability Boundaries and Secure Tool Use
13. Alignment, Policies, and Constraint Enforcement

**Part III: Observability and Evaluation**

14. Trace Semantics and Agent Telemetry
15. Evaluation: Stability, Cost, and Behavioral Fidelity

**Part IV: Synthesis**

16. Case Studies and Design Patterns

Every chapter closes with a summary, a section on common misunderstandings, exercises meant to be worked rather than admired, and bibliographic notes. The book cites work published through mid-2026, and in several places that work corrected the earlier account rather than adding to it: rollback turns out to be leakier than the first edition claimed, benchmark scores turn out to measure the harness as much as the model, and context compaction turns out to delete safety constraints quietly. Where the field proved the first edition wrong, the text says so.

## Repository layout

| Path | Contents |
|---|---|
| `main.tex` | The complete book source, one file, with a bibliography per chapter |
| `docs/` | The HTML edition served by GitHub Pages, plus the PDF and the figures |
| `covers/` | Front and back cover images, generated from fractals |
| `build_html.py` | Builds `docs/` from `main.tex`: one page per chapter, figures rendered to PNG |
| `make_covers.py` | Renders the cover artwork (a Mandelbrot zoom for the front, a Julia set for the back) |
| `splice_chapter.py` | Replaces one chapter's prose in `main.tex` and runs the style checks |
| `STYLE.md` | The writing and figure conventions the book follows |

## Building

The PDF needs a TeX Live installation with the XCharter, Inter, and Inconsolata fonts.

```
pdflatex main.tex
pdflatex main.tex
```

The HTML edition needs pandoc, pdflatex, and poppler's `pdftoppm`.

```
python3 build_html.py
```

The covers are optional to rebuild; the committed images are used as they are. To regenerate them, create a virtual environment with `numpy` and `pillow` and run `python make_covers.py`. The preamble of `main.tex` has a `\coversfalse` switch for building without covers.

## Figures

The book has 49 figures, all drawn in TikZ from the source, in a shared set of styles: one color per role, heavy strokes, saturated fills. The HTML build renders each to a 300 dpi PNG and reduces it to a 256-color palette, so a figure costs tens of kilobytes rather than hundreds. The conventions are in `STYLE.md`.

## Citing

Madhava Gaikwad. *Agent Algorithmics: Principles for Cost, Reliability, and Safety in Tool-Using AI Systems.* 2026. https://krimler.github.io/agent-algorithmics/
