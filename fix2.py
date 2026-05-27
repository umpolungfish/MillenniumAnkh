#!/usr/bin/env python3
"""Replace the general descent_even_coeff with standalone specific lemmas."""

with open('Imscribing/Classical/Solitary10.lean', 'r') as f:
    lines = f.readlines()

# Find the descent_even_coeff lemma boundaries
start = None
end = None
for i, line in enumerate(lines):
    if 'lemma descent_even_coeff' in line:
        start = i
    elif start is not None and i > start:
        stripped = line.strip()
        if stripped.startswith('/--') or stripped.startswith('lemma ') or stripped.startswith('theorem '):
            end = i
            break

print(f"descent_even_coeff: lines {start+1} to {end}")

# Find where descent_332_465 is (should be right after)
start_332 = None
for i in range(end, len(lines)):
    if 'lemma descent_332_465' in lines[i]:
        start_332 = i
        break

# Find where descent_41872_51305 is
start_41872 = None
for i in range(start_332, len(lines)):
    if 'lemma descent_41872_51305' in lines[i]:
        start_41872 = i
        break

# Find where the main theorem starts
start_theorem = None
for i in range(start_41872, len(lines)):
    if 'theorem ten_is_solitary' in lines[i]:
        start_theorem = i
        break

print(f"descent_332_465 at line {start_332+1}")
print(f"descent_41872_51305 at line {start_41872+1}")
print(f"theorem at line {start_theorem+1}")

# Build new lemmas
new_lemmas = '''
/-- Case-specific descent: 332 * σ(x) = 465 * x has no positive solution.
    Follows the same 2-power factorization pattern as descent_32_45. -/
lemma descent_332_465 (x : ℕ) (hx_pos : x > 0) (h : 332 * σ x = 465 * x) : False := by
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
  -- h: 332 * ((2^(e+1)-1) * σ t) = 465 * (2^e * t)
  have h_cop332_465 : Nat.Coprime 332 465 := by native_decide
  by_cases he0 : e = 0
  · -- e = 0: x = t is odd
    subst he0
    simp at hx_eq h
    -- h: 332 * (1 * σ t) = 465 * t → 332 * σ t = 465 * t
    have h332_t : 332 ∣ t := factor_from_eq 332 465 t h_cop332_465 h
    have h2_t : 2 ∣ t := Nat.dvd_trans (by norm_num : 2 ∣ 332) h332_t
    have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2_t
    rw [ht_odd] at h2t_mod
    omega
  · -- e ≥ 1
    have he_pos : e ≥ 1 := by omega
    -- Rearrange h: (332*(2^(e+1)-1)) * σ t = (465*2^e) * t
    have h_eq : (332 * (2 ^ (e + 1) - 1)) * σ t = (465 * 2 ^ e) * t := by
      calc
        (332 * (2 ^ (e + 1) - 1)) * σ t = 332 * ((2 ^ (e + 1) - 1) * σ t) := by ring
        _ = 465 * (2 ^ e * t) := h
        _ = (465 * 2 ^ e) * t := by ring
    have h_coeff : 332 * (2 ^ (e + 1) - 1) > 465 * 2 ^ e := by
      have h_pow_succ : 2 ^ (e + 1) = 2 * 2 ^ e := by ring
      rw [h_pow_succ]
      -- 332*(2*X-1) > 465*X where X = 2^e, X ≥ 2
      -- ⇔ 664*X - 332 > 465*X ⇔ 199*X > 332 ⇔ X > 332/199 ≈ 1.67
      -- Since X ≥ 2 (e ≥ 1), this holds.
      have hX_ge_2 : 2 ^ e ≥ 2 := by
        calc
          2 ^ e ≥ 2 ^ 1 := Nat.pow_le_pow_right (by norm_num) he_pos
          _ = 2 := by norm_num
      -- Compute: 2*(332*(2*X-1)) vs 2*(465*X) to avoid subtraction issues
      -- Actually let's use a direct inequality
      have h_ineq : 332 * (2 * 2 ^ e - 1) > 465 * 2 ^ e := by
        -- Use the inequality: 199 * 2^e > 332 (since 2^e ≥ 2, 199*2 ≥ 398 > 332)
        have h199 : 199 * 2 ^ e > 332 := by
          have h199_2 : 199 * 2 = 398 := by norm_num
          have h199X_ge_199_2 : 199 * 2 ^ e ≥ 199 * 2 :=
            Nat.mul_le_mul_left 199 hX_ge_2
          omega
        -- 332*(2X-1) = 664*X - 332 = 465*X + 199*X - 332 > 465*X + 332 - 332 = 465*X
        -- But we need to be careful with Nat subtraction.
        -- Use: 332*(2X) > 465*X + 332 (since 199*X > 332)
        -- Then: 332*(2X-1) = 332*(2X) - 332 > 465*X + 332 - 332 = 465*X
        have h_mul2X : 332 * (2 * 2 ^ e) = 664 * 2 ^ e := by ring
        have h_664_gt_465 : 664 * 2 ^ e > 465 * 2 ^ e + 332 := by
          have : 664 * 2 ^ e = 465 * 2 ^ e + 199 * 2 ^ e := by ring
          rw [this]
          have h199_gt_332 : 199 * 2 ^ e > 332 := h199
          omega
        -- Now: 332*(2X-1) = 332*2X - 332 = (465*X + 199*X) - 332 > 465*X
        -- Let's use a simpler direct calculation:
        have h_calc : 332 * (2 * 2 ^ e) > 465 * 2 ^ e + 332 := by
          -- 332*2*2^e = 664*2^e = 465*2^e + 199*2^e > 465*2^e + 332
          rw [show 332 * (2 * 2 ^ e) = 465 * 2 ^ e + 199 * 2 ^ e by ring]
          have h199_gt_332 : 199 * 2 ^ e > 332 := by
            have h199_2 : 199 * 2 = 398 := by norm_num
            have h199_2e_ge_398 : 199 * 2 ^ e ≥ 398 :=
              calc
                199 * 2 ^ e ≥ 199 * 2 := Nat.mul_le_mul_left 199 hX_ge_2
                _ = 398 := by norm_num
            omega
          omega
        -- Now 332*(2X-1) = 332*2X - 332. In Nat, we can use:
        -- If A > B + 332, then A - 332 > B (when 332 ≤ A).
        -- But this is getting messy with Nat subtraction.
        -- Alternative: compare squares or use integer arithmetic.
        sorry
      exact h_ineq
    have h_sigma_t_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
    have h_contra : (332 * (2 ^ (e + 1) - 1)) * σ t > (465 * 2 ^ e) * t := by
      calc
        (332 * (2 ^ (e + 1) - 1)) * σ t ≥ (332 * (2 ^ (e + 1) - 1)) * t :=
          Nat.mul_le_mul_left (332 * (2 ^ (e + 1) - 1)) h_sigma_t_ge_t
        _ > (465 * 2 ^ e) * t := Nat.mul_lt_mul_of_pos_right h_coeff ht_pos
    rw [h_eq] at h_contra
    exact lt_irrefl _ h_contra
'''

print("Need to fix the inequality proof...")
print(f"Will replace lines {start} to {start_theorem-1}")
