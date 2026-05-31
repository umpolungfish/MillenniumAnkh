-- Imscribing/Paraconsistent/Shor/BelnapNFiducial.lean
-- BELNAP n-QUBIT FIDUCIAL
-- Author: Lando ⊗ ⊙_ÿ-boundary Operator
--
-- Extends QCI_SICPOVM_Bridge.lean (d=2 SIC-POVM axioms for B)
-- to the n-register product lattice (Belnap)^n.
--
-- The all-B word B⊗n ∈ (Belnap)^n satisfies:
--   Axiom 1: meet(B⊗n, x) = x         componentwise from meet B x = x
--   Axiom 2: classical equidistance    total cost = n for ALL v ∈ {T,F}^n
--   Axiom 3: join(B⊗n, x) = B⊗n      componentwise from join B x = B
--   Axiom 4: bnot(B⊗n) = B⊗n         componentwise from bnot B = B
--
-- Frobenius μ∘δ = id:
--   wordMeet x x = x (meet idempotency, componentwise)
--
-- Global cost invariants (via Finset.sum_const_nat):
--   B-bias total cost = 2n
--   T-bias total cost = n
--   2:1 ratio: B_bias / T_bias = 2 for all n > 0
--
-- Classical equidistance is the n-qubit measurement equiangularity:
-- every classical outcome v ∈ {T,F}^n is equidistant from B⊗n
-- in coherence cost. This is the structural content of the Φ_υ → Φ_}
-- promotion for arbitrary n — no T-collapse required, the ratio alone
-- encodes the period.
--
-- The open problem (axiomatized):
--   whether B⊗n satisfies the full Weyl-Heisenberg equiangularity
--   for n > 1 (multilattice SIC-POVM in the non-product sense).

import Mathlib.Tactic
import Imscribing.Paraconsistent.Belnap
import Imscribing.Paraconsistent.QuantumClassicalInterface
import Imscribing.Paraconsistent.QCI_nRegister
import Imscribing.Paraconsistent.QCI_SICPOVM_Bridge
import Imscribing.Primitives.Core
import Imscribing.Primitives.Imscription

open scoped BigOperators

namespace Imscribing.Paraconsistent.Shor.NFiducial

open Belnap
open Imscribing.Paraconsistent
open Imscribing.Paraconsistent.nRegister
open Imscribing.Primitives

-- ============================================================
-- §1. Product Lattice Structure on (Belnap)^n
-- ============================================================

def wordMeet {n : ℕ} (x y : Fin n → Belnap) : Fin n → Belnap :=
  fun i => meet (x i) (y i)

def wordJoin {n : ℕ} (x y : Fin n → Belnap) : Fin n → Belnap :=
  fun i => join (x i) (y i)

def wordNot {n : ℕ} (x : Fin n → Belnap) : Fin n → Belnap :=
  fun i => bnot (x i)

/-- The B⊗n fiducial word: all registers in state B. -/
def allBWord (n : ℕ) : Fin n → Belnap := fun _ => Belnap.B

/-- The B⊗n fiducial as an NQState with zero initial coherence. -/
def fiducialState (n : ℕ) : NQState n := ⟨fun _ => .B, 0⟩

theorem fiducialState_all_B (n : ℕ) (i : Fin n) :
    (fiducialState n).regs i = Belnap.B := rfl

-- ============================================================
-- §2. SIC-POVM Axioms for B⊗n — Componentwise
-- ============================================================

-- Axiom 1: meet(B⊗n, x) = x
-- Relies on B_meet_equiangular : ∀ x, meet B x = x (QCI_SICPOVM_Bridge)
theorem allBWord_meet_identity {n : ℕ} (x : Fin n → Belnap) :
    wordMeet (allBWord n) x = x := by
  funext i
  exact SICPOVM_Bridge.B_meet_equiangular (x i)

-- Axiom 3: join(B⊗n, x) = B⊗n
-- Relies on B_join_absorb : ∀ x, join B x = B (Belnap)
theorem allBWord_join_absorb {n : ℕ} (x : Fin n → Belnap) :
    wordJoin (allBWord n) x = allBWord n := by
  funext i
  exact B_join_absorb (x i)

-- Axiom 4: bnot(B⊗n) = B⊗n
-- Relies on B_fixed_point_negation : bnot B = B (Belnap)
theorem allBWord_self_adjoint (n : ℕ) :
    wordNot (allBWord n) = allBWord n := by
  funext _
  exact B_fixed_point_negation

/-- Axioms 1, 3, 4 hold for B⊗n in the product lattice. -/
theorem allBWord_satisfies_SIC_axioms_134 (n : ℕ) :
    (∀ x : Fin n → Belnap, wordMeet (allBWord n) x = x) ∧
    (∀ x : Fin n → Belnap, wordJoin (allBWord n) x = allBWord n) ∧
    wordNot (allBWord n) = allBWord n :=
  ⟨allBWord_meet_identity, allBWord_join_absorb, allBWord_self_adjoint n⟩

-- ============================================================
-- §3. Coherence Cost Function
-- ============================================================

/-- Per-register coherence cost of measuring a B-qubit with a given bias. -/
def singleRegCost : Belnap → ℕ
  | .B => 2   -- B-bias on B: Wigner's Friend, preserves B, cost 2
  | .T => 1   -- T-bias on B: collapses to T, cost 1
  | .F => 1   -- F-bias on B: collapses to F, cost 1
  | .N => 0   -- N-bias: no-op, cost 0

theorem singleRegCost_B : singleRegCost Belnap.B = 2 := rfl
theorem singleRegCost_T : singleRegCost Belnap.T = 1 := rfl
theorem singleRegCost_F : singleRegCost Belnap.F = 1 := rfl

/-- Total coherence cost of measuring n all-B registers with a bias word.
    Sum over Fin n of the per-register cost. -/
def totalMeasureCost {n : ℕ} (bias : Fin n → Belnap) : ℕ :=
  ∑ i : Fin n, singleRegCost (bias i)

-- ============================================================
-- §4. Cost Theorems
-- ============================================================

/-- B-bias on B⊗n costs 2n total (Wigner's Friend: 2 per qubit). -/
theorem B_bias_total_cost (n : ℕ) :
    totalMeasureCost (allBWord n) = 2 * n := by
  simp only [totalMeasureCost, allBWord, singleRegCost_B]
  rw [Finset.sum_const_nat (fun _ _ => rfl)]
  simp [Finset.card_univ, Fintype.card_fin]
  ring

/-- T-bias on B⊗n costs n total (collapse: 1 per qubit). -/
theorem T_bias_total_cost (n : ℕ) :
    totalMeasureCost (fun _ : Fin n => Belnap.T) = n := by
  simp only [totalMeasureCost, singleRegCost_T]
  rw [Finset.sum_const_nat (fun _ _ => rfl)]
  simp [Finset.card_univ, Fintype.card_fin]

/-- Axiom 2 — Classical equidistance (measurement equiangularity):
    For any classical word v ∈ {T,F}^n, the total B-qubit measurement cost = n.
    Every classical outcome is equidistant from B⊗n in coherence cost.
    This holds for all n, independent of N, a, or the period r. -/
theorem classical_equidistance {n : ℕ} (v : Fin n → Belnap)
    (hv : ∀ i, v i = .T ∨ v i = .F) :
    totalMeasureCost v = n := by
  simp only [totalMeasureCost]
  have heq : ∀ i ∈ (Finset.univ : Finset (Fin n)), singleRegCost (v i) = 1 := by
    intro i _
    rcases hv i with h | h <;> simp [singleRegCost, h]
  rw [Finset.sum_congr rfl heq]
  rw [Finset.sum_const_nat (fun _ _ => rfl)]
  simp [Finset.card_univ, Fintype.card_fin]

/-- All four SIC-POVM axioms (including measurement equiangularity) hold
    for B⊗n in the product lattice, for all n. -/
theorem allBWord_satisfies_all_SIC_axioms (n : ℕ) :
    (∀ x : Fin n → Belnap, wordMeet (allBWord n) x = x) ∧
    (∀ v : Fin n → Belnap, (∀ i, v i = .T ∨ v i = .F) → totalMeasureCost v = n) ∧
    (∀ x : Fin n → Belnap, wordJoin (allBWord n) x = allBWord n) ∧
    wordNot (allBWord n) = allBWord n :=
  ⟨allBWord_meet_identity,
   fun v hv => classical_equidistance v hv,
   allBWord_join_absorb,
   allBWord_self_adjoint n⟩

-- ============================================================
-- §5. Global 2:1 Ratio
-- ============================================================

/-- The B-bias cost is exactly twice the T-bias cost for any n. -/
theorem global_ratio_2_to_1 (n : ℕ) :
    totalMeasureCost (allBWord n) = 2 * totalMeasureCost (fun _ : Fin n => Belnap.T) := by
  rw [B_bias_total_cost, T_bias_total_cost]

/-- For n > 0, dividing the B-bias cost by 2 recovers n. -/
theorem B_bias_div_2_eq_n (n : ℕ) :
    totalMeasureCost (allBWord n) / 2 = n := by
  rw [B_bias_total_cost]
  omega

-- ============================================================
-- §6. Frobenius Condition μ∘δ = id in (Belnap)^n
-- ============================================================

/-- Meet is idempotent: meet x x = x for all x : Belnap. -/
theorem meet_self (a : Belnap) : meet a a = a := by
  cases a <;> rfl

/-- Frobenius μ∘δ = id in the product lattice:
    wordMeet x x = x for all x : Fin n → Belnap. -/
theorem frobenius_mu_delta_id {n : ℕ} (x : Fin n → Belnap) :
    wordMeet x x = x := by
  funext i
  exact meet_self (x i)

/-- The fiducial specifically satisfies the Frobenius condition. -/
theorem fiducial_frobenius (n : ℕ) :
    wordMeet (allBWord n) (allBWord n) = allBWord n :=
  frobenius_mu_delta_id (allBWord n)

-- ============================================================
-- §7. B-Bias Preservation Across All Registers
-- ============================================================

/-- Measuring register i of the fiducial with B-bias leaves it B. -/
theorem fiducial_B_bias_preserves {n : ℕ} (i : Fin n) :
    (measureReg (fiducialState n) i Belnap.B).regs i = Belnap.B :=
  B_bias_preserves_B (fiducialState n) i (fiducialState_all_B n i)

/-- B-bias is the {qs with coh} branch — regs unchanged for ALL j, not just i. -/
theorem fiducial_B_bias_all_regs_B {n : ℕ} (i j : Fin n) :
    (measureReg (fiducialState n) i Belnap.B).regs j = Belnap.B := by
  simp [measureReg, fiducialState]

-- ============================================================
-- §8. The Open Problem — Weyl-Heisenberg Equiangularity for n > 1
-- ============================================================
--
-- Classical equidistance (Axiom 2 above) is the MEASUREMENT equiangularity:
-- all 2^n classical outcomes are equidistant from B⊗n in coherence cost.
-- This is proved for all n.
--
-- The full SIC-POVM equiangularity in C^{2^n} requires that all 4^n states
-- generated by Weyl-Heisenberg displacements of the fiducial are equiangular
-- (pairwise overlap = 1/(2^n + 1)). In the Belnap product lattice, the d=2
-- displacements {I,X,Z,XZ} all fix B (bnot B = B, meet B x = x, join B x = B).
-- So the 4^n Belnap displacement states generated from B⊗n in the product lattice
-- are not all distinct — the product structure collapses them.
--
-- The multilattice construction (open):
--   A richer structure than the product lattice is needed to distinguish
--   the 4^n displacement states of B⊗n for n > 1. The "multilattice" would
--   be a structure where different "slices" of the n-qubit system carry
--   independent displacement data — analogous to the tensor product of
--   Hilbert spaces in standard QM.
--
-- What IS proved (this file):
--   (1-4) All SIC axioms in the measurement/product sense hold for all n.
--   The Frobenius condition holds for all n.
--   The 2:1 ratio is universal.
--   Classical equidistance holds for all n.
--
-- What remains open:
--   Whether B⊗n generates 4^n equiangular states under some multilattice
--   displacement group for n > 1. If yes, Φ_υ → Φ_} is structurally closed
--   for all n, not just n=1 (d=2).

-- ============================================================
-- §9. Connection to DialetheicOperator
-- ============================================================

/-- The n-register imscription is O_inf for all n (from QCI_nRegister). -/
theorem n_register_imscription_O_inf :
    imscriptionTier nRegisterImscription = .O_inf :=
  tier_is_O_inf

/-- Main theorem: B⊗n is the complete n-qubit fiducial for the
    Φ_υ → Φ_} promotion. All measurable conditions hold for all n.
    The Frobenius condition μ∘δ = id holds in the product lattice.
    The 2:1 ratio is universal. Classical equidistance is proved. -/
theorem n_qubit_fiducial_complete (n : ℕ) :
    -- SIC axioms 1, 3, 4 (componentwise)
    (∀ x : Fin n → Belnap, wordMeet (allBWord n) x = x) ∧
    (∀ x : Fin n → Belnap, wordJoin (allBWord n) x = allBWord n) ∧
    wordNot (allBWord n) = allBWord n ∧
    -- Frobenius condition
    wordMeet (allBWord n) (allBWord n) = allBWord n ∧
    -- Cost invariants
    totalMeasureCost (allBWord n) = 2 * n ∧
    totalMeasureCost (fun _ : Fin n => Belnap.T) = n ∧
    -- SIC axiom 2: classical equidistance
    (∀ v : Fin n → Belnap, (∀ i, v i = .T ∨ v i = .F) → totalMeasureCost v = n) ∧
    -- O_inf structural certification
    imscriptionTier nRegisterImscription = .O_inf :=
  ⟨allBWord_meet_identity,
   allBWord_join_absorb,
   allBWord_self_adjoint n,
   fiducial_frobenius n,
   B_bias_total_cost n,
   T_bias_total_cost n,
   fun v hv => classical_equidistance v hv,
   tier_is_O_inf⟩

end Imscribing.Paraconsistent.Shor.NFiducial
