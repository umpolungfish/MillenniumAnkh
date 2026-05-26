#!/usr/bin/env python3
"""Comprehensive fix for OPN_2adic.lean"""
import re

with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    content = f.read()

# === FIX 1: Line 360 - h_prod_split ===
old1 = """    have h_prod_split : (∏ r ∈ S, sigma 1 (r ^ ((Nat.factorization n) r))) =
        sigma 1 (p ^ k) * (∏ r ∈ S.erase p, sigma 1 (r ^ ((Nat.factorization n) r))) := by
      rw [Finset.prod_insert h_not_mem]; simp"""

new1 = """    have h_prod_split : (∏ r ∈ S, sigma 1 (r ^ ((Nat.factorization n) r))) =
        sigma 1 (p ^ k) * (∏ r ∈ S.erase p, sigma 1 (r ^ ((Nat.factorization n) r))) := by
      simpa [k] using (Finset.mul_prod_erase S (fun r => sigma 1 (r ^ ((Nat.factorization n) r))) hpS).symm"""

assert old1 in content, "Fix 1 not found!"
content = content.replace(old1, new1, 1)

# === FIX 2: Line 410 - hpm_sq ===
old2 = """      have hpm_sq : p ∣ m ^ 2 := by
        have : m ^ 2 = m * m := by ring
        rw [this]; exact mul_dvd_mul_left m hpm"""

new2 = """      have hpm_sq : p ∣ m ^ 2 :=
        hpm.trans (by simpa [sq] using dvd_mul_right m m)"""

assert old2 in content, "Fix 2 not found!"
content = content.replace(old2, new2, 1)

# === FIX 3: Line 422 - Finset.ne_of_mem_erase ===
old3 = """    have h_rest_odd : (∏ r ∈ S.erase p, sigma 1 (r ^ ((Nat.factorization n) r))) % 2 = 1 :=
      prod_odd (S.erase p) (fun r => sigma 1 (r ^ ((Nat.factorization n) r))) (fun x hx => h_others_odd x (Finset.mem_of_mem_erase hx) (Finset.ne_of_mem_erase hx))"""

new3 = """    have h_rest_odd : (∏ r ∈ S.erase p, sigma 1 (r ^ ((Nat.factorization n) r))) % 2 = 1 :=
      prod_odd (S.erase p) (fun r => sigma 1 (r ^ ((Nat.factorization n) r))) (fun x hx => h_others_odd x (Finset.mem_of_mem_erase hx) (by
        have hx' := Finset.mem_erase.mp hx
        exact hx'.1))"""

assert old3 in content, "Fix 3 not found!"
content = content.replace(old3, new3, 1)

# === FIX 4+5: Lines 430-460 - complete rewrite of h_p_not_dvd_m proof ===
old4 = """    have h_p_not_dvd_m : ¬ p ∣ m := by
      intro hpm
      have hpm_sq : p ∣ m ^ 2 :=
        hpm.trans (by simpa [sq] using dvd_mul_right m m)
      have hp_dvd_other : p ∣ ∏ q ∈ other_primes, q ^ ((Nat.factorization n) q) := by
        rw [hm_sq_eq]; exact hpm_sq
      have hp_not_dvd_other : ¬ p ∣ ∏ q ∈ other_primes, q ^ ((Nat.factorization n) q) := by
        have h_prime_factor : ∀ q ∈ other_primes, ¬ p ∣ q := by
          intro q hq
          have hq_prime : q.Prime := by
            have hq_mem : q ∈ n.primeFactors := by
              have hq_S : q ∈ S := Finset.mem_of_mem_erase hq
              have : S = n.primeFactors := rfl
              simpa [this] using hq_S
            exact (Nat.mem_primeFactors.mp hq_mem).1
          have hne : p ≠ q := Finset.ne_of_mem_erase hq
          intro hpq
          apply hne
          have := hq_prime.eq_one_or_self_of_dvd p hpq
          rcases this with (h | h)
          · have : 1 < p := hp_prime.one_lt; omega
          · exact h.symm
        have h_p_dvd_factor : ∃ q ∈ other_primes, p ∣ q ^ ((Nat.factorization n) q) :=
          by
            have : (∏ q ∈ other_primes, q ^ ((Nat.factorization n) q)) = (∏ q ∈ other_primes, q ^ ((Nat.factorization n) q)) := rfl
            have h_dvd_prod : p ∣ (∏ q ∈ other_primes, q ^ ((Nat.factorization n) q)) := hp_dvd_other
            have h_prime_factors : ∀ q ∈ other_primes, Nat.Prime q := by
              intro q hq
              have hq_S : q ∈ S := Finset.mem_of_mem_erase hq
              have hq_mem : q ∈ n.primeFactors := by
                have : S = n.primeFactors := rfl
                simpa [this] using hq_S
              exact (Nat.mem_primeFactors.mp hq_mem).1
            have h_exists := Nat.exists_prime_and_dvd h_dvd_prod
            rcases h_exists with ⟨q, hq_prime, hq_mem, hq_dvd⟩
            refine ⟨q, hq_mem, ?_⟩
            have hq_prime' : Nat.Prime q := h_prime_factors q hq_mem
            have h_dvd_q : p ∣ q := hq_prime'.dvd_of_dvd_pow hq_dvd
            exact hq_dvd
        rcases h_p_dvd_factor with ⟨q, hq, hpq⟩
        have hq_prime : q.Prime := by
          have hq_mem : q ∈ n.primeFactors := by
            have hq_S : q ∈ S := Finset.mem_of_mem_erase hq
            have : S = n.primeFactors := rfl
            simpa [this] using hq_S
          exact (Nat.mem_primeFactors.mp hq_mem).1
        have h_p_dvd_q : p ∣ q := hq_prime.dvd_of_dvd_pow hpq
        exact h_prime_factor q hq h_p_dvd_q
      exact hp_not_dvd_other hp_dvd_other"""

new4 = """    have h_p_not_dvd_m : ¬ p ∣ m := by
      intro hpm
      have hpm_sq : p ∣ m ^ 2 :=
        hpm.trans (by simpa [sq] using dvd_mul_right m m)
      have hp_dvd_other : p ∣ ∏ q ∈ other_primes, q ^ ((Nat.factorization n) q) := by
        rw [hm_sq_eq]; exact hpm_sq
      have hp_not_dvd_other : ¬ p ∣ ∏ q ∈ other_primes, q ^ ((Nat.factorization n) q) := by
        have h_prime_factor : ∀ q ∈ other_primes, ¬ p ∣ q := by
          intro q hq
          have hq_prime : q.Prime := by
            have hq_S : q ∈ S := Finset.mem_of_mem_erase hq
            have hq_mem : q ∈ n.primeFactors := by
              have : S = n.primeFactors := rfl
              simpa [this] using hq_S
            exact (Nat.mem_primeFactors.mp hq_mem).1
          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            exact hq_erase.1.symm
          intro hpq
          apply hne
          have := hq_prime.eq_one_or_self_of_dvd p hpq
          rcases this with (h | h)
          · have : 1 < p := hp_prime.one_lt; omega
          · exact h.symm
        have h_exists := hp_prime.dvd_prod_iff.mp ?_
        · rcases h_exists with ⟨q, hq, hpq⟩
          have hq_prime : q.Prime := by
            have hq_S : q ∈ S := Finset.mem_of_mem_erase hq
            have hq_mem : q ∈ n.primeFactors := by
              have : S = n.primeFactors := rfl
              simpa [this] using hq_S
            exact (Nat.mem_primeFactors.mp hq_mem).1
          have h_p_dvd_q : p ∣ q := hp_prime.dvd_of_dvd_pow hpq
          exact h_prime_factor q hq h_p_dvd_q
        · exact Finset.mem_of_mem_erase
        · exact hp_dvd_other
      exact hp_not_dvd_other hp_dvd_other"""

assert old4 in content, "Fix 4 not found!"
content = content.replace(old4, new4, 1)

# === FIX 6+7: Lines 482-488 - calc block in h_sum_even_pairs ===
old5 = """        calc
          ((∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3)) % 4
              = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + (p ^ (2*n+2) + p ^ (2*n+3))) % 4 := by ring
          _ = (((∑ i ∈ Finset.range (2*n+2), p ^ i) % 4) + ((p ^ (2*n+2) + p ^ (2*n+3)) % 4)) % 4 := by rw [Nat.add_mod]
          _ = (0 + 0) % 4 := by rw [h_ih_mod, h_last_two]
          _ = 0 := by norm_num"""

new5 = """        calc
          (∑ i ∈ Finset.range ((2*n+2) + 2), p ^ i) % 4
              = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3)) % 4 := by
                rw [Finset.sum_range_succ, Finset.sum_range_succ, add_assoc]
          _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + (p ^ (2*n+2) + p ^ (2*n+3))) % 4 := by ring
          _ = (((∑ i ∈ Finset.range (2*n+2), p ^ i) % 4) + ((p ^ (2*n+2) + p ^ (2*n+3)) % 4)) % 4 := by rw [Nat.add_mod]
          _ = (0 + 0) % 4 := by rw [h_ih_mod, h_last_two]
          _ = 0 := by norm_num"""

assert old5 in content, "Fix 5 not found!"
content = content.replace(old5, new5, 1)

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(content)

print("All fixes applied successfully!")
