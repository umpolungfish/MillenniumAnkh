#!/usr/bin/env python3
"""Fix the descent_even_coeff lemma to have a proper inequality proof."""

with open('Imscribing/Classical/Solitary10.lean', 'r') as f:
    content = f.read()

# Find the descent_even_coeff lemma and fix the sorry
old_lemma = '''/-- A general descent lemma: if a * σ(x) = b * x with a even, b odd, gcd(a,b)=1,
    a > 0, and 2*a > b, then no positive x can satisfy the equation.
    The proof factors x = 2^e * t with t odd:
    - If e = 0 (x odd): a | x (from gcd(a,b)=1) but a even and x odd → contradiction.
    - If e ≥ 1: uses the inequality a*(2^(e+1)-1) > b*2^e (which follows from 2*a > b). -/
lemma descent_even_coeff (a b x : ℕ) (ha_even : a % 2 = 0) (hb_odd : b % 2 = 1)
    (hcop : Nat.Coprime a b) (hx_pos : x > 0) (h : a * σ x = b * x) (h_ineq : 2 * a > b) :
    False := by
  rcases factor_2_pow_odd x hx_pos with ⟨e, t, ht_odd, hx_eq⟩
  rw [hx_eq] at h
  have ht_pos : t > 0 := by
    by_contra! hle
    have ht0 : t = 0 := by omega
    rw [ht0, mul_zero] at hx_eq
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
  -- h: a * ((2^(e+1)-1) * σ t) = b * (2^e * t)
  by_cases he0 : e = 0
  · -- e = 0: x = t is odd
    subst he0
    simp at hx_eq h
    -- h: a * (1 * σ t) = b * t → a * σ t = b * t
    have ha_t : a ∣ t := factor_from_eq a b t hcop h
    have h2_t : 2 ∣ t := by
      have h2a : 2 ∣ a := Nat.dvd_of_mod_eq_zero ha_even
      exact Nat.dvd_trans h2a ha_t
    have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2_t
    rw [ht_odd] at h2t_mod
    omega
  · -- e ≥ 1
    have he_pos : e ≥ 1 := by omega
    -- Rearrange h: (a*(2^(e+1)-1)) * σ t = (b*2^e) * t
    have h_eq : (a * (2 ^ (e + 1) - 1)) * σ t = (b * 2 ^ e) * t := by
      calc
        (a * (2 ^ (e + 1) - 1)) * σ t = a * ((2 ^ (e + 1) - 1) * σ t) := by ring
        _ = b * (2 ^ e * t) := h
        _ = (b * 2 ^ e) * t := by ring
    have h_coeff : a * (2 ^ (e + 1) - 1) > b * 2 ^ e := by
      have h_pow_succ : 2 ^ (e + 1) = 2 * 2 ^ e := by ring
      rw [h_pow_succ]
      have h_sub : a * (2 * 2 ^ e - 1) = 2 * a * 2 ^ e - a := by
        have h_2pow_ge_1 : 2 * 2 ^ e ≥ 1 := by
          have hpos : 2 ^ e ≥ 1 := pow_pos (by norm_num) e
          omega
        omega
      rw [h_sub]
      have h_diff_pos : 2 * a - b ≥ 1 := by omega
      have h_ineq2 : 2 * a * 2 ^ e - a > b * 2 ^ e := by
        -- 2*a*2^e - a > b*2^e ⇔ (2*a - b)*2^e > a
        -- Since 2*a - b ≥ 1 and 2^e ≥ 2 (for e ≥ 1):
        -- (2*a - b)*2^e ≥ 1*2 = 2
        -- But we need > a. This requires 3*a > 2*b (equivalently b < 3*a/2).
        -- We'll use omega which can handle the arithmetic.
        have hpos_2e : 2 ^ e ≥ 2 := by
          calc
            2 ^ e ≥ 2 ^ 1 := Nat.pow_le_pow_right (by norm_num) he_pos
            _ = 2 := by norm_num
        have hineq' : (2 * a - b) * 2 ^ e > a := by
          -- We need 3*a > 2*b for this to work with e=1.
          -- But this is not a hypothesis. We'll use a different approach.
          -- Actually, let's use: (2*a - b)*2^e ≥ (2*a - b)*2 and we need (2*a-b)*2 > a.
          -- This is equivalent to 3*a > 2*b.
          -- For our specific cases this holds. Let me make it a hypothesis.
          sorry
        omega
      omega
    have h_sigma_t_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
    have h_contra : (a * (2 ^ (e + 1) - 1)) * σ t > (b * 2 ^ e) * t := by
      calc
        (a * (2 ^ (e + 1) - 1)) * σ t ≥ (a * (2 ^ (e + 1) - 1)) * t :=
          Nat.mul_le_mul_left (a * (2 ^ (e + 1) - 1)) h_sigma_t_ge_t
        _ > (b * 2 ^ e) * t := Nat.mul_lt_mul_of_pos_right h_coeff ht_pos
    rw [h_eq] at h_contra
    exact lt_irrefl _ h_contra'''

new_lemma = '''/-- A general descent lemma: if a * σ(x) = b * x with a even, b odd, gcd(a,b)=1,
    x > 0, 2*a > b, and 3*a > 2*b, then no positive x can satisfy the equation.
    The proof factors x = 2^e * t with t odd:
    - If e = 0 (x odd): a | x (from gcd(a,b)=1) but a even and x odd → contradiction.
    - If e ≥ 1: uses the inequality a*(2^(e+1)-1) > b*2^e.
      This reduces to (2*a - b)*2^e > a, which holds for e ≥ 1 when 3*a > 2*b. -/
lemma descent_even_coeff (a b x : ℕ) (ha_even : a % 2 = 0) (hb_odd : b % 2 = 1)
    (hcop : Nat.Coprime a b) (hx_pos : x > 0) (h : a * σ x = b * x)
    (h_ineq : 2 * a > b) (h_ineq2 : 3 * a > 2 * b) : False := by
  rcases factor_2_pow_odd x hx_pos with ⟨e, t, ht_odd, hx_eq⟩
  rw [hx_eq] at h
  have ht_pos : t > 0 := by
    by_contra! hle
    have ht0 : t = 0 := by omega
    rw [ht0, mul_zero] at hx_eq
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
  -- h: a * ((2^(e+1)-1) * σ t) = b * (2^e * t)
  by_cases he0 : e = 0
  · -- e = 0: x = t is odd
    subst he0
    simp at hx_eq h
    -- h: a * (1 * σ t) = b * t → a * σ t = b * t
    have ha_t : a ∣ t := factor_from_eq a b t hcop h
    have h2_t : 2 ∣ t := by
      have h2a : 2 ∣ a := Nat.dvd_of_mod_eq_zero ha_even
      exact Nat.dvd_trans h2a ha_t
    have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2_t
    rw [ht_odd] at h2t_mod
    omega
  · -- e ≥ 1
    have he_pos : e ≥ 1 := by omega
    -- Rearrange h: (a*(2^(e+1)-1)) * σ t = (b*2^e) * t
    have h_eq : (a * (2 ^ (e + 1) - 1)) * σ t = (b * 2 ^ e) * t := by
      calc
        (a * (2 ^ (e + 1) - 1)) * σ t = a * ((2 ^ (e + 1) - 1) * σ t) := by ring
        _ = b * (2 ^ e * t) := h
        _ = (b * 2 ^ e) * t := by ring
    have h_coeff : a * (2 ^ (e + 1) - 1) > b * 2 ^ e := by
      have h_pow_succ : 2 ^ (e + 1) = 2 * 2 ^ e := by ring
      rw [h_pow_succ]
      -- Need: a*(2*2^e - 1) > b*2^e
      -- ⇔ 2*a*2^e - a > b*2^e
      -- ⇔ (2*a - b)*2^e > a
      have hpos_2e : 2 ^ e ≥ 2 := by
        calc
          2 ^ e ≥ 2 ^ 1 := Nat.pow_le_pow_right (by norm_num) he_pos
          _ = 2 := by norm_num
      have h_diff_pos : 2 * a - b ≥ 1 := by omega
      have h_key : (2 * a - b) * 2 ^ e > a := by
        -- (2*a - b)*2^e ≥ (2*a - b)*2 > a (since 3*a > 2*b → 4*a - 2*b > a → (2*a-b)*2 > a)
        have h_mul2 : (2 * a - b) * 2 > a := by omega
        have h_le : (2 * a - b) * 2 ≤ (2 * a - b) * 2 ^ e :=
          Nat.mul_le_mul_left (2 * a - b) hpos_2e
        omega
      have h_arith : a * (2 * 2 ^ e - 1) = (2 * a - b) * 2 ^ e + (b * 2 ^ e - a) := by
        omega
      rw [h_arith]
      have hsum : (2 * a - b) * 2 ^ e + (b * 2 ^ e - a) > b * 2 ^ e := by
        -- (2*a-b)*2^e > a, so (2*a-b)*2^e + (b*2^e - a) > a + (b*2^e - a) = b*2^e
        omega
      omega
    have h_sigma_t_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
    have h_contra : (a * (2 ^ (e + 1) - 1)) * σ t > (b * 2 ^ e) * t := by
      calc
        (a * (2 ^ (e + 1) - 1)) * σ t ≥ (a * (2 ^ (e + 1) - 1)) * t :=
          Nat.mul_le_mul_left (a * (2 ^ (e + 1) - 1)) h_sigma_t_ge_t
        _ > (b * 2 ^ e) * t := Nat.mul_lt_mul_of_pos_right h_coeff ht_pos
    rw [h_eq] at h_contra
    exact lt_irrefl _ h_contra'''

if old_lemma in content:
    content = content.replace(old_lemma, new_lemma)
    print("Replaced descent_even_coeff lemma")
else:
    print("WARNING: old descent_even_coeff not found!")

with open('Imscribing/Classical/Solitary10.lean', 'w') as f:
    f.write(content)

print(f"File size: {len(content)} chars")
