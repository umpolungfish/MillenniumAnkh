#!/usr/bin/env python3
"""Append descent_31_45 and main theorem."""
LEAN_FILE = "/home/mrnob0dy666/MillenniumAnkh/Imscribing/Classical/Solitary10.lean"

p3 = r"""

/-- From 31*σ(x) = 45*x with x>0, derive a contradiction.
    Either 31∥x (reducing to 32*σ(x/31)=45*(x/31)) or 31²|x
    (reducing to 993*σ(x/31²)=1395*(x/31²) → 331*σ(z)=465*z).
    Both cases lead to contradiction. -/
lemma descent_31_45 (x : ℕ) (hx_pos : x > 0) (h_eq : 31 * σ x = 45 * x) : False := by
  have h31x : 31 ∣ x := by
    have h31_dvd_45x : 31 ∣ 45 * x := by
      rw [← h_eq]; exact ⟨σ x, by ring⟩
    exact coprime_31_45.dvd_of_dvd_mul_left h31_dvd_45x
  rcases factor_p_pow 31 x prime_31 hx_pos with ⟨k, t, h31t, hx_factor⟩
  have hk_ge1 : k ≥ 1 := by
    by_contra! hk0
    have hk0' : k = 0 := by omega
    rw [hk0', pow_zero, one_mul] at hx_factor
    exact h31t (by rw [hx_factor]; exact h31x)
  have ht_pos : t > 0 := by
    by_contra! ht0; rw [ht0] at hx_factor; simp at hx_factor; omega
  have h_cop : Nat.Coprime (31 ^ k) t :=
    ((Nat.Prime.coprime_iff_not_dvd prime_31).mpr h31t).pow_left k
  rw [hx_factor] at h_eq
  have h_sigma : σ (31 ^ k * t) = σ (31 ^ k) * σ t := sigma_mul_coprime h_cop
  rw [h_sigma] at h_eq
  -- If k=1: 31*σ(31)*σ(t) = 45*31*t → 32*σ(t) = 45*t
  -- If k≥2: 31*σ(31^k) > 45*31^k? No, 31<45 so 31*σ(31^k) < 45*31^k for small k.
  -- But we can use k=1 case and handle k≥2 separately via σ(31²) factorization.
  by_cases hk_eq1 : k = 1
  · rw [hk_eq1] at h_eq
    have h_sigma_31 : σ (31 ^ 1) = σ 31 := by norm_num
    rw [h_sigma_31, sigma_31_val] at h_eq
    have h_eq2 : 32 * σ t = 45 * t := by omega
    exact descent_32_45 t ht_pos h_eq2
  · have hk_ge2 : k ≥ 2 := by omega
    -- k≥2: factor σ(31²) = 993 = 3*331
    -- 31*σ(31^k)*σ(t) = 45*31^k*t
    -- Since σ(31^k) ≥ σ(31²) = 993 for k≥2, and 31*993 = 30783, 45*31² = 43245
    -- 30783 < 43245, so no direct contradiction
    -- Instead: factor out 31² explicitly
    have h_31sq_dvd : 31 ^ 2 ∣ x := by
      rw [hx_factor]
      have : 31 ^ 2 ∣ 31 ^ k := Nat.pow_dvd_pow 31 (by omega)
      exact Nat.dvd_mul_of_dvd_left this t
    rcases h_31sq_dvd with ⟨z, hx_31sq_eq⟩
    rw [hx_31sq_eq] at h_eq
    have hz_pos : z > 0 := by
      by_contra! hz0; rw [hz0] at hx_31sq_eq; simp at hx_31sq_eq; omega
    -- x = 31²*z, so σ(x) = σ(31²*z). Need gcd(31²,z)=1 or not.
    by_cases h31z : 31 ∣ z
    · -- 31³|x: factor more
      rcases factor_p_pow 31 z prime_31 hz_pos with ⟨a, w, h31w, hz_factor⟩
      rw [hz_factor] at hx_31sq_eq
      -- x = 31² * (31^a * w) = 31^(a+2) * w
      -- σ(x) = σ(31^(a+2)) * σ(w)
      -- 31*σ(31^(a+2))*σ(w) = 45*31^(a+2)*w
      -- We need a contradiction. Use the same factorization approach.
      -- For a≥0: 31^(a+2) has factor 31², and σ(31^(a+2)) has factor σ(31²)=993.
      -- 31*993*σ(31^a)*σ(w) = 45*31^(a+2)*w ... hmm, not quite right.
      -- Actually, σ(31^(a+2)) = (31^(a+3)-1)/30, which is divisible by σ(31²) = 993
      -- So we get the 331 factor.
      sorry
    · -- gcd(31²,z)=1
      have h_cop_31sq_z : Nat.Coprime (31 ^ 2) z :=
        ((Nat.Prime.coprime_iff_not_dvd prime_31).mpr h31z).pow_left 2
      have h_sigma_31sq_z : σ (31 ^ 2 * z) = σ (31 ^ 2) * σ z := sigma_mul_coprime h_cop_31sq_z
      rw [h_sigma_31sq_z, sigma_31_sq_val] at h_eq
      -- 31*993*σ(z) = 45*961*z → 30783*σ(z) = 43245*z → 993*σ(z) = 1395*z
      have h_eq2 : 993 * σ z = 1395 * z := by omega
      -- 993=3*331, 1395=3*465 → 331*σ(z) = 465*z
      have h_eq3 : 331 * σ z = 465 * z := by omega
      -- Need descent_331_465 lemma
      sorry
"""

with open(LEAN_FILE, 'a') as f:
    f.write(p3)
print(f"Part 3: {len(p3)} chars")
