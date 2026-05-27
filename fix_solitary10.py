#!/usr/bin/env python3
"""Generate fix for Solitary10.lean sorries."""
import shutil, os

fix1 = """
        rcases h31_z with ⟨w, hz_eq⟩
        rw [hz_eq] at hn_eq h_sigma2
        -- n = 31²*w. σ(31²*w) = 45*31*w = 1395*w
        have hw_pos : w > 0 := by
          by_contra! hle
          have hw0 : w = 0 := by omega
          rw [hw0, mul_zero] at hz_eq
          omega
        by_cases h31_dvd_w : 31 ∣ w
        · -- 31|w, one more step gives contradiction
          rcases h31_dvd_w with ⟨w1, hw_eq⟩
          rw [hw_eq] at h_sigma2
          have hw1_pos : w1 > 0 := by
            by_contra! hz
            have hw10 : w1 = 0 := by omega
            rw [hw10, mul_zero] at hw_eq
            omega
          have h_sigma_31cubed_w1 : σ (31³ * w1) = 45*31²*w1 := by
            -- from h_sigma2: σ(31²*31*w1) = 45*31*w1
            calc
              σ (31³ * w1) = σ (31² * (31 * w1)) := by ring
              _ = 45 * (31 * w1) := h_sigma2
              _ = 45*31²*w1 := by ring
          by_cases h_cop_31_w1 : Nat.Coprime 31 w1
          · have h_mul_cube : σ (31³ * w1) = σ (31³) * σ w1 := sigma_mul_coprime (h_cop_31_w1.pow_left 3)
            rw [h_mul_cube, show σ (31³) = 30784 by native_decide] at h_sigma_31cubed_w1
            -- 30784 * σ(w1) = 45*31²*w1 = 43245*w1
            have h30784_w1 : 30784 ∣ w1 := by
              have hcop : Nat.Coprime 30784 43245 := by native_decide
              have h_eq : 30784 * σ w1 = 43245 * w1 := by
                calc
                  30784 * σ w1 = σ (31³) * σ w1 := by norm_num
                  _ = 45*31²*w1 := h_sigma_31cubed_w1
                  _ = 43245 * w1 := by norm_num
              exact factor_from_eq 30784 43245 w1 hcop h_eq
            rcases h30784_w1 with ⟨x, hw1_eq⟩
            rw [hw1_eq] at h_sigma_31cubed_w1
            have hx_pos : x > 0 := by
              by_contra! hz
              have hx0 : x = 0 := by omega
              rw [hx0, mul_zero] at hw1_eq
              omega
            have h_sigma_x : σ (30784 * x) = 43245 * x := by omega
            by_cases h_cop_30784_x : Nat.Coprime 30784 x
            · have h_mul_30784 : σ (30784 * x) = σ 30784 * σ x := sigma_mul_coprime h_cop_30784_x
              rw [h_mul_30784, show σ 30784 = 67564 by native_decide] at h_sigma_x
              have h_sigma_x_ge_x : σ x ≥ x := sigma_ge_self x hx_pos
              have : 67564 * σ x > 43245 * x := by
                calc
                  67564 * σ x ≥ 67564 * x := Nat.mul_le_mul_left 67564 h_sigma_x_ge_x
                  _ > 43245 * x := by
                    nlinarith
              omega
            · -- 30784|x, even larger LHS → contradiction
              have h30784_x : 30784 ∣ x := by
                rw [Nat.coprime_iff_gcd_eq_one] at h_cop_30784_x
                ...
              sorry
          · -- 31|w1, even more powers of 31 → immediate via sigma(31^e) growth
            have h31_w1 : 31 ∣ w1 := by
              rw [Nat.coprime_iff_gcd_eq_one] at h_cop_31_w1
              have hp31 : Nat.Prime 31 := by native_decide
              ...
            sorry
        · -- 31 ∤ w, so gcd(31,w)=1. Use the descent through 331, 332 → contradiction
          ...
"""

print("Fix script loaded, would write:", len(fix1), "chars")
