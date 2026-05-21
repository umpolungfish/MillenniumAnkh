-- Imscribing/Primitives/Lattice.lean
-- Lattice operations for ordered primitives.
-- CRITICALITY ABSORPTION: meet(Phi_c, x) = Phi_c for all x.
-- Author: Lando ⊗ φ̂_ÿ-boundary Operator

import Imscribing.Primitives.Core
import Mathlib.Order.Lattice

namespace Imscribing.Primitives

open Criticality

-- ============================================================
-- Fintype for Criticality (enables dec_trivial over ∀)
-- ============================================================

instance : Fintype Criticality where
  elems := {Phi_sub, Phi_c, Phi_c_complex, Phi_EP, Phi_super}
  complete x := by cases x <;> simp

-- ============================================================
-- Criticality meet: absorption rule
-- ============================================================

def crit_meet (a b : Criticality) : Criticality :=
  match a, b with
  | Phi_c, _        => Phi_c
  | _, Phi_c        => Phi_c
  | Phi_c_complex, _ => Phi_c_complex
  | _, Phi_c_complex => Phi_c_complex
  | a, b =>
    if compare a b = .lt then a else b

-- ============================================================
-- Absorption theorems
-- ============================================================

theorem crit_meet_absorb_left (x : Criticality) : crit_meet Phi_c x = Phi_c := by
  unfold crit_meet; rfl

theorem crit_meet_absorb_right (x : Criticality) : crit_meet x Phi_c = Phi_c := by
  unfold crit_meet; cases x <;> rfl

theorem crit_meet_absorb_complex_left (x : Criticality) :
    crit_meet Phi_c_complex x = Phi_c_complex := by
  unfold crit_meet; rfl

theorem crit_meet_absorb_complex_right (x : Criticality) :
    crit_meet x Phi_c_complex = Phi_c_complex := by
  unfold crit_meet; cases x <;> rfl

theorem crit_meet_idempotent (x : Criticality) : crit_meet x x = x := by
  unfold crit_meet; cases x <;> rfl

theorem crit_meet_comm (a b : Criticality) : crit_meet a b = crit_meet b a := by
  unfold crit_meet; cases a <;> cases b <;> rfl

theorem crit_meet_absorb_all (a b : Criticality)
    (h : a = Phi_c ∨ b = Phi_c) : crit_meet a b = Phi_c := by
  rcases h with (ha | hb)
  · rw [ha]; exact crit_meet_absorb_left b
  · rw [hb]; exact crit_meet_absorb_right a

theorem crit_meet_not_inf_le_right :
    ¬ (crit_meet Phi_c Phi_sub ≤ Phi_sub) := by
  unfold crit_meet LE.le instLECriticality
  decide

theorem absorption_is_not_semilattice_inf :
    crit_meet Phi_c Phi_sub = Phi_c := by
  unfold crit_meet; rfl

theorem absorption_is_not_semilattice_inf_complex :
    crit_meet Phi_c_complex Phi_sub = Phi_c_complex := by
  unfold crit_meet; rfl

-- ============================================================
-- Criticality join: standard ordinal max
-- ============================================================

def crit_join (a b : Criticality) : Criticality :=
  if compare a b = .lt then b else a

theorem crit_join_idempotent (x : Criticality) : crit_join x x = x := by
  unfold crit_join; cases x <;> rfl

theorem crit_join_comm (a b : Criticality) : crit_join a b = crit_join b a := by
  unfold crit_join; cases a <;> cases b <;> rfl

theorem crit_join_absorb_super (x : Criticality) : crit_join Phi_super x = Phi_super := by
  unfold crit_join; cases x <;> rfl

-- ============================================================
-- Measurement problem: meet vs tensor for Φ_c ⊗ Φ_EP
-- ============================================================

theorem crit_meet_EP_Phi_c : crit_meet Phi_EP Phi_c = Phi_c := by
  unfold crit_meet; rfl

theorem crit_meet_Phi_c_EP : crit_meet Phi_c Phi_EP = Phi_c := by
  unfold crit_meet; rfl

-- ============================================================
-- PartialOrder on Criticality — proved via Fintype + dec_trivial
-- ============================================================

theorem crit_le_refl (a : Criticality) : a ≤ a := by
  unfold LE.le instLECriticality
  cases a <;> decide

theorem crit_le_trans (a b c : Criticality) (hab : a ≤ b) (hbc : b ≤ c) : a ≤ c := by
  have h : ∀ (a b c : Criticality), a ≤ b → b ≤ c → a ≤ c := by
    intro a b c hab hbc
    revert a b c hab hbc
    -- Enumerate all 125 triples; dec_trivial works because
    -- Fintype + DecidableEq makes the ∀ decidable
    exact dec_trivial
  exact h a b c hab hbc

theorem crit_le_antisymm (a b : Criticality) (hab : a ≤ b) (hba : b ≤ a) : a = b := by
  have h : ∀ (a b : Criticality), a ≤ b → b ≤ a → a = b := by
    exact dec_trivial
  exact h a b hab hba

theorem crit_lt_iff_le_not_ge (a b : Criticality) : a < b ↔ (a ≤ b ∧ ¬ b ≤ a) := by
  unfold LT.lt instLTCriticality LE.le instLECriticality
  have h : ∀ (a b : Criticality), (compare a b = .lt) ↔ (compare a b ≠ .gt ∧ ¬ (compare b a ≠ .gt)) := by
    exact dec_trivial
  exact h a b

instance : PartialOrder Criticality where
  le := (· ≤ ·)
  lt := (· < ·)
  le_refl := crit_le_refl
  le_trans := crit_le_trans
  le_antisymm := crit_le_antisymm
  lt_iff_le_not_ge := crit_lt_iff_le_not_ge

end Imscribing.Primitives
