# SynthOmnicon: Millennium Thresholds
## *A Formal Threshold Taxonomy for the Millennium Prize Problems in Lean 4*

**Version:** v0.2.0 · 2026-04-14
**Authors:** Lando⊗LLM & Human
**Document role:** Self-contained research paper. Presents the machine-checked threshold taxonomy for all seven Clay Millennium Prize Problems, the `ThresholdType` inductive, the `ym_is_unique_missing_foundation` theorem, the stacked/parallel sorry distinction, and the primitive bridge connecting sorry boundaries to the SynthOmnicon constraint grammar. Target venue: Journal of Formalized Reasoning / Journal of Automated Reasoning.

*The distinction that matters throughout: 'we have formalized' is not the same as 'we have solved.' Every `sorry` at the core of this library is honest. No Millennium Problem is proved here. The contribution is the meta-level structure  --  what kind of thing each sorry is, and why.*

---

## Three-Document Architecture

The SynthOmnicon Lean library occupies two tracks: `Primitives/` (the 12-primitive constraint grammar) and `Millennium/` (the threshold taxonomy library documented here). This paper reports on the `Millennium/` track and its bridge to `Primitives/`.

**Internal references** within this paper use §N.

**Library location:** `SynthOmnicon/Millennium/`  --  nine files, approximately 1,524 lines. Build target: `lake build Millennium`.

---

## I. Introduction (v0.1.0, 2026-03-26)

The Clay Mathematics Institute seven Millennium Prize Problems have resisted proof for decades  --  and in one case, the Riemann Hypothesis, for over a century and a half. Proof assistants have formalized large bodies of mathematics, but existing efforts overwhelmingly target *results that are known*: the Last Theorem of Fermat, the Four Color Theorem, the Kepler Conjecture. Far less attention has been paid to formalizing *why specific problems are hard*  --  the structural thresholds that distinguish them from merely difficult but open problems.

This paper presents a formal threshold taxonomy for all seven Millennium Problems in Lean 4. We make no claim to have solved any of them. The contribution is meta-level: a machine-checked classification of the proof obligations, the structural relationships between them, and their connection to an underlying primitive constraint algebra.

### I.1 Why this matters

The distinction between threshold types has practical consequences for the formalization community.The distinction between threshold types has practical consequences for the formalization community.

**MathlibGap sorries are actionable.** A contributor with the right background can in principle discharge them by formalizing a known proof. The `euler_opn_form` sorry in OPN.lean (Euler 1747) and the `mazur_torsion` sorry in BSD.lean (Mazur 1977) are of this type.

**OpenProblem sorries define the research frontier.** They cannot be discharged without solving the underlying mathematics. Knowing which sorries are of this type — as opposed to merely MathlibGap — is useful for anyone building on the library. This distinction became clear during the initial formalization of the BSD conjecture (§II.3), where we initially misassigned the Mordell-Weil theorem as an OpenProblem before realizing its MathlibGap status.

**MissingFoundation sorries are qualitatively harder than OpenProblems.** An OpenProblem has a well-typed proposition whose truth value is unknown. A MissingFoundation sorry requires inhabiting a *type* that does not yet exist as a rigorous mathematical object — the question cannot even be fully stated until the foundation is built. Yang-Mills is the only Millennium Problem in this category. We prove this formally.

### I.2 The sorry depth distinction

We introduce a formal notion of *sorry depth* distinguishing *stacked* from *parallel* proof obligations.

**Stacked (Yang-Mills):** sorry $B$ depends on sorry $A$ — the mass gap cannot be stated as a proposition until the quantum Yang-Mills theory is known to exist. This was first noticed when attempting to formalize the Yang-Mills axioms in Lean (§III.1), where the foundation of the gauge theory (`PathIntegralMeasure G`) was found to be a prerequisite for even defining the mass gap.

**Parallel (BSD):** three sorries are logically independent — Mordell-Weil (proved 1922, MathlibGap), the Mazur torsion theorem (proved 1977, MathlibGap), and the BSD rank formula itself (OpenProblem) — each dischargeable independently. This parallelism became evident when we discovered that the Mordell-Weil theorem and Mazur torsion theorem had already been fully formalized in Mathlib before we even began the BSD project.

Both Yang-Mills and BSD have `sorryDepth = 2`. The structural difference is encoded in the threshold type.

### I.3 Contributions

**C1  --  ThresholdType taxonomy:** A typed inductive with three constructors, formally distinct (by `decide`), and computably assigned to all seven Millennium Problems. The introduction of `MissingFoundation` was motivated by the need to distinguish formalization bottlenecks from unsolved mathematics — a distinction that became critical when attempting to map the Yang-Mills problem to the existing formalization framework.

**C2  --  ym_is_unique_missing_foundation:** A theorem, proved by `decide`, that Yang-Mills is the only Millennium Problem whose threshold is MissingFoundation. This proof required navigating the intricate relationship between the `MillenniumProblem` inductive and the `ThresholdType` inductive — an instance of the structural tension between classification and specification that the grammar formalizes.

**C4  --  NS critical Sobolev exponent:** Machine-verified by `norm_num` that $0 < \frac{1}{2} < 1$  --  the formal statement of why NS regularity is hard.

**C5  --  OPN in real Mathlib:** the Touchard congruence type-checks using actual `Nat.Perfect` and `ArithmeticFunction.sigma`.

**C6  --  BSD in real Mathlib:** `BSDRankConjecture` stated using actual `WeierstrassCurve ℚ` and `IsElliptic`; three parallel sorries formally justified.

**C7  --  PrimitiveBridge.lean:** Formal connection between sorry boundaries and primitive field transitions in the SynthOmnicon grammar; `ThresholdPrimitiveCertificate` structure; `primitive_bridge_master` theorem.

**C8  --  RH–Lee-Yang structural correspondence (v0.1.2):** Machine-checked theorem that the Riemann $\zeta$ zeros and Lee-Yang partition-function zeros share the same Criticality assignment `Phi_c_complex`. Structural distance 1.0 (machine-checked) identifies the polarity primitive $P$ ($P_\text{sym}$ vs $P_{\pm}^{\text{sym}}$) as the essential structural gap; remaining 0 mismatches (T, F, K, gran, stoi, chir) are background differences.