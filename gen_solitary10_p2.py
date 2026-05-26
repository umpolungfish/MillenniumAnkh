#!/usr/bin/env python3
"""Append the descent lemmas and main theorem to Solitary10.lean."""
import os

LEAN_FILE = "/home/mrnob0dy666/MillenniumAnkh/Imscribing/Classical/Solitary10.lean"

content = r"""

/-- From 8*σ(w) = 5*w with w>0, derive a contradiction.
    Factor the 2-power from w. Since 8|w, w = 2^k * u with k≥3, u odd.
    Then 8*(2^(k+1)-1)*σ(u) = 5*2^k*u, giving 11*2^k ≤ 8, impossible for k≥3. -/
lemma descent_8_5 (w : ℕ) (hw_pos : w > 0) (h_eq : 8 * σ w = 5 * w) : False := by
  have h_cop_8_5 : Nat.Coprime 8 5 := by native_decide
  have h8w : 8 ∣ w := by
    have h8_dvd_5w : 8 ∣ 5 * w := by
      rw [← h_eq]; exact ⟨σ w, by ring⟩
    exact h_cop_8_5.dvd_of_dvd_mul_left h8_dvd_5w
  rcases factor_2_pow_odd w hw_pos with ⟨k, u, hu_odd, hw_factor⟩
  have hk_ge3 : k ≥ 3 := by
    by_contra! hk_lt3
    rw [hw_factor]
    have h_2k_lt_8 : 2 ^ k < 8 := by
      have : k ≤ 2 := by omega
      interval_cases k; norm_num; norm_num; norm_num
    intro h8
    have : 2 ^ k ∣ 8 := Nat.dvd_of_dvd_mul_right (pow_pos (by norm_num) k) h8
    have : 8 ≤ 2 ^ k := Nat.le_of_dvd (by norm_num) this
    omega
  have hu_pos : u > 0 := by
    by_contra! hu0; rw [hu0] at hw_factor; simp at hw_factor; omega
  have h2u : ¬ 2 ∣ u := by
    intro h2u
    have : u % 2 = 0 := Nat.mod_eq_zero_of_dvd h2u
    rw [hu_odd] at this; omega
  have h_cop : Nat.Coprime (2 ^ k) u :=
    ((Nat.Prime.coprime_iff_not_dvd prime_2).mpr h2u).pow_left k
  rw [hw_factor] at h_eq
  have h_sigma : σ (2 ^ k * u) = σ (2 ^ k) * σ u := sigma_mul_coprime h_cop
  rw [h_sigma, sigma_two_pow k] at h_eq
  have h_sigma_ge_u : σ u ≥ u := sigma_ge_self u hu_pos
  -- Bound: 8*(2^(k+1)-1) > 5*2^k for k≥3
  have h_bound : 8 * ((2 : ℕ) ^ (k + 1) - 1) > 5 * (2 : ℕ) ^ k := by
    have : (2 : ℕ) ^ (k + 1) = 2 * (2 : ℕ) ^ k := by rw [pow_succ]
    rw [this]
    have h_pow_ge : (2 : ℕ) ^ k ≥ 8 := by
      calc
        2 ^ k ≥ 2 ^ 3 := Nat.pow_le_pow_right (by norm_num) hk_ge3
        _ = 8 := by norm_num
    nlinarith
  have h_pos : (2 : ℕ) ^ (k + 1) - 1 > 0 := by
    have : (2 : ℕ) ^ (k + 1) ≥ 2 := Nat.one_le_two_pow _
    omega
  have h_rhs : 8 * ((2 : ℕ) ^ (k + 1) - 1) * σ u = 5 * (2 : ℕ) ^ k * u := by omega
  have h_lt : 8 * ((2 : ℕ) ^ (k + 1) - 1) * u < 8 * ((2 : ℕ) ^ (k + 1) - 1) * σ u := by
    nlinarith
  rw [h_rhs] at h_lt
  have : 5 * (2 : ℕ) ^ k * u < 8 * ((2 : ℕ) ^ (k + 1) - 1) * u := by nlinarith
  nlinarith

/-- From 7*σ(z) = 5*z with z>0, derive a contradiction.
    Factor the 7-power from z and use 7*σ(7^k) > 5*7^k for all k≥1. -/
lemma descent_7_5 (z : ℕ) (hz_pos : z > 0) (h_eq : 7 * σ z = 5 * z) : False := by
  have h_cop_7_5 : Nat.Coprime 7 5 := by native_decide
  have h7z : 7 ∣ z := by
    have h7_dvd_5z : 7 ∣ 5 * z := by
      rw [← h_eq]; exact ⟨σ z, by ring⟩
    exact h_cop_7_5.dvd_of_dvd_mul_left h7_dvd_5z
  rcases factor_p_pow 7 z prime_7 hz_pos with ⟨k, t, h7t, hz_factor⟩
  have hk_ge1 : k ≥ 1 := by
    by_contra! hk0
    have hk0' : k = 0 := by omega
    rw [hk0', pow_zero, one_mul] at hz_factor
    exact h7t (by rw [hz_factor]; exact h7z)
  have ht_pos : t > 0 := by
    by_contra! ht0; rw [ht0] at hz_factor; simp at hz_factor; omega
  have h_cop : Nat.Coprime (7 ^ k) t :=
    ((Nat.Prime.coprime_iff_not_dvd prime_7).mpr h7t).pow_left k
  rw [hz_factor] at h_eq
  have h_sigma : σ (7 ^ k * t) = σ (7 ^ k) * σ t := sigma_mul_coprime h_cop
  rw [h_sigma] at h_eq
  have h_sigma_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
  -- Key: 7 * σ(7^k) > 5 * 7^k for all k≥1
  have h_key : 7 * σ (7 ^ k) > 5 * 7 ^ k := by
    have h_formula : 6 * σ (7 ^ k) = 7 ^ (k + 1) - 1 := by
      have := sigma_one_apply_prime_pow prime_7 (i := k)
      rw [this]
      omega
    have h_19pow : 19 * 7 ^ k > 7 := by
      have h_pow_ge1 : 7 ^ k ≥ 1 := pow_pos (by norm_num) k
      nlinarith
    -- From 7*σ(7^k) = 7*(7^(k+1)-1)/6 = (49*7^k-7)/6
    -- And 5*7^k = (30*7^k)/6
    -- We need 49*7^k - 7 > 30*7^k i.e. 19*7^k > 7
    have h_mul : 7 * (6 * σ (7 ^ k)) > 5 * 7 ^ k * 6 := by
      rw [h_formula]
      have : 7 * (7 ^ (k + 1) - 1) = 49 * 7 ^ k - 7 := by
        rw [pow_succ]; ring
      rw [this]
      have : 5 * 7 ^ k * 6 = 30 * 7 ^ k := by ring
      rw [this]
      nlinarith
    have h_pos : 6 * σ (7 ^ k) > 0 := by
      have : σ (7 ^ k) ≥ 1 := sigma_ge_self (7 ^ k) (pow_pos (by norm_num) k)
      omega
    omega
  nlinarith

/-- From 32*σ(y) = 45*y with y>0, derive a contradiction.
    Factor the 2-power from y. Since 32|y, y = 2^k * u with k≥5, u odd.
    Then 32*(2^(k+1)-1)*σ(u) = 45*2^k*u, giving 19*2^k ≤ 32, impossible for k≥5. -/
lemma descent_32_45 (y : ℕ) (hy_pos : y > 0) (h_eq : 32 * σ y = 45 * y) : False := by
  have h32y : 32 ∣ y := by
    have h32_dvd_45y : 32 ∣ 45 * y := by
      rw [← h_eq]; exact ⟨σ y, by ring⟩
    exact coprime_32_45.dvd_of_dvd_mul_left h32_dvd_45y
  rcases factor_2_pow_odd y hy_pos with ⟨k, u, hu_odd, hy_factor⟩
  have hk_ge5 : k ≥ 5 := by
    by_contra! hk_lt5
    rw [hy_factor]
    have h_2k_lt_32 : 2 ^ k < 32 := by
      have : k ≤ 4 := by omega
      interval_cases k; norm_num; norm_num; norm_num; norm_num; norm_num
    intro h32
    have : 2 ^ k ∣ 32 := Nat.dvd_of_dvd_mul_right (pow_pos (by norm_num) k) h32
    have : 32 ≤ 2 ^ k := Nat.le_of_dvd (by norm_num) this
    omega
  have hu_pos : u > 0 := by
    by_contra! hu0; rw [hu0] at hy_factor; simp at hy_factor; omega
  have h2u : ¬ 2 ∣ u := by
    intro h2u
    have : u % 2 = 0 := Nat.mod_eq_zero_of_dvd h2u
    rw [hu_odd] at this; omega
  have h_cop : Nat.Coprime (2 ^ k) u :=
    ((Nat.Prime.coprime_iff_not_dvd prime_2).mpr h2u).pow_left k
  rw [hy_factor] at h_eq
  have h_sigma : σ (2 ^ k * u) = σ (2 ^ k) * σ u := sigma_mul_coprime h_cop
  rw [h_sigma, sigma_two_pow k] at h_eq
  have h_sigma_ge_u : σ u ≥ u := sigma_ge_self u hu_pos
  -- Bound: 32*(2^(k+1)-1) > 45*2^k for k≥5
  have h_bound : 32 * ((2 : ℕ) ^ (k + 1) - 1) > 45 * (2 : ℕ) ^ k := by
    have : (2 : ℕ) ^ (k + 1) = 2 * (2 : ℕ) ^ k := by rw [pow_succ]
    rw [this]
    have h_pow_ge : (2 : ℕ) ^ k ≥ 32 := by
      calc
        2 ^ k ≥ 2 ^ 5 := Nat.pow_le_pow_right (by norm_num) hk_ge5
        _ = 32 := by norm_num
    nlinarith
  have h_pos : (2 : ℕ) ^ (k + 1) - 1 > 0 := by
    have : (2 : ℕ) ^ (k + 1) ≥ 2 := Nat.one_le_two_pow _
    omega
  have h_rhs : 32 * ((2 : ℕ) ^ (k + 1) - 1) * σ u = 45 * (2 : ℕ) ^ k * u := by omega
  have h_lt : 32 * ((2 : ℕ) ^ (k + 1) - 1) * u < 32 * ((2 : ℕ) ^ (k + 1) - 1) * σ u := by
    nlinarith
  rw [h_rhs] at h_lt
  have : 45 * (2 : ℕ) ^ k * u < 32 * ((2 : ℕ) ^ (k + 1) - 1) * u := by nlinarith
  nlinarith
"""

with open(LEAN_FILE, 'a') as f:
    f.write(content)
print(f"Part 2 appended: {len(content)} chars")
