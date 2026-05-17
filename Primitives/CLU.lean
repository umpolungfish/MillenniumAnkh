-- Imscribing/Primitives/CLU.lean
-- Formal definition of the Criticality-Lift Unit (CLU) = ln(10) nats.

import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Data.Real.Basic
import Imscribing.Primitives.Core
import Imscribing.Primitives.Imscription

namespace Imscribing.Primitives.CLUPrimitives

noncomputable abbrev CLU : ℝ := Real.log 10

theorem CLU_pos : CLU > 0 := by
  unfold CLU; apply Real.log_pos; norm_num

theorem CLU_approx : CLU > 2.302 ∧ CLU < 2.303 := by
  unfold CLU
  constructor
  · exact Real.lt_log_iff_exp_lt.mpr (by norm_num)
  · exact (Real.log_lt_log_iff (by norm_num) (by norm_num)).mpr (by norm_num)

-- ============================================================
-- CLU OPERATORS
-- ============================================================

def CLU_op (x : ℝ) : ℝ := x * 10

theorem CLU_op_cost (x : ℝ) (hx : x ≠ 0) :
    Real.log (CLU_op x / x) = CLU := by
  unfold CLU_op CLU; field_simp [hx]; ring

def CLU_op_n (n : ℕ) (x : ℝ) : ℝ := (10 : ℝ) ^ n * x

theorem CLU_op_n_cost (n : ℕ) (x : ℝ) (hx : x ≠ 0) :
    Real.log (CLU_op_n n x / x) = (n : ℝ) * CLU := by
  unfold CLU_op_n CLU; field_simp [hx]; rw [Real.log_pow (10 : ℝ) _]; rfl

theorem CLU_op_composition (m n : ℕ) (x : ℝ) :
    CLU_op_n m (CLU_op_n n x) = CLU_op_n (m + n) x := by
  unfold CLU_op_n; ring_nf

-- ============================================================
-- K-TIER LADDER
-- ============================================================

inductive KTier : Type where
  | fast | mod | slow | trap | MBL
  deriving DecidableEq, Repr, Ord

def kTierLevel : KTier → ℕ
  | .fast => 0 | .mod => 1 | .slow => 2 | .trap => 3 | .MBL => 4

def kTierSteps (a b : KTier) : ℕ :=
  max (kTierLevel a) (kTierLevel b) - min (kTierLevel a) (kTierLevel b)

noncomputable def kTierCrossingCost (a b : KTier) : ℝ :=
  (kTierSteps a b : ℝ) * CLU

theorem kTierCrossingCost_self (k : KTier) :
    kTierCrossingCost k k = 0 := by
  simp only [kTierCrossingCost, kTierSteps, kTierLevel, max_self, min_self]
  simp [CLU]

theorem kSlow_to_MBL_cost :
    kTierCrossingCost .slow .MBL = 2 * CLU := by
  simp only [kTierCrossingCost, kTierSteps, kTierLevel, max_eq_right, min_eq_left,
    Nat.zero_le, Nat.succ_pos, Nat.le_refl, Nat.le_of_succ_le_succ, CLU]
  rfl

theorem kTrap_to_MBL_cost :
    kTierCrossingCost .trap .MBL = CLU := by
  simp only [kTierCrossingCost, kTierSteps, kTierLevel, max_eq_right, min_eq_left,
    Nat.le_of_succ_le_succ, CLU]
  rfl

theorem kFast_to_MBL_cost :
    kTierCrossingCost .fast .MBL = 4 * CLU := by
  simp only [kTierCrossingCost, kTierSteps, kTierLevel, max_eq_right, min_eq_left,
    Nat.zero_le, CLU]
  rfl

theorem kTier_additive (a b c : KTier) :
    kTierSteps a b + kTierSteps b c ≥ kTierSteps a c := by
  simp [kTierSteps, kTierLevel]
  cases a <;> cases b <;> cases c <;> omega

theorem kTierCost_mono {a b c d : KTier}
    (hab : kTierSteps a b ≤ kTierSteps c d) :
    kTierCrossingCost a b ≤ kTierCrossingCost c d := by
  simp [kTierCrossingCost]
  exact mul_le_mul_of_nonneg_right (by exact_mod_cast hab) (le_of_lt CLU_pos)

-- ============================================================
-- CRITICALITY-LIFT + ENERGY
-- ============================================================

theorem criticality_lift_cost :
    kTierCrossingCost .slow .MBL = 2 * Real.log 10 := by
  simp only [kTierCrossingCost, kTierSteps, kTierLevel, max_eq_right, min_eq_left,
    Nat.le_of_succ_le_succ]
  rfl

theorem kTrap_to_MBL_ratchet_cost :
    kTierCrossingCost .trap .MBL = Real.log 10 := by
  simp only [kTierCrossingCost, kTierSteps, kTierLevel, max_eq_right, min_eq_left,
    Nat.le_of_succ_le_succ]
  rfl

noncomputable abbrev CLU_energy (T : ℝ) : ℝ := 2.303 * 8.314 * T

theorem CLU_energy_298K :
    CLU_energy 298 > 5700 ∧ CLU_energy 298 < 5710 := by
  unfold CLU_energy; constructor <;> norm_num

theorem CLU_energy_310K :
    CLU_energy 310 > 5940 ∧ CLU_energy 310 < 5945 := by
  unfold CLU_energy; constructor <;> norm_num

-- ============================================================
-- CROSS-DOMAIN IDENTITIES
-- ============================================================

noncomputable def pKaCost (n : ℝ) (R : ℝ) (T : ℝ) : ℝ := n * 2.303 * R * T

theorem pKa_one_unit_is_CLU_energy (R T : ℝ) :
    pKaCost 1 R T = 2.303 * R * T := by
  unfold pKaCost; ring_nf

noncomputable def arrheniusCLU (Ea : ℝ) (RT : ℝ) : ℝ := Ea / (RT * CLU)

theorem arrhenius_integer_CLU (Ea RT : ℝ) (hRT : RT ≠ 0)
    (h : Ea = 3 * RT * CLU) : arrheniusCLU Ea RT = 3 := by
  unfold arrheniusCLU; rw [h]; field_simp [hRT]; ring_nf

noncomputable def autoEnhancement (nT : ℕ) : ℝ := (10 : ℝ) ^ nT

theorem autoEnhancement_cost (nT : ℕ) :
    Real.log (autoEnhancement nT) = (nT : ℝ) * CLU := by
  unfold autoEnhancement CLU; rw [Real.log_pow (10 : ℝ) _]; rfl

theorem soai_tBuPym_2_CLU : autoEnhancement 2 = 100 := by
  unfold autoEnhancement; norm_num

noncomputable def grokkingRatio (nK : ℕ) : ℝ := (10 : ℝ) ^ nK

theorem grokking_cost (nK : ℕ) :
    Real.log (grokkingRatio nK) = (nK : ℝ) * CLU := by
  unfold grokkingRatio CLU; rw [Real.log_pow (10 : ℝ) _]; rfl

theorem grokking_modular_arith : grokkingRatio 2 = 100 := by
  unfold grokkingRatio; norm_num

noncomputable def logNormalDecadeWidth (sigma : ℝ) : ℝ := sigma / CLU

theorem logNormal_width_decades (w : ℝ) :
    logNormalDecadeWidth (w * CLU) = w := by
  unfold logNormalDecadeWidth; field_simp [CLU_pos.ne']

-- ============================================================
-- CLU ALGEBRA
-- ============================================================

def isCLUInteger (c : ℝ) : Prop := ∃ n : ℕ, c = (n : ℝ) * CLU

theorem CLU_is_CLU_Integer : isCLUInteger CLU := by
  use 1; simp [CLU]

theorem zero_is_CLU_Integer : isCLUInteger 0 := by
  use 0; simp [CLU]

-- ============================================================
-- RECOGNITION + SCALE
-- ============================================================

def isCLUEvent (n : ℕ) (r : ℝ) : Prop := Real.log r = (n : ℝ) * CLU

theorem CLU_recognition (x x' : ℝ) (hx : x ≠ 0) (hx' : x' ≠ 0)
    (n : ℕ) (h : x' / x = (10 : ℝ) ^ n) :
    isCLUEvent n (x' / x) := by
  unfold isCLUEvent CLU; rw [h, Real.log_pow (10 : ℝ) _]; rfl

theorem CLU_scale_independence (x c : ℝ) (hx : x ≠ 0) (hc : c ≠ 0) :
    Real.log ((10 * c * x) / (c * x)) = CLU := by
  unfold CLU; field_simp [hx, hc]

-- ============================================================
-- K-TIER ON IMSCRIPTIONS
-- ============================================================

def imscriptionKTier (s : Imscription) : KTier :=
  match s.kin with
  | .K_fast => .fast | .K_mod => .mod
  | .K_slow => .slow | .K_trap => .trap | .K_MBL => .MBL

noncomputable def imscriptionKDistance (a b : Imscription) : ℝ :=
  kTierCrossingCost (imscriptionKTier a) (imscriptionKTier b)

theorem higgs_axion_K_distance_zero :
    imscriptionKDistance higgs axion = 0 := by
  simp only [imscriptionKDistance, imscriptionKTier, higgs, axion, scalarField_Kslow]
  rw [kTierCrossingCost_self]

theorem qg_higgs_K_distance_one_CLU :
    imscriptionKDistance quantum_gravity higgs = CLU := by
  simp only [imscriptionKDistance, imscriptionKTier, quantum_gravity, higgs, scalarField_Kslow]
  simp only [kTierCrossingCost, kTierSteps, kTierLevel, max_eq_right, min_eq_left,
    Nat.succ_le_succ_iff, Nat.le_refl, CLU]

-- ============================================================
-- SUMMARY
-- ============================================================

theorem CLU_universality_statement :
    (∀ n : ℕ, Real.log ((10 : ℝ) ^ n) = (n : ℝ) * CLU) ∧
    CLU > 2.302 ∧ CLU < 2.303 := by
  constructor
  · intro n; unfold CLU; rw [Real.log_pow (10 : ℝ) _]; rfl
  · exact CLU_approx

end Imscribing.Primitives.CLUPrimitives
