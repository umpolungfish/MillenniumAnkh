#!/usr/bin/env python3
"""Final comprehensive fix for ALL remaining errors in OPN_2adic.lean"""
with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    content = f.read()

# === FIX 1: Line 431 - intro/apply/symm block ===
old1 = """          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            intro hpq; apply hq_erase.1; exact hpq.symm"""
new1 = """          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            exact fun h => hq_erase.1 h.symm"""
assert old1 in content, "Fix 1 not found!"
content = content.replace(old1, new1, 1)

# === FIX 2: Line 437 - absurd with wrong type ===
old2 = """          · intro h
            simp at h
            exact absurd h (hp_prime.not_dvd_one)"""
new2 = """          · intro h
            simp at h
            exact hp_prime.not_dvd_one h"""
assert old2 in content, "Fix 2 not found!"
content = content.replace(old2, new2, 1)

# === FIX 3: Line 452 - hp_not_dvd_other needs intro h_dvd ===
old3 = """    have hp_not_dvd_other : ¬ p ∣ ∏ q ∈ other_primes, q ^ ((Nat.factorization n) q) := by
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
            exact fun h => hq_erase.1 h.symm
          intro hpq
          apply hne
          have := hq_prime.eq_one_or_self_of_dvd p hpq
          rcases this with (h | h)
          · have : 1 < p := hp_prime.one_lt; omega
          · exact h.symm
        have h_find_factor : (p ∣ ∏ q ∈ other_primes, q ^ ((Nat.factorization n) q)) → 
            ∃ q ∈ other_primes, p ∣ q ^ ((Nat.factorization n) q) := by
          refine Finset.induction_on other_primes ?_ ?_
          · intro h
            simp at h
            exact hp_prime.not_dvd_one h
          · intro a s has ih h_dvd'
            rw [Finset.prod_insert has] at h_dvd'
            rcases hp_prime.dvd_mul.mp h_dvd' with (h | h)
            · exact ⟨a, Finset.mem_insert_self a s, h⟩
            · rcases ih h with ⟨q, hq, hq_dvd⟩
              exact ⟨q, Finset.mem_insert_of_mem hq, hq_dvd⟩
        rcases h_find_factor hp_dvd_other with ⟨q, hq, hpq⟩
        have hq_prime : q.Prime := by
          have hq_S : q ∈ S := Finset.mem_of_mem_erase hq
          have hq_mem : q ∈ n.primeFactors := by
            have : S = n.primeFactors := rfl
            simpa [this] using hq_S
          exact (Nat.mem_primeFactors.mp hq_mem).1
        have h_p_dvd_q : p ∣ q := hp_prime.dvd_of_dvd_pow hpq
        exact h_prime_factor q hq h_p_dvd_q"""
new3 = """    have hp_not_dvd_other : ¬ p ∣ ∏ q ∈ other_primes, q ^ ((Nat.factorization n) q) := by
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
            exact fun h => hq_erase.1 h.symm
          intro hpq
          apply hne
          have := hq_prime.eq_one_or_self_of_dvd p hpq
          rcases this with (h | h)
          · have : 1 < p := hp_prime.one_lt; omega
          · exact h.symm
        have h_find_factor : (p ∣ ∏ q ∈ other_primes, q ^ ((Nat.factorization n) q)) → 
            ∃ q ∈ other_primes, p ∣ q ^ ((Nat.factorization n) q) := by
          refine Finset.induction_on other_primes ?_ ?_
          · intro h
            simp at h
            exact hp_prime.not_dvd_one h
          · intro a s has ih h_dvd'
            rw [Finset.prod_insert has] at h_dvd'
            rcases hp_prime.dvd_mul.mp h_dvd' with (h | h)
            · exact ⟨a, Finset.mem_insert_self a s, h⟩
            · rcases ih h with ⟨q, hq, hq_dvd⟩
              exact ⟨q, Finset.mem_insert_of_mem hq, hq_dvd⟩
        intro h_dvd
        rcases h_find_factor h_dvd with ⟨q, hq, hpq⟩
        have hq_prime : q.Prime := by
          have hq_S : q ∈ S := Finset.mem_of_mem_erase hq
          have hq_mem : q ∈ n.primeFactors := by
            have : S = n.primeFactors := rfl
            simpa [this] using hq_S
          exact (Nat.mem_primeFactors.mp hq_mem).1
        have h_p_dvd_q : p ∣ q := hp_prime.dvd_of_dvd_pow hpq
        exact h_prime_factor q hq h_p_dvd_q"""
assert old3 in content, "Fix 3 not found!"
content = content.replace(old3, new3, 1)

# === FIX 4+5: h_sum_even_pairs induction step + final omega ===
# Replace the entire block from h_sum_even_pairs to the end
old4 = """    have h_sum_even_pairs (r : ℕ) : (∑ i ∈ Finset.range (2*r+2), p ^ i) % 4 = 0 := by
      induction' r with n ih
      · simpa [add_comm] using h_one_plus_p_mod4
      · rw [show 2*(n+1)+2 = (2*n+2) + 2 by omega]
        rw [Finset.sum_range_succ, Finset.sum_range_succ, add_assoc]
        have h_ih_mod : (∑ i ∈ Finset.range (2*n+2), p ^ i) % 4 = 0 := ih
        have h_last_two : (p ^ (2*n+2) + p ^ (2*n+3)) % 4 = 0 := by
          have h_factor : p ^ (2*n+2) * (1 + p) = p ^ (2*n+2) + p ^ (2*n+3) := by ring
          rw [← h_factor, Nat.mul_mod]
          have h_pow_mod4 : p ^ (2*n+2) % 4 = 1 := by
            rw [show p ^ (2*n+2) = (p ^ 2) ^ (n+1) by ring]
            induction' (n+1) with m ih'
            · simp
            · rw [pow_succ, Nat.mul_mod, hp_sq_mod4, ih']; norm_num
          simp [h_pow_mod4, h_one_plus_p_mod4]
        rw [Finset.sum_range_succ, Finset.sum_range_succ, add_assoc]
        rw [Nat.add_mod, h_ih_mod, h_last_two]
        norm_num
    have hk_form : ∃ r : ℕ, k = 2*r+1 := by
      have := Nat.mod_two_eq_zero_or_one k
      rcases this with (h | h)
      · omega
      · refine ⟨k/2, ?_⟩
        have := Nat.div_add_mod k 2
        omega
    rcases hk_form with ⟨r, hkr⟩
    have h_range : k+1 = 2*r+2 := by rw [hkr]; omega
    have h_sig_mod4' : (∑ i ∈ Finset.range (2*r+2), p ^ i) % 4 = 2 := by
      simpa [h_range] using h_sigma_pk_mod4
    have h_sum_mod4 : (∑ i ∈ Finset.range (2*r+2), p ^ i) % 4 = 0 := h_sum_even_pairs r
    rw [h_sum_mod4] at h_sig_mod4'
    omega"""

new4 = """    have h_sum_even_pairs (r : ℕ) : (∑ i ∈ Finset.range (2*r+2), p ^ i) % 4 = 0 := by
      induction' r with n ih
      · simpa [add_comm] using h_one_plus_p_mod4
      · have h_last_two : (p ^ (2*n+2) + p ^ (2*n+3)) % 4 = 0 := by
          have h_factor : p ^ (2*n+2) * (1 + p) = p ^ (2*n+2) + p ^ (2*n+3) := by ring
          rw [← h_factor, Nat.mul_mod]
          have h_pow_mod4 : p ^ (2*n+2) % 4 = 1 := by
            rw [show p ^ (2*n+2) = (p ^ 2) ^ (n+1) by ring]
            induction' (n+1) with m ih'
            · simp
            · rw [pow_succ, Nat.mul_mod, hp_sq_mod4, ih']; norm_num
          simp [h_pow_mod4, h_one_plus_p_mod4]
        calc
          (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) % 4
              = (∑ i ∈ Finset.range (2*n+4), p ^ i) % 4 := by ring
          _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3)) % 4 := by
            simp [Finset.sum_range_succ, add_assoc]
          _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + (p ^ (2*n+2) + p ^ (2*n+3))) % 4 := by ring
          _ = (((∑ i ∈ Finset.range (2*n+2), p ^ i) % 4) + ((p ^ (2*n+2) + p ^ (2*n+3)) % 4)) % 4 := by rw [Nat.add_mod]
          _ = (0 + 0) % 4 := by rw [ih, h_last_two]
          _ = 0 := by norm_num
    have hk_form : ∃ r : ℕ, k = 2*r+1 := by
      have := Nat.mod_two_eq_zero_or_one k
      rcases this with (h | h)
      · omega
      · refine ⟨k/2, ?_⟩
        have := Nat.div_add_mod k 2
        omega
    rcases hk_form with ⟨r, hkr⟩
    have h_range : k+1 = 2*r+2 := by rw [hkr]; omega
    have h_contra : (∑ i ∈ Finset.range (2*r+2), p ^ i) % 4 = 2 := by
      simpa [h_range] using h_sigma_pk_mod4
    have h_sum_mod4 : (∑ i ∈ Finset.range (2*r+2), p ^ i) % 4 = 0 := h_sum_even_pairs r
    rw [h_sum_mod4] at h_contra
    omega"""

assert old4 in content, "Fix 4 not found!"
content = content.replace(old4, new4, 1)

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(content)
print("All fixes applied!")
