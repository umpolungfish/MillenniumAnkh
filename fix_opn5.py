#!/usr/bin/env python3
"""Fix remaining 3 errors in OPN_2adic.lean"""
with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    c = f.read()

# Fix 1: Line 431 - hne block
c = c.replace("""          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            exact fun h => hq_erase.1 h.symm""",
"""          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            intro h; apply hq_erase.1; exact h.symm""")

# Fix 2: Line 437 - simp rewrote p∣1 to p=1
c = c.replace("""          · intro h
            simp at h
            exact hp_prime.not_dvd_one h""",
"""          · intro h
            have h' : p ∣ 1 := by simpa [Finset.prod_empty] using h
            exact hp_prime.not_dvd_one h'""")

# Fix 3: Line 478 - calc block with ring issues
# Replace the calc block with a direct rw chain
c = c.replace("""        calc
          (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) % 4
              = (∑ i ∈ Finset.range (2*n+4), p ^ i) % 4 := by ring
          _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3)) % 4 := by
            simp [Finset.sum_range_succ, add_assoc]
          _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + (p ^ (2*n+2) + p ^ (2*n+3))) % 4 := by ring
          _ = (((∑ i ∈ Finset.range (2*n+2), p ^ i) % 4) + ((p ^ (2*n+2) + p ^ (2*n+3)) % 4)) % 4 := by rw [Nat.add_mod]
          _ = (0 + 0) % 4 := by rw [ih, h_last_two]
          _ = 0 := by norm_num""",
"""        have h_sum_eq : (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) =
            (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by
          calc
            (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) = (∑ i ∈ Finset.range (2*n+4), p ^ i) := by omega
            _ = (∑ i ∈ Finset.range (2*n+3), p ^ i) + p ^ (2*n+3) := by rw [Finset.sum_range_succ]
            _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2)) + p ^ (2*n+3) := by rw [Finset.sum_range_succ]
            _ = (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by ring
        rw [h_sum_eq, add_assoc, Nat.add_mod, ih, h_last_two]
        norm_num""")

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(c)
print("Done!")
