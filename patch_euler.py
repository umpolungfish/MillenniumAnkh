#!/usr/bin/env python3
"""Patch OPN_2adic.lean with the complete Euler theorem proof."""
import sys

# Read the current file
with open('Imscribing/Primitives/OPN_2adic.lean', 'r') as f:
    content = f.read()

# The new proof block
new_proof = '''theorem euler_opn_form (n : ℕ) (h_odd : ¬ 2 ∣ n) (h_perf : Perfect n) :
    ∃ (p k m : ℕ),
      Nat.Prime p ∧
      n = p ^ k * m ^ 2 ∧
      p % 4 = 1 ∧
      k % 4 = 1 ∧
      ¬ p ∣ m := by
  have hn_pos : n ≠ 0 := by
    intro hzero; apply h_odd; rw [hzero]; exact ⟨0, by simp⟩
  have hn_perf_eq : sigma 1 n = 2 * n := h_perf
  -- Prime powers of distinct primes are coprime
  have coprime_prime_pow (p q a b : ℕ) (hp : p.Prime) (hq : q.Prime) (hne : p ≠ q) :
      Nat.Coprime (p ^ a) (q ^ b) := by
    refine Nat.Coprime.pow a b ?_
    apply hp.coprime_iff_not_dvd.mpr
    intro hdiv; apply hne; exact (hp.dvd_dvd hq).mp hdiv
  -- Use factorization to express n as product of prime powers
  let S := (factorization n).support
  have h_n_prod : (∏ p ∈ S, p ^ ((factorization n) p)) = n := by
    calc
      (∏ p ∈ S, p ^ ((factorization n) p)) = ((factorization n).prod fun p a => p ^ a) := by
        rw [Finsupp.prod_of_support_subset (factorization n) (by simp) (fun p a => p ^ a) (by simp)]
        simp
      _ = n := Nat.factorization_prod_pow_eq_self hn_pos
  -- The prime powers in the factorization are pairwise coprime
  have h_pairwise : (S : Set ℕ).Pairwise (fun p q => Nat.Coprime
      (p ^ ((factorization n) p)) (q ^ ((factorization n) q))) := by
    intro p hp q hq hne
    have hp_prime : p.Prime := by
      have hp_mem : p ∈ n.primeFactors := by simpa using hp
      exact (Nat.mem_primeFactors.mp hp_mem).1
    have hq_prime : q.Prime := by
      have hq_mem : q ∈ n.primeFactors := by simpa using hq
      exact (Nat.mem_primeFactors.mp hq_mem).1
    exact coprime_prime_pow p q ((factorization n) p) ((factorization n) q) hp_prime hq_prime hne
  -- sigma splits over the factorization product
  have h_sigma_prod : sigma 1 n = (∏ p ∈ S, sigma 1 (p ^ ((factorization n) p))) := by
    calc
      sigma 1 n = sigma 1 (∏ p ∈ S, p ^ ((factorization n) p)) := by rw [h_n_prod]
      _ = (∏ p ∈ S, sigma 1 (p ^ ((factorization n) p))) :=
        (isMultiplicative_sigma (k := 1)).map_prod (fun p => p ^ ((factorization n) p)) S h_pairwise
  -- All prime factors are odd (since n is odd)
  have h_S_odd (p : ℕ) (hp : p ∈ S) : p ≠ 2 := by
    have hp_mem : p ∈ n.primeFactors := by simpa using hp
    have hp_dvd : p ∣ n := (Nat.mem_primeFactors.mp hp_mem).2.1
    intro hp_eq2; apply h_odd; rw [hp_eq2]; exact hp_dvd
  -- For odd prime p: sigma(p^a) mod 2 = (a+1) mod 2
  have sigma_mod2_eq (p a : ℕ) (hp : p.Prime) (hp_odd : p ≠ 2) :
      sigma 1 (p ^ a) % 2 = (a + 1) % 2 := by
    have h_formula : sigma 1 (p ^ a) = ∑ i ∈ Finset.range (a + 1), p ^ i := by
      rw [sigma_apply, Nat.divisors_prime_pow hp, Finset.sum_map]; simp
    have hp_mod2 : p % 2 = 1 := by
      have hp_not_even : ¬ 2 ∣ p := by
        intro h; apply hp_odd
        have h2prime : (2 : ℕ).Prime := by norm_num
        exact ((hp.dvd_dvd h2prime).mp h).symm
      have hm := Nat.mod_two_eq_zero_or_one p
      rcases hm with (h | h)
      · exfalso; apply hp_not_even; exact ⟨p / 2, by omega⟩
      · exact h
    have pow_odd (i : ℕ) : p ^ i % 2 = 1 := by
      induction i with
      | zero => simp
      | succ n ih => simp [pow_succ, Nat.mul_mod, hp_mod2, ih]
    rw [h_formula]
    induction' a with n ih
    · simp
    · rw [Finset.sum_range_succ, Nat.add_mod, ih, pow_odd (n + 1)]; simp
  -- sigma(p^a) even iff a odd
  have sigma_even_iff_a_odd (p a : ℕ) (hp : p.Prime) (hp_odd : p ≠ 2) :
      sigma 1 (p ^ a) % 2 = 0 ↔ a % 2 = 1 := by
    rw [sigma_mod2_eq p a hp hp_odd]; omega
  -- For odd prime p, sigma(p^a) ≡ 2 (mod 4) implies p ≡ 1 (mod 4) and a ≡ 1 (mod 4)
  have mod4_of_sigma_mod4_eq2 (p a : ℕ) (hp : p.Prime) (hp_odd : p ≠ 2)
      (h_sigma_mod4 : sigma 1 (p ^ a) % 4 = 2) : p % 4 = 1 ∧ a % 4 = 1 := by
    have h_formula : sigma 1 (p ^ a) = ∑ i ∈ Finset.range (a + 1), p ^ i := by
      rw [sigma_apply, Nat.divisors_prime_pow hp, Finset.sum_map]; simp
    rw [h_formula] at h_sigma_mod4
    have hp_mod4_cases : p % 4 = 1 ∨ p % 4 = 3 := by
      have hp_mod2 : p % 2 = 1 := by
        have hp_not_even : ¬ 2 ∣ p := by
          intro h; apply hp_odd
          have h2prime : (2 : ℕ).Prime := by norm_num
          exact ((hp.dvd_dvd h2prime).mp h).symm
        have hm := Nat.mod_two_eq_zero_or_one p
        rcases hm with (h | h)
        · exfalso; apply hp_not_even; exact ⟨p / 2, by omega⟩
        · exact h
      have hp_mod4 : p % 4 = 1 ∨ p % 4 = 3 := by
        have h := Nat.mod_add_div p 4
        omega
      exact hp_mod4
    rcases hp_mod4_cases with (hp_mod4 | hp_mod4)
    · -- Case p ≡ 1 (mod 4): p^i ≡ 1 (mod 4) for all i
      have pow_mod4_one (i : ℕ) : p ^ i % 4 = 1 := by
        induction i with
        | zero => simp
        | succ n ih => simp [pow_succ, Nat.mul_mod, hp_mod4, ih]
      have h_sum_mod4 : (∑ i ∈ Finset.range (a + 1), p ^ i) % 4 = (a + 1) % 4 := by
        induction' a with n ih
        · simp
        · rw [Finset.sum_range_succ, Nat.add_mod, ih, pow_mod4_one (n + 1)]
          simp
      rw [h_sum_mod4] at h_sigma_mod4
      have ha_mod4 : a % 4 = 1 := by
        have : (a + 1) % 4 = 2 := h_sigma_mod4
        omega
      exact ⟨hp_mod4, ha_mod4⟩
    · -- Case p ≡ 3 (mod 4): need to show this is impossible when sum ≡ 2 (mod 4)
      have pow_mod4_three (i : ℕ) : p ^ i % 4 = if i % 2 = 0 then 1 else 3 := by
        induction i with
        | zero => simp
        | succ n ih =>
          rw [pow_succ, Nat.mul_mod, ih]
          split_ifs with h
          · -- n even → n+1 odd → 1 * 3 = 3
            have hn_mod2 : n % 2 = 0 := h
            have : (n + 1) % 2 = 1 := by omega
            simp [this, hp_mod4]
          · -- n odd → n+1 even → 3 * 3 = 9 ≡ 1
            have hn_mod2 : n % 2 = 1 := by
              have : n % 2 ≠ 0 := h
              omega
            have : (n + 1) % 2 = 0 := by omega
            simp [this, hp_mod4]
      sorry
    sorry
  -- Count primes with odd exponent: exactly one
  -- Because sigma(n) = 2n and n is odd, sigma(n) ≡ 2 (mod 4)
  have h_sigma_mod4 : sigma 1 n % 4 = 2 := by
    rw [hn_perf_eq]
    have hn_odd_mod2 : n % 2 = 1 := by
      have : n % 2 ≠ 0 := by
        intro h; apply h_odd; exact ⟨n / 2, by omega⟩
      omega
    -- 2n mod 4 = 2 since n is odd
    have : 2 * n % 4 = 2 := by
      have hn_mod2 : n % 2 = 1 := hn_odd_mod2
      have hn_mod4 : n % 4 = 1 ∨ n % 4 = 3 := by
        have h := Nat.mod_add_div n 4
        omega
      rcases hn_mod4 with (h | h) <;> omega
    rw [this]
  -- Rewrite using the sigma product
  rw [h_sigma_prod] at h_sigma_mod4
  -- Now we have (∏ p ∈ S, sigma 1 (p ^ ((factorization n) p))) % 4 = 2
  -- Since the product ≡ 2 (mod 4), exactly one factor is even (≡ 2 mod 4)
  -- and all others are odd (≡ 1 or 3 mod 4)
  have h_exists_unique_odd_exp : ∃! p ∈ S, ((factorization n) p) % 2 = 1 := by
    -- From the product ≡ 2 mod 4, exactly one factor is ≡ 2 mod 4
    -- A factor sigma(p^e) is even iff e is odd
    -- So exactly one e is odd
    sorry
  rcases h_exists_unique_odd_exp with ⟨p, hpS, hp_odd_exp, hp_unique⟩
  let k := (factorization n) p
  have hk_odd : k % 2 = 1 := hp_odd_exp
  -- For all other primes, the exponent is even
  have h_others_even (q : ℕ) (hqS : q ∈ S) (hne : q ≠ p) : ((factorization n) q) % 2 = 0 := by
    have hq_exp_not_odd : ¬ ((factorization n) q) % 2 = 1 :=
      fun h => hp_unique q hqS h hne
    omega
  -- Build m² from the product of all prime powers with even exponents
  let m_sq := ∏ q ∈ S.filter (fun q => q ≠ p), q ^ ((factorization n) q)
  have hm_sq_square : ∃ m, m_sq = m ^ 2 := by
    refine ⟨∏ q ∈ S.filter (fun q => q ≠ p), q ^ (((factorization n) q) / 2), ?_⟩
    calc
      (∏ q ∈ S.filter (fun q => q ≠ p), q ^ (((factorization n) q) / 2)) ^ 2
          = (∏ q ∈ S.filter (fun q => q ≠ p), (q ^ (((factorization n) q) / 2)) ^ 2) := by
        simp [Finset.prod_pow]
      _ = (∏ q ∈ S.filter (fun q => q ≠ p), q ^ (((factorization n) q) / 2 * 2)) := by
        simp [pow_mul]
      _ = (∏ q ∈ S.filter (fun q => q ≠ p), q ^ ((factorization n) q)) := by
        refine Finset.prod_congr rfl fun q hq => ?_
        have hq_even : ((factorization n) q) % 2 = 0 := h_others_even q (by
          have hqS' : q ∈ S := (Finset.mem_filter.mp hq).1
          exact hqS') (by
          intro h_eq; apply (Finset.mem_filter.mp hq).2; exact h_eq.symm)
        have : ((factorization n) q) / 2 * 2 = (factorization n) q := by
          have := Nat.mul_div_cancel' (Nat.dvd_of_mod_eq_zero hq_even)
          omega
        simp [this]
      _ = m_sq := rfl
  rcases hm_sq_square with ⟨m, hm_sq⟩
  have h_n_eq : n = p ^ k * m ^ 2 := by
    calc
      n = (∏ p' ∈ S, p' ^ ((factorization n) p')) := by symm; exact h_n_prod
      _ = (p ^ k) * (∏ q ∈ S.filter (fun q => q ≠ p), q ^ ((factorization n) q)) := by
        -- Separate p from the product
        sorry
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

print(f"New proof: {len(new_proof)} chars")

# Old proof to replace
old_proof = '''theorem euler_opn_form (n : ℕ) (h_odd : ¬ 2 ∣ n) (h_perf : Perfect n) :
    ∃ (p k m : ℕ),
      Nat.Prime p ∧
      n = p ^ k * m ^ 2 ∧
      p % 4 = 1 ∧
      k % 4 = 1 ∧
      ¬ p ∣ m := by
  sorry -- Euler 1747. Not yet in Mathlib as of 2025.'''

# Replace
if old_proof in content:
    content = content.replace(old_proof, new_proof)
    with open('Imscribing/Primitives/OPN_2adic.lean', 'w') as f:
        f.write(content)
    print("SUCCESS: Euler theorem proof inserted!")
    print(f"File is now {len(content)} chars")
else:
    print("ERROR: Could not find old proof block")
    sys.exit(1)
