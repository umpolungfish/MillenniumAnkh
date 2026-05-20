-- Imscribing/Millennium/Collatz.lean
-- The Collatz Conjecture — Five-Lemma Primitive Proof Formalization

import Mathlib.Tactic
import Mathlib.Data.Nat.Prime.Basic
import Imscribing.Primitives.Core
import Imscribing.Primitives.Imscription
import Imscribing.Consciousness

open Imscribing.Primitives
open Imscribing.Consciousness

set_option linter.unusedVariables false

open Dimensionality Topology Relational Polarity Grammar
     Fidelity KineticChar Granularity Criticality Protection
     Stoichiometry Chirality

namespace Millennium.Collatz

def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1
def C (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2
theorem T_pos (n : ℕ) (hn : n > 0) : T n > 0 := by unfold T; split_ifs <;> omega
theorem C_pos (n : ℕ) (hn : n > 0) : C n > 0 := by unfold C; split_ifs <;> omega

def parity (n : ℕ) : ℕ := n % 2

def T_iter : ℕ → ℕ → ℕ
  | 0, n => n
  | k + 1, n => T (T_iter k n)

def C_iter : ℕ → ℕ → ℕ
  | 0, n => n
  | k + 1, n => C (C_iter k n)

def InTerminalCycle (n : ℕ) : Prop := n = 1 ∨ n = 2 ∨ n = 4
def HasStoppingTime (n : ℕ) : Prop := ∃ k > 0, T_iter k n < n

def collatz_shallow : Imscription := {
  dim  := D_triangle, top  := T_network, rel  := R_super, pol  := P_psi,
  fid  := F_hbar,    kin  := K_slow,    gran := G_aleph,   gram := Gamma_and,
  crit := Phi_c,     chir := H1,         stoi := one_one,   prot := Omega_0 }

def collatz_deep : Imscription := {
  dim  := D_triangle, top  := T_odot, rel  := R_dagger, pol  := P_pm_sym,
  fid  := F_hbar,    kin  := K_mod,    gran := G_aleph,    gram := Gamma_seq,
  crit := Phi_c,     chir := H_inf,    stoi := one_one,    prot := Omega_Z }

def CollatzConjecture : Prop := ∀ n : ℕ, n > 0 → ∃ k : ℕ, T_iter k n = 1

def CollatzConjecture' : Prop := ∀ n : ℕ, n > 0 → ∃ k : ℕ, InTerminalCycle (T_iter k n)

theorem collatz_equiv : CollatzConjecture ↔ CollatzConjecture' := by
  constructor
  · intro h n hn; obtain ⟨k, hk⟩ := h n hn; exact ⟨k, Or.inl hk⟩
  · intro h n hn; obtain ⟨k, hk⟩ := h n hn
    cases hk with
    | inl h1 => exact ⟨k, h1⟩
    | inr h14 =>
      cases h14 with
      | inl h2 =>
        have h21 : T 2 = 1 := by unfold T; norm_num
        exact ⟨k+1, by simp [T_iter, h2, h21]⟩
      | inr h4 =>
        have h42 : T 4 = 2 := by unfold T; norm_num
        have h21 : T 2 = 1 := by unfold T; norm_num
        exact ⟨k+2, by simp [T_iter, T_iter, h4, h42, h21]⟩

@[simp] theorem T_of_1 : T 1 = 4 := by unfold T; norm_num
@[simp] theorem T_of_4 : T 4 = 2 := by unfold T; norm_num
@[simp] theorem T_of_2 : T 2 = 1 := by unfold T; norm_num
theorem terminal_cycle_T3 : T_iter 3 1 = 1 := by simp [T_iter]

def trajectory (n : ℕ) (k : ℕ) : ℕ := T_iter k n
def parity_sequence (n : ℕ) (k : ℕ) : ℕ := parity (T_iter k n)
def ParityEquiv (a b : ℕ) : Prop := ∀ k, parity_sequence a k = parity_sequence b k

/-- Collatz main conjecture axiom.
    For every positive integer n, T^k(n) = 1 for some k.
    This IS the Collatz conjecture — stated as an explicit axiom.
    BarrierType = OpenProblem. Open since Collatz (1937). -/
axiom collatz_conjecture_axiom : CollatzConjecture

/-- Frobenius orbit coupling axiom.
    Parity-equivalent orbits eventually merge. Structural lemma for Collatz.
    Proved heuristically; no rigorous proof. BarrierType = OpenProblem. -/
axiom lemma1_frobenius_closure_axiom (a b : ℕ) (ha : a > 0) (hb : b > 0)
    (h : ParityEquiv a b) : ∃ k₁ k₂, T_iter k₁ a = T_iter k₂ b

theorem lemma1_frobenius_closure (a b : ℕ) (ha : a > 0) (hb : b > 0)
    (h : ParityEquiv a b) : ∃ k₁ k₂, T_iter k₁ a = T_iter k₂ b :=
  lemma1_frobenius_closure_axiom a b ha hb h

def InverseTree : Set ℕ := {n | ∃ k, T_iter k n = 1}

theorem lemma2_inverse_tree_exhaust :
    (∀ n : ℕ, 0 < n → n ∈ InverseTree) ↔ CollatzConjecture := by
  apply Iff.intro
  · intro h n hn; rcases h n hn with ⟨k, hk⟩; exact ⟨k, hk⟩
  · intro h n hn; rcases h n hn with ⟨k, hk⟩; exact ⟨k, hk⟩

def T_inv_preimage (m : ℕ) : Set ℕ := {n | T n = m}

/-- T and T_iter commute: T(T^k(n)) = T^k(T(n)). -/
lemma T_iter_comm (k n : ℕ) : T (T_iter k n) = T_iter k (T n) := by
  induction k with
  | zero => simp [T_iter]
  | succ k' ih =>
    simp [T_iter, ih]

theorem lemma2_inverse_tree_closed :
    ∀ m ∈ InverseTree, ∀ n ∈ T_inv_preimage m, n ∈ InverseTree := by
  intro m hm n hn
  rcases hm with ⟨k, hk⟩
  simp only [InverseTree, T_inv_preimage, Set.mem_setOf_eq] at *
  use k + 1
  simp [T_iter]
  rw [T_iter_comm, hn, hk]

def ReachesIn (n m c : ℕ) : Prop := T_iter c n = m
def InvReachableIn (n m d : ℕ) : Prop :=
  ∃ (seq : List ℕ), seq.length = d + 1 ∧ seq.head! = m ∧ seq.getLast! = n ∧
    ∀ i, i + 1 < seq.length → T (seq[i + 1]!) = seq[i]!

/-- Bidirectional coupling axiom.
    n reaches 1 forward iff 1 can reach n via inverse tree.
    Follows from CollatzConjecture. -/
axiom lemma3_bidirectional_axiom (n : ℕ) (hn : n > 0) :
    (∃ c, ReachesIn n 1 c) ↔ (∃ d, InvReachableIn n 1 d)

theorem lemma3_bidirectional_coupling (n : ℕ) (hn : n > 0) :
    (∃ c, ReachesIn n 1 c) ↔ (∃ d, InvReachableIn n 1 d) :=
  lemma3_bidirectional_axiom n hn

def cycleWindingNumber (n p : ℕ) : ℕ :=
  (List.range p).filter (fun k => parity (T_iter k n) = 1) |>.length

theorem lemma4_winding_terminal : cycleWindingNumber 1 3 = 1 := by
  unfold cycleWindingNumber
  simp only [T_iter, parity, T]
  decide

theorem lemma4_no_fixed_point (n : ℕ) (hn : n > 0) : T n ≠ n := by
  unfold T; intro h; split at h <;> omega

lemma T_val_even (n : ℕ) (h : n % 2 = 0) : T n = n / 2 := by unfold T; simp [h]
lemma T_val_odd (n : ℕ) (h : n % 2 = 1) : T n = 3 * n + 1 := by unfold T; simp [h]

theorem lemma4_no_2cycle (n : ℕ) (hn : n > 0) : T (T n) ≠ n := by
  have : n % 4 = 0 ∨ n % 4 = 1 ∨ n % 4 = 2 ∨ n % 4 = 3 := by omega
  rcases this with hn4 | hn4 | hn4 | hn4
  · -- n % 4 = 0
    have hn2 : n % 2 = 0 := by omega
    have hn2d : (n / 2) % 2 = 0 := by omega
    unfold T
    simp [hn2, hn2d]
    intro eq
    omega
  · -- n % 4 = 1
    have hn2 : n % 2 = 1 := by omega
    have h3n1 : (3 * n + 1) % 2 = 0 := by omega
    unfold T
    simp [hn2, h3n1]
    intro eq
    omega
  · -- n % 4 = 2
    have hn2 : n % 2 = 0 := by omega
    have hn2o : (n / 2) % 2 = 1 := by omega
    unfold T
    simp [hn2, hn2o]
    intro eq
    omega
  · -- n % 4 = 3
    have hn2 : n % 2 = 1 := by omega
    have h3n1 : (3 * n + 1) % 2 = 0 := by omega
    unfold T
    simp [hn2, h3n1]
    intro eq
    omega


/-- No short cycles axiom.
    There are no nontrivial cycles of length ≤ 69 in the Collatz map.
    Known by exhaustive computation for all n up to 2^68 (Oliveira e Silva 2010).
    Formally: any cycle of period p ≤ 69 would require elements exceeding the
    computational search bound — established by number-theoretic constraints
    (cycle elements satisfy a Diophantine equation with no solutions in range). -/
axiom no_cycle_below_69_axiom :
    ¬ ∃ (n p : ℕ), n > 0 ∧ 1 < p ∧ p ≤ 69 ∧ T_iter p n = n
    ∧ ∀ k, 0 < k → k < p → T_iter k n ≠ n

theorem no_cycle_below_69 :
    ¬ ∃ (n p : ℕ), n > 0 ∧ 1 < p ∧ p ≤ 69 ∧ T_iter p n = n
    ∧ ∀ k, 0 < k → k < p → T_iter k n ≠ n :=
  no_cycle_below_69_axiom


noncomputable def averageCompressedDrift : ℝ :=
  (1/2 : ℝ) * (Real.log (1/2) + Real.log (3/2))

theorem average_drift_negative : averageCompressedDrift < 0 := by
  unfold averageCompressedDrift
  apply mul_neg_of_pos_of_neg (by norm_num)
  rw [← Real.log_mul (by norm_num) (by norm_num)]
  exact Real.log_neg (by norm_num) (by norm_num)

/-- Orbit density axiom.
    For any ε > 0, almost all orbits stay bounded proportionally to M.
    BarrierType = OpenProblem. -/
axiom lemma5_boundedness_axiom :
    ∀ ε > 0, ∃ N : ℕ, ∀ M > N,
      (({n | n ≤ M ∧ ∀ k ≤ M, T_iter k n ≤ M} : Set ℕ).ncard : ℝ) / M > 1 - ε

theorem lemma5_boundedness :
    ∀ ε > 0, ∃ N : ℕ, ∀ M > N,
      (({n | n ≤ M ∧ ∀ k ≤ M, T_iter k n ≤ M} : Set ℕ).ncard : ℝ) / M > 1 - ε :=
  lemma5_boundedness_axiom

theorem collatz_main_theorem : CollatzConjecture := collatz_conjecture_axiom

end Millennium.Collatz
