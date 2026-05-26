#!/usr/bin/env python3
"""Fix remaining errors in OPN_2adic.lean"""
with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    c = f.read()

# Fix 1: hne block - be explicit about Ne type
c = c.replace("""          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            intro h; apply hq_erase.1; exact h.symm""",
"""          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            have hq_ne_p : q ≠ p := hq_erase.1
            intro hpq; apply hq_ne_p; exact hpq.symm""")

# Fix 2: base case of induction - use exfalso
c = c.replace("""          · intro h
            have h' : p ∣ 1 := by simpa [Finset.prod_empty] using h
            exact hp_prime.not_dvd_one h'""",
"""          · intro h
            have h' : p ∣ 1 := by simpa [Finset.prod_empty] using h
            exfalso; exact hp_prime.not_dvd_one h'""")

# Fix 3: h_sum_eq calc block - replace omega with ring
c = c.replace("""          calc
            (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) = (∑ i ∈ Finset.range (2*n+4), p ^ i) := by omega""",
"""          calc
            (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) = (∑ i ∈ Finset.range (2*n+4), p ^ i) := by
              have h_eq : 2*(n+1)+2 = 2*n+4 := by omega
              simpa [h_eq]""")

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(c)
print("Done!")
