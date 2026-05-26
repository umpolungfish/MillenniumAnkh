-- Key lemmas needed to complete the proof

lemma sigma_prime (p : ℕ) (hp : Nat.Prime p) : σ p = p + 1 := by
  rw [sigma_one_apply, Nat.divisors_prime hp, Finset.sum_insert, Finset.sum_singleton]
  simp

lemma coprime_of_not_dvd_prime {p n : ℕ} (hp : Nat.Prime p) (hpn : ¬ p ∣ n) : Coprime p n :=
  (Nat.Prime.coprime_iff_not_dvd hp).mpr hpn

-- The product bound inequality
lemma product_bound_ineq : 32*332*41872*10939240*5 > 9*25*331*36631*7194483 := by
  native_decide

-- sigma(31^2) = 993, sigma(331^2) = 109893, sigma(36631^2) = 1561202811
-- These are computed with native_decide
lemma sigma_31sq : σ (31^2) = 993 := by native_decide
lemma sigma_331sq : σ (331^2) = 109893 := by native_decide
lemma sigma_36631sq : σ (36631^2) = 1561202811 := by native_decide

-- gcd values
lemma gcd_3_109893_153915 : 109893 / 3 = 36631 ∧ 153915 / 3 = 51305 := by
  native_decide

lemma gcd_217_1561202811_1879353455 : 1561202811 / 217 = 7194483 ∧ 1879353455 / 217 = 8660615 := by
  native_decide

-- Coprime lemmas
lemma coprime_36631_51305 : Coprime 36631 51305 := by native_decide
lemma coprime_7194483_8660615 : Coprime 7194483 8660615 := by native_decide
lemma coprime_7_5233 : Coprime 7 5233 := by native_decide
lemma coprime_7_x_if_not_dvd (x : ℕ) (h7x : ¬ 7 ∣ x) : Coprime 7 x := by
  have hp7 : Nat.Prime 7 := by native_decide
  exact (Nat.Prime.coprime_iff_not_dvd hp7).mpr h7x
lemma coprime_5233_x_if_not_dvd (x : ℕ) (h5233x : ¬ 5233 ∣ x) : Coprime 5233 x := by
  have hp5233 : Nat.Prime 5233 := by native_decide
  exact (Nat.Prime.coprime_iff_not_dvd hp5233).mpr h5233x
lemma coprime_36631_x_if_not_dvd (x : ℕ) (h36631x : ¬ 36631 ∣ x) : Coprime 36631 x := by
  have h_36631_factor : 36631 = 7 * 5233 := by native_decide
  rw [h_36631_factor]
  have h7x : ¬ 7 ∣ x := by
    intro h; apply h36631x; rw [h_36631_factor]; exact dvd_mul_of_dvd_left h 5233
  have h5233x : ¬ 5233 ∣ x := by
    intro h; apply h36631x; rw [h_36631_factor]; exact dvd_mul_of_dvd_right h 7
  have h_cop7 : Coprime 7 x := coprime_7_x_if_not_dvd x h7x
  have h_cop5233 : Coprime 5233 x := coprime_5233_x_if_not_dvd x h5233x
  have hx_cop7 : Coprime x 7 := h_cop7.symm
  have hx_cop5233 : Coprime x 5233 := h_cop5233.symm
  have hx_cop_prod : Coprime x (7 * 5233) := hx_cop7.mul hx_cop5233
  exact hx_cop_prod.symm
