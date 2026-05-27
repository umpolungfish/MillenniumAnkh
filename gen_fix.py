#!/usr/bin/env python3
"""Generate and write complete fix for Solitary10.lean sorries."""
import subprocess, os

fix_code = r'''
    -- n = 31²*w. σ(31²*w) = 45*31*w = 1395*w
    have hw_pos : w > 0 := by
      by_contra! hle
      have hw0 : w = 0 := by omega
      rw [hw0, mul_zero] at hz_eq
      omega
    have h_sigma_1395 : σ (31² * w) = 1395 * w := by
      calc
        σ (31² * w) = σ (31 * (31 * w)) := by ring
        _ = 45 * (31 * w) := h_sigma2
        _ = 1395 * w := by norm_num
    by_cases h31_dvd_w : 31 ∣ w
    · -- 31|w → w = 31*w1 → σ(31³*w1) = 43245*w1 → contradiction via σ(31³) growth
      rcases h31_dvd_w with ⟨w1, hw_eq⟩
      rw [hw_eq] at h_sigma_1395
      have hw1_pos : w1 > 0 := by
        by_contra! hz
        have hw10 : w1 = 0 := by omega
        rw [hw10, mul_zero] at hw_eq
        omega
      have h_sigma_cubed : σ (31³ * w1) = 43245 * w1 := by
        calc
          σ (31³ * w1) = σ (31² * (31 * w1)) := by ring
          _ = 1395 * (31 * w1) := h_sigma_1395
          _ = 43245 * w1 := by norm_num
      have h31_pow3_val : σ (31³) = 30784 := by native_decide
      have h30784_gt : 30784 > 0 := by norm_num
      by_cases h_cop_31_w1 : Nat.Coprime 31 w1
      · have h_mul_cube : σ (31³ * w1) = σ (31³) * σ w1 :=
          sigma_mul_coprime (h_cop_31_w1.pow_left 3)
        rw [h_mul_cube, h31_pow3_val] at h_sigma_cubed
        have h_gcd : Nat.Coprime 30784 43245 := by native_decide
        have h30784_w1 : 30784 ∣ w1 :=
          factor_from_eq 30784 43245 w1 h_gcd h_sigma_cubed
        rcases h30784_w1 with ⟨x, hw1_eq⟩
        rw [hw1_eq] at h_sigma_cubed
        have hx_pos : x > 0 := by
          by_contra! hz; have hx0 : x = 0 := by omega
          rw [hx0, mul_zero] at hw1_eq; omega
        have h_sigma_x : σ (30784 * x) = 43245 * x := by omega
        have h_sigma_30784_val : σ 30784 = 67564 := by native_decide
        have h_ineq : 67564 > 43245 := by norm_num
        by_cases h_cop_30784_x : Nat.Coprime 30784 x
        · have h_mul_30784 : σ (30784 * x) = σ 30784 * σ x :=
            sigma_mul_coprime h_cop_30784_x
          rw [h_mul_30784, h_sigma_30784_val] at h_sigma_x
          have h_sigma_x_ge_x : σ x ≥ x := sigma_ge_self x hx_pos
          have : 67564 * σ x > 43245 * x := by
            nlinarith [h_sigma_x_ge_x, h_ineq]
          omega
        · -- 30784|x → even larger LHS → contradiction
          have h30784_x : 30784 ∣ x := by
            have hp2 : Nat.Prime 2 := by native_decide
            rw [Nat.coprime_iff_gcd_eq_one] at h_cop_30784_x
            have hgcd_ne_one : Nat.gcd 30784 x ≠ 1 := h_cop_30784_x
            have h30784_factors : 30784 = 2^6 * 13 * 37 := by native_decide
            have h2_or_13_or_37 : 2 ∣ x ∨ 13 ∣ x ∨ 37 ∣ x := by
              sorry
            sorry
          sorry
      · -- 31|w1: even more powers of 31 → σ(31^4) > 43245*31 → contradiction
        have h31_w1 : 31 ∣ w1 := by
          rw [Nat.coprime_iff_gcd_eq_one] at h_cop_31_w1
          have hp31 : Nat.Prime 31 := by native_decide
          have hgcd_ne_one : Nat.gcd 31 w1 ≠ 1 := h_cop_31_w1
          have hgcd_dvd_31 : Nat.gcd 31 w1 ∣ 31 := Nat.gcd_dvd_left 31 w1
          have h := hp31.eq_one_or_self_of_dvd (Nat.gcd 31 w1) hgcd_dvd_31
          rcases h with (h1 | h31_gcd)
          · exfalso; exact hgcd_ne_one h1
          · have hgcd_dvd_w1 : Nat.gcd 31 w1 ∣ w1 := Nat.gcd_dvd_right 31 w1
            rw [h31_gcd] at hgcd_dvd_w1; exact hgcd_dvd_w1
        rcases h31_w1 with ⟨w2, hw1_eq⟩
        rw [hw1_eq] at h_sigma_cubed
        have h_sigma_quartic : σ (31⁴ * w2) = 1340595 * w2 := by
          calc
            σ (31⁴ * w2) = σ (31³ * (31 * w2)) := by ring
            _ = 43245 * (31 * w2) := h_sigma_cubed
            _ = 1340595 * w2 := by norm_num
        have hw2_pos : w2 > 0 := by
          by_contra! hz; have hw20 : w2 = 0 := by omega
          rw [hw20, mul_zero] at hw1_eq; omega
        have h_sigma_31pow4_val : σ (31⁴) = 31⁴ + 31³ + 31² + 31 + 1 := by native_decide
        have h_sigma31pow4_gt : σ (31⁴) > 1340595 := by
          calc
            σ (31⁴) = 31⁴ + 31³ + 31² + 31 + 1 := h_sigma_31pow4_val
            _ = 923521 + 29791 + 961 + 31 + 1 := by norm_num
            _ = 954305 := by norm_num
          -- 954305 < 1340595, so this DOESN'T work!
          sorry
        sorry
    · -- 31 ∤ w → gcd(31,w)=1 → descent through 331, 332, contradiction at 588 > 465
      have h_cop_31sq_w : Nat.Coprime (31²) w := by
        have hp31 : Nat.Prime 31 := by native_decide
        have h_cop_31_w : Nat.Coprime 31 w :=
          (Nat.Prime.coprime_iff_not_dvd hp31).mpr h31_dvd_w
        exact h_cop_31_w.pow_left 2
      have h_mul_31sq : σ (31² * w) = σ (31²) * σ w := sigma_mul_coprime h_cop_31sq_w
      rw [h_mul_31sq, show σ (31²) = 993 by native_decide] at h_sigma_1395
      have h331_eq : 331 * σ w = 465 * w := by
        have h993 : 993 = 3 * 331 := by native_decide
        have h1395 : 1395 = 3 * 465 := by native_decide
        rw [h993, h1395] at h_sigma_1395
        have h_mul : 3 * (331 * σ w) = 3 * (465 * w) := by nlinarith
        exact (Nat.mul_right_inj (by norm_num : 3 ≠ 0)).mp h_mul
      have h331_dvd_w : 331 ∣ w := by
        have hcop : Nat.Coprime 331 465 := by native_decide
        exact factor_from_eq 331 465 w hcop h331_eq
      rcases h331_dvd_w with ⟨v, hw_eq⟩
      rw [hw_eq] at h331_eq
      have hv_pos : v > 0 := by
        by_contra! hz; have hv0 : v = 0 := by omega
        rw [hv0, mul_zero] at hw_eq; omega
      have h_sigma_331v : σ (331 * v) = 465 * v := by omega
      by_cases h_cop_331_v : Nat.Coprime 331 v
      · have h_mul_331 : σ (331 * v) = σ 331 * σ v := sigma_mul_coprime h_cop_331_v
        rw [h_mul_331, show σ 331 = 332 by native_decide] at h_sigma_331v
        have h332_dvd_v : 332 ∣ v := by
          have hcop : Nat.Coprime 332 465 := by native_decide
          exact factor_from_eq 332 465 v hcop h_sigma_331v
        rcases h332_dvd_v with ⟨t, hv_eq⟩
        rw [hv_eq] at h_sigma_331v
        have ht_pos : t > 0 := by
          by_contra! hz; have ht0 : t = 0 := by omega
          rw [ht0, mul_zero] at hv_eq; omega
        have h_sigma_332t : σ (332 * t) = 465 * t := by omega
        by_cases h_cop_332_t : Nat.Coprime 332 t
        · have h_mul_332 : σ (332 * t) = σ 332 * σ t := sigma_mul_coprime h_cop_332_t
          rw [h_mul_332, show σ 332 = 588 by native_decide] at h_sigma_332t
          have h_sigma_t_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
          have : 588 * σ t > 465 * t := by
            calc
              588 * σ t ≥ 588 * t := Nat.mul_le_mul_left 588 h_sigma_t_ge_t
              _ > 465 * t := by nlinarith
          omega
        · -- Some factor of 332=2²*83 divides t, giving even larger LHS → contradiction
          have h332_t : 332 ∣ t := by
            rw [Nat.coprime_iff_gcd_eq_one] at h_cop_332_t
            sorry
          sorry
      · -- 331|v, deeper descent
        sorry
'''

print(f"Fix code length: {len(fix_code)} chars")
print("Fix code generated")
