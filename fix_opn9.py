#!/usr/bin/env python3
"""Complete fix: restore r/hkr, fix calc, fix hk_form"""
with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    c = f.read()

# Fix 1: h_sum_eq - simplify calc block
c = c.replace("""        have h_sum_eq : (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) =
            (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by
          have h1 : 2*(n+1)+2 = 2*n+4 := by omega
          have h_eq1 : (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) = (∑ i ∈ Finset.range (2*n+4), p ^ i) := by
            simp [h1]
          have h_eq2 : (∑ i ∈ Finset.range (2*n+4), p ^ i) = (∑ i ∈ Finset.range (2*n+3), p ^ i) + p ^ (2*n+3) := by
            rw [Finset.sum_range_succ]
          have h_eq3 : (∑ i ∈ Finset.range (2*n+3), p ^ i) = (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) := by
            rw [Finset.sum_range_succ]
          calc
            (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) = (∑ i ∈ Finset.range (2*n+4), p ^ i) := h_eq1
            _ = (∑ i ∈ Finset.range (2*n+3), p ^ i) + p ^ (2*n+3) := h_eq2
            _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2)) + p ^ (2*n+3) := by rw [h_eq3]
            _ = (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := rfl""",
"""        have h_sum_eq : (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) =
            (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by
          simp [Finset.sum_range_succ, add_assoc, show 2*(n+1)+2 = 2*n+4 by omega]""")

# Fix 2: restore r and hkr properly
c = c.replace("""    have hk_form : ∃ r : ℕ, k = 2*r+1 := ⟨k/2, hk_eq_form⟩
    have h_range : k+1 = 2*r+2 := by rw [hkr]; omega""",
"""    have hk_form : ∃ r : ℕ, k = 2*r+1 := ⟨k/2, hk_eq_form⟩
    rcases hk_form with ⟨r, hkr⟩
    have h_range : k+1 = 2*r+2 := by rw [hkr]; omega""")

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(c)
print("Done!")
