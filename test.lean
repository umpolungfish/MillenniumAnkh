import Mathlib.Analysis.Complex.Basic

noncomputable def theta_combined (s : ℂ) : ℂ := 1 - starRingEnd ℂ s

theorem theta_combined_involution (s : ℂ) : theta_combined (theta_combined s) = s := by
  simp [theta_combined]

theorem theta_fixed_iff_critical (s : ℂ) :
    theta_combined s = s ↔ s.re = 1 / 2 := by
  constructor
  · intro h
    have hre := congr_arg Complex.re h
    simp [theta_combined] at hre
    linarith
  · intro h
    apply Complex.ext
    · simp [theta_combined]
      linarith
    · simp [theta_combined]
