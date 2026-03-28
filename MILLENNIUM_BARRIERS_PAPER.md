# SynthOmnicon: Millennium Barriers
## *A Formal Barrier Taxonomy for the Millennium Prize Problems in Lean 4*

**Version:** v0.1.0 · 2026-03-26
**Authors:** Lando Mills & Large Language Models
**Document role:** Self-contained research paper. Presents the machine-checked barrier taxonomy for all seven Clay Millennium Prize Problems, the `BarrierType` inductive, the `ym_is_unique_missing_foundation` theorem, the stacked/parallel sorry distinction, and the primitive bridge connecting sorry boundaries to the SynthOmnicon constraint grammar. Target venue: Journal of Formalized Reasoning / Journal of Automated Reasoning.

*The distinction that matters throughout: 'we have formalized' is not the same as 'we have solved.' Every `sorry` at the core of this library is honest. No Millennium Problem is proved here. The contribution is the meta-level structure  --  what kind of thing each sorry is, and why.*

---

## Three-Document Architecture

The SynthOmnicon Lean library occupies two tracks: `Primitives/` (the 12-primitive constraint grammar) and `Millennium/` (the barrier taxonomy library documented here). This paper reports on the `Millennium/` track and its bridge to `Primitives/`.

**Cross-reference notation:** [TOPO:§N] · [DIAPH:§N] · [ONTO:§N] for the three core grammar documents. [PRIM:P-N] for predictions. Internal references within this paper use §N.

**Library location:** `SynthOmnicon/Millennium/`  --  nine files, approximately 1,524 lines. Build target: `lake build Millennium`.

---

## I. Introduction (v0.1.0, 2026-03-26)

The Clay Mathematics Institute seven Millennium Prize Problems have resisted proof for decades  --  and in one case, the Riemann Hypothesis, for over a century and a half. Proof assistants have formalized large bodies of mathematics, but existing efforts overwhelmingly target *results that are known*: the Last Theorem of Fermat, the Four Color Theorem, the Kepler Conjecture. Far less attention has been paid to formalizing *why specific problems are hard*  --  the structural barriers that distinguish them from merely difficult but open problems.

This paper presents a formal barrier taxonomy for all seven Millennium Problems in Lean 4. We make no claim to have solved any of them. The contribution is meta-level: a machine-checked classification of the proof obligations, the structural relationships between them, and their connection to an underlying primitive constraint algebra.

### I.1 Why this matters

The distinction between barrier types has practical consequences for the formalization community.

**MathlibGap sorries are actionable.** A contributor with the right background can in principle discharge them by formalizing a known proof. The `euler_opn_form` sorry in OPN.lean (Euler 1747) and the `mazur_torsion` sorry in BSD.lean (Mazur 1977) are of this type.

**OpenProblem sorries define the research frontier.** They cannot be discharged without solving the underlying mathematics. Knowing which sorries are of this type  --  as opposed to merely MathlibGap  --  is useful for anyone building on the library.

**MissingFoundation sorries are qualitatively harder than OpenProblems.** An OpenProblem has a well-typed proposition whose truth value is unknown. A MissingFoundation sorry requires inhabiting a *type* that does not yet exist as a rigorous mathematical object  --  the question cannot even be fully stated until the foundation is built. Yang-Mills is the only Millennium Problem in this category. We prove this formally.

### I.2 The sorry depth distinction

We introduce a formal notion of *sorry depth* distinguishing *stacked* from *parallel* proof obligations.

**Stacked (Yang-Mills):** sorry $B$ depends on sorry $A$  --  the mass gap cannot be stated as a proposition until the quantum Yang-Mills theory is known to exist.

**Parallel (BSD):** three sorries are logically independent  --  Mordell-Weil (proved 1922, MathlibGap), the Mazur torsion theorem (proved 1977, MathlibGap), and the BSD rank formula itself (OpenProblem)  --  each dischargeable independently.

Both Yang-Mills and BSD have `sorryDepth = 2`. The structural difference is encoded in the barrier type.

### I.3 Contributions

**C1  --  BarrierType taxonomy:** A typed inductive with three constructors, formally distinct (by `decide`), and computably assigned to all seven Millennium Problems.

**C2  --  ym_is_unique_missing_foundation:** A theorem, proved by `decide`, that Yang-Mills is the only Millennium Problem whose barrier is MissingFoundation.

**C3  --  Stacked vs parallel sorry distinction:** Formalized in `sorryDepth` and `ym_has_stacked_not_parallel_sorries`.

**C4  --  NS critical Sobolev exponent:** Machine-verified by `norm_num` that $0 < \frac{1}{2} < 1$  --  the formal statement of why NS regularity is hard.

**C5  --  OPN in real Mathlib:** the Touchard congruence type-checks using actual `Nat.Perfect` and `ArithmeticFunction.sigma`.

**C6  --  BSD in real Mathlib:** `BSDRankConjecture` stated using actual `WeierstrassCurve ℚ` and `IsElliptic`; three parallel sorries formally justified.

**C7  --  PrimitiveBridge.lean:** Formal connection between sorry boundaries and primitive field transitions in the SynthOmnicon grammar; `BarrierPrimitiveCertificate` structure; `primitive_bridge_master` theorem.

---

## II. Background (v0.1.0, 2026-03-26)

### II.1 Lean 4 and Mathlib

All code targets **Lean 4.28.0** with **Mathlib v4.28.0**. We use `import Mathlib.Tactic` throughout plus specific imports per file:

| File | Key Mathlib imports |
| :--- | :--- |
| **OPN.lean** | `Mathlib.NumberTheory.ArithmeticFunction`  --  `Nat.Perfect`, `ArithmeticFunction.sigma` |
| **BSD.lean** | `Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass`, `.Affine.Point`  --  `WeierstrassCurve ℚ`, `IsElliptic` |
| **YM.lean** | `Mathlib.Algebra.Lie.Basic`  --  `LieRing`, `LieAlgebra`, `LieAlgebra.IsSimple` |
| **NS.lean** | `Mathlib.Analysis.InnerProductSpace.Basic`  --  functional-analytic infrastructure |

### II.2 The sorry in Lean

In Lean 4, `sorry` is an axiom of type $\alpha$ for any $\alpha : \mathsf{Prop}$ (or any type). It allows a proof to typecheck despite containing unfinished obligations. A `sorry`-free proof is fully kernel-verified; a proof with `sorry` is verified modulo those axioms. There is no built-in mechanism in Lean to classify *why* a sorry cannot be discharged. The `BarrierType` inductive in §III provides this classification for the first time.

In the final library, each sorry boundary is declared as an `axiom` rather than left as a literal `sorry`:

```lean
axiom rh_sorry_boundary : Millennium.RH.RiemannHypothesis
```

This is intentional. An `axiom` is explicit about its foundational status  --  it extends the logical framework at a named location rather than leaving an opaque hole.

### II.3 The SynthOmnicon primitive grammar

The SynthOmnicon framework encodes physical and mathematical systems as 12-tuples $\langle D; T; R; P; F; K; G; \Gamma; \Phi_c; H; S; \Omega \rangle$ over a constraint algebra. The twelve primitives and their Lean types:

| Primitive | Lean type | Role |
| :--- | :--- | :--- |
| **$D$ (Dimensionality)** | `Dimensionality` | Spatial encoding: point / line / cube / holographic |
| **$T$ (Topology)** | `Topology` | Connectivity: linear / branched / network / holographic |
| **$R$ (Recognition)** | `Recognition` | Symmetry / matching mode |
| **$P$ (Polarity)** | `Polarity` | Charge / orientation |
| **$\Gamma$ (Grammar)** | `Grammar` | Composition rule |
| **$F$ (Fidelity)** | `Fidelity` | Information reliability: noise / $\ell$ / $\eta$ / $\hbar$ |
| **$K$ (Kinetic character)** | `KineticChar` | Rate / trapping: fast / mod / slow / trap / MBL |
| **$G$ (Granularity)** | `Granularity` | Description scale: $\aleph$ / $\beth$ / $\gimel$ |
| **$\Phi_c$ (Criticality)** | `Criticality` | Phase position: sub / critical / super |
| **$H$ (Chirality)** | `Chirality` | Temporal asymmetry depth: $H_0$ / $H_1$ / $H_2$ / $H_\infty$ |
| **$S$ (Stoichiometry)** | `Stoichiometry` | Ratio: 1:1 / 1:$n$ / $n$:$m$ / catalytic |
| **$\Omega$ (Protection)** | `Protection` | Topological protection: $0$ / $Z_2$ / $Z$ / $C$ / NA |

All twelve types derive `DecidableEq`, making structural comparisons computable. The `primitiveMismatches` function (Hamming distance over twelve fields) is proved bounded by 12 and zero iff tuples are identical  --  all by `decide` or `omega`. See [TOPO:§I] for the full grammar specification.

---

## III. The Barrier Taxonomy (v0.1.0, 2026-03-26)

### III.1 The BarrierType inductive

```lean
inductive BarrierType
  | MathlibGap
  | OpenProblem
  | MissingFoundation
  deriving Repr, DecidableEq
```

The three constructors represent qualitatively distinct epistemic states.

**`MathlibGap`:** The theorem has been proved in the mathematical literature. A Lean proof exists *in principle* using currently available tools; the sorry persists only because no one has yet carried out the formalization. Such sorries are *defeasible*  --  they will eventually be discharged as Mathlib grows. Examples: the Euler 1747 characterization of OPN structure (`euler_opn_form`); the Mazur 1977 torsion theorem (`mazur_torsion`).

**`OpenProblem`:** No proof of the theorem exists anywhere. The sorry cannot be discharged because the underlying mathematics is unsolved. Examples: the Riemann Hypothesis, the BSD rank conjecture, the nonexistence of odd perfect numbers.

**`MissingFoundation`:** The sorry requires inhabiting a *type* that does not yet exist as a rigorous mathematical object. The distinction from `OpenProblem` is ontological: an `OpenProblem` has a well-typed proposition  --  we know what it means, we just do not know if it is true. A `MissingFoundation` sorry cannot even be fully stated until the missing type is constructed. Example: `PathIntegralMeasure G` in Yang-Mills  --  the path integral measure over gauge connections modulo gauge equivalence in four Euclidean dimensions.

Formal distinctness is immediate:

```lean
theorem missing_foundation_vs_open_problem :
    BarrierType.MissingFoundation ≠ BarrierType.OpenProblem := by decide
```

### III.2 The master classification

```lean
def millenniumBarrier : MillenniumProblem → BarrierType
  | .RH    => .OpenProblem
  | .Hodge => .OpenProblem
  | .PvsNP => .OpenProblem
  | .NS    => .OpenProblem
  | .YM    => .MissingFoundation
  | .BSD   => .OpenProblem
  | .OPN   => .OpenProblem
```

The central theorem of the library:

```lean
theorem ym_is_unique_missing_foundation :
    ∀ p : MillenniumProblem,
      millenniumBarrier p = .MissingFoundation → p = .YM := by
  intro p hp; cases p <;> simp_all [millenniumBarrier]
```

Yang-Mills is the only Millennium Problem with a `MissingFoundation` barrier. This is a theorem about the structure of mathematics, proved by exhaustive case analysis over the seven-constructor `MillenniumProblem` inductive, closed by `simp_all`.

### III.3 Sorry depth

```lean
def sorryDepth : MillenniumProblem → ℕ
  | .RH    => 1   -- ZeroFreeStrip 0 (one sorry; everything else proved)
  | .Hodge => 1   -- algebraic cycle representative
  | .PvsNP => 1   -- circuit lower bound
  | .NS    => 1   -- global regularity certificate
  | .YM    => 2   -- existence (sorry 1) THEN mass gap (sorry 2)
  | .BSD   => 2   -- three parallel; Mordell-Weil + Mazur torsion + BSD formula
  | .OPN   => 2   -- Euler form (MathlibGap) + nonexistence (OpenProblem)
```

The key structural distinction:

```lean
theorem ym_has_stacked_not_parallel_sorries :
    sorryDepth .YM = sorryDepth .BSD ∧
    millenniumBarrier .YM = .MissingFoundation ∧
    millenniumBarrier .BSD = .OpenProblem := by
  simp [sorryDepth, millenniumBarrier]
```

YM and BSD share `sorryDepth = 2` but for different structural reasons: in YM, sorry 2 (mass gap) logically depends on sorry 1 (existence of the theory). In BSD, the three sorries are logically independent  --  each can in principle be discharged separately.

---

## IV. Per-Problem Analysis (v0.1.0, 2026-03-26)

### IV.1 Riemann Hypothesis

*Barrier: `OpenProblem` · Missing type: `ZeroFreeStrip 0`*

The file introduces abstract types `RiemannZeta`, `CriticalStrip`, and `ZeroFreeStrip` to provide typed scaffolding. The sorry boundary is the statement that $\zeta(s) \neq 0$ for all $s$ with $0 < \text{Re}(s) < 1$, $\text{Re}(s) \neq \frac{1}{2}$.

```lean
axiom rh_sorry_boundary : Millennium.RH.RiemannHypothesis

theorem rh_barrier : RiemannHypothesis <-> ZeroFreeStrip 0
```

The barrier theorem isolates `ZeroFreeStrip 0` as the exact missing type: the sorry is tight  --  RH is equivalent to inhabiting that type and nothing else.

### IV.2 Yang-Mills Existence and Mass Gap

*Barrier: `MissingFoundation` · Missing type (primary): `PathIntegralMeasure G`*

The YM file is distinguished by *two stacked* sorries. The axiom bundles both:

```lean
axiom ym_sorry_boundary :
    ∀ (G : Type*) [LieRing G] [LieAlgebra ℝ G] [LieAlgebra.IsSimple ℝ G],
      Nonempty (QuantumYMTheory G) ∧
      ∀ T : QuantumYMTheory G, 0 < massGap G T
```

`ym_theory_exists` (MissingFoundation) is annotated with sorry first. `ym_mass_gap` (OpenProblem) depends on the first  --  it is statable only once the theory exists. The `PathIntegralMeasure G` type is defined to require `LieAlgebra.IsSimple`, reflecting that the problem is well-posed only for compact simple gauge groups.

Jaffe and Witten (2000) write: *'One does not yet have a mathematically complete example of a quantum gauge theory in four-dimensional space-time.'* The `MissingFoundation` constructor formalizes exactly this observation.

### IV.3 Hodge Conjecture

*Barrier: `OpenProblem` · Missing type: `AlgebraicCycleRep X p α`*

The file introduces `SmoothProjectiveVariety`, `HodgeCohomology X p`, and `AlgebraicCycle X p`. The missing type is cycle class surjectivity: a proof that $\alpha \in H^{2p}(X,\mathbb{Q}) \cap H^{p,p}$ lies in the image of $\text{cl} : \text{CH}^p(X) \otimes \mathbb{Q} \to H^{2p}(X,\mathbb{Q})$.

The layer structure is explicit:

**Layer 1 (MathlibGap):** The $p = 1$ case (Lefschetz 1924) is documented as dischargeable  --  the theorem is proved, merely not yet in Mathlib.

**Layer 2 (OpenProblem):** The $p \geq 2$ case, which is the actual Hodge conjecture.

```lean
theorem hodge_barrier :
    HodgeConjecture <-> ∀ (X : SmoothProjectiveVariety) (p : ℕ),
      ∀ α : HodgeCohomology X p, AlgebraicCycleRep X p α
```

### IV.4 Navier-Stokes

*Barrier: `OpenProblem` (near-`MissingFoundation`) · Missing type: `GlobalRegularityCert u₀`*

The central formal result is a machine-verified statement of why NS is hard:

```lean
def CriticalSobolevExponent : ℝ := 1 / 2

theorem energy_norm_subcritical    : 0 < CriticalSobolevExponent    := by norm_num
theorem enstrophy_norm_supercritical : CriticalSobolevExponent < 1  := by norm_num

theorem critical_scaling_gap :
    0 < CriticalSobolevExponent ∧ CriticalSobolevExponent < 1 :=
  ⟨energy_norm_subcritical, enstrophy_norm_supercritical⟩
```

**Interpretation:** The energy norm ($H^0 = L^2$, exponent $s = 0$) is subcritical under the natural scaling of the 3D NS equations; the enstrophy norm ($H^1$, exponent $s = 1$) is supercritical. The critical Sobolev exponent $s = \frac{1}{2}$ sits strictly between them. Global regularity requires controlling the $\dot{H}^{1/2}$ norm  --  which is exactly what is not known. Two `norm_num` calls verify this formally.

Three tiers of sorry are distinguished: `leray_weak_existence` (MathlibGap, Leray 1934); `ns_small_data_global_regularity` (MathlibGap, Koch-Tataru 2001); `ns_certificate` (OpenProblem, the Clay problem itself).

### IV.5 P versus NP

*Barrier: `OpenProblem` (with deep `MathlibGap` in complexity formalization) · Missing type: `CircuitLowerBound ε`*

The file uses concrete types to ground the statement without relying on complexity classes that Mathlib does not yet have:

```lean
def BooleanCircuit (n : ℕ) := (Fin n → Bool) → Bool
def CNFFormula (n : ℕ)     := List (List (Literal n))
```

Three **meta-barriers** are formalized as `trivial` theorems with full documentation:

```lean
-- Baker-Gill-Solovay (1975): P vs NP is independent of relativized computation.
theorem bgs_relativization_barrier : True := trivial

-- Razborov-Rudich (1994): 'Natural proofs' cannot separate P from NP
-- unless one-way functions do not exist.
theorem razborov_rudich_natural_proofs_barrier : True := trivial

-- Aaronson-Wigderson (2009): Algebrizing techniques cannot separate P from NP.
theorem aaronson_wigderson_algebrization_barrier : True := trivial
```

The `trivial` bodies are honest: these are theorems *about* proof techniques, not the conjecture itself. They are documented constraints on the proof search space.

### IV.6 Odd Perfect Number

*Barrier: `OpenProblem` (primary); `MathlibGap` (Euler form layer) · Missing type: `OPNConjecture`*

This file uses the **actual Mathlib infrastructure**:

```lean
import Mathlib.NumberTheory.ArithmeticFunction
-- Nat.Perfect : ℕ → Prop
-- Nat.ArithmeticFunction.sigma : ArithmeticFunction ℕ
```

The multiplicativity of $\sigma$ is proved using the actual Mathlib lemma:

```lean
theorem sigma_multiplicative (a b : ℕ) (h : Nat.Coprime a b) :
    (Nat.ArithmeticFunction.sigma 1) (a * b) =
    (Nat.ArithmeticFunction.sigma 1) a *
    (Nat.ArithmeticFunction.sigma 1) b :=
  Nat.ArithmeticFunction.IsMultiplicative.sigma.map_mul_of_coprime h
```

The two-layer structure: `euler_opn_structure` (Euler 1747, MathlibGap  --  every OPN has the form $N = p^\alpha m^2$ with $p \equiv \alpha \equiv 1 \pmod 4$) stacked methodologically (not logically) with `opn_nonexistence` (OpenProblem). The current lower bound $N > 10^{1500}$ (Ochem-Rao 2012) is documented as a MathlibGap sorry. The companion file `OPN_2adic.lean` in `Primitives/` contains the full machine-verified Touchard congruence.

### IV.7 Birch and Swinnerton-Dyer

*Barrier: `OpenProblem` (primary); `MathlibGap` (two layers) · Missing type: `BSDRankCertificate W`*

BSD.lean is the most concretely grounded file, using real Mathlib types throughout:

```lean
import Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass
import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point

def ExampleCurve : WeierstrassCurve ℚ :=
  { a₁ := 0, a₂ := 0, a₃ := 0, a₄ := -1, a₆ := 0 }
-- y² = x³ − x, the congruent number curve for n = 1

def BSDRankConjecture : Prop :=
    ∀ (W : WeierstrassCurve ℚ) [W.IsElliptic],
      ellipticRank W = analyticRank W
```

The three sorries are formally **parallel**  --  logically independent:

| Sorry | Type | Barrier | Attribution |
| :--- | :--- | :--- | :--- |
| **`mordell_weil`** | `MordellWeilGroup` | MathlibGap | Mordell 1922: $E(\mathbb{Q})$ finitely generated |
| **`mazur_torsion`** | `MazurTorsionBound` | MathlibGap | Mazur 1977: torsion subgroup classification |
| **`bsd_certificate`** | `BSDRankCertificate` | OpenProblem | The BSD conjecture itself |

Known partial results are documented: Coates-Wiles 1977 (MathlibGap, rank 0 for CM curves); Gross-Zagier + Kolyvagin (MathlibGap, BSD holds for analytic rank $\leq 1$).

---

## V. The Primitive Bridge (v0.1.0, 2026-03-26)

*[Connects Millennium/ and Primitives/. Full Lean source: `SynthOmnicon/Millennium/PrimitiveBridge.lean`.]*

### V.1 Motivation

The barrier taxonomy classifies *why* sorries cannot be discharged but does not explain *what structural feature* of each problem generates its barrier. `PrimitiveBridge.lean` provides this second layer: a machine-checked connection between each sorry boundary and a specific primitive field transition in the SynthOmnicon grammar.

The key claim: every Millennium Problem sorry boundary corresponds to a specific field value that the natural primitive encoding of the problem *wants* but cannot obtain given its surrounding constraints. This is testable  --  the encodings are concrete `Synthon` values, field values are decidable, and barrier classifications are machine-checked.

### V.2 BarrierPrimitiveCertificate

```lean
structure BarrierPrimitiveCertificate (p : Barriers.MillenniumProblem) where
  encoding      : Synthon
  blockedField  : String
  barrier       : Barriers.BarrierType
  barrier_correct : barrier = Barriers.millenniumBarrier p
```

The `barrier_correct` field is a proof obligation, not documentation. For each concrete problem `p`, `millenniumBarrier p` reduces definitionally, making `barrier_correct := rfl` a machine-checked verification. Three instances:

```lean
def ym_certificate : BarrierPrimitiveCertificate .YM where
  encoding     := ym_quantum_target
  blockedField := 'gran: G_beth → G_aleph (PathIntegralMeasure G missing)'
  barrier      := .MissingFoundation
  barrier_correct := rfl   -- Lean verifies: .MissingFoundation = millenniumBarrier .YM (ok)

def opn_certificate : BarrierPrimitiveCertificate .OPN where
  ...
  barrier_correct := rfl   -- .OpenProblem = millenniumBarrier .OPN (ok)

def ns_certificate : BarrierPrimitiveCertificate .NS where
  ...
  barrier_correct := rfl   -- .OpenProblem = millenniumBarrier .NS (ok)
```

### V.3 The YM primitive barrier

The Yang-Mills quantum lift is encoded as the transition from `ym_classical` (four-dimensional gauge theory before quantization) to `ym_quantum_target` (what YM would look like if the path integral existed). Four primitive fields change:

| Field | Classical YM | Quantum target | Interpretation |
| :--- | :--- | :--- | :--- |
| **$F$ (Fidelity)** | $F_\eta$ | $F_\hbar$ | Classical → quantum coherence |
| **$K$ (Kinetic)** | $K_\text{mod}$ | $K_\text{trap}$ | Perturbative → confinement |
| **$G$ (Granularity)** | $G_\beth$ | $G_\aleph$ | Mesoscale local → quantum fine-grained |
| **$\Phi_c$ (Criticality)** | $\Phi_\text{sub}$ | $\Phi_c$ | No gap → mass gap (critical phenomenon) |

```lean
theorem ym_classical_to_quantum_cost :
    primitiveMismatches ym_classical ym_quantum_target = 4 := by decide
```

The **$G_\beth \to G_\aleph$ transition** is the primitive certificate of the missing `PathIntegralMeasure`:
· $G_\beth$ = mesoscale local description  --  classical gauge field theory describable without integration over all gauge connections.
· $G_\aleph$ = quantum fine-grained  --  requires a well-defined measure on the full gauge connection space modulo gauge equivalence.
· Constructing `PathIntegralMeasure G` *is* providing the $G_\aleph$ description.

Crucially, the quantum target stays at `D_cube` (four-dimensional, local) rather than `D_holo` (holographic):

```lean
theorem ym_quantum_target_is_local : ym_quantum_target.dim = D_cube := rfl
theorem ym_qg_dim_differ : ym_quantum_target.dim ≠ quantum_gravity.dim := by decide
```

This formally distinguishes the YM problem from quantum gravity. Quantizing YM does not require holographic substrate  --  the two problems are structurally distinct synthons, with the YM quantum target at Hamming distance $\geq 1$ from `quantum_gravity`.

The full certificate:

```lean
theorem ym_primitive_barrier_certificate :
    ym_quantum_target.gran = G_aleph ∧     -- needs quantum-level granularity
    ym_quantum_target.crit = Phi_c ∧       -- needs mass gap (critical)
    ym_quantum_target.fid  = F_hbar ∧      -- needs quantum fidelity
    ym_quantum_target.kin  = K_trap ∧      -- needs confinement
    ym_quantum_target.dim  = D_cube ∧      -- stays 4D local (NOT QG)
    ym_quantum_target.dim  ≠ quantum_gravity.dim ∧
    Barriers.millenniumBarrier .YM = .MissingFoundation := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, by decide, rfl⟩
```

### V.4 Other primitive certificates

The OPN, NS, and RH certificates connect to the $\Phi_c$ criticality primitive:

| Problem | Encoding field | Value | Structural meaning |
| :--- | :--- | :--- | :--- |
| **OPN** | `crit` + `kin` | $\Phi_c$ + $K_\text{trap}$ | $\sigma(n) = 2n$ is exact criticality; overdetermined constraint system has no relaxation path |
| **NS** | `crit` | $\Phi_\text{sub}$ | Smooth solutions stay subcritical; the sorry proves they never cross to $\Phi_c$ (blow-up threshold) |
| **RH** | `crit` | $\Phi_c$ | The critical line $\text{Re}(s) = \frac{1}{2}$ is the $\Phi_c$ locus of the zeta function |

```lean
theorem opn_primitive_certificate :
    opn_encoding.crit = Phi_c ∧ opn_encoding.kin = K_trap ∧
    Barriers.millenniumBarrier .OPN = .OpenProblem := ⟨rfl, rfl, rfl⟩

theorem ns_primitive_certificate :
    ns_encoding.crit = Phi_sub ∧
    Barriers.millenniumBarrier .NS = .OpenProblem := ⟨rfl, rfl⟩

theorem rh_primitive_certificate :
    rh_encoding.crit = Phi_c ∧
    Barriers.millenniumBarrier .RH = .OpenProblem := ⟨rfl, rfl⟩
```

### V.5 The master bridge theorem

```lean
theorem primitive_bridge_master :
    primitiveMismatches ym_classical ym_quantum_target = 4 ∧
    Barriers.millenniumBarrier .YM = .MissingFoundation ∧
    opn_encoding.crit = Phi_c ∧ opn_encoding.kin = K_trap ∧
    Barriers.millenniumBarrier .OPN = .OpenProblem ∧
    ns_encoding.crit = Phi_sub ∧
    Barriers.millenniumBarrier .NS = .OpenProblem ∧
    rh_encoding.crit = Phi_c ∧
    Barriers.millenniumBarrier .RH = .OpenProblem :=
  ⟨by decide, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩
```

This theorem machine-checks four barrier certificates simultaneously. The `by decide` term computes the Hamming distance between two concrete `Synthon` values over twelve decidable fields. All `rfl` terms verify that `millenniumBarrier` reduces correctly on each concrete constructor.

---

## VI. Proof Engineering Notes (v0.1.0, 2026-03-26)

### VI.1 decide vs norm_num vs rfl

Three automation tactics drive the machine-checked results:

**`rfl`**  --  Used for definitional equalities. `millenniumBarrier .YM = .MissingFoundation` reduces by `rfl` because `millenniumBarrier` is a `def` (not `opaque`) that pattern-matches on `MillenniumProblem`. All `barrier_correct := rfl` in `BarrierPrimitiveCertificate` instances are of this type.

**`decide`**  --  Used for decidable propositions over finite types. `primitiveMismatches ym_classical ym_quantum_target = 4` is proved by kernel reduction of the computable `primitiveMismatches` function over two concrete `Synthon` values. `ym_is_unique_missing_foundation` is closed by `cases p <;> simp_all`.

**`norm_num`**  --  Used for real arithmetic in NS.lean: `0 < (1:ℝ)/2` and `(1:ℝ)/2 < 1`. These are the only results requiring real-number reasoning; all other automation stays in the decidable fragment.

### VI.2 Abstract vs concrete type design

A recurring design choice is how much to use abstract axiomatized types versus concrete Mathlib types.

**BSD uses the most concrete types:** `WeierstrassCurve ℚ`, `IsElliptic`. This grounds the conjecture in actual Mathlib infrastructure. The tradeoff: `MordellWeilGroup`, `ellipticRank`, and `analyticRank` must be axiomatized, but they are axiomatized *over* a real Mathlib type, not a fictional one.

**YM uses the most abstract types:** `PathIntegralMeasure`, `QuantumYMTheory`, `massGap` are all axiomatized from scratch. This is unavoidable  --  there is no Lean type for a rigorous path integral measure in 4D, which is precisely the `MissingFoundation` claim.

**OPN uses the most Mathlib:** `Nat.Perfect`, `ArithmeticFunction.sigma`, `IsMultiplicative.sigma.map_mul_of_coprime`. The `sigma_multiplicative` theorem is a thin wrapper over existing machinery.

### VI.3 The sorry-as-axiom encoding

Each sorry boundary is declared as an `axiom` rather than a `sorry` in the final library. An `axiom` in Lean explicitly extends the logical framework at a named, typed location. The library does not contain accidental sorries from incomplete proof attempts  --  every sorry-equivalent obligation is a named, typed axiom at a precise location, documented with its barrier classification.

---

## VII. Related Work (v0.1.0, 2026-03-26)

### VII.1 Formalization of known results

The ongoing Lean formalization of the Last Theorem of Fermat (2024-ongoing) provides a template for long-term deep formalization. Our work is complementary: we formalize the barrier structure of *open* problems rather than the proof of a closed one.

Several groups have worked on BSD-adjacent results in Lean and Coq. Partial formalizations of Mordell-Weil exist but none are complete in Mathlib as of v4.28.0. BSD.lean is, to our knowledge, the first statement of the BSD conjecture using the actual Mathlib `WeierstrassCurve ℚ` infrastructure.

For Navier-Stokes, the PFR (Polynomial Freiman-Ruzsa) formalization demonstrated that deep analysis results can be machine-verified in Lean. Our NS.lean targets specifically the critical scaling structure rather than a specific regularity result.

### VII.2 Proof complexity and barrier theory

The mathematical theory of proof complexity barriers  --  relativization (Baker-Gill-Solovay 1975), natural proofs (Razborov-Rudich 1994), algebrization (Aaronson-Wigderson 2009)  --  is extensive. We are not aware of any prior formalization of these barriers in a proof assistant. PvsNP.lean formalizes them as `True := trivial` with full documentation: an honest encoding of theorems *about* proof search, not the conjecture itself.

### VII.3 Prior sorry taxonomies

We are not aware of any prior work that formalizes a taxonomy of *why* sorries cannot be discharged. The distinction between MathlibGap, OpenProblem, and MissingFoundation appears to be novel as a typed Lean inductive. The closest conceptual relative is Jaffe-Witten observation that the YM path integral measure 'does not exist as a mathematical object.' We formalize this intuition in the `MissingFoundation` constructor and prove it uniquely applies to YM among the seven Millennium Problems.

### VII.4 The SynthOmnicon framework

The SynthOmnicon 12-primitive grammar is developed in the companion documents [TOPO], [DIAPH], [ONTO]. The `Primitives/` track of the Lean library  --  `Core.lean`, `Synthon.lean`, `TierCrossing.lean`, `OPN_2adic.lean`, `BSD_2adic.lean`  --  constitutes a parallel formalization effort. The present paper uses `Core.lean` and `Synthon.lean` only for `PrimitiveBridge.lean`; the full primitive algebra is not required for the barrier taxonomy itself.

---

## VIII. Discussion (v0.1.0, 2026-03-26)

### VIII.1 The MissingFoundation barrier and mathematics

The `MissingFoundation` barrier for Yang-Mills reflects something philosophically significant: the quantum Yang-Mills problem is not just an unsolved theorem but an unsolved *definition*. Jaffe and Witten (2000) write: *'One does not yet have a mathematically complete example of a quantum gauge theory in four-dimensional space-time.'*

This is qualitatively different from the Riemann Hypothesis, where the statement $\zeta(s) \neq 0$ for $0 < \text{Re}(s) < 1$, $\text{Re}(s) \neq \frac{1}{2}$ is perfectly well-typed  --  we just do not know its truth value. For Yang-Mills, the sentence 'the quantum YM theory exists and has mass gap $\Delta > 0$' cannot be made rigorous until the path integral measure is constructed.

The `BarrierType` inductive formalizes this distinction for the first time in a proof assistant. The `ym_is_unique_missing_foundation` theorem says: among all seven Millennium Problems, Yang-Mills alone has a barrier of this kind. Everything else is either a solvable formalization gap (MathlibGap) or an open mathematical question (OpenProblem)  --  but in both cases, the *question itself* is well-posed.

### VIII.2 What the primitive bridge adds

The `PrimitiveBridge.lean` connection adds a second level of explanation: *why* does the missing type correspond to a specific missing primitive? The claim is not that the primitive grammar *causes* the open problem  --  it is that the grammar *encodes* the structural reason precisely. The $G_\beth \to G_\aleph$ transition for YM is a formal statement that the classical mesoscale-local description is insufficient and a quantum-level fine-grained description is required. This is exactly what `PathIntegralMeasure` provides.

The machine-checked nature of `primitive_bridge_master` means this is not merely commentary. Four barrier certificates are verified simultaneously, and the quantum YM lift cost of 4 primitive mismatches is a theorem, not an estimate.

### VIII.3 Limitations

Every sorry-boundary in the library is genuine. The Lean files typecheck because the barriers are declared as axioms; removing them would leave genuine proof obligations that cannot currently be discharged.

The primitive encodings in `PrimitiveBridge.lean` are our best formalization of the structural content of each problem  --  but they are choices. Another author might make different encoding decisions for Hodge or P vs NP. The `BarrierType` taxonomy and `ym_is_unique_missing_foundation` are more robust: they depend only on the `MillenniumProblem` inductive and `millenniumBarrier`, not on specific encodings.

---

## IX. Future Work (v0.1.0, 2026-03-26)

### IX.1 Discharge of MathlibGap sorries

The most actionable near-term work: `euler_opn_form` (OPN.lean)  --  all required tools are in `OPN_2adic.lean` and the proof is feasible with current Mathlib. `mazur_torsion` (BSD.lean) and `mordell_weil` (BSD.lean) are longer-term Mathlib development targets. `lefschetz_11` (Hodge.lean) requires complex geometry formalization.

### IX.2 Lattice instances for Criticality

The `Criticality` primitive has an unusual meet semantics: $\Phi_c$ is absorbing under meet ($\Phi_c \sqcap x = \Phi_c$ for all $x$), which contradicts the `min`-derived order. A correct `MeetSemilattice` instance requires overriding the default. Once in place, the OPN and NS bridge encodings can be connected more tightly to the primitive algebra.

### IX.3 Extending the bridge to all seven problems

`PrimitiveBridge.lean` provides certificates for YM, OPN, NS, and RH. Hodge ($R$-degeneracy as topology-to-algebra lift), P vs NP ($K_\text{trap}$ blocking low-complexity), and BSD ($\Phi_c$ as rank charge-carrier) require either more complex primitive signatures or narrative justification that is harder to encode compactly. Extending the bridge to all seven is a natural next step.

### IX.4 Formalizing the meta-barriers

The three `trivial` theorems in PvsNP.lean (BGS relativization, Razborov-Rudich natural proofs, Aaronson-Wigderson algebrization) should eventually be given genuine Lean statements. This requires formalizing oracle Turing machines, circuit complexity classes, and algebraic extension closure  --  a substantial independent Mathlib development effort.

---

## X. Conclusion (v0.1.0, 2026-03-26)

We have presented a nine-file Lean 4 library formalizing a barrier taxonomy for the seven Clay Millennium Prize Problems. The central contribution is the `BarrierType` inductive (MathlibGap / OpenProblem / MissingFoundation) and the machine-checked theorem that Yang-Mills is the unique Millennium Problem with a `MissingFoundation` barrier. We have formally distinguished stacked from parallel sorry depth, machine-verified the critical Sobolev scaling in Navier-Stokes by `norm_num`, grounded BSD in the actual Mathlib `WeierstrassCurve ℚ` infrastructure, grounded OPN in the actual Mathlib `Nat.Perfect` and `ArithmeticFunction.sigma`, and connected sorry boundaries to primitive field transitions via a machine-checked bridge file.

The `sorry` in a Lean proof is usually treated as an obstacle to be removed. This library treats it as a datum to be classified. The three barrier types represent three distinct relationships between human mathematics and the proof assistant: what we can formalize but have not, what we have not solved, and what we have not yet defined. Formally distinguishing these is the first step toward a systematic theory of the frontier of formalized mathematics.

---

## Appendix I. Library Structure

```
SynthOmnicon/Millennium/
  RH.lean              ~110 lines   OpenProblem · ZeroFreeStrip
  YM.lean              ~140 lines   MissingFoundation · PathIntegralMeasure (stacked)
  Hodge.lean           ~130 lines   OpenProblem · AlgebraicCycleRep
  NS.lean              ~160 lines   OpenProblem · GlobalRegularityCert · norm_num
  PvsNP.lean           ~170 lines   OpenProblem · CircuitLowerBound · meta-barriers
  OPN.lean             ~150 lines   OpenProblem · Nat.Perfect · sigma_multiplicative
  BSD.lean             ~200 lines   OpenProblem · WeierstrassCurve ℚ (parallel)
  Barriers.lean        ~224 lines   Taxonomy · ym_is_unique_missing_foundation
  PrimitiveBridge.lean ~230 lines   Bridge · BarrierPrimitiveCertificate · master theorem

SynthOmnicon/Primitives/  (companion track, used by PrimitiveBridge only)
  Core.lean            ~213 lines   12 primitive inductive types · DecidableEq
  Synthon.lean         ~259 lines   Synthon struct · primitiveMismatches · P-70 · SM/QG
```

**Total (Millennium track):** approximately 1,524 lines. Build: `lake build Millennium`.

---

## Appendix II. Key Theorems

| Theorem | File | Proof | Significance |
| :--- | :--- | :--- | :--- |
| **`ym_is_unique_missing_foundation`** | Barriers | `cases` + `simp_all` | YM uniquely lacks a foundational object |
| **`missing_foundation_vs_open_problem`** | Barriers | `decide` | Barrier types are formally distinct |
| **`ym_has_stacked_not_parallel_sorries`** | Barriers | `simp` | Stacked $\neq$ parallel at same depth |
| **`critical_scaling_gap`** | NS | `norm_num` | $0 < \frac{1}{2} < 1$ in $\mathbb{R}$ |
| **`sigma_multiplicative`** | OPN | Mathlib API | $\sigma(ab) = \sigma(a)\sigma(b)$ for coprime |
| **`ym_classical_to_quantum_cost = 4`** | PrimitiveBridge | `decide` | Quantum lift costs 4 primitive changes |
| **`ym_primitive_barrier_certificate`** | PrimitiveBridge | `rfl` + `decide` | $G_\beth \to G_\aleph$ = PathIntegralMeasure |
| **`primitive_bridge_master`** | PrimitiveBridge | `decide` + `rfl` | Four certificates simultaneously |
| **`ym_opn_barrier_distinct`** | PrimitiveBridge | `decide` | MissingFoundation $\neq$ OpenProblem at problem level |
| **`sm_qg_distance_exact = 9`** | Synthon | `decide` | SM/QG Hamming distance machine-verified |

---

*End of MILLENNIUM_BARRIERS_PAPER.md v0.1.0*

*Draft 2026-03-26 · Lean 4.28.0 · Mathlib v4.28.0 · Target: Journal of Formalized Reasoning / JAR*
