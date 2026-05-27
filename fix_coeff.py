with open('Imscribing/Classical/Solitary10.lean', 'r') as f:
    content = f.read()

# Find and replace the h_coeff block
old_coeff = """    have h_coeff : 332 * (2 ^ (e + 1) - 1) > 465 * 2 ^ e := by
      have h2e_ge_2 : 2 ^ e ≥ 2 := by
        calc
          2 ^ e ≥ 2 ^ 1 := Nat.pow_le_pow_right (by norm_num) he_pos
          _ = 2 := by norm_num
      have h199_gt_332 : 199 * 2 ^ e > 332 := by
        have h_mul : 199 * 2 ^ e ≥ 199 * 2 := Nat.mul_le_mul_left 199 h2e_ge_2
        have h199_2 : 199 * 2 = 398 := by norm_num
        omega
      have h_pow_succ : 2 ^ (e + 1) = 2 * 2 ^ e := by ring
      have h_total : 332 * 2 ^ (e + 1) > 465 * 2 ^ e + 332 := by
        rw [h_pow_succ]
        calc
          332 * (2 * 2 ^ e) = 664 * 2 ^ e := by ring
          _ = 465 * 2 ^ e + 199 * 2 ^ e := by ring
          _ > 465 * 2 ^ e + 332 := by omega
      have h_id : 332 * 2 ^ (e + 1) = 332 * (2 ^ (e + 1) - 1) + 332 := by
        have hpos : 2 ^ (e + 1) ≥ 1 := pow_pos (by norm_num) (e + 1)
        have h_sub : 2 ^ (e + 1) = (2 ^ (e + 1) - 1) + 1 := by omega
        rw [h_sub, mul_add]
        simp
      rw [h_id] at h_total
      omega"""

new_coeff = """    have h_coeff : 332 * (2 ^ (e + 1) - 1) > 465 * 2 ^ e := by
      have h2e_ge_2 : 2 ^ e ≥ 2 := by
        calc
          2 ^ e ≥ 2 ^ 1 := Nat.pow_le_pow_right (by norm_num) he_pos
          _ = 2 := by norm_num
      have h199_gt_332 : 199 * 2 ^ e > 332 := by
        have h_mul : 199 * 2 ^ e ≥ 199 * 2 := Nat.mul_le_mul_left 199 h2e_ge_2
        have h199_2 : 199 * 2 = 398 := by norm_num
        omega
      have h_pow_succ : 2 ^ (e + 1) = 2 * 2 ^ e := by ring
      rw [h_pow_succ]
      -- Goal: 332*(2*2^e - 1) > 465*2^e in ℕ
      -- Use integer arithmetic to avoid Nat subtraction issues
      have h_ineq : (332 : ℤ) * ((2 : ℤ) * ((2 : ℕ) ^ e : ℤ) - 1) > (465 : ℤ) * ((2 : ℕ) ^ e : ℤ) := by
        have h199 : (199 : ℤ) * ((2 : ℕ) ^ e : ℤ) > (332 : ℤ) := by exact_mod_cast h199_gt_332
        nlinarith
      -- Both sides are positive, so we can cast back
      have hpos_left : 0 < 332 * (2 * 2 ^ e - 1) := by
        have h_2pow_ge_2 : 2 * 2 ^ e ≥ 4 := by
          omega
        omega
      exact_mod_cast h_ineq"""

if old_coeff in content:
    content = content.replace(old_coeff, new_coeff)
    print("Replaced h_coeff block")
else:
    print("WARNING: old_coeff not found exactly")
    # Check if partial match
    if 'h_coeff : 332 * (2 ^ (e + 1) - 1) > 465 * 2 ^ e' in content:
        print("  partial match found")

with open('Imscribing/Classical/Solitary10.lean', 'w') as f:
    f.write(content)
