#!/usr/bin/env python3
"""Absolute final fix for all remaining errors in OPN_2adic.lean"""
with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    c = f.read()

# Fix 1: hne - use explicit lambda
c = c.replace("""          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            have hq_ne_p : q ≠ p := hq_erase.1
            intro hpq; apply hq_ne_p; exact hpq.symm""",
"""          have hne : p ≠ q := by
            have hq_erase := Finset.mem_erase.mp hq
            have hq_ne_p : q ≠ p := hq_erase.1
            exact fun hpq => hq_ne_p (hpq.symm)""")

# Fix 2: h_sum_eq - replace calc with direct simp
c = c.replace("""        have h_sum_eq : (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) =
            (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by
          calc
            (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) = (∑ i ∈ Finset.range (2*n+4), p ^ i) := by
              have h_eq : 2*(n+1)+2 = 2*n+4 := by omega
              simpa [h_eq]
            _ = (∑ i ∈ Finset.range (2*n+3), p ^ i) + p ^ (2*n+3) := by rw [Finset.sum_range_succ]
            _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2)) + p ^ (2*n+3) := by rw [Finset.sum_range_succ]
            _ = (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by ring""",
"""        have h_sum_eq : (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) =
            (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by
          have h1 : 2*(n+1)+2 = 2*n+4 := by omega
          calc
            (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) = (∑ i ∈ Finset.range (2*n+4), p ^ i) := by simp [h1]
            _ = (∑ i ∈ Finset.range (2*n+3), p ^ i) + p ^ (2*n+3) := by rw [Finset.sum_range_succ]
            _ = ((∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2)) + p ^ (2*n+3) := by rw [Finset.sum_range_succ]
            _ = (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := rfl""")

# Fix 3: hk_form - make omega's job explicit
c = c.replace("""    have hk_form : ∃ r : ℕ, k = 2*r+1 := by
      have := Nat.mod_two_eq_zero_or_one k
      rcases this with (h | h)
      · omega
      · refine ⟨k/2, ?_⟩
        have := Nat.div_add_mod k 2
        omega""",
"""    have hk_odd_val : k % 2 = 1 := hk_odd
    have hk_form : ∃ r : ℕ, k = 2*r+1 := by
      have h_cases := Nat.mod_two_eq_zero_or_one k
      rcases h_cases with (h | h)
      · rw [hk_odd_val] at h; omega
      · refine ⟨k/2, ?_⟩
        have := Nat.div_add_mod k 2
        omega""")

# Fix 4: final omega - replace with explicit contradiction
c = c.replace("""    rw [h_sum_mod4] at h_contra
    omega""",
"""    rw [h_sum_mod4] at h_contra
    have : (0 : ℕ) ≠ 2 := by omega
    exact this h_contra""")

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(c)
print("Done!")
