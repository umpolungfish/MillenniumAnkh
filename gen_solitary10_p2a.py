#!/usr/bin/env python3
"""Append descent_8_5, descent_7_5, descent_32_45 to Solitary10.lean."""
LEAN_FILE = "/home/mrnob0dy666/MillenniumAnkh/Imscribing/Classical/Solitary10.lean"

p2 = r"""

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
"""

with open(LEAN_FILE, 'a') as f:
    f.write(p2)
print(f"Part 2a: {len(p2)} chars")
