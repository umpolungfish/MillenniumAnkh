#!/usr/bin/env python3
"""Comprehensive fix for ALL remaining errors in OPN_2adic.lean"""
with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    content = f.read()

# === FIX 1: Ne.symm doesn't exist as expected - use explicit lambda ===
old1 = """          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            exact Ne.symm hq_erase.1"""
new1 = """          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            intro hpq; apply hq_erase.1; exact hpq.symm"""
assert old1 in content, "Fix 1 not found!"
content = content.replace(old1, new1, 1)

# === FIX 2+3: h_find_factor with wrong type and Finset.induction_on signature ===
old2 = """        have h_find_factor : ∃ q ∈ other_primes, p ∣ q ^ ((Nat.factorization n) q) := by
          refine Finset.induction_on other_primes ?_ ?_
          · intro h; exact hp_prime.not_dvd_one (by simpa [Finset.prod_empty] using h)
          · intro a s has ih h_dvd
            rw [Finset.prod_insert has] at h_dvd
            rcases hp_prime.dvd_mul.mp h_dvd with (h | h)
            · exact ⟨a, Finset.mem_insert_self a s, h⟩
            · rcases ih h with ⟨q, hq, hq_dvd⟩
              exact ⟨q, Finset.mem_insert_of_mem hq, hq_dvd⟩
        rcases h_find_factor with ⟨q, hq, hpq⟩"""
new2 = """        have h_find_factor : (p ∣ ∏ q ∈ other_primes, q ^ ((Nat.factorization n) q)) → 
            ∃ q ∈ other_primes, p ∣ q ^ ((Nat.factorization n) q) := by
          refine Finset.induction_on other_primes ?_ ?_
          · intro h
            simp at h
            exact absurd h (hp_prime.not_dvd_one)
          · intro a s has ih h_dvd'
            rw [Finset.prod_insert has] at h_dvd'
            rcases hp_prime.dvd_mul.mp h_dvd' with (h | h)
            · exact ⟨a, Finset.mem_insert_self a s, h⟩
            · rcases ih h with ⟨q, hq, hq_dvd⟩
              exact ⟨q, Finset.mem_insert_of_mem hq, hq_dvd⟩
        rcases h_find_factor hp_dvd_other with ⟨q, hq, hpq⟩"""
assert old2 in content, "Fix 2 not found!"
content = content.replace(old2, new2, 1)

# === FIX 4: h_range_sum block — replace with direct approach ===
old3 = """        have h_range_sum : (∑ i ∈ Finset.range ((2*n+2)+2), p ^ i) =
            (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by
          simp [Finset.sum_range_succ, add_assoc]
        rw [h_range_sum, Nat.add_mod, h_ih_mod, h_last_two]
        norm_num"""
new3 = """        rw [Finset.sum_range_succ, Finset.sum_range_succ, add_assoc]
        rw [Nat.add_mod, h_ih_mod, h_last_two]
        norm_num"""
assert old3 in content, "Fix 3 not found!"
content = content.replace(old3, new3, 1)

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(content)
print("3 fixes applied!")
