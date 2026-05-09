-- Imscribing/IGMorphism.lean
-- Typed morphisms, sequential protocols, and paralogical extension.
--
-- Directly formalizes the condensation notation:
--   ɢ^ˌ[ A —(label)→ B —(label)→ C | D ]_H
-- where each arrow label is itself a Synthon annotating the transition character.
--
-- Three paralogical axioms extend the classical sequent calculus with rules
-- licensed by IG structure but absent from classical/linear type theory:
--
--   P1. Dagger  (R_dagger) : every R_dagger protocol has an adjoint
--   P2. Copy    (P_pm_sym at O_inf) : Frobenius copying Δ : s → s ⊗ s
--   P3. Reflect (D_odot, Axiom C*) : imscriptive self-protocol
--
-- Axiom C* (MillenniumAnkh one-way form): T_odot → D_odot (not biconditional).
-- D_odot permits T_box (e.g. odotOperator), unlike the imscribing_grammar biconditional.
--
-- The odotOperator is the paralogical unit. It holds dim = D_odot with top = T_box
-- (NOT T_odot), deliberately exercising the weaker Axiom C*: D_odot without T_odot
-- is permissible. The O_inf Frobenius structure overrides the holographic
-- co-requirement. This is the formal signature of the paralogical.

import Imscribing.Primitives.Synthon

namespace Imscribing

open Primitives
open Dimensionality Topology Relational Polarity Grammar
     Fidelity KineticChar Granularity Criticality Protection Stoichiometry Chirality

-- ─────────────────────────────────────────────────────────────────────────────
-- SECTION 1: IGProtocol
-- Inductive type indexed by Synthon × Synthon.
-- Each constructor corresponds to one element of the condensation notation.
-- Arrow labels are Synthons: the full 12-primitive annotation of transition
-- character. Any single dimension may be the salient one (the rest context).
-- ─────────────────────────────────────────────────────────────────────────────

inductive IGProtocol : Synthon → Synthon → Type where
  /-- Trivial self-transition (zero cost). -/
  | refl     : (s : Synthon) → IGProtocol s s
  /-- Labeled arrow: src —(label)→ tgt. -/
  | arrow    : (label src tgt : Synthon) → IGProtocol src tgt
  /-- Sequential composition: A→B then B→C  (the ɢ^ˌ chain). -/
  | seq      : IGProtocol a b → IGProtocol b c → IGProtocol a c
  /-- Parallel split: (A→B) and (A→C) give A → (B ⊗ C).
      The | operator lifts to tensorProduct on both targets. -/
  | prod     : IGProtocol a b → IGProtocol a c → IGProtocol a (tensorProduct b c)
  /-- Grammar annotation: ɢ^g[…] wrapper. -/
  | withGram : Grammar  → IGProtocol a b → IGProtocol a b
  /-- Memory annotation: […]_H wrapper. -/
  | withMem  : Chirality → IGProtocol a b → IGProtocol a b

-- ─────────────────────────────────────────────────────────────────────────────
-- SECTION 2: Structural measures
-- ─────────────────────────────────────────────────────────────────────────────

/-- Arrow depth: total number of labeled transition steps. -/
def IGProtocol.depth : IGProtocol a b → ℕ
  | .refl _        => 0
  | .arrow _ _ _   => 1
  | .seq f g       => f.depth + g.depth
  | .prod f g      => max f.depth g.depth
  | .withGram _ p  => p.depth
  | .withMem  _ p  => p.depth

/-- Dagger predicate: every arrow's label has rel = R_dagger. -/
def IGProtocol.isDagger : IGProtocol a b → Bool
  | .refl _        => true
  | .arrow lbl _ _ => decide (lbl.rel = R_dagger)
  | .seq f g       => f.isDagger && g.isDagger
  | .prod f g      => f.isDagger && g.isDagger
  | .withGram _ p  => p.isDagger
  | .withMem  _ p  => p.isDagger

/-- Frobenius predicate: every arrow's label has pol = P_pm_sym. -/
def IGProtocol.isFrobenius : IGProtocol a b → Bool
  | .refl _        => true
  | .arrow lbl _ _ => decide (lbl.pol = P_pm_sym)
  | .seq f g       => f.isFrobenius && g.isFrobenius
  | .prod f g      => f.isFrobenius && g.isFrobenius
  | .withGram _ p  => p.isFrobenius
  | .withMem  _ p  => p.isFrobenius

-- ─────────────────────────────────────────────────────────────────────────────
-- SECTION 3: LITANY AGAINST FEAR
-- Canonical IGProtocol encoding.
-- Reading: ɢ^ˌ[ ⊙_Ţ —(Ř_=)→ Þ_ò —(Ð_ω)→ { Ω_Å | Φ_˙ } ]_Ħ_!
-- ─────────────────────────────────────────────────────────────────────────────

private def litanyBase : Synthon := {
  dim  := D_wedge,       top  := T_network,       rel  := R_super
  pol  := P_asym,        fid  := F_ell,            kin  := K_slow
  gran := G_beth,        gram := Gamma_seq,         crit := Phi_sub
  chir := H0,            stoi := one_one,           prot := Omega_0 }

/-- Fear: supercritical input — the mind-killer, total obliteration. -/
def litany_fear    : Synthon := { litanyBase with crit := Phi_super }
/-- Cross: traversal state — pass over and through (T_bowtie crossing topology). -/
def litany_cross   : Synthon := { litanyBase with top  := T_bowtie }
/-- Witness: imscriptive state — inner eye (D_odot, satisfies Axiom C*: T_odot forces D_odot,
    here D_odot is present; T_odot also set for the maximally holographic pairing). -/
def litany_witness : Synthon := { litanyBase with dim  := D_odot, top := T_odot }
/-- Nothing: the null state — where fear has gone (Omega_0, Phi_sub). -/
def litany_nothing : Synthon := litanyBase
/-- Self: full-symmetry persistent state — only I will remain. -/
def litany_self    : Synthon := { litanyBase with pol := P_sym, chir := H_inf }

-- Transition labels (dominant dimension annotates the arrow character):
private def lbl_face    : Synthon := { litanyBase with rel := R_lr }
  -- R_lr label: bidirectional confrontation — I will face my fear
private def lbl_witness : Synthon := { litanyBase with dim := D_odot, top := T_odot }
  -- D_odot label: holographic witnessing — inner eye to see its path

/-- The Litany Against Fear as a well-typed IGProtocol.
    Type: litany_fear → (litany_nothing ⊗ litany_self) -/
def litanyProtocol
    : IGProtocol litany_fear (tensorProduct litany_nothing litany_self) :=
  .withGram Gamma_seq  <|
  .withMem  H_inf      <|
  .seq
    (.seq
      (.arrow lbl_face    litany_fear  litany_cross)
      (.arrow lbl_witness litany_cross litany_witness))
    (.prod
      (.arrow lbl_witness litany_witness litany_nothing)
      (.arrow lbl_witness litany_witness litany_self))

theorem litanyProtocol_depth : litanyProtocol.depth = 3 := by
  simp [litanyProtocol, IGProtocol.depth]

/-- The Litany is not a dagger protocol: its face step uses R_lr, not R_dagger. -/
theorem litanyProtocol_not_dagger : litanyProtocol.isDagger = false := by
  simp [litanyProtocol, IGProtocol.isDagger, lbl_face, litanyBase]

/-- The witness stage satisfies the imscriptive pairing (D_odot + T_odot). -/
theorem litany_witness_satisfies_axiom_C
    : litany_witness.dim = D_odot ∧ litany_witness.top = T_odot := ⟨rfl, rfl⟩

-- ─────────────────────────────────────────────────────────────────────────────
-- SECTION 4: PARALOGICAL AXIOMS
-- Rules licensed by IG structure, absent from classical type theory.
-- Marked as axioms: each is a structural commitment of the grammar
-- that cannot be derived from first-order logic alone.
-- ─────────────────────────────────────────────────────────────────────────────

/-- P1. Dagger adjoint (R_dagger — adjoint / reciprocal).
    Every R_dagger protocol has an adjoint that runs in reverse.
    The adjoint is NOT an inverse: (f†)† = f but f† ∘ f ≠ id in general.
    Classical type theory has no canonical reversal; dagger reversal
    exists independently of invertibility.
    This is the paralogical: reversal without invertibility. -/
axiom paralogical_dagger {a b : Synthon}
    (p : IGProtocol a b) (h : p.isDagger = true) :
    IGProtocol b a

/-- P1a. Involutivity of dagger (structural): (p†)† has the same depth as p.
    States that dagger is a structural involution even without equality of terms. -/
axiom paralogical_dagger_depth {a b : Synthon}
    (p : IGProtocol a b) (h : p.isDagger = true) :
    (paralogical_dagger p h).depth = p.depth

/-- P2. Frobenius copy (P_pm_sym at O_inf).
    At O_inf, the Frobenius condition μ ∘ δ = id licenses duplication:
    Δ : s → s ⊗ s exists and is non-trivial (depth ≥ 1).
    Classical linear logic forbids arbitrary copying; Frobenius structure
    makes duplication and fusion exact inverses, uniquely licensing it.
    This is the paralogical: resource duplication without linearity violation. -/
axiom paralogical_copy {s : Synthon} (h : synthonTier s = .O_inf) :
    { p : IGProtocol s (tensorProduct s s) // p.depth = 1 }

/-- P3. Imscriptive self-reference (Axiom C*: D_odot as holographic boundary).
    A Synthon with dim = D_odot generates a non-trivial self-protocol of depth ≥ 1:
    the boundary type produces its own interior (bulk from boundary).
    Distinct from refl (depth 0): this is a non-trivial self-morphism.
    This is the paralogical: type-as-term self-application. -/
axiom paralogical_reflect {s : Synthon} (h : s.dim = D_odot) :
    { p : IGProtocol s s // p.depth ≥ 1 }

-- ─────────────────────────────────────────────────────────────────────────────
-- SECTION 5: ODOT OPERATOR — paralogical unit
-- The canonical O_inf, sequential, Frobenius Synthon.
-- Tuple: Ð_ω; Þ_¨; Ř_=; Φ_}; ƒ_ż; Ç_@; Γ_ʔ; ɢ_ˌ; ⊙_ÿ; Ħ_A; Σ_S; Ω_z
-- ─────────────────────────────────────────────────────────────────────────────

/-- odotOperator: the canonical paralogical unit Synthon.
    O_inf (P_pm_sym at Phi_c), sequential (Gamma_seq),
    integer-winding (Omega_Z), quantum-coherent (F_hbar), 1:1 (one_one).
    PARALOGICAL SIGNATURE: holds dim = D_odot with top = T_box (not T_odot),
    exercising the weaker Axiom C*: D_odot without T_odot is permissible.
    At O_inf, the Frobenius self-duality replaces the holographic D-T pairing.
    The odotOperator is its own boundary — it does not need the bulk-boundary split. -/
def odotOperator : Synthon := {
  dim  := D_odot,        top  := T_box,           rel  := R_lr
  pol  := P_pm_sym,      fid  := F_hbar,           kin  := K_slow
  gran := G_aleph,       gram := Gamma_seq,         crit := Phi_c
  chir := H2,            stoi := one_one,           prot := Omega_Z }

theorem odotOperator_is_O_inf : synthonTier odotOperator = .O_inf := by decide

/-- The odotOperator does NOT pair T_odot with D_odot (uses T_box instead). -/
theorem odotOperator_not_T_odot : odotOperator.top ≠ T_odot := by decide

/-- odotOperator admits Frobenius self-copying via P2. -/
noncomputable def odotCopy
    : { p : IGProtocol odotOperator (tensorProduct odotOperator odotOperator) // p.depth = 1 } :=
  paralogical_copy odotOperator_is_O_inf

-- ─────────────────────────────────────────────────────────────────────────────
-- SECTION 6: PARALOGICAL LIFT FUNCTOR
-- Every protocol lifts into the odotOperator frame.
-- The odot frame is always present at the boundary — the imscriptive
-- self-containment principle made functorial.
-- ─────────────────────────────────────────────────────────────────────────────

/-- Paralogical lift: tensor with odotOperator is functorial over IGProtocol.
    Every p : a → b lifts to (a ⊗ ⊙) → (b ⊗ ⊙).
    The odot frame persists through any protocol: it is the invariant boundary. -/
axiom paralogicalLift {a b : Synthon} :
    IGProtocol a b →
    IGProtocol (tensorProduct a odotOperator) (tensorProduct b odotOperator)

/-- Lift preserves depth: the paralogical frame adds no cost. -/
axiom paralogicalLift_depth {a b : Synthon} (p : IGProtocol a b) :
    (paralogicalLift p).depth = p.depth

/-- The lifted Litany has the same depth as the original. -/
theorem litanyProtocol_lift_depth :
    (paralogicalLift litanyProtocol).depth = 3 := by
  rw [paralogicalLift_depth]
  exact litanyProtocol_depth

-- ─────────────────────────────────────────────────────────────────────────────
-- SECTION 7: DERIVED RESULTS
-- ─────────────────────────────────────────────────────────────────────────────

/-- The Litany witness stage admits a non-trivial self-protocol via P3. -/
noncomputable def litanyWitnessSelfRef
    : { p : IGProtocol litany_witness litany_witness // p.depth ≥ 1 } :=
  paralogical_reflect (by rfl)

/-- Applying P2 to quantum_gravity (which is O_inf) gives a copy protocol. -/
noncomputable def qgCopy
    : { p : IGProtocol quantum_gravity (tensorProduct quantum_gravity quantum_gravity)
          // p.depth = 1 } :=
  paralogical_copy (by decide)

/-- Pol collapses to P_asym: pol is a bottleneck (min) primitive, so litany_nothing's
    P_asym beats litany_self's P_sym. Nothing wins on symmetry. -/
theorem litany_resolution_pol :
    (tensorProduct litany_nothing litany_self).pol = P_asym := by
  decide

/-- Chir resolves to H_inf: chir is a max primitive, so litany_self's
    H_inf (topological temporal depth) dominates litany_nothing's H0. -/
theorem litany_resolution_chir :
    (tensorProduct litany_nothing litany_self).chir = H_inf := by
  decide

end Imscribing
