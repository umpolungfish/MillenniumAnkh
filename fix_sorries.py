with open('/home/mrnob0dy666/MillenniumAnkh/Imscribing/Classical/Solitary10.lean', 'r') as f:
    content = f.read()

# Add descent_41872_51305 before the main theorem
# Find the insertion point: before "theorem ten_is_solitary"
insert_pos = content.find('theorem ten_is_solitary')

descent_41872 = '''
/-- 41872 * σ(x) = 51305 * x has no positive solution.
    Same 2-power factorization pattern as descent_332_465.
    Key inequality: 41872*(2^(e+1)-1) > 51305*2^e from 32439*2^e > 41872. -/
lemma descent_41872_51305 (x : ℕ) (hx_pos : x > 0) (h : 41872 * σ x = 51305 * x) : False := by
  rcases factor_2_pow_odd x hx_pos with ⟨e, t, ht_odd, hx_eq⟩
  rw [hx_eq] at h
  have ht_pos : t > 0 := by
    by_contra! hle
    have ht0 : t = 0 := by omega
    rw [ht0, mul_zero] at hx_eq
    omega
  have h_cop : Nat.Coprime (2 ^ e) t := by
    have hp2 : Nat.Prime 2 := by norm_num
    have h2t : ¬ 2 ∣ t := by
      intro h2t
      have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2t
      rw [ht_odd] at h2t_mod
      omega
    have h_cop_2_t : Nat.Coprime 2 t :=
      (Nat.Prime.coprime_iff_not_dvd hp2).mpr h2t
    exact h_cop_2_t.pow_left e
  have h_sigma_mul : σ (2 ^ e * t) = σ (2 ^ e) * σ t := sigma_mul_coprime h_cop
  rw [h_sigma_mul, sigma_two_pow e] at h
  have h_cop_a_b : Nat.Coprime 41872 51305 := by native_decide
  by_cases he0 : e = 0
  · subst he0; simp at hx_eq h
    have ha_t : 41872 ∣ t := factor_from_eq 41872 51305 t h_cop_a_b h
    have h2_t : 2 ∣ t := Nat.dvd_trans (by norm_num : 2 ∣ 41872) ha_t
    have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2_t
    rw [ht_odd] at h2t_mod
    omega
  · have he_pos : e ≥ 1 := by omega
    have h_eq : (41872 * (2 ^ (e + 1) - 1)) * σ t = (51305 * 2 ^ e) * t := by
      calc
        (41872 * (2 ^ (e + 1) - 1)) * σ t = 41872 * ((2 ^ (e + 1) - 1) * σ t) := by ring
        _ = 51305 * (2 ^ e * t) := h
        _ = (51305 * 2 ^ e) * t := by ring
    have h_coeff : 41872 * (2 ^ (e + 1) - 1) > 51305 * 2 ^ e := by
      have h2e_ge_2 : 2 ^ e ≥ 2 := by
        calc
          2 ^ e ≥ 2 ^ 1 := Nat.pow_le_pow_right (by norm_num) he_pos
          _ = 2 := by norm_num
      -- Key constant: 2*41872 - 51305 = 32439
      have h32439_gt : 32439 * 2 ^ e > 41872 := by
        have h_mul : 32439 * 2 ^ e ≥ 32439 * 2 := Nat.mul_le_mul_left 32439 h2e_ge_2
        have h_base : 32439 * 2 = 64878 := by norm_num
        omega
      have h_pow_succ : 2 ^ (e + 1) = 2 * 2 ^ e := by ring
      have h_total : 41872 * 2 ^ (e + 1) > 51305 * 2 ^ e + 41872 := by
        rw [h_pow_succ]
        calc
          41872 * (2 * 2 ^ e) = 83744 * 2 ^ e := by ring
          _ = 51305 * 2 ^ e + 32439 * 2 ^ e := by ring
          _ > 51305 * 2 ^ e + 41872 := by omega
      have h_id : 41872 * 2 ^ (e + 1) = 41872 * (2 ^ (e + 1) - 1) + 41872 := by
        have h_sub : 2 ^ (e + 1) = (2 ^ (e + 1) - 1) + 1 := by
          have hpos : 2 ^ (e + 1) ≥ 1 := by
            exact calc
              2 ^ (e + 1) ≥ 2 ^ 0 := Nat.pow_le_pow_right (by norm_num) (Nat.zero_le _)
              _ = 1 := by norm_num
          omega
        rw [h_sub, mul_add]
        simp
      rw [h_id] at h_total
      -- h_total : 41872*(2^(e+1)-1) + 41872 > 51305*2^e + 41872
      -- Cancel 41872
      exact Nat.lt_of_add_lt_add_right h_total
    have h_sigma_t_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
    have h_contra : (41872 * (2 ^ (e + 1) - 1)) * σ t > (51305 * 2 ^ e) * t := by
      calc
        (41872 * (2 ^ (e + 1) - 1)) * σ t ≥ (41872 * (2 ^ (e + 1) - 1)) * t :=
          Nat.mul_le_mul_left (41872 * (2 ^ (e + 1) - 1)) h_sigma_t_ge_t
        _ > (51305 * 2 ^ e) * t := Nat.mul_lt_mul_of_pos_right h_coeff ht_pos
    rw [h_eq] at h_contra
    exact lt_irrefl _ h_contra

'''

content = content[:insert_pos] + descent_41872 + content[insert_pos:]

# Now fill the sorry at "331 ∣ v"
old_sorry_331 = """          · -- 331 ∣ v, need to continue descent through 36631 → 7194483
            sorry"""

new_sorry_331 = """          · -- 331 ∣ v, so v = 331*u, continue descent
            have h331_v : 331 ∣ v := by
              rw [Nat.coprime_iff_gcd_eq_one] at h_cop_331_v
              have hp331 : Nat.Prime 331 := by native_decide
              have hgcd_ne_one : Nat.gcd 331 v ≠ 1 := h_cop_331_v
              have hgcd_dvd_331 : Nat.gcd 331 v ∣ 331 := Nat.gcd_dvd_left 331 v
              have h := hp331.eq_one_or_self_of_dvd (Nat.gcd 331 v) hgcd_dvd_331
              rcases h with (h1 | h331_gcd)
              · exfalso; exact hgcd_ne_one h1
              · have hgcd_dvd_v : Nat.gcd 331 v ∣ v := Nat.gcd_dvd_right 331 v
                rw [h331_gcd] at hgcd_dvd_v
                exact hgcd_dvd_v
            rcases h331_v with ⟨u, hv_eq⟩
            rw [hv_eq] at h_sigma3
            -- σ(331*(331*u)) = 465*(331*u) → σ(331²*u) = 153915*u
            have h_sigma4 : σ (331 ^ 2 * u) = 153915 * u := by
              -- from h_sigma3: σ(331*(331*u)) = 465*(331*u)
              simpa [mul_comm, mul_left_comm, mul_assoc, pow_two] using h_sigma3
            have hu_pos : u > 0 := by
              by_contra! hle
              have hu0 : u = 0 := by omega
              rw [hu0, mul_zero] at hv_eq
              omega
            by_cases h_cop_331_u : Nat.Coprime 331 u
            · -- σ(331²)*σ(u) = 109893*σ(u) = 153915*u → 36631*σ(u) = 51305*u
              have h_cop_331sq_u : Nat.Coprime (331 ^ 2) u := h_cop_331_u.pow_left 2
              have h_mul_sq : σ (331 ^ 2 * u) = σ (331 ^ 2) * σ u := sigma_mul_coprime h_cop_331sq_u
              have h_sigma_331sq : σ (331 ^ 2) = 109893 := by native_decide
              rw [h_mul_sq, h_sigma_331sq] at h_sigma4
              -- 109893 * σ u = 153915 * u → divide by 3: 36631 * σ u = 51305 * u
              have h36631 : 36631 * σ u = 51305 * u := by omega
              have h_cop_36631_51305 : Nat.Coprime 36631 51305 := by native_decide
              have h36631_u : 36631 ∣ u := factor_from_eq 36631 51305 u h_cop_36631_51305 h36631
              rcases h36631_u with ⟨s, hu_eq⟩
              rw [hu_eq] at h36631
              -- 36631*σ(36631*s) = 51305*36631*s → σ(36631*s) = 51305*s
              have h_sigma5 : σ (36631 * s) = 51305 * s := by omega
              have hs_pos : s > 0 := by
                by_contra! hle
                have hs0 : s = 0 := by omega
                rw [hs0, mul_zero] at hu_eq
                omega
              by_cases h_cop_36631_s : Nat.Coprime 36631 s
              · -- σ(36631)*σ(s) = 41872*σ(s) = 51305*s → descent_41872_51305
                have h_mul5 : σ (36631 * s) = σ 36631 * σ s := sigma_mul_coprime h_cop_36631_s
                rw [h_mul5] at h_sigma5
                have h_sigma_36631 : σ 36631 = 41872 := by native_decide
                rw [h_sigma_36631] at h_sigma5
                exfalso; exact descent_41872_51305 s hs_pos (by omega)
              · -- 36631 ∣ s, continue descent (deeper chain, product bound applies)
                sorry
            · -- 331 ∣ u, continue factoring 331
              sorry"""

if old_sorry_331 in content:
    content = content.replace(old_sorry_331, new_sorry_331)
    print("Fixed 331|v sorry")
else:
    print("WARNING: 331|v sorry not found")

with open('/home/mrnob0dy666/MillenniumAnkh/Imscribing/Classical/Solitary10.lean', 'w') as f:
    f.write(content)
