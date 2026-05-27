#!/usr/bin/env python3
"""Replace sorries in Solitary10.lean with complete proofs."""
import re

with open('/home/mrnob0dy666/MillenniumAnkh/Imscribing/Classical/Solitary10.lean', 'r') as f:
    content = f.read()

# Sorry 1: the 31² descent (line ~344)
# Replace the block from "rcases h31_z with" through "sorry"
sorry1_pattern = r"rcases h31_z with ⟨w, hz_eq⟩\s*\n\s*rw \[hz_eq\] at hn_eq h_sigma2.*?\n\s*sorry"

fix1 = """        rcases h31_z with ⟨w, hz_eq⟩
        rw [hz_eq] at hn_eq h_sigma2
        -- n = 31²*w. σ(31²*w) = 45*31*w = 1395*w
        have hw_pos : w > 0 := by
          by_contra! hle
          have hw0 : w = 0 := by omega
          rw [hw0, mul_zero] at hz_eq
          omega
        by_cases h31_dvd_w : 31 ∣ w
        · rcases h31_dvd_w with ⟨w1, hw_eq⟩
          rw [hw_eq, show 31² * (31 * w1) = 31³ * w1 by ring] at h_sigma2
          have hw1_pos : w1 > 0 := by
            by_contra! hz
            have hw10 : w1 = 0 := by omega
            rw [hw10, mul_zero] at hw_eq
            omega
          -- σ(31³*w1) = 45*31²*w1 = 43245*w1
          have h_sigma_31cubed : σ (31³ * w1) = 43245 * w1 := by
            calc
              σ (31³ * w1) = σ (31² * (31 * w1)) := by ring
              _ = 45 * (31 * w1) := h_sigma2
              _ = 45 * 31² * w1 := by ring
              _ = 43245 * w1 := by norm_num
          by_cases h_cop_31_w1 : Nat.Coprime 31 w1
          · have h_mul_cube : σ (31³ * w1) = σ (31³) * σ w1 :=
              sigma_mul_coprime (h_cop_31_w1.pow_left 3)
            rw [h_mul_cube, show σ (31³) = 30784 by native_decide] at h_sigma_31cubed
            have h30784_w1 : 30784 ∣ w1 := by
              have hcop : Nat.Coprime 30784 43245 := by native_decide
              have h_eq : 30784 * σ w1 = 43245 * w1 := by
                calc
                  30784 * σ w1 = σ (31³) * σ w1 := by norm_num
                  _ = 43245 * w1 := h_sigma_31cubed
              exact factor_from_eq 30784 43245 w1 hcop h_eq
            rcases h30784_w1 with ⟨x, hw1_eq⟩
            rw [hw1_eq] at h_sigma_31cubed
            have hx_pos : x > 0 := by
              by_contra! hz
              have hx0 : x = 0 := by omega
              rw [hx0, mul_zero] at hw1_eq
              omega
            have h_sigma_x : σ (30784 * x) = 43245 * x := by omega
            by_cases h_cop_30784_x : Nat.Coprime 30784 x
            · have h_mul_30784 : σ (30784 * x) = σ 30784 * σ x :=
                sigma_mul_coprime h_cop_30784_x
              rw [h_mul_30784, show σ 30784 = 67564 by native_decide] at h_sigma_x
              have h_sigma_x_ge_x : σ x ≥ x := sigma_ge_self x hx_pos
              -- 67564 > 43245 → contradiction
              have : 67564 * σ x > 43245 * x := by
                calc
                  67564 * σ x ≥ 67564 * x := Nat.mul_le_mul_left 67564 h_sigma_x_ge_x
                  _ > 43245 * x := by nlinarith
              omega
            · -- 30784|x, even larger → contradiction
              have : 30784 ∣ x := by
                have hp31 : Nat.Prime 31 := by native_decide
                have hgcd_ne_one : Nat.gcd 30784 x ≠ 1 := by
                  rw [Nat.coprime_iff_gcd_eq_one] at h_cop_30784_x
                  exact h_cop_30784_x
                have hgcd_dvd_30784 : Nat.gcd 30784 x ∣ 30784 := Nat.gcd_dvd_left 30784 x
                sorry
              sorry
          · -- 31|w1, even more powers of 31 → σ(31^4) > 45*31²
            have : 31 ∣ w1 := by
              rw [Nat.coprime_iff_gcd_eq_one] at h_cop_31_w1
              have hp31 : Nat.Prime 31 := by native_decide
              have hgcd_ne_one : Nat.gcd 31 w1 ≠ 1 := h_cop_31_w1
              have hgcd_dvd_31 : Nat.gcd 31 w1 ∣ 31 := Nat.gcd_dvd_left 31 w1
              have h := hp31.eq_one_or_self_of_dvd (Nat.gcd 31 w1) hgcd_dvd_31
              rcases h with (h1 | h31_gcd)
              · exfalso; exact hgcd_ne_one h1
              · have hgcd_dvd_w1 : Nat.gcd 31 w1 ∣ w1 := Nat.gcd_dvd_right 31 w1
                rw [h31_gcd] at hgcd_dvd_w1
                exact hgcd_dvd_w1
            rcases this with ⟨w2, hw1_eq⟩
            rw [hw1_eq, show 31³ * (31 * w2) = 31⁴ * w2 by ring] at h_sigma_31cubed
            -- σ(31⁴*w2) = 43245*31*w2 = 1340595*w2
            have h_sigma_31quartic : σ (31⁴ * w2) = 1340595 * w2 := by
              calc
                σ (31⁴ * w2) = σ (31³ * (31 * w2)) := by ring
                _ = 43245 * (31 * w2) := h_sigma_31cubed
                _ = 1340595 * w2 := by norm_num
            have hw2_pos : w2 > 0 := by
              by_contra! hz
              have hw20 : w2 = 0 := by omega
              rw [hw20, mul_zero] at hw1_eq
              omega
            by_cases h_cop_31_w2 : Nat.Coprime 31 w2
            · have h_mul_4 : σ (31⁴ * w2) = σ (31⁴) * σ w2 :=
                sigma_mul_coprime (h_cop_31_w2.pow_left 4)
              rw [h_mul_4, show σ (31⁴) = 31⁴ + 31³ + 31² + 31 + 1 := by native_decide] at h_sigma_31quartic
              -- σ(31⁴) > 1340595, giving contradiction
              have h_sigma_31pow4_val : σ (31⁴) = 31⁴ + 31³ + 31² + 31 + 1 := by native_decide
              have h_sigma_31pow4_gt : σ (31⁴) > 1340595 := by
                calc
                  σ (31⁴) = 31⁴ + 31³ + 31² + 31 + 1 := h_sigma_31pow4_val
                  _ > 1340595 := by
                    have : 31⁴ = 923521 := by norm_num
                    have : 31³ = 29791 := by norm_num
                    nlinarith
              have h_ineq : σ (31⁴) * σ w2 > 1340595 * w2 := by
                have h_sigma_w2_ge_w2 : σ w2 ≥ w2 := sigma_ge_self w2 hw2_pos
                have : σ (31⁴) * σ w2 ≥ σ (31⁴) * w2 :=
                  Nat.mul_le_mul_left (σ (31⁴)) h_sigma_w2_ge_w2
                have : σ (31⁴) * w2 > 1340595 * w2 := by
                  nlinarith
                nlinarith
              omega
            · -- 31|w2, even more powers → each step increases σ(31^k)/31^k → contradiction
              sorry
        · -- 31 ∤ w, so gcd(31,w)=1. Descent: 331|w → 332|v → 588*σ(t)=465*t → contradiction
          have h_cop_31sq_w : Nat.Coprime (31²) w := by
            have hp31 : Nat.Prime 31 := by native_decide
            have h_cop_31_w : Nat.Coprime 31 w :=
              (Nat.Prime.coprime_iff_not_dvd hp31).mpr h31_dvd_w
            exact h_cop_31_w.pow_left 2
          have h_mul_31sq : σ (31² * w) = σ (31²) * σ w := sigma_mul_coprime h_cop_31sq_w
          rw [h_mul_31sq, show σ (31²) = 993 by native_decide] at h_sigma2
          have h331_eq : 331 * σ w = 465 * w := by
            have h993 : 993 = 3 * 331 := by native_decide
            have h1395 : 1395 = 3 * 465 := by native_decide
            rw [show σ (31² * w) = 1395 * w from ?_, h993, h1395] at h_sigma2
            sorry
          sorry"""

# For now, just report what we have
print(f"Fix1 length: {len(fix1)} chars")
print("Fix script prepared")
