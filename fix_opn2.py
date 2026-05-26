#!/usr/bin/env python3
"""Fix remaining 5 errors in OPN_2adic.lean"""
with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    content = f.read()

# === FIX 1: Line 431 - Ne.symm not Eq.symm ===
old1 = "            exact hq_erase.1.symm"
new1 = "            exact Ne.symm hq_erase.1"
assert old1 in content, "Fix 1 not found!"
content = content.replace(old1, new1, 1)

# === FIX 2: Line 432 - hp_prime.dvd_prod_iff doesn't exist ===
# Replace the entire h_exists block with Finset induction using hp_prime.dvd_mul
old2 = """        have h_exists := hp_prime.dvd_prod_iff.mp ?_
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
        · exact hp_dvd_other"""

new2 = """        have h_find_factor : ∃ q ∈ other_primes, p ∣ q ^ ((Nat.factorization n) q) := by
          refine Finset.induction_on other_primes ?_ ?_
          · intro h; exact hp_prime.not_dvd_one (by simpa [Finset.prod_empty] using h)
          · intro a s has ih h_dvd
            rw [Finset.prod_insert has] at h_dvd
            rcases hp_prime.dvd_mul.mp h_dvd with (h | h)
            · exact ⟨a, Finset.mem_insert_self a s, h⟩
            · rcases ih h with ⟨q, hq, hq_dvd⟩
              exact ⟨q, Finset.mem_insert_of_mem hq, hq_dvd⟩
        rcases h_find_factor with ⟨q, hq, hpq⟩
        have hq_prime : q.Prime := by
          have hq_S : q ∈ S := Finset.mem_of_mem_erase hq
          have hq_mem : q ∈ n.primeFactors := by
            have : S = n.primeFactors := rfl
            simpa [this] using hq_S
          exact (Nat.mem_primeFactors.mp hq_mem).1
        have h_p_dvd_q : p ∣ q := hp_prime.dvd_of_dvd_pow hpq
        exact h_prime_factor q hq h_p_dvd_q"""

assert old2 in content, "Fix 2 not found!"
content = content.replace(old2, new2, 1)

# === FIXES 3+4: Lines 469-480 - calc block in h_sum_even_pairs ===
old3 = """        calc
          (∑ i ∈ Finset.range ((2*n+2) + 2), p ^ i) % 4
              = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3)) % 4 := by
                rw [Finset.sum_range_succ, Finset.sum_range_succ, add_assoc]
          _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + (p ^ (2*n+2) + p ^ (2*n+3))) % 4 := by ring
          _ = (((∑ i ∈ Finset.range (2*n+2), p ^ i) % 4) + ((p ^ (2*n+2) + p ^ (2*n+3)) % 4)) % 4 := by rw [Nat.add_mod]
          _ = (0 + 0) % 4 := by rw [h_ih_mod, h_last_two]
          _ = 0 := by norm_num"""

new3 = """        have h_range_sum : (∑ i ∈ Finset.range ((2*n+2)+2), p ^ i) =
            (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by
          simp [Finset.sum_range_succ, add_assoc]
        rw [h_range_sum, Nat.add_mod, h_ih_mod, h_last_two]
        norm_num"""

assert old3 in content, "Fix 3 not found!"
content = content.replace(old3, new3, 1)

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(content)
print("All 5 fixes applied!")
