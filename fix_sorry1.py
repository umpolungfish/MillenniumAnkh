with open('/home/mrnob0dy666/MillenniumAnkh/Imscribing/Classical/Solitary10.lean', 'r') as f:
    content = f.read()

old_sorry1 = """        rcases h31_z with ⟨w, hz_eq⟩
        rw [hz_eq] at hn_eq h_sigma2
        -- n = 31²*w. σ(31²*w) = 45*31*w = 1395*w
        -- If gcd(31,w)=1: σ(31²)*σ(w) = 993*σ(w) = 1395*w → 331*σ(w) = 465*w
        -- This leads to another round of descent via 331.
        -- The full descent chain: 31 → 331 → 36631 → 7194483
        -- Each step: either coprime → contradiction (like descent_32_45), or p²|n → next prime.
        -- The product bound gives final contradiction after 7194483.
        -- For this formalization, we complete the main steps.
        sorry"""

new_sorry1 = """        rcases h31_z with ⟨w, hz_eq⟩
        rw [hz_eq] at hn_eq h_sigma2
        -- n = 31²*w. σ(31²*w) = 45*31*w = 1395*w
        have h_sigma_sq : σ (31 ^ 2 * w) = 1395 * w := by
          -- from h_sigma2: σ(31*(31*w)) = 45*(31*w)
          -- i.e., σ(31²*w) = 1395*w
          simpa [mul_comm, mul_left_comm, mul_assoc, pow_two] using h_sigma2
        have hw_pos : w > 0 := by
          by_contra! hle
          have hw0 : w = 0 := by omega
          rw [hw0, mul_zero] at h_sigma_sq
          have := sigma_ge_self 0 (by norm_num : 0 > 0)
          omega
        by_cases h_cop_31_w : Nat.Coprime 31 w
        · -- gcd(31,w)=1: σ(31²)*σ(w) = 993*σ(w) = 1395*w → 331*σ(w) = 465*w
          have h_mul_sq : σ (31 ^ 2 * w) = σ (31 ^ 2) * σ w := sigma_mul_coprime h_cop_31_w
          have h_sigma_31sq : σ (31 ^ 2) = 993 := by native_decide
          rw [h_mul_sq, h_sigma_31sq] at h_sigma_sq
          -- 993 * σ w = 1395 * w → divide by 3: 331 * σ w = 465 * w
          have h331 : 331 * σ w = 465 * w := by omega
          have h_cop_331_465 : Nat.Coprime 331 465 := by native_decide
          have h331_w : 331 ∣ w := factor_from_eq 331 465 w h_cop_331_465 h331
          rcases h331_w with ⟨v, hw_eq⟩
          rw [hw_eq] at h331
          -- 331*σ(331*v) = 465*331*v → σ(331*v) = 465*v
          have h_sigma3 : σ (331 * v) = 465 * v := by omega
          have hv_pos : v > 0 := by
            by_contra! hle
            have hv0 : v = 0 := by omega
            rw [hv0, mul_zero] at hw_eq
            omega
          by_cases h_cop_331_v : Nat.Coprime 331 v
          · -- 332*σ(v) = 465*v → contradiction via descent_332_465
            have h_mul3 : σ (331 * v) = σ 331 * σ v := sigma_mul_coprime h_cop_331_v
            have h_sigma_331_val : σ 331 = 332 := by native_decide
            rw [h_mul3, h_sigma_331_val] at h_sigma3
            -- 332 * σ v = 465 * v
            exfalso; exact descent_332_465 v hv_pos (by omega)
          · -- 331 ∣ v, need to continue descent through 36631 → 7194483
            sorry
        · -- 31 ∣ w, need to factor out higher powers of 31
          sorry"""

if old_sorry1 in content:
    content = content.replace(old_sorry1, new_sorry1)
    print("Replaced first sorry")
else:
    print("WARNING: old_sorry1 not found")

with open('/home/mrnob0dy666/MillenniumAnkh/Imscribing/Classical/Solitary10.lean', 'w') as f:
    f.write(content)
