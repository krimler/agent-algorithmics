# arXiv Study — September 2025 to September 2026

**Scope of the sweep.** 22 topic queries keyed to the book's own chapters, run against the arXiv API
with `submittedDate:[2025-09-01 TO 2026-09-04]`. After deduplication: **1,802 unique papers**
(375 from late 2025, 1,427 from 2026). Of those, **112 were selected for inclusion**; 100 of them are cited in the rewritten manuscript,
and 42 carry an accepted-venue note (ICML/ICLR/ACL/EMNLP/NeurIPS/OSDI/MLSys/KDD/TMLR and similar).

The current manuscript's newest citations are from 2025 and it has no 2026 references at all, which is
the staleness the review flagged.

---

## What changed in the field this year

Five shifts matter enough to change the book's argument, not just its footnotes.

**1. Failure attribution became its own research area.** A year ago, "why did the agent fail?" was a
debugging anecdote. There is now a benchmark (`Seeing the Whole Elephant`, ACL 2026), a dozen competing
methods, and a measured finding that the step where an error *surfaces* is usually not the step that
*caused* it. Chapter 13 currently treats causality and attribution in a short section; it now deserves
a full treatment with real methods and real numbers.

**2. The harness turned out to be a confound.** Several independent groups showed that a benchmark score
reflects a *model-harness-environment* triple, not a model. `Model or Harness?` and `Measuring
Harness-Induced Belief Divergence` both show the same failure changing identity depending on the scaffold.
Chapter 14 argues for stability and behavioral fidelity but does not warn that the harness itself is an
uncontrolled variable. That is now a documented reproducibility problem.

**3. Rollback stopped being clean.** The book treats abort as cheap and complete. `Aborted but Not
Forgotten` shows that clearing a branch from the transcript does not clear it from the serving session's
KV state, so the model keeps attending to work that was supposedly undone; `Safe to Resume?` shows
checkpoint/rollback is itself an attack surface. Meanwhile `DeltaBox` and `Crab` made sandbox
checkpoint/restore fast enough (milliseconds) that speculation is affordable in practice. Chapter 7's
central claim survives, but its cost model and its abort assumption both need correcting.

**4. Routing moved inside the trajectory.** The book models routing as a per-query decision. Three 2026
papers do it per *step*, mid-reasoning, and `UCCI` shows deployed routers mostly use uncalibrated
confidence, which is exactly the calibration failure Chapter 8 warns about, appearing in Chapter 6's
machinery. These two chapters should now reference each other.

**5. Context compaction was shown to erase safety constraints.** `Governance Decay` demonstrates that
routine context compaction silently drops policy and safety instructions over a long horizon. This
connects Chapter 9 (memory/forgetting) to Chapter 12 (constraint enforcement) through a concrete
mechanism, and it is the single most useful new result for the book's thesis that control must be
explicit rather than emergent.

---

## Included, by chapter

### Ch4 Cost Models — 8 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| Token Economics for LLM Agents: A Dual-View Study from Computing and E | 2026-05-09 | `2605.09104v1` | Token economics survey: tokens as the unit of account for agent cost |
| Notation Matters: A Benchmark Study of Token-Optimized Formats in Agen | 2026-05-28 | `2605.29676v2` | JSON vs token-optimized tool-call formats: measurable token overhead |
| Towards Efficient Large Language Model Serving: A Survey on System-Awa | 2026-07-09 | `2607.08057v1` | System-aware KV cache optimization survey (ACL 2026) |
| TriAxialKV: Toward Extreme Low-Precision KV-Cache Quantization for Age | 2026-05-16 | `2605.17170v1` | KV quantization specifically for agentic (long-context, multi-turn) workloads |
| ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM W | 2026-08-26 | `2608.25992v2` | Progress-guided orchestration under an explicit quality-cost budget |
| SC-MAS: Constructing Cost-Efficient Multi-Agent Systems with Edge-Leve | 2026-01-14 | `2601.09434v1` | Edge-level heterogeneous collaboration for cost-efficient multi-agent |
| The Hidden Footprint: Making Storage a First-Class Metric for LLM Agen | 2026-07-13 | `2607.11149v3` | Storage as a first-class agent cost metric - a cost axis the book omits |
| When KV Cache Reuse Fails in Multi-Agent Systems: Cross-Candidate Inte | 2026-01-13 | `2601.08343v1` | KV cache reuse across candidates changes multi-agent results, not just speed |

### Ch5 Budget-Aware Policies — 7 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| Budget-Aware Tool Use Enables Effective Agent Scaling | 2025-11-21 | `2511.17006v2` | Budget-aware tool use enables agent scaling (COLM 2026) - core evidence |
| ContextBudget: Budget-Aware Context Management for Long-Horizon Search | 2026-04-02 | `2604.01664v1` | Budget-aware context management for long-horizon search agents |
| Conformal Thinking: Risk Control for Reasoning on a Compute Budget | 2026-02-03 | `2602.03814v2` | Conformal risk control on a compute budget (ICML 2026) - budget meets gates |
| Aligning Tree-Search Policies with Fixed Token Budgets in Test-Time Sc | 2026-02-10 | `2602.09574v2` | Aligning tree-search policies with fixed token budgets (ICML 2026) |
| Timely Machine: Awareness of Time Makes Test-Time Scaling Agentic | 2026-01-23 | `2601.16486v1` | Time-aware rather than length-based budgets for agentic test-time scaling |
| Avoiding Overthinking and Underthinking: Curriculum-Aware Budget Sched | 2026-03-29 | `2604.19780v1` | Overthinking/underthinking: curriculum-aware budget scheduling |
| Budget-Aware Anytime Reasoning with LLM-Synthesized Preference Data | 2026-01-16 | `2601.11038v2` | Budget-aware anytime reasoning: useful partial answers under a cap |

### Ch6 Action Selection / Routing — 7 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing | 2026-05-11 | `2605.18796v1` | Calibrated uncertainty for cost-optimal cascade routing - fixes uncalibrated routers |
| CascadeDebate: Multi-Agent Deliberation for Cost-Aware LLM Cascades | 2026-04-14 | `2604.12262v1` | Cost-aware cascades with deliberation and abstention |
| Policy-Guided Stepwise Model Routing for Cost-Effective Reasoning | 2026-05-07 | `2605.06116v1` | Policy-guided STEPWISE routing - routing inside a trajectory, not per query |
| Confidence-Guided Stepwise Model Routing for Cost-Efficient Reasoning | 2025-11-09 | `2511.06190v2` | Confidence-guided stepwise model routing |
| Conformal Constrained Policy Optimization for Cost-Effective LLM Agent | 2025-11-14 | `2511.11828v2` | Conformal constrained policy optimization for cost-effective agents |
| AutoTool: Efficient Tool Selection for Large Language Model Agents | 2025-11-18 | `2511.14650v1` | Efficient tool selection - shrinking the candidate action set |
| CAST: Critique-Aware Supervision for Training Reliable Long-Horizon To | 2026-08-31 | `2608.30147v1` | Long-horizon tool-calling where one wrong action is irreversible (EMNLP 2026) |

### Ch7 Speculation and Commit — 13 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| Aborted but Not Forgotten: KV-Cache Retention Breaks Rollback Consiste | 2026-08-16 | `2608.15939v1` | KV-cache retention breaks rollback consistency - abort is not abort |
| CoAgent: Concurrency Control for Multi-Agent Systems | 2026-06-13 | `2606.15376v1` | Concurrency control for agents mutating shared state (git, k8s) |
| Safe to Resume? Breaking Execution Continuity of Agent Execution via R | 2026-08-29 | `2608.29381v1` | Breaking execution continuity via rollback - C/R as an attack surface |
| DeltaBox: Scaling Stateful AI Agents with Millisecond-Level Sandbox Ch | 2026-05-21 | `2605.22781v2` | Millisecond sandbox checkpoint/rollback - makes speculation affordable |
| Crab: A Semantics-Aware Checkpoint/Restore Runtime for Agent Sandboxes | 2026-04-30 | `2604.28138v1` | Semantics-aware checkpoint/restore runtime for agent sandboxes |
| TClone: Low-Latency Forking of Live GUI Environments for Computer-Use  | 2026-05-17 | `2605.17320v1` | Forking live GUI environments - speculation for computer-use agents |
| Cost-Aware Speculative Execution for LLM-Agent Workflows: An Integrate | 2026-06-05 | `2606.07846v1` | Cost-aware speculative execution for LLM-agent workflows |
| Certified Speculative Execution for Untrusted AI Agents | 2026-06-30 | `2606.31023v1` | Certified speculative execution preserving a solver's feasibility guarantee |
| RLM-Cascade: Response-Level Speculative Decoding for Cost-Efficient LL | 2026-06-22 | `2606.22840v1` | Response-level speculative decoding across API boundaries |
| AgentSpec: Speculative Decoding for Batch Inference of LLM Agents | 2026-08-25 | `2608.24004v1` | Speculative decoding for batch inference of agents (EMNLP 2026) |
| AsymSpec: Context-Asymmetric Speculative Decoding for Agentic LLMs | 2026-08-26 | `2608.26004v1` | Context-asymmetric speculative decoding for agentic pipelines (EMNLP 2026) |
| Oilbird: Training-Free Speculative Decoding with Keys the Verifier Alr | 2026-08-04 | `2608.03839v1` | Training-free speculation exploiting tool-call repetition - updates suffix decoding |
| GhostServe: A Lightweight Checkpointing System in the Shadow for Fault | 2026-03-26 | `2605.00831v1` | Checkpointing for fault-tolerant long-running LLM serving (MLSys 2026) |

### Ch8 Risk-Aware Gates — 9 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| AgentAbstain: Do LLM Agents Know When Not to Act? | 2026-07-11 | `2607.10059v1` | Do agents know when NOT to act? - abstention at the action level |
| Entropy Alone is Insufficient for Safe Selective Prediction in LLMs | 2026-03-22 | `2603.21172v1` | Entropy alone is insufficient for safe selective prediction - negative result |
| Verify, Repair, Repeat, or Stop? Robust Stopping for Noisy Verify-Repa | 2026-07-20 | `2607.17641v1` | Robust stopping for NOISY verify-repair loops - when verification hurts |
| Verify Before You Commit: Towards Faithful Reasoning in LLM Agents via | 2026-04-09 | `2604.08401v1` | Verify before you commit: self-auditing (ACL 2026) |
| Abstain-R1: Calibrated Abstention and Post-Refusal Clarification via V | 2026-04-18 | `2604.17073v1` | Calibrated abstention + post-refusal clarification (ACL 2026) |
| Leveraging Data to Say No: Memory Augmented Plug-and-Play Selective Pr | 2026-01-30 | `2601.22570v1` | Memory-augmented selective prediction for open-set tasks (ICLR 2026) |
| Confidence-Calibrated Small-Large Language Model Collaboration for Cos | 2026-03-04 | `2603.03752v1` | Confidence-calibrated small-large collaboration (EACL 2026) |
| ReDAct: Uncertainty-Aware Deferral for LLM Agents | 2026-04-08 | `2604.07036v1` | Uncertainty-aware deferral for LLM agents |
| Sherlock: Reliable and Efficient Agentic Workflow Execution | 2025-11-01 | `2511.00330v1` | Reliable and efficient agentic workflow execution |

### Ch9 Memory and Context — 10 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| Governance Decay: How Context Compaction Silently Erases Safety Constr | 2026-06-21 | `2606.22528v2` | Context compaction silently erases safety constraints - critical cross-cutting result |
| Control-Plane Placement Shapes Forgetting: An Architectural Study of A | 2026-06-14 | `2606.15903v2` | Control-plane placement shapes forgetting, across 13 memory systems |
| A Survey of Agent Memory in the Second Half: Towards Self-Evolving and | 2026-01-14 | `2602.06052v4` | Agent memory survey for long-horizon agents (TMLR) |
| From Recall to Forgetting: Benchmarking Long-Term Memory for Personali | 2026-04-21 | `2604.20006v1` | From recall to forgetting: benchmark where memory must be UPDATED (ACL 2026) |
| AMemGym: Interactive Memory Benchmarking for Assistants in Long-Horizo | 2026-03-02 | `2603.01966v1` | Interactive, on-policy memory benchmarking (ICLR 2026) |
| MemFail: Stress-Testing Failure Modes of LLM Memory Systems | 2026-05-26 | `2605.26667v1` | Stress-testing failure modes of memory systems |
| Toward Reliable Context Compression for Long-Horizon Agents: An Empiri | 2026-08-06 | `2608.06503v1` | Context compression weakens recency - a measured side effect |
| Context as an Environment: Programmatic Context Management for Long-Ho | 2026-08-21 | `2608.21690v1` | Context as an environment: programmatic, revisable context management |
| Agentic Context Management: Solving Agent Memory and Cost by Treating  | 2026-07-23 | `2607.21503v1` | Agentic context management as lifecycle + architecture |
| A Survey on Long-Term Memory Security in LLM Agents: Attacks, Defenses | 2026-04-17 | `2604.16548v2` | Long-term memory security: persistence, statefulness, propagation |

### Ch10 Retrieval and Evidence — 5 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| Cost-Aware Query Routing in RAG: Empirical Analysis of Retrieval Depth | 2026-03-26 | `2606.02581v1` | Cost-aware query routing in RAG: retrieval depth vs token cost vs latency |
| Cascading Hallucination in Agentic RAG: The CHARM Framework for Detect | 2026-06-03 | `2606.04435v1` | Cascading hallucination in agentic RAG - error compounding across hops |
| Is Agentic RAG worth it? An experimental comparison of RAG approaches | 2026-01-12 | `2601.07711v2` | Is agentic RAG worth it? - controlled cost/benefit comparison |
| KidnapRAG: A Black-Box Attack for Hijacking Reasoning in Agentic Retri | 2026-07-01 | `2607.00422v2` | Black-box attack hijacking reasoning in agentic RAG |
| Verbal-R3: Verbal Reranker as the Missing Bridge between Retrieval and | 2026-05-02 | `2605.01399v1` | Verbal reranking bridging retrieval and reasoning |

### Ch11 Capability Boundaries — 13 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| Beyond Static Sandboxing: Learned Capability Governance for Autonomous | 2026-04-12 | `2604.11839v2` | Beyond static sandboxing: learned capability governance |
| AgenTRIM: Tool Risk Mitigation for Agentic AI | 2026-01-18 | `2601.12449v2` | Tool risk mitigation - per-tool risk tiers |
| SkillGuard: A Permission-Centric Framework for Agent Skill Security | 2026-06-02 | `2606.03024v2` | Permission-centric framework for agent SKILL security - new attack surface |
| What If Prompt Injection Never Left? Rethinking Agent Security through | 2026-06-03 | `2606.04425v2` | Cross-session stored prompt injection - injection that persists in memory |
| APPA: Recoverable Information-Flow Control for Real-World LLM Agents | 2026-07-27 | `2607.24625v2` | Recoverable information-flow control for real-world agents |
| GitInject: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pip | 2026-06-07 | `2606.09935v1` | Real-world prompt injection in CI/CD pipelines |
| Data Leakage Prevention in Agentic Applications via Preemptive Hardeni | 2026-07-21 | `2607.18847v1` | Preemptive hardening against data leakage in agentic apps |
| WebMCP-Phalanx: Enforcing and Characterizing Trust Boundaries for Brow | 2026-08-25 | `2608.24017v1` | Trust boundaries for browser-integrated agents |
| MATRA: Modeling the Attack Surface of Agentic AI Systems -- OpenClaw C | 2026-05-11 | `2605.10763v1` | Attack-surface modeling for agentic AI systems |
| VATS: Exploiting Implicit Authority in Error-Path Injection via System | 2026-06-06 | `2606.07992v1` | Error-path injection: exploiting implicit authority in failure handling |
| MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills | 2026-06-05 | `2606.07131v3` | Runtime-verified benchmark of malicious agent skills |
| IPI-proxy: An Intercepting Proxy for Red-Teaming Web-Browsing AI Agent | 2026-05-12 | `2605.11868v1` | Intercepting proxy for red-teaming web-browsing agents |
| Security Considerations for Artificial Intelligence Agents | 2026-03-12 | `2603.12230v2` | Frontier-agent security recommendations from production deployment |

### Ch12 Alignment and Policy — 7 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| AIR: Improving Agent Safety through Incident Response | 2026-02-12 | `2602.11749v2` | Agent safety through incident response - operational, not aspirational |
| POLARIS: Typed Planning and Governed Execution for Agentic AI in Back- | 2026-01-16 | `2601.11816v1` | Typed planning + governed execution in back-office automation |
| Proof-of-Guardrail in AI Agents and What (Not) to Trust from It | 2026-03-06 | `2603.05786v2` | Proof-of-guardrail: what a guardrail attestation does and does not buy |
| Autoformalization of Agent Instructions into Policy-as-Code | 2026-06-25 | `2606.26649v1` | Autoformalizing agent instructions into policy-as-code |
| Policy-as-Prompt: Turning AI Governance Rules into Guardrails for AI A | 2025-09-28 | `2509.23994v2` | Turning governance rules into runtime guardrails |
| Don't Make Models Guess Security and Safety: Symbolic Guardrails for D | 2026-04-16 | `2604.15579v2` | Symbolic guardrails for domain-specific agents |
| Uncertainty Quantification in LLM Agents: Foundations, Emerging Challe | 2026-02-04 | `2602.05073v3` | Uncertainty quantification in LLM agents: foundations and challenges |

### Ch13 Traces and Telemetry — 16 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM- | 2026-04-24 | `2604.22708v1` | Failure-attribution benchmark for multi-agent systems (ACL 2026) |
| StepFinder: A Temporal Semantic Framework for Failure Attribution in M | 2026-06-02 | `2606.03467v1` | Temporal semantic framework for failure attribution (KDD 2026) |
| AgentRx: Diagnosing AI Agent Failures from Execution Trajectories | 2026-02-02 | `2602.02475v2` | Diagnosing agent failures from execution trajectories (EMNLP 2026) |
| VerifyMAS: Hypothesis Verification for Failure Attribution in LLM Mult | 2026-05-17 | `2605.17467v1` | Hypothesis verification for failure attribution |
| Adaptive Influence Graphs for Failure Attribution in Multi-Agent Syste | 2026-08-25 | `2608.24361v1` | Adaptive influence graphs for failure attribution |
| CASPIAN: Online Detection and Attribution of Cascade Attacks in LLM Mu | 2026-05-19 | `2605.19240v1` | Online detection and attribution of cascade attacks in multi-agent systems |
| AgentTrace: Causal Graph Tracing for Root Cause Analysis in Deployed M | 2026-03-16 | `2603.14688v2` | Causal graph tracing for root cause analysis in deployed systems |
| AgentTrace: A Structured Logging Framework for Agent System Observabil | 2026-02-07 | `2602.10133v1` | Structured logging framework for agent observability |
| AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribu | 2026-07-21 | `2607.18754v1` | Open-source toolkit for failure observability and attribution |
| From Agent Traces to Trust: A Survey of Evidence Tracing and Execution | 2026-06-03 | `2606.04990v4` | Survey of evidence tracing and execution provenance |
| Observability and Fault Injection for LLM-Based Multi-Agent Systems in | 2026-08-25 | `2608.24271v1` | OpenTelemetry-based observability + fault injection for agent MAS |
| When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failu | 2026-06-12 | `2606.14589v1` | Longitudinal taxonomy of SILENT failures in a production agent |
| TRAJDEBUG: Tracing Error Lifecycle to Identify Critical Failures in Lo | 2026-08-06 | `2608.06346v1` | Tracing error lifecycle across long-horizon agent trajectories |
| FALAT: Tracing Failures in LLM Agent Trajectories via Dependency-Guide | 2026-05-30 | `2606.00765v1` | Dependency-guided search for failure tracing in agent trajectories |
| Beyond LLM-Based Reasoning: Lightweight GNNs for Agent Failure Attribu | 2026-08-19 | `2608.18575v1` | Lightweight GNNs for agent failure attribution at low cost |
| Insights Generator: Systematic Corpus-Level Trace Diagnostics for LLM  | 2026-05-20 | `2605.21347v3` | Corpus-level trace diagnostics across many agent runs |

### Ch14 Evaluation — 8 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent | 2026-07-30 | `2607.28802v1` | Model or harness? Localizing whether the model or the scaffold failed |
| Measuring Harness-Induced Belief Divergence in Multi-Step LLM Agents | 2026-07-05 | `2607.04528v1` | Measuring harness-induced belief divergence - the harness is a confound |
| UniACE: A Unified Framework for Evaluating LLM Agentic Capabilities | 2026-05-27 | `2605.27898v3` | A score reflects model-harness-environment, not the model alone |
| Can LLM-as-a-Judge Reliably Verify Rubrics in Agentic Scenarios? | 2026-06-29 | `2606.29920v2` | Can LLM-as-judge reliably verify rubrics in agentic settings? (EMNLP 2026) |
| Industrializing Prediction-Powered Inference: The GLIDE Library for Re | 2026-05-29 | `2605.31278v2` | Prediction-powered inference: debiased estimates from cheap judges + few humans |
| WildClawBench: A Benchmark for Real-World, Long-Horizon Agent Evaluati | 2026-05-11 | `2605.10912v1` | Real-world long-horizon agent evaluation beyond synthetic sandboxes |
| AEVAL: From Anecdotal to Deterministic Testing for Agentic Skill Workf | 2026-07-16 | `2607.16345v2` | From anecdotal to deterministic testing of agentic workflows |
| JADE: Expert-Grounded Dynamic Evaluation for Open-Ended Professional T | 2026-02-06 | `2602.06486v4` | Expert-grounded dynamic evaluation for open-ended tasks (ICML 2026) |

### Ch15 Case Studies and Patterns — 9 papers

| Paper | Date | arXiv | Why it earns a place |
|---|---|---|---|
| Scaling Test-Time Compute for Agentic Coding | 2026-04-16 | `2604.16529v1` | Scaling test-time compute for agentic coding - long-horizon TTS |
| Cost-Effective Repository Exploration for Agentic Issue Localization | 2026-08-30 | `2608.29675v1` | Delegating repository exploration to cheaper models |
| SWE-Replay: Efficient Test-Time Scaling for Software Engineering Agent | 2026-01-29 | `2601.22129v2` | Replay instead of resampling trajectories from scratch |
| When Parallelism Pays Off: Cohesion-Aware Task Partitioning for Multi- | 2026-05-31 | `2606.00953v1` | When parallelism pays off: partitioning vs communication overhead |
| Long Live the Librarian! A Persistent Search Sub-Agent for Energy-Effi | 2026-05-27 | `2605.27787v2` | Persistent search sub-agent cuts redundant retrieval energy (EMNLP 2026) |
| CODESTRUCT: Code Agents over Structured Action Spaces | 2026-04-07 | `2604.05407v3` | Structured action spaces beat brittle string-matching edits (ACL 2026) |
| Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnes | 2026-06-10 | `2606.12344v1` | Benchmarking general-purpose agent harnesses on coding tasks |
| Efficient GUI Agents: A Systems Survey of Observation, Memory, Action, | 2026-09-02 | `2609.02309v1` | Systems survey of GUI agents: observation, memory, action, runtime |
| Web Agents Should Use Typed Actions Instead of Click-Based Browsing | 2026-02-19 | `2602.17245v2` | Typed actions instead of click-based browsing |

---

## Deliberately excluded

Roughly 1,700 in-window papers were reviewed and left out. The exclusions are not arbitrary; each
category conflicts with a commitment the book already makes in its preface.

| Excluded category | Approx. count | Reason |
|---|---|---|
| Domain applications (clinical, legal, financial, geospatial, robotics/UAV, education, e-commerce) | ~520 | The book is deliberately domain-neutral. A healthcare RAG system illustrates nothing the abstract mechanism does not. |
| RL post-training and policy-optimization methods (EPO, GiGPO variants, credit assignment) | ~240 | The preface names training foundation models as a non-goal. These change how a model is built, not how a system controls it. |
| Serving-infrastructure internals (disaggregated prefill/decode, FPGA KV caches, MoE cold-start, LoRA co-hosting) | ~180 | Below the book's abstraction layer. Included only where the result changes an agent-level decision (KV survey, agentic KV quantization, rollback/KV interaction). |
| Capability benchmarks the book does not model (geometry, translation, games, bargaining) | ~150 | The book evaluates control properties, not task capability. |
| Multimodal/VLM and GUI-specific methods | ~140 | Kept only the two that establish a transferable principle: the GUI systems survey and typed-actions-over-clicks. |
| Framework, SDK, and platform announcements without evaluation | ~110 | The preface rules out a catalog of product frameworks. |
| Prompt-engineering and prompt-optimization techniques | ~90 | Explicit non-goal. |
| Incremental variants with no quantitative claim over a cited baseline | ~270 | Nothing to cite. |

### Judgment calls worth recording

- **Speculative decoding.** The field produced far more of this than the book can absorb. Included five
  that are specifically *agentic* (tool-call repetition, batch agent inference, context asymmetry,
  response-level across an API boundary, cost-aware workflow speculation) and dropped the rest as
  decoder-internal.
- **Memory systems.** Dozens of new architectures, mostly incremental. Preferred the benchmarks and the
  negative results (`MemFail`, `Control-Plane Placement`, `From Recall to Forgetting`) over yet another
  architecture, because the book's claim is about *what breaks*, not about which store wins.
- **`Token Economics` and `The Hidden Footprint`** are included despite being survey-ish, because they
  add a cost axis the book currently omits entirely: persistent storage left behind by agent runs.
- **Anthropic/OpenAI model pricing** is deliberately *not* re-cited to specific numbers. The book's own
  LLMflation section makes prices a moving target; the rewrite keeps the ratios (which are stable) and
  drops absolute per-token figures that will be wrong again in six months.

---

## What changed in the manuscript

The rewrite is installed at `main.tex` (original preserved as `main.tex.orig-backup`).
It builds clean with `pdflatex` in three passes: **331 pages**, zero undefined
citations, zero undefined references.

### Voice
- **Aphoristic contrastive constructions cut 57 → 2 (96%).** These were the "AI slop"
  signal: nearly every section closed with an inverted aphorism ("X is not Y. It is Z.").
  Ordinary technical contrast ("evaluate the path, not just the destination") was left
  alone — removing it would make the prose stilted, not cleaner.
- Chapter and section openings rewritten to start from a concrete situation rather than
  an abstract definition. Chapter 3 (Mathematical Foundations) already wrote this way and
  was used as the house style rather than inventing a new one.

### Content repaired
- **Three chapters were skeletons, not prose.** Cost Models, Budget-Aware Policies, and
  Alignment had sections of 4–20 words each. Both "Worked Example" sections were a single
  sentence *describing* an example that did not exist. All are now written out, with the
  research-agent and budget-aware-agent examples carried through step by step.
- **Chapter 5 retitled** from "Cost Models and Critical Paths—Part II" to
  "Budget-Aware Policies and Horizon Estimation", which is what it covers.
- **Cross-references were broken.** `\ref{ch:...}` was used 9 times with zero `\label{}`
  definitions, so every one printed as `??`. Labels added for all 15 chapters.
- **Four citations had no bibliography entry** (`adaptiverag`, `replug`, `embeddingsurvey`,
  `mohan1986transaction`). Real entries added.
- Stale model names and per-token prices replaced with tier ratios, which have been stable
  for years and are what the arguments actually depend on.
- Missing chapter scaffolding added where absent (Fallacies / Summary / Exercises).

Word count: ~67,100 → ~85,800.

### Where the new research changed the argument, not just the footnotes
- **Ch7** — rollback is leakier than the first edition claimed. Added a *Complete abort*
  property and the KV-retention result; added millisecond checkpoint/restore, which changes
  the speculation break-even; added concurrency control for agents sharing state.
- **Ch9 + Ch12** — context compaction silently deletes safety constraints. This is now a
  named failure mode in both chapters with three design rules, and it is the strongest
  available support for the book's own thesis.
- **Ch13** — failure attribution rewritten from a short section into a full treatment with
  four method families, plus silent failure and corpus-level diagnostics.
- **Ch14** — new section *The Harness Is a Confound*, plus judge debiasing via
  prediction-powered inference.
- **Ch6** — stepwise (per-step) routing and the calibration problem, which links this
  chapter to Ch8 in both directions.
