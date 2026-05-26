#!/usr/bin/env python3
"""Replace induction' with intro r; induction r"""
with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    c = f.read()

# Replace the entire h_sum_even_pairs block
old = """    have h_sum_even_pairs (r : ℕ) : (∑ i ∈ Finset.range (2*r+2), p ^ i) % 4 = 0 := by
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
        have h_sum_eq : (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) =
            (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by
          simp [Finset.sum_range_succ, add_assoc, show 2*(n+1)+2 = 2*n+4 by omega]
        rw [h_sum_eq, add_assoc, Nat.add_mod, ih, h_last_two]
        norm_num"""

new = """    have h_sum_even_pairs : ∀ r : ℕ, (∑ i ∈ Finset.range (2*r+2), p ^ i) % 4 = 0 := by
      intro r
      induction r with
      | zero =>
        simpa [add_comm] using h_one_plus_p_mod4
      | succ n ih =>
        have h_last_two : (p ^ (2*n+2) + p ^ (2*n+3)) % 4 = 0 := by
          have h_factor : p ^ (2*n+2) * (1 + p) = p ^ (2*n+2) + p ^ (2*n+3) := by ring
          rw [← h_factor, Nat.mul_mod]
          have h_pow_mod4 : p ^ (2*n+2) % 4 = 1 := by
            rw [show p ^ (2*n+2) = (p ^ 2) ^ (n+1) by ring]
            induction (n+1) with
            | zero => simp
            | succ m ih' =>
              rw [pow_succ, Nat.mul_mod, hp_sq_mod4, ih']; norm_num
          simp [h_pow_mod4, h_one_plus_p_mod4]
        have h_sum_eq : (∑ i ∈ Finset.range (2*(n+1)+2), p ^ i) =
            (∑ i ∈ Finset.range (2*n+2), p ^ i) + p ^ (2*n+2) + p ^ (2*n+3) := by
          simp [Finset.sum_range_succ, add_assoc, show 2*(n+1)+2 = 2*n+4 by omega]
        rw [h_sum_eq, add_assoc, Nat.add_mod, ih, h_last_two]
        norm_num"""

assert old in c, "Old block not found!"
c = c.replace(old, new, 1)

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(c)
print("Done!")
