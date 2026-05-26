#!/usr/bin/env python3
"""Fix remaining issues in the Euler proof."""
import sys

with open('Imscribing/Primitives/OPN_2adic.lean', 'r') as f:
    content = f.read()

# Fix 1: Replace the h_n_eq block
old_h_n_eq = """  have h_n_eq : n = p ^ k * m ^ 2 := by
    calc
      n = (∏ r ∈ S, r ^ ((factorization n) r)) := by symm; exact h_n_prod
      _ = (p ^ k) * (∏ q ∈ S.erase p, q ^ ((factorization n) q)) := by
        rw [Finset.prod_erase_mul (fun r => r ^ ((factorization n) r)) hpS]
        simp [k]
      _ = p ^ k * m_sq := rfl
      _ = p ^ k * (m ^ 2) := by rw [hm_sq]
      _ = p ^ k * m ^ 2 := by ring"""

new_h_n_eq = """  have hp_prime : p.Prime := by
    have hp_mem : p ∈ n.primeFactors := by simpa using hpS
    exact (Nat.mem_primeFactors.mp hp_mem).1

  have h_n_eq : n = p ^ k * m ^ 2 := by
    calc
      n = (∏ r ∈ S, r ^ ((factorization n) r)) := by symm; exact h_n_prod
      _ = (p ^ k) * (∏ q ∈ S.erase p, q ^ ((factorization n) q)) := by
        have h_not_mem : p ∉ S.erase p := Finset.not_mem_erase p S
        rw [Finset.prod_insert h_not_mem]
        simp [k]
      _ = p ^ k * m_sq := rfl
      _ = p ^ k * (m ^ 2) := by rw [hm_sq]
      _ = p ^ k * m ^ 2 := by ring"""

assert old_h_n_eq in content, "Could not find old h_n_eq block!"
content = content.replace(old_h_n_eq, new_h_n_eq)

# Fix 2: Fill in h_p_mod4, h_k_mod4, h_p_not_dvd_m
old_mods = """  have h_p_mod4 : p % 4 = 1 := by
    sorry

  have h_k_mod4 : k % 4 = 1 := by
    sorry

  have h_p_not_dvd_m : ¬ p ∣ m := by
    sorry

  exact ⟨p, k, m, ?_, h_n_eq, h_p_mod4, h_k_mod4, h_p_not_dvd_m⟩"""

new_mods = """  have h_p_mod4 : p % 4 = 1 := by
    -- Since v₂(σ(p^k)) = 1 (only one factor of 2),
    -- and p is an odd prime, we must have p ≡ 1 (mod 4)
    -- σ(p^k) ≡ 2 (mod 4) because Σ v₂ = 1 and all other σ are odd
    have h_sigma_pk_mod4 : sigma 1 (p ^ k) % 4 = 2 := by
      -- From the full product ≡ 2 (mod 4), all other factors are odd (≡ ±1 mod 4)
      -- So σ(p^k) ≡ 2 (mod 4)
      have h_others_odd : ∀ r ∈ S, r ≠ p → (sigma 1 (r ^ ((factorization n) r))) % 2 = 1 := by
        intro r hr hne
        have hr_prime : r.Prime := by
          have hr_mem : r ∈ n.primeFactors := by simpa using hr
          exact (Nat.mem_primeFactors.mp hr_mem).1
        have hr_odd : r ≠ 2 := h_S_odd r hr
        have hr_exp_even : ((factorization n) r) % 2 = 0 := h_no_other_odd r hr hne
        rw [sigma_mod2_eq r ((factorization n) r) hr_prime hr_odd]
        have : (((factorization n) r) + 1) % 2 = 1 := by omega
        exact this
      have h_prod_split : (∏ r ∈ S, sigma 1 (r ^ ((factorization n) r))) =
          sigma 1 (p ^ k) * (∏ r ∈ (S.erase p), sigma 1 (r ^ ((factorization n) r))) := by
        have h_not_mem : p ∉ S.erase p := Finset.not_mem_erase p S
        rw [Finset.prod_insert h_not_mem]
        simp
      rw [h_prod_split] at h_sigma_mod4
      have h_rest_odd : (∏ r ∈ (S.erase p), sigma 1 (r ^ ((factorization n) r))) % 2 = 1 :=
        prod_odd (S.erase p) (fun r => sigma 1 (r ^ ((factorization n) r))) h_others_odd
      have h_rest_odd' : (∏ r ∈ (S.erase p), sigma 1 (r ^ ((factorization n) r))) % 4 = 1 ∨
          (∏ r ∈ (S.erase p), sigma 1 (r ^ ((factorization n) r))) % 4 = 3 := by
        have h_mod2 : (∏ r ∈ (S.erase p), sigma 1 (r ^ ((factorization n) r))) % 2 = 1 := h_rest_odd
        have h := Nat.mod_add_div (∏ r ∈ (S.erase p), sigma 1 (r ^ ((factorization n) r))) 4
        omega
      rcases h_rest_odd' with (h | h)
      · have : (sigma 1 (p ^ k) * (∏ r ∈ (S.erase p), sigma 1 (r ^ ((factorization n) r)))) % 4 = 2 := h_sigma_mod4
        rw [Nat.mul_mod, h] at this
        have : sigma 1 (p ^ k) % 4 = 2 := by omega
        exact this
      · have : (sigma 1 (p ^ k) * (∏ r ∈ (S.erase p), sigma 1 (r ^ ((factorization n) r)))) % 4 = 2 := h_sigma_mod4
        rw [Nat.mul_mod, h] at this
        have : sigma 1 (p ^ k) % 4 = 2 := by
          have : 3 * (sigma 1 (p ^ k) % 4) % 4 = 2 := this
          have h3 : (3 : ℕ) % 4 = 3 := by norm_num
          -- 3*x ≡ 2 (mod 4) implies x ≡ 2 (mod 4) since 3*2 = 6 ≡ 2 (mod 4)
          -- 3*0=0, 3*1=3, 3*2=6≡2, 3*3=9≡1
          omega
        exact this
    have h_formula : sigma 1 (p ^ k) = ∑ i ∈ Finset.range (k + 1), p ^ i := by
      rw [sigma_apply, Nat.divisors_prime_pow hp_prime, Finset.sum_map]; simp
    rw [h_formula] at h_sigma_pk_mod4
    -- Now analyze p mod 4 and k mod 4 from sum ≡ 2 (mod 4)
    have hp_mod4_cases : p % 4 = 1 ∨ p % 4 = 3 := by
      have hp_mod2 : p % 2 = 1 := by
        have hp_not_even : ¬ 2 ∣ p := by
          intro h; apply h_S_odd p hpS
          have h2prime : (2 : ℕ).Prime := by norm_num
          have h_cases : 2 = 1 ∨ 2 = p := hp_prime.eq_one_or_self_of_dvd 2 h
          rcases h_cases with (h2 | h2)
          · norm_num at h2
          · exact h2.symm
        have hm := Nat.mod_two_eq_zero_or_one p
        rcases hm with (h | h)
        · exfalso; apply hp_not_even; exact ⟨p / 2, by omega⟩
        · exact h
      have h := Nat.mod_add_div p 4; omega
    rcases hp_mod4_cases with (hp_mod4 | hp_mod4)
    · exact hp_mod4
    · -- p ≡ 3 (mod 4): show impossible because sum would be ≡ 0 (mod 4)
      have h_sum_mod4_if_p3 : (∑ i ∈ Finset.range (k + 1), p ^ i) % 4 = 0 := by
        -- When p ≡ 3 (mod 4), p^i ≡ 1 (i even) or 3 (i odd)
        -- For k odd: pairs of (1+3) = 4 ≡ 0, and there are (k+1)/2 such pairs
        have hk_odd_mod2 : k % 2 = 1 := hk_odd
        have h_terms_even : (k+1) % 2 = 0 := by omega
        -- Sum of (k+1)/2 pairs of (1+3) ≡ 0 (mod 4)
        have h_pow_mod4 (i : ℕ) : p ^ i % 4 = if i % 2 = 0 then 1 else 3 := by
          induction i with
          | zero => simp
          | succ n ih =>
            rw [pow_succ, Nat.mul_mod, ih]
            split_ifs with h
            · simp [hp_mod4]
            · have : (n+1) % 2 = 0 := by omega
              simp [this, hp_mod4]
        -- The sum of pairs: (1+3) + (1+3) + ... = 0
        sorry
      rw [h_sum_mod4_if_p3] at h_sigma_pk_mod4
      omega

  have h_k_mod4 : k % 4 = 1 := by
    sorry

  have h_p_not_dvd_m : ¬ p ∣ m := by
    intro hpm
    have hp_dvd_msq : p ∣ m ^ 2 := by
      have : m ^ 2 = m * m := by ring
      rw [this]; exact mul_dvd_mul hpm hpm
    have hp_dvd_n : p ∣ n := by
      rw [h_n_eq]; exact mul_dvd_mul (dvd_pow_self p (by omega)) hp_dvd_msq
    have hp_dvd_msq' : p ∣ m_sq := by
      rw [hm_sq]; exact hp_dvd_msq
    -- Since m_sq = ∏_{q≠p} q^e_q, and p does not divide any other prime factor,
    -- p cannot divide m_sq. Contradiction.
    have hp_not_dvd_m_sq : ¬ p ∣ m_sq := by
      have h_factor : ∀ q ∈ S.erase p, ¬ p ∣ q := by
        intro q hq
        have hq_prime : q.Prime := by
          have hq_mem : q ∈ n.primeFactors := by
            have : q ∈ S := Finset.mem_of_mem_erase hq
            simpa using this
          exact (Nat.mem_primeFactors.mp hq_mem).1
        have hne : p ≠ q := Finset.ne_of_mem_erase hq
        have : p ∣ q := ?
        sorry
      sorry
    exact hp_not_dvd_m_sq hp_dvd_msq'

  have hp_prime : p.Prime := hp_prime
  exact ⟨p, k, m, hp_prime, h_n_eq, h_p_mod4, h_k_mod4, h_p_not_dvd_m⟩"""

content = content.replace(old_mods, new_mods)

with open('Imscribing/Primitives/OPN_2adic.lean', 'w') as f:
    f.write(content)
print(f"File written: {len(content)} chars")
