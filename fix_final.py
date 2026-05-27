#!/usr/bin/env python3
"""Fix Solitary10.lean: remove broken general lemma, add standalone descent_332_465."""

with open('Imscribing/Classical/Solitary10.lean', 'r') as f:
    content = f.read()

# The descent_332_465 lemma (standalone, no dependency on descent_even_coeff)
descent_332_465 = """
/-- 332 * σ(x) = 465 * x has no positive solution.
    Proof: factor x = 2^e * t (t odd).
    e=0: 332|x but 332 even, x odd → contradiction.
    e≥1: inequality 332*(2^(e+1)-1) > 465*2^e from 199*2^e > 332. -/
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
  have h_cop332_465 : Nat.Coprime 332 465 := by native_decide
  by_cases he0 : e = 0
  · subst he0; simp at hx_eq h
    have h332_t : 332 ∣ t := factor_from_eq 332 465 t h_cop332_465 h
    have h2_t : 2 ∣ t := Nat.dvd_trans (by norm_num : 2 ∣ 332) h332_t
    have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2_t
    rw [ht_odd] at h2t_mod
    omega
  · have he_pos : e ≥ 1 := by omega
    have h_eq : (332 * (2 ^ (e + 1) - 1)) * σ t = (465 * 2 ^ e) * t := by
      calc
        (332 * (2 ^ (e + 1) - 1)) * σ t = 332 * ((2 ^ (e + 1) - 1) * σ t) := by ring
        _ = 465 * (2 ^ e * t) := h
        _ = (465 * 2 ^ e) * t := by ring
    have h_coeff : 332 * (2 ^ (e + 1) - 1) > 465 * 2 ^ e := by
      have h2e_ge_2 : 2 ^ e ≥ 2 := by
        calc
          2 ^ e ≥ 2 ^ 1 := Nat.pow_le_pow_right (by norm_num) he_pos
          _ = 2 := by norm_num
      have h199_gt_332 : 199 * 2 ^ e > 332 := by
        have h_mul : 199 * 2 ^ e ≥ 199 * 2 := Nat.mul_le_mul_left 199 h2e_ge_2
        have h199_2 : 199 * 2 = 398 := by norm_num
        omega
      have h_pow_succ : 2 ^ (e + 1) = 2 * 2 ^ e := by ring
      have h_total : 332 * 2 ^ (e + 1) > 465 * 2 ^ e + 332 := by
        rw [h_pow_succ]
        calc
          332 * (2 * 2 ^ e) = 664 * 2 ^ e := by ring
          _ = 465 * 2 ^ e + 199 * 2 ^ e := by ring
          _ > 465 * 2 ^ e + 332 := Nat.add_lt_add_left h199_gt_332 (465 * 2 ^ e)
      have h_id : 332 * 2 ^ (e + 1) = 332 * (2 ^ (e + 1) - 1) + 332 := by
        have h_sub : 2 ^ (e + 1) = (2 ^ (e + 1) - 1) + 1 := by
          have hpos : 2 ^ (e + 1) ≥ 1 := pow_pos (by norm_num) (e + 1)
          omega
        rw [h_sub]
        ring
      rw [h_id] at h_total
      omega
    have h_sigma_t_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
    have h_contra : (332 * (2 ^ (e + 1) - 1)) * σ t > (465 * 2 ^ e) * t := by
      calc
        (332 * (2 ^ (e + 1) - 1)) * σ t ≥ (332 * (2 ^ (e + 1) - 1)) * t :=
          Nat.mul_le_mul_left (332 * (2 ^ (e + 1) - 1)) h_sigma_t_ge_t
        _ > (465 * 2 ^ e) * t := Nat.mul_lt_mul_of_pos_right h_coeff ht_pos
    rw [h_eq] at h_contra
    exact lt_irrefl _ h_contra

"""

# Find the old descent_even_coeff and everything up to the theorem
import re
m_even = re.search(r'/-- A general descent lemma.*?lemma descent_even_coeff', content, re.DOTALL)
m_theorem = re.search(r'theorem ten_is_solitary', content)

if m_even and m_theorem:
    start = m_even.start()
    end = m_theorem.start()
    print(f"Replacing positions {start} to {end}")
    
    # Keep everything up to the general lemma, add standalone lemma, then theorem
    new_content = content[:start] + descent_332_465 + "\n" + content[end:]
    
    with open('Imscribing/Classical/Solitary10.lean', 'w') as f:
        f.write(new_content)
    print(f"Written {len(new_content)} chars")
else:
    print(f"Could not find boundaries: even={m_even is not None}, theorem={m_theorem is not None}")
