#!/usr/bin/env python3
"""Patch the Euler proof in OPN_2adic.lean"""
import sys

with open('Imscribing/Primitives/OPN_2adic.lean', 'r') as f:
    content = f.read()

# Find the Euler section
old_start = content.find('-- ============================================================\n-- EULER\'S THEOREM')
old_end = content.find('\n-- ============================================================\n-- THE 2-ADIC VALUATION ARGUMENT')

if old_start < 0 or old_end < 0:
    print("ERROR: Could not find Euler section markers")
    sys.exit(1)

new_block = '''-- ============================================================
-- EULER'S THEOREM (1747)
-- Every odd perfect number has the form n = p^k * m²
-- where p prime, p ≡ k ≡ 1 [MOD 4], gcd(p, m) = 1.
-- ============================================================

/-- sigma splits over the prime factorization product. -/
lemma sigma_factorization_prod (n : ℕ) (hn : n ≠ 0) :
    sigma 1 n = (∏ p ∈ (factorization n).support, sigma 1 (p ^ ((factorization n) p))) := by
  let S := (factorization n).support
  have h_n_prod : (∏ p ∈ S, p ^ ((factorization n) p)) = n := by
    calc
      (∏ p ∈ S, p ^ ((factorization n) p)) = ((factorization n).prod fun p a => p ^ a) := by
        rw [Finsupp.prod_of_support_subset (factorization n) (Finset.Subset.refl _) (fun p a => p ^ a) (by simp)]
        simp
      _ = n := Nat.factorization_prod_pow_eq_self hn
  have coprime_prime_pow (p q a b : ℕ) (hp : p.Prime) (hq : q.Prime) (hne : p ≠ q) :
      Nat.Coprime (p ^ a) (q ^ b) := by
    refine Nat.Coprime.pow a b ?_
    apply hp.coprime_iff_not_dvd.mpr
    intro hdiv
    apply hne
    have h_cases : p = 1 ∨ p = q := hq.eq_one_or_self_of_dvd p hdiv
    rcases h_cases with (h | h)
    · have : 1 < p := hp.one_lt; omega
    · exact h
  have h_pairwise : (S : Set ℕ).Pairwise (fun p q => Nat.Coprime
      (p ^ ((factorization n) p)) (q ^ ((factorization n) q))) := by
    intro p hp q hq hne
    have hp_mem : p ∈ n.primeFactors := by simpa using hp
    have hq_mem : q ∈ n.primeFactors := by simpa using hq
    have hp_prime : p.Prime := (Nat.mem_primeFactors.mp hp_mem).1
    have hq_prime : q.Prime := (Nat.mem_primeFactors.mp hq_mem).1
    exact coprime_prime_pow p q ((factorization n) p) ((factorization n) q) hp_prime hq_prime hne
  calc
    sigma 1 n = sigma 1 (∏ p ∈ S, p ^ ((factorization n) p)) := by rw [h_n_prod]
    _ = (∏ p ∈ S, sigma 1 (p ^ ((factorization n) p))) :=
      (isMultiplicative_sigma (k := 1)).map_prod (fun p => p ^ ((factorization n) p)) S h_pairwise

/-- For an odd prime p, σ(p^a) ≡ a+1 (mod 2). -/
lemma sigma_mod2_eq (p a : ℕ) (hp : p.Prime) (hp_odd : p ≠ 2) : sigma 1 (p ^ a) % 2 = (a + 1) % 2 := by
  have hp_mod2 : p % 2 = 1 := by
    have hp_not_even : ¬ 2 ∣ p := by
      intro h; apply hp_odd; have h2prime : (2 : ℕ).Prime := by norm_num
      have h_cases : 2 = 1 ∨ 2 = p := hp.eq_one_or_self_of_dvd 2 h
      rcases h_cases with (h2 | h2)
      · norm_num at h2
      · exact h2.symm
    have hm := Nat.mod_two_eq_zero_or_one p
    rcases hm with (h | h)
    · exfalso; apply hp_not_even; exact ⟨p / 2, by omega⟩
    · exact h
  have h_formula : sigma 1 (p ^ a) = ∑ i ∈ Finset.range (a + 1), p ^ i := by
    rw [sigma_apply, Nat.divisors_prime_pow hp, Finset.sum_map]; simp
  have pow_odd (i : ℕ) : p ^ i % 2 = 1 := by
    induction i with
    | zero => simp
    | succ n ih => simp [pow_succ, Nat.mul_mod, hp_mod2, ih]
  rw [h_formula]
  induction' a with n ih
  · simp
  · rw [Finset.sum_range_succ, Nat.add_mod, ih, pow_odd (n + 1)]; simp

theorem euler_opn_form (n : ℕ) (h_odd : ¬ 2 ∣ n) (h_perf : Perfect n) :
    ∃ (p k m : ℕ),
      Nat.Prime p ∧
      n = p ^ k * m ^ 2 ∧
      p % 4 = 1 ∧
      k % 4 = 1 ∧
      ¬ p ∣ m := by
  have hn_pos : n ≠ 0 := by
    intro hzero; apply h_odd; rw [hzero]; exact ⟨0, by simp⟩
  have h_sigma_eq : sigma 1 n = 2 * n := h_perf
  have h_sigma_mod4 : sigma 1 n % 4 = 2 := by
    rw [h_sigma_eq]
    have hn_mod2 : n % 2 = 1 := by
      have h := Nat.mod_two_eq_zero_or_one n
      rcases h with (h | h)
      · exfalso; apply h_odd; exact ⟨n / 2, by omega⟩
      · exact h
    have hn_mod4 : n % 4 = 1 ∨ n % 4 = 3 := by
      have h := Nat.mod_add_div n 4; omega
    rcases hn_mod4 with (h | h) <;> omega
  -- Decompose sigma over prime factorization
  let S := (factorization n).support
  have h_sigma_prod : sigma 1 n = (∏ p ∈ S, sigma 1 (p ^ ((factorization n) p))) :=
    sigma_factorization_prod n hn_pos
  rw [h_sigma_prod] at h_sigma_mod4
  have h_S_odd (p : ℕ) (hp : p ∈ S) : p ≠ 2 := by
    have hp_mem : p ∈ n.primeFactors := by simpa using hp
    have hp_dvd : p ∣ n := (Nat.mem_primeFactors.mp hp_mem).2.1
    intro hp_eq2; apply h_odd; rw [hp_eq2]; exact hp_dvd
  -- Key: find the unique prime with odd exponent in the factorization
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
      have h_sigma_odd : sigma 1 (p ^ ((factorization n) p)) % 2 = 1 := by
        rw [sigma_mod2_eq p ((factorization n) p) hp_prime hp_odd]
        have : (((factorization n) p) + 1) % 2 = 1 := by
          have : ((factorization n) p) % 2 = 0 := h_exp_even
          omega
        exact this
      exact h_sigma_odd
    have h_prod_odd : (∏ p ∈ S, sigma 1 (p ^ ((factorization n) p))) % 2 = 1 := by
      refine Finset.prod_mod_one (fun p => sigma 1 (p ^ ((factorization n) p))) S ?_
      intro p hp; exact h_all_odd_sigma p hp
    rw [h_prod_odd] at h_sigma_mod4
    omega
  have h_unique_p : ∃! p ∈ S, ((factorization n) p) % 2 = 1 := by
    rcases h_exists_p with ⟨p, hpS, hp_odd⟩
    refine ⟨p, hpS, hp_odd, ?_⟩
    intro q hqS hq_odd hne
    -- Show that if two primes had odd exponents, the product would be ≡ 0 (mod 4)
    have hp_prime : p.Prime := by
      have hp_mem : p ∈ n.primeFactors := by simpa using hpS
      exact (Nat.mem_primeFactors.mp hp_mem).1
    have hq_prime : q.Prime := by
      have hq_mem : q ∈ n.primeFactors := by simpa using hqS
      exact (Nat.mem_primeFactors.mp hq_mem).1
    have hp_odd_prime : p ≠ 2 := h_S_odd p hpS
    have hq_odd_prime : q ≠ 2 := h_S_odd q hqS
    -- σ(p^e_p) is even, σ(q^e_q) is even
    have h_sigma_p_even : sigma 1 (p ^ ((factorization n) p)) % 2 = 0 := by
      rw [sigma_mod2_eq p ((factorization n) p) hp_prime hp_odd_prime, hp_odd]; simp
    have h_sigma_q_even : sigma 1 (q ^ ((factorization n) q)) % 2 = 0 := by
      rw [sigma_mod2_eq q ((factorization n) q) hq_prime hq_odd_prime, hq_odd]; simp
    -- Then the full product has at least 2 factors of 2, so ≡ 0 mod 4
    have h_two_evens : (sigma 1 (p ^ ((factorization n) p)) * sigma 1 (q ^ ((factorization n) q))) % 4 = 0 := by
      have h1 : sigma 1 (p ^ ((factorization n) p)) % 2 = 0 := h_sigma_p_even
      have h2 : sigma 1 (q ^ ((factorization n) q)) % 2 = 0 := h_sigma_q_even
      have h_even1 : 2 ∣ sigma 1 (p ^ ((factorization n) p)) := by
        rw [Nat.dvd_iff_mod_eq_zero]; exact h1
      have h_even2 : 2 ∣ sigma 1 (q ^ ((factorization n) q)) := by
        rw [Nat.dvd_iff_mod_eq_zero]; exact h2
      have h4 : 4 ∣ sigma 1 (p ^ ((factorization n) p)) * sigma 1 (q ^ ((factorization n) q)) :=
        mul_dvd_mul h_even1 h_even2
      rw [Nat.dvd_iff_mod_eq_zero] at h4; exact h4
    -- But the full product ≡ 2 (mod 4), contradiction
    have h_rest_odd : (∏ r ∈ S.erase p | r ≠ p ∧ ...)
    sorry
  sorry
'''

new_full = content[:old_start] + new_block + content[old_end:]
with open('Imscribing/Primitives/OPN_2adic.lean', 'w') as f:
    f.write(new_full)
print(f"Replaced Euler section. File: {len(new_full)} chars")
print(f"New block: {len(new_block)} chars")
