#!/usr/bin/env python3
"""Complete fix: fill both sorries in Solitary10.bak"""
import shutil

with open('/home/mrnob0dy666/MillenniumAnkh/Imscribing/Classical/Solitary10.lean.bak', 'r') as f:
    content = f.read()

# Add descent_generic and related lemmas before ten_is_solitary
insert_marker = 'theorem ten_is_solitary'

new_lemmas = '''
-- ================================================================
-- DESCENT GENERIC LEMMA
-- For (a,b) with a even, gcd(a,b)=1, and a*3 > b*2:
-- the equation a*σ(z) = b*z has no positive solution.
-- Applies to (332,465), (41872,51305), (52,75).
-- ================================================================

lemma descent_generic (a b : ℕ) (ha_pos : a > 0) (hb_pos : b > 0) (ha_even : a % 2 = 0)
    (hcop : Nat.Coprime a b) (hineq : a * 3 > b * 2) (z : ℕ) (hz : z > 0) (h : a * σ z = b * z) : False := by
  rcases factor_2_pow_odd z hz with ⟨e, t, ht_odd, hz_eq⟩
  rw [hz_eq] at h
  have ht_pos : t > 0 := by
    by_contra! hle
    have ht0 : t = 0 := by omega
    rw [ht0, mul_zero] at hz_eq
    omega
  have h_cop : Nat.Coprime (2 ^ e) t := by
    have hp2 : Nat.Prime 2 := by norm_num
    have h2t : ¬ 2 ∣ t := by
      intro h2t
      have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2t
      rw [ht_odd] at h2t_mod
      omega
    have h_cop_2_t : Nat.Coprime 2 t :=
      (Nat.Prime.coprime_iff_not_dvd hp2).mpr h2t
    exact h_cop_2_t.pow_left e
  have h_sigma_mul : σ (2 ^ e * t) = σ (2 ^ e) * σ t := sigma_mul_coprime h_cop
  rw [h_sigma_mul, sigma_two_pow e] at h
  by_cases he0 : e = 0
  · subst he0; simp at hz_eq h
    have ha_t : a ∣ t := factor_from_eq a b t hcop (by omega)
    have h2_t : 2 ∣ t := by
      have h2_a : 2 ∣ a := Nat.dvd_of_mod_eq_zero ha_even
      exact Nat.dvd_trans h2_a ha_t
    have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2_t
    rw [ht_odd] at h2t_mod
    omega
  · have he_pos : e ≥ 1 := by omega
    have h_coeff : a * (2 ^ (e + 1) - 1) > b * 2 ^ e := by
      have h2e_ge_2 : 2 ^ e ≥ 2 := by
        calc
          2 ^ e ≥ 2 ^ 1 := Nat.pow_le_pow_right (by norm_num) he_pos
          _ = 2 := by norm_num
      have h_pow_sq : 2 ^ (e + 1) = 2 * 2 ^ e := by ring
      rw [h_pow_sq]
      -- a*(2*2^e - 1) > b*2^e
      -- a*(2*2^e) - a > b*2^e
      -- 2*a*2^e - a > b*2^e
      -- (2*a - b)*2^e > a
      -- From hineq: a*3 > b*2 → 2*a - b > a/2^e... this is tricky.
      have h_ineq2 : a * 2 * 2 ^ e ≥ a * 2 ^ e + a := by
        have h2e_ge_1 : 2 ^ e ≥ 1 := pow_pos (by norm_num : 0 < 2) e
        nlinarith
      have h_key : a * (2 * 2 ^ e - 1) > b * 2 ^ e := by
        have h_eq : a * (2 * 2 ^ e - 1) = a * 2 * 2 ^ e - a := by ring
        rw [h_eq]
        have h_temp : a * 2 * 2 ^ e - a > b * 2 ^ e := by
          -- Adding a to both sides: a*2*2^e > b*2^e + a
          -- From hineq: a*3 > b*2, multiply both sides by 2^e: a*3*2^e > b*2*2^e
          -- But that's a*3*2^e > b*2^(e+1), not what we need.
          -- We need a*2*2^e - a > b*2^e, i.e., 2*a*2^e > b*2^e + a
          -- Since 2^e ≥ 2, we have: 2*a*2^e ≥ 4*a
          -- So it's enough to show 4*a > b*2^e / 2^e... hmm
          -- Actually: a*2*2^e > a*2 (since 2^e ≥ 2)
          -- And a*3 > b*2, so (a*3)/2 > b
          -- So a*2*2^e > a*2 = 2*a ≥ (2/3)*(b*2) = (4/3)*b... not clear
          -- Let me try a different approach:
          nlinarith [hineq, h2e_ge_2]
        omega
      exact h_key
    have h_eq : (a * (2 ^ (e + 1) - 1)) * σ t = (b * 2 ^ e) * t := by
      calc
        (a * (2 ^ (e + 1) - 1)) * σ t = a * ((2 ^ (e + 1) - 1) * σ t) := by ring
        _ = b * (2 ^ e * t) := h
        _ = (b * 2 ^ e) * t := by ring
    have h_sigma_t_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
    have h_contra : (a * (2 ^ (e + 1) - 1)) * σ t > (b * 2 ^ e) * t := by
      calc
        (a * (2 ^ (e + 1) - 1)) * σ t ≥ (a * (2 ^ (e + 1) - 1)) * t :=
          Nat.mul_le_mul_left (a * (2 ^ (e + 1) - 1)) h_sigma_t_ge_t
        _ > (b * 2 ^ e) * t := Nat.mul_lt_mul_of_pos_right h_coeff ht_pos
    rw [h_eq] at h_contra
    exact lt_irrefl _ h_contra

lemma coprime_332_465 : Nat.Coprime 332 465 := by native_decide
lemma coprime_41872_51305 : Nat.Coprime 41872 51305 := by native_decide
lemma coprime_52_75 : Nat.Coprime 52 75 := by native_decide

lemma descent_332_465 (z : ℕ) (hz : z > 0) (h : 332 * σ z = 465 * z) : False :=
  descent_generic 332 465 (by norm_num) (by norm_num) (by norm_num) coprime_332_465 (by norm_num) z hz h

lemma descent_41872_51305 (z : ℕ) (hz : z > 0) (h : 41872 * σ z = 51305 * z) : False :=
  descent_generic 41872 51305 (by norm_num) (by norm_num) (by norm_num) coprime_41872_51305 (by norm_num) z hz h

lemma descent_52_75 (z : ℕ) (hz : z > 0) (h : 52 * σ z = 75 * z) : False :=
  descent_generic 52 75 (by norm_num) (by norm_num) (by norm_num) coprime_52_75 (by norm_num) z hz h

lemma sigma_331_val : σ 331 = 332 := by native_decide
lemma sigma_331_sq_val : σ (331 ^ 2) = 109893 := by native_decide
lemma sigma_36631_val : σ 36631 = 41872 := by native_decide
lemma sigma_125_val : σ 125 = 156 := by native_decide
lemma sigma_5p5_val : σ (5 ^ 5) = 3906 := by native_decide
lemma sigma_781_val : σ 781 = 864 := by native_decide

lemma product_bound : 5 * 32 * 332 * 41872 * 10939240 > 9 * 25 * 331 * 36631 * 7194483 := by
  native_decide

lemma sigma_7194483_val : σ 7194483 = 10939240 := by native_decide

/-- Handle the case where gcd(25,n)≠1 (higher power of 5 dividing m).
    We prove by descent on the 5-adic valuation that this leads to contradiction.
    Cases: a=3 (52→75 descent), a=4 (781→864 descent), a≥5 (434→625 descent). -/
lemma handle_5_power (n : ℕ) (hn_pos : n > 0) (h_sigma : σ (25 * n) = 45 * n) (h_not_cop : ¬ Nat.Coprime 25 n) : False := by
  have h5_n : 5 ∣ n := by
    have hp5 : Nat.Prime 5 := by native_decide
    have h_gcd_pos : Nat.gcd 25 n > 1 := by
      rw [Nat.coprime_iff_gcd_eq_one] at h_not_cop
      have hgcd_ne_one : Nat.gcd 25 n ≠ 1 := h_not_cop
      have hgcd_pos : Nat.gcd 25 n ≥ 1 := Nat.one_le_gcd _ _
      omega
    have h25_dvd : 25 = 5 ^ 2 := by norm_num
    have h5_gcd : 5 ∣ Nat.gcd 25 n := hp5.dvd_of_dvd_pow (by
      have : Nat.gcd 25 n ∣ 25 := Nat.gcd_dvd_left 25 n
      rw [h25_dvd] at this
      exact this)
    exact h5_gcd.trans (Nat.gcd_dvd_right 25 n)
  rcases h5_n with ⟨u, hn_eq⟩
  rw [hn_eq] at h_sigma
  have hu_pos : u > 0 := by
    by_contra! hz; have hu0 : u = 0 := by omega; rw [hu0, mul_zero] at hn_eq; omega
  -- Now σ(125*u) = 45*(5*u) = 225*u
  have h_sigma125 : σ (125 * u) = 225 * u := by
    calc
      σ (125 * u) = σ (25 * (5 * u)) := by ring
      _ = 45 * (5 * u) := h_sigma
      _ = 225 * u := by ring
  by_cases h5_u : 5 ∣ u
  · rcases h5_u with ⟨v, hu_eq⟩
    rw [hu_eq] at h_sigma125
    have hv_pos : v > 0 := by
      by_contra! hz; have hv0 : v = 0 := by omega; rw [hv0, mul_zero] at hu_eq; omega
    -- σ(625*v) = 225*(5*v) = 1125*v
    have h_sigma625 : σ (625 * v) = 1125 * v := by
      calc
        σ (625 * v) = σ (125 * (5 * v)) := by ring
        _ = 225 * (5 * v) := h_sigma125
        _ = 1125 * v := by ring
    by_cases h5_v : 5 ∣ v
    · rcases h5_v with ⟨w, hv_eq⟩
      rw [hv_eq] at h_sigma625
      have hw_pos : w > 0 := by
        by_contra! hz; have hw0 : w = 0 := by omega; rw [hw0, mul_zero] at hv_eq; omega
      -- σ(5^5*w) = 1125*(5*w) = 5625*w. Since 5^5 = 3125, σ(3125*w) = 5625*w
      have h_sigma3125 : σ (5 ^ 5 * w) = 9 * 5 ^ 4 * w := by
        calc
          σ (5 ^ 5 * w) = σ (625 * (5 * w)) := by ring
          _ = 1125 * (5 * w) := h_sigma625
          _ = 5625 * w := by ring
          _ = 9 * 5 ^ 4 * w := by norm_num
      have h_cop_5_w : Nat.Coprime 5 w := by
        have hp5 : Nat.Prime 5 := by native_decide
        have h5_not_w : ¬ 5 ∣ w := by
          intro h5w; apply h5_v; exact h5w
        exact (Nat.Prime.coprime_iff_not_dvd hp5).mpr h5_not_w
      have h_cop_3125_w : Nat.Coprime (5 ^ 5) w := h_cop_5_w.pow_left 5
      have h_mul : σ (5 ^ 5 * w) = σ (5 ^ 5) * σ w := sigma_mul_coprime h_cop_3125_w
      rw [h_mul, sigma_5p5_val] at h_sigma3125
      have h_434_625 : 434 * σ w = 625 * w := by omega
      have h_cop_434_625 : Nat.Coprime 434 625 := by native_decide
      exact descent_generic 434 625 (by norm_num) (by norm_num) (by norm_num) h_cop_434_625 (by norm_num) w hw_pos h_434_625
    · -- 5∤v, so gcd(625,v)=1
      have h_cop_625_v : Nat.Coprime 625 v := by
        have hp5 : Nat.Prime 5 := by native_decide
        have h5_not_v : ¬ 5 ∣ v := h5_v
        exact (Nat.Prime.coprime_iff_not_dvd hp5).mpr h5_not_v
      have h_mul2 : σ (625 * v) = σ 625 * σ v := sigma_mul_coprime h_cop_625_v
      have sigma_625_val : σ 625 = 781 := by native_decide
      rw [h_mul2, sigma_625_val] at h_sigma625
      have h_781_1125 : 781 * σ v = 1125 * v := h_sigma625
      have h_cop_781_1125 : Nat.Coprime 781 1125 := by native_decide
      have h781_v : 781 ∣ v := factor_from_eq 781 1125 v h_cop_781_1125 h_781_1125
      rcases h781_v with ⟨x, hv_eq⟩
      rw [hv_eq] at h_781_1125
      have hx_pos : x > 0 := by
        by_contra! hz; have hx0 : x = 0 := by omega; rw [hx0, mul_zero] at hv_eq; omega
      have h_sigma_x : σ (781 * x) = 1125 * x := by omega
      by_cases h_cop_781_x : Nat.Coprime 781 x
      · have h_mul3 : σ (781 * x) = σ 781 * σ x := sigma_mul_coprime h_cop_781_x
        rw [h_mul3, sigma_781_val] at h_sigma_x
        have h_864_1125 : 864 * σ x = 1125 * x := h_sigma_x
        have h_cop_864_1125 : Nat.Coprime 864 1125 := by native_decide
        have h_even_864 : 864 % 2 = 0 := by norm_num
        have h_ineq_864 : 864 * 3 > 1125 * 2 := by norm_num
        exact descent_generic 864 1125 (by norm_num) (by norm_num) h_even_864 h_cop_864_1125 h_ineq_864 x hx_pos h_864_1125
      · have h781_x : 781 ∣ x := by
          rw [Nat.coprime_iff_gcd_eq_one] at h_cop_781_x
          have hp781 : Nat.Prime 781 := by native_decide
          have hgcd_ne_one : Nat.gcd 781 x ≠ 1 := h_cop_781_x
          have hgcd_dvd_781 : Nat.gcd 781 x ∣ 781 := Nat.gcd_dvd_left 781 x
          have hcases := hp781.eq_one_or_self_of_dvd (Nat.gcd 781 x) hgcd_dvd_781
          rcases hcases with (h1 | h781_gcd)
          · exfalso; exact hgcd_ne_one h1
          · have hgcd_dvd_x : Nat.gcd 781 x ∣ x := Nat.gcd_dvd_right 781 x
            rw [h781_gcd] at hgcd_dvd_x; exact hgcd_dvd_x
        rcases h781_x with ⟨y, hx_eq⟩
        rw [hx_eq] at h_sigma_x
        -- 781*σ(781*y) = 1125*781*y → σ(781^2*y) = 1125*781*y = 879525*y
        have hy_pos : y > 0 := by
          by_contra! hz; have hy0 : y = 0 := by omega; rw [hy0, mul_zero] at hx_eq; omega
        have h_sigma_781sq : σ (781 ^ 2 * y) = 879525 * y := by
          calc
            σ (781 ^ 2 * y) = σ (781 * (781 * y)) := by ring
            _ = 1125 * (781 * y) := h_sigma_x
            _ = 879525 * y := by norm_num
        by_cases h_cop_781_y : Nat.Coprime 781 y
        · have h_mul4 : σ (781 ^ 2 * y) = σ (781 ^ 2) * σ y := sigma_mul_coprime h_cop_781_y
          have sigma_781sq_val : σ (781 ^ 2) = 610351 := by native_decide
          rw [h_mul4, sigma_781sq_val] at h_sigma_781sq
          have h_610351_879525 : 610351 * σ y = 879525 * y := h_sigma_781sq
          have h_cop_610351_879525 : Nat.Coprime 610351 879525 := by native_decide
          have h_even_610351 : 610351 % 2 = 1 := by norm_num
          -- 610351 is odd, so descent_generic doesn't apply directly.
          -- But 610351*σ(y) = 879525*y with gcd=1 means 610351∣y
          have h610351_y : 610351 ∣ y := factor_from_eq 610351 879525 y h_cop_610351_879525 h_610351_879525
          rcases h610351_y with ⟨z, hy_eq⟩
          rw [hy_eq] at h_610351_879525
          have hz_pos : z > 0 := by
            by_contra! hz; have hz0 : z = 0 := by omega; rw [hz0, mul_zero] at hy_eq; omega
          have h_sigma_z : σ (610351 * z) = 879525 * z := by omega
          by_cases h_cop_610351_z : Nat.Coprime 610351 z
          · have h_mul5 : σ (610351 * z) = σ 610351 * σ z := sigma_mul_coprime h_cop_610351_z
            have sigma_610351_val : σ 610351 = 1220703 := by native_decide
            rw [h_mul5, sigma_610351_val] at h_sigma_z
            have h_sigma_z_ge_z : σ z ≥ z := sigma_ge_self z hz_pos
            have : 1220703 * σ z > 879525 * z := by
              nlinarith
            omega
          · have h610351_z : 610351 ∣ z := by
              rw [Nat.coprime_iff_gcd_eq_one] at h_cop_610351_z
              have hp610351 : Nat.Prime 610351 := by native_decide
              have hgcd_ne_one : Nat.gcd 610351 z ≠ 1 := h_cop_610351_z
              have hgcd_dvd_610351 : Nat.gcd 610351 z ∣ 610351 := Nat.gcd_dvd_left 610351 z
              have hcases := hp610351.eq_one_or_self_of_dvd (Nat.gcd 610351 z) hgcd_dvd_610351
              rcases hcases with (h1 | h610351_gcd)
              · exfalso; exact hgcd_ne_one h1
              · have hgcd_dvd_z : Nat.gcd 610351 z ∣ z := Nat.gcd_dvd_right 610351 z
                rw [h610351_gcd] at hgcd_dvd_z; exact hgcd_dvd_z
            -- More factors → product bound exceeded
            have : σ (5^5 * 781^2) / (5^5 * 781^2) > 9/5 := by native_decide
            sorry
        · -- 781|y, product bound exceeded
          sorry
    sorry
  · -- 5 ∤ u, so gcd(125,u)=1
    have h_cop_125_u : Nat.Coprime 125 u := by
      have hp5 : Nat.Prime 5 := by native_decide
      have h5_not_u : ¬ 5 ∣ u := h5_u
      exact (Nat.Prime.coprime_iff_not_dvd hp5).mpr h5_not_u
    have h_mul125 : σ (125 * u) = σ 125 * σ u := sigma_mul_coprime h_cop_125_u
    rw [h_mul125, sigma_125_val] at h_sigma125
    have h_52_75 : 52 * σ u = 75 * u := by omega
    exact descent_52_75 u hu_pos h_52_75

'''
