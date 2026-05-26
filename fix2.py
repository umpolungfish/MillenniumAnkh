#!/usr/bin/env python3
"""Fix the remaining issues in the Euler proof."""
import sys

with open('Imscribing/Primitives/OPN_2adic.lean', 'r') as f:
    content = f.read()

# The part to replace: from "have h_exists_p" to the end of euler_opn_form
old_start = content.find('  -- Key: find the unique prime with odd exponent in the factorization')
old_end = content.find('\n-- ============================================================\n-- THE 2-ADIC VALUATION ARGUMENT')

if old_start < 0 or old_end < 0:
    print("ERROR: Could not find section markers")
    sys.exit(1)

replacement = '''  -- Key: find the unique prime with odd exponent in the factorization
  -- Lemma: product of odd numbers is odd
  have prod_odd (s : Finset ℕ) (f : ℕ → ℕ) (h : ∀ x ∈ s, f x % 2 = 1) : (∏ x ∈ s, f x) % 2 = 1 := by
    classical
    refine Finset.induction_on s ?_ ?_
    · simp
    · intro a s has ih
      rw [Finset.prod_insert has]
      have ha : f a % 2 = 1 := h a (Finset.mem_insert_self a s)
      have hs : ∀ x ∈ s, f x % 2 = 1 := fun x hx => h x (Finset.mem_insert_of_mem hx)
      rw [Nat.mul_mod, ha, ih hs]; simp

  have h_exists_p : ∃ p ∈ S, ((factorization n) p) % 2 = 1 := by
    by_contra h_all_even
    push_neg at h_all_even
    have h_all_odd_sigma : ∀ p ∈ S, sigma 1 (p ^ ((factorization n) p)) % 2 = 1 := by
      intro p hp
      have hp_prime : p.Prime := by
        have hp_mem : p ∈ n.primeFactors := by simpa using hp
        exact (Nat.mem_primeFactors.mp hp_mem).1
      have hp_odd : p ≠ 2 := h_S_odd p hp
      have h_exp_even : ((factorization n) p) % 2 = 0 := by
        have h_not_odd : ¬ ((factorization n) p) % 2 = 1 := h_all_even p hp
        omega
      rw [sigma_mod2_eq p ((factorization n) p) hp_prime hp_odd]
      have : (((factorization n) p) + 1) % 2 = 1 := by
        have h := h_exp_even; omega
      exact this
    have h_prod_odd : (∏ p ∈ S, sigma 1 (p ^ ((factorization n) p))) % 2 = 1 :=
      prod_odd S (fun p => sigma 1 (p ^ ((factorization n) p))) h_all_odd_sigma
    rw [h_prod_odd] at h_sigma_mod4
    omega

  rcases h_exists_p with ⟨p, hpS, hp_odd⟩
  let k := (factorization n) p
  have hk_odd : k % 2 = 1 := hp_odd

  -- Show that NO other prime has odd exponent
  have h_no_other_odd : ∀ q ∈ S, q ≠ p → ((factorization n) q) % 2 = 0 := by
    intro q hqS hne
    by_contra hq_odd
    have hq_odd' : ((factorization n) q) % 2 = 1 := by omega
    -- Both p and q have odd exponents → both σ(p^k) and σ(q^e) are even
    -- Their product has at least 2 factors of 2 → divisible by 4
    have hp_prime : p.Prime := by
      have hp_mem : p ∈ n.primeFactors := by simpa using hpS
      exact (Nat.mem_primeFactors.mp hp_mem).1
    have hq_prime : q.Prime := by
      have hq_mem : q ∈ n.primeFactors := by simpa using hqS
      exact (Nat.mem_primeFactors.mp hq_mem).1
    have hp_odd_prime : p ≠ 2 := h_S_odd p hpS
    have hq_odd_prime : q ≠ 2 := h_S_odd q hqS
    have h_sigma_p_even : sigma 1 (p ^ k) % 2 = 0 := by
      rw [sigma_mod2_eq p k hp_prime hp_odd_prime, hk_odd]; simp
    have h_sigma_q_even : sigma 1 (q ^ ((factorization n) q)) % 2 = 0 := by
      rw [sigma_mod2_eq q ((factorization n) q) hq_prime hq_odd_prime, hq_odd']; simp
    have h_2_dvd_p : 2 ∣ sigma 1 (p ^ k) := by
      rw [Nat.dvd_iff_mod_eq_zero]; exact h_sigma_p_even
    have h_2_dvd_q : 2 ∣ sigma 1 (q ^ ((factorization n) q)) := by
      rw [Nat.dvd_iff_mod_eq_zero]; exact h_sigma_q_even
    -- The full product is divisible by 4
    have h_4_dvd_prod : 4 ∣ ∏ r ∈ S, sigma 1 (r ^ ((factorization n) r)) := by
      have h_p_in_S : p ∈ S := hpS
      have h_q_in_S : q ∈ S := hqS
      have h_dvd_prod : 2 ∣ ∏ r ∈ S, sigma 1 (r ^ ((factorization n) r)) :=
        Finset.dvd_prod_of_mem (fun r => sigma 1 (r ^ ((factorization n) r))) h_p_in_S
      have h_even_prod : 2 ∣ (∏ r ∈ S, sigma 1 (r ^ ((factorization n) r))) / 2 := by
        have h_dvd_q : 2 ∣ sigma 1 (q ^ ((factorization n) q)) := h_2_dvd_q
        have h_q_mul : sigma 1 (q ^ ((factorization n) q)) ∣ ∏ r ∈ S, sigma 1 (r ^ ((factorization n) r)) :=
          Finset.dvd_prod_of_mem (fun r => sigma 1 (r ^ ((factorization n) r))) h_q_in_S
        have : sigma 1 (p ^ k) * (sigma 1 (q ^ ((factorization n) q))) ∣ ∏ r ∈ S, sigma 1 (r ^ ((factorization n) r)) := by
          apply mul_dvd_mul (Finset.dvd_prod_of_mem (fun r => sigma 1 (r ^ ((factorization n) r))) h_p_in_S)
          exact Finset.dvd_prod_of_mem (fun r => sigma 1 (r ^ ((factorization n) r))) h_q_in_S
        have h4 : 4 ∣ sigma 1 (p ^ k) * sigma 1 (q ^ ((factorization n) q)) :=
          mul_dvd_mul h_2_dvd_p h_2_dvd_q
        exact (h4.trans this)
      sorry
    -- But product ≡ 2 (mod 4), contradiction
    have h_prod_mod4 : (∏ r ∈ S, sigma 1 (r ^ ((factorization n) r))) % 4 = 2 := h_sigma_mod4
    have h_4_dvd_prod' : 4 ∣ ∏ r ∈ S, sigma 1 (r ^ ((factorization n) r)) := h_4_dvd_prod
    rw [Nat.dvd_iff_mod_eq_zero] at h_4_dvd_prod'
    rw [h_4_dvd_prod'] at h_prod_mod4
    omega

  -- Build m² from the product of all prime powers with even exponents
  let m_sq := ∏ q ∈ S.erase p, q ^ ((factorization n) q)
  have hm_sq_square : ∃ m, m_sq = m ^ 2 := by
    refine ⟨∏ q ∈ S.erase p, q ^ (((factorization n) q) / 2), ?_⟩
    calc
      (∏ q ∈ S.erase p, q ^ (((factorization n) q) / 2)) ^ 2
          = (∏ q ∈ S.erase p, (q ^ (((factorization n) q) / 2)) ^ 2) := by
        simp [Finset.prod_pow]
      _ = (∏ q ∈ S.erase p, q ^ ((((factorization n) q) / 2) * 2)) := by
        simp [pow_mul]
      _ = (∏ q ∈ S.erase p, q ^ ((factorization n) q)) := by
        refine Finset.prod_congr rfl fun q hq => ?_
        have hq_even : ((factorization n) q) % 2 = 0 :=
          h_no_other_odd q (by
            apply Finset.mem_of_mem_erase hq) (Finset.ne_of_mem_erase hq)
        have h_eq : (((factorization n) q) / 2) * 2 = (factorization n) q := by
          have h_dvd : 2 ∣ (factorization n) q := Nat.dvd_of_mod_eq_zero hq_even
          omega
        simp [h_eq]
      _ = m_sq := rfl
  rcases hm_sq_square with ⟨m, hm_sq⟩

  have h_n_eq : n = p ^ k * m ^ 2 := by
    calc
      n = (∏ r ∈ S, r ^ ((factorization n) r)) := by symm; exact h_n_prod
      _ = (p ^ k) * (∏ q ∈ S.erase p, q ^ ((factorization n) q)) := by
        rw [Finset.prod_erase_mul (fun r => r ^ ((factorization n) r)) hpS]
        simp [k]
      _ = p ^ k * m_sq := rfl
      _ = p ^ k * (m ^ 2) := by rw [hm_sq]
      _ = p ^ k * m ^ 2 := by ring

  have h_p_mod4 : p % 4 = 1 := by
    sorry

  have h_k_mod4 : k % 4 = 1 := by
    sorry

  have h_p_not_dvd_m : ¬ p ∣ m := by
    sorry

  exact ⟨p, k, m, ?_, h_n_eq, h_p_mod4, h_k_mod4, h_p_not_dvd_m⟩
'''

new_full = content[:old_start] + replacement + content[old_end:]
with open('Imscribing/Primitives/OPN_2adic.lean', 'w') as f:
    f.write(new_full)
print(f"Replaced. File: {len(new_full)} chars")
