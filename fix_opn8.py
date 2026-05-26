#!/usr/bin/env python3
"""Fix: h.symm->h, calc, hk_form, final exfalso"""
with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    c = f.read()

# Fix 1: h.symm -> h (line 432)
# After apply hne, the goal is p = q, so we need h, not h.symm
c = c.replace("""          · exact h.symm""", """          · exact h""")

# Fix 2: calc block - replace with direct approach 
c = c.replace("""        have h_sum_eq : (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) =
            (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by
          have h1 : 2*(n+1)+2 = 2*n+4 := by omega
          calc
            (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) = (∑ i ∈ Finset.range (2*n+4), p ^ i) := by simp [h1]
            _ = (∑ i ∈ Finset.range (2*n+3), p ^ i) + p ^ (2*n+3) := by rw [Finset.sum_range_succ]
            _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2)) + p ^ (2*n+3) := by rw [Finset.sum_range_succ]
            _ = (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := rfl""",
"""        have h_sum_eq : (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) =
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
            _ = (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := rfl""")

# Fix 3: hk_form - simplify to avoid omega issues
c = c.replace("""    have hk_odd_val : k % 2 = 1 := hk_odd
    have hk_form : ∃ r : ℕ, k = 2*r+1 := by
      have h_cases := Nat.mod_two_eq_zero_or_one k
      rcases h_cases with (h | h)
      · rw [hk_odd_val] at h; omega
      · refine ⟨k/2, ?_⟩
        have := Nat.div_add_mod k 2
        omega
    rcases hk_form with ⟨r, hkr⟩""",
"""    have hk_odd_val : k % 2 = 1 := hk_odd
    have hk_eq_form : k = 2*(k/2) + 1 := by
      have h_mod := Nat.div_add_mod k 2
      rw [hk_odd_val, add_comm] at h_mod
      omega
    have hk_form : ∃ r : ℕ, k = 2*r+1 := ⟨k/2, hk_eq_form⟩""")

# Fix 4: final exfalso needed
c = c.replace("""    rw [h_sum_mod4] at h_contra
    have : (0 : ℕ) ≠ 2 := by omega
    exact this h_contra""",
"""    rw [h_sum_mod4] at h_contra
    exfalso; exact (by omega : (0 : ℕ) ≠ 2) h_contra""")

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(c)
print("Done!")
