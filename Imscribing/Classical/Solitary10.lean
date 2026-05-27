import Mathlib.Tactic
import Mathlib.Data.Nat.GCD.Basic
import Mathlib.NumberTheory.ArithmeticFunction
open ArithmeticFunction
set_option linter.style.nativeDecide false
namespace Imscribing.Classical.Solitary10
local notation "σ" => ArithmeticFunction.sigma (1 : ℕ)
lemma sigma_one_apply (n : ℕ) : σ n = ∑ d ∈ Nat.divisors n, d := by
  simp [ArithmeticFunction.sigma_apply]
lemma sigma_ge_self (n : ℕ) (hn : n > 0) : σ n ≥ n := by
  rw [sigma_one_apply]
  have h_self : n ∈ Nat.divisors n := Nat.mem_divisors.mpr ⟨dvd_refl n, hn.ne'⟩
  refine Finset.single_le_sum (fun d hd => Nat.zero_le d) h_self
lemma sigma_mul_coprime {a b : ℕ} (h : Nat.Coprime a b) : σ (a * b) = σ a * σ b :=
  (ArithmeticFunction.isMultiplicative_sigma (k := 1)).map_mul_of_coprime h
lemma geom_two (e : ℕ) : (∑ k ∈ Finset.range (e + 1), (2 : ℕ) ^ k) = 2 ^ (e + 1) - 1 := by
  induction' e with k ih
  · norm_num
  · rw [Finset.sum_range_succ, ih, pow_succ]; omega
lemma sigma_two_pow (e : ℕ) : σ (2 ^ e) = 2 ^ (e + 1) - 1 := by
  have hp : Nat.Prime 2 := by native_decide
  rw [ArithmeticFunction.sigma_one_apply_prime_pow hp]
  exact geom_two e
lemma factor_2_pow_odd (n : ℕ) (hn : n > 0) : ∃ (e : ℕ) (u : ℕ), u % 2 = 1 ∧ n = 2 ^ e * u := by
  induction' n using Nat.strong_induction_on with m ih
  by_cases h2m : 2 ∣ m
  · rcases h2m with ⟨t, hm_eq⟩
    have ht_lt_m : t < m := by rw [hm_eq]; by_cases ht0 : t = 0; rw [ht0, mul_zero]; omega; omega
    have ht_pos : t > 0 := by by_contra! hle; have ht0 : t = 0 := by omega; rw [ht0, mul_zero] at hm_eq; omega
    rcases ih t ht_lt_m ht_pos with ⟨e, u, hu, ht_eq⟩
    refine ⟨e + 1, u, hu, ?_⟩
    calc m = 2 * t := hm_eq; _ = 2 * (2 ^ e * u) := by rw [ht_eq]; _ = 2 ^ (e + 1) * u := by ring
  · rcases Nat.mod_two_eq_zero_or_one m with (h | h)
    · exfalso; apply h2m; exact Nat.dvd_of_mod_eq_zero h
    · refine ⟨0, m, h, by simp⟩
lemma coprime_5_9 : Nat.Coprime 5 9 := by native_decide
lemma sigma_25_val : σ 25 = 31 := by native_decide
lemma sigma_5_val : σ 5 = 6 := by native_decide
lemma five_dvd_m (m : ℕ) (h : σ m * 5 = 9 * m) : 5 ∣ m := by
  have h5_9m : 5 ∣ 9 * m := by rw [← h]; exact ⟨σ m, by ring⟩
  exact coprime_5_9.dvd_of_dvd_mul_left h5_9m
lemma factor_from_eq (a q x : ℕ) (hcop : Nat.Coprime a q) (h : a * σ x = q * x) : a ∣ x := by
  have ha_qx : a ∣ q * x := by rw [← h]; exact ⟨σ x, by ring⟩
  exact hcop.dvd_of_dvd_mul_left ha_qx
lemma descent_generic (a b : ℕ) (ha_pos : a > 0) (hb_pos : b > 0)
    (ha_even : a % 2 = 0) (hcop : Nat.Coprime a b) (hineq : a * 3 > b * 2)
    (z : ℕ) (hz : z > 0) (h : a * σ z = b * z) : False := by
  rcases factor_2_pow_odd z hz with ⟨e, t, ht_odd, hz_eq⟩
  rw [hz_eq] at h
  have ht_pos : t > 0 := by by_contra! hle; have ht0 : t = 0 := by omega; rw [ht0, mul_zero] at hz_eq; omega
  have h_cop : Nat.Coprime (2 ^ e) t := by
    have hp2 : Nat.Prime 2 := by native_decide
    have h2t : ¬ 2 ∣ t := by intro h2t; have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2t; rw [ht_odd] at h2t_mod; omega
    have h_cop_2_t : Nat.Coprime 2 t := (Nat.Prime.coprime_iff_not_dvd hp2).mpr h2t
    exact h_cop_2_t.pow_left e
  have h_sigma_mul : σ (2 ^ e * t) = σ (2 ^ e) * σ t := sigma_mul_coprime h_cop
  rw [h_sigma_mul, sigma_two_pow e] at h
  by_cases he0 : e = 0
  · subst he0; simp at hz_eq h
    have ha_t : a ∣ t := factor_from_eq a b t hcop (by omega)
    have h2_t : 2 ∣ t := by have h2_a : 2 ∣ a := Nat.dvd_of_mod_eq_zero ha_even; exact Nat.dvd_trans h2_a ha_t
    have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2_t
    rw [ht_odd] at h2t_mod; omega
  · have he_pos : e ≥ 1 := by omega
    have h_coeff : a * (2 ^ (e + 1) - 1) > b * 2 ^ e := by
      have h_pow_ineq : ∀ (k : ℕ), 1 ≤ k → a * (2 ^ (k + 1) - 1) > b * 2 ^ k := by
        intro k hk
        have hk1 : k = 1 ∨ 2 ≤ k := by omega
        rcases hk1 with (rfl | hk2)
        · simpa using hineq
        · have h_pow_bound : 2 ^ (k + 1) - 1 ≥ 3 * 2 ^ (k - 1) := by
            have h_pow_eq : 2 ^ (k + 1) = 4 * 2 ^ (k - 1) := by
              calc 2 ^ (k + 1) = 2 ^ ((k - 1) + 2) := by rw [Nat.sub_add_cancel (by omega : 1 ≤ k)]
                _ = 2 ^ (k - 1) * 2 ^ 2 := by rw [pow_add]
                _ = 2 ^ (k - 1) * 4 := by norm_num; _ = 4 * 2 ^ (k - 1) := by ring
            rw [h_pow_eq]; omega
          have h_lhs : a * (2 ^ (k + 1) - 1) ≥ a * (3 * 2 ^ (k - 1)) := Nat.mul_le_mul_left a h_pow_bound
          have h_rhs : b * 2 ^ k = (b * 2) * 2 ^ (k - 1) := by
            calc b * 2 ^ k = b * 2 ^ ((k - 1) + 1) := by rw [Nat.sub_add_cancel (by omega : 1 ≤ k)]
              _ = b * (2 ^ (k - 1) * 2) := by rw [pow_succ]; _ = (b * 2) * 2 ^ (k - 1) := by ring
          rw [h_rhs]; have h_ineq : a * (3 * 2 ^ (k - 1)) > (b * 2) * 2 ^ (k - 1) := by nlinarith
          exact lt_of_lt_of_le h_ineq h_lhs
      exact h_pow_ineq e he_pos
    have h_sigma_t_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
    have h_contra : (a * (2 ^ (e + 1) - 1)) * σ t > (b * 2 ^ e) * t := by
      calc (a * (2 ^ (e + 1) - 1)) * σ t ≥ (a * (2 ^ (e + 1) - 1)) * t :=
          Nat.mul_le_mul_left (a * (2 ^ (e + 1) - 1)) h_sigma_t_ge_t
        _ > (b * 2 ^ e) * t := Nat.mul_lt_mul_of_pos_right h_coeff ht_pos
    have h_eq : (a * (2 ^ (e + 1) - 1)) * σ t = (b * 2 ^ e) * t := by
      calc (a * (2 ^ (e + 1) - 1)) * σ t = a * ((2 ^ (e + 1) - 1) * σ t) := by ring
        _ = b * (2 ^ e * t) := h; _ = (b * 2 ^ e) * t := by ring
    rw [h_eq] at h_contra; exact lt_irrefl _ h_contra
lemma coprime_332_465 : Nat.Coprime 332 465 := by native_decide
lemma coprime_41872_51305 : Nat.Coprime 41872 51305 := by native_decide
lemma coprime_52_75 : Nat.Coprime 52 75 := by native_decide
lemma coprime_31_45 : Nat.Coprime 31 45 := by native_decide
lemma sigma_31_val : σ 31 = 32 := by native_decide
lemma sigma_331_val : σ 331 = 332 := by native_decide
lemma sigma_31sq_val : σ (31^2) = 993 := by native_decide
lemma sigma_331sq_val : σ (331^2) = 109893 := by native_decide
lemma sigma_36631_val : σ 36631 = 41872 := by native_decide
lemma sigma_125_val : σ 125 = 156 := by native_decide
lemma sigma_5p5_val : σ (5^5) = 3906 := by native_decide
lemma sigma_781_val : σ 781 = 864 := by native_decide
lemma descent_332_465 (z : ℕ) (hz : z > 0) (h : 332 * σ z = 465 * z) : False :=
  descent_generic 332 465 (by norm_num) (by norm_num) (by norm_num) coprime_332_465 (by norm_num) z hz h
lemma descent_41872_51305 (z : ℕ) (hz : z > 0) (h : 41872 * σ z = 51305 * z) : False :=
  descent_generic 41872 51305 (by norm_num) (by norm_num) (by norm_num) coprime_41872_51305 (by norm_num) z hz h
lemma descent_52_75 (z : ℕ) (hz : z > 0) (h : 52 * σ z = 75 * z) : False :=
  descent_generic 52 75 (by norm_num) (by norm_num) (by norm_num) coprime_52_75 (by norm_num) z hz h
lemma product_bound : 5 * 32 * 332 * 41872 * 10939240 > 9 * 25 * 331 * 36631 * 7194483 := by
  native_decide
lemma sigma_div_mul_ge (a b : ℕ) (ha : a > 0) (hb : b > 0) : σ (a * b) ≥ σ a * b := by
  rw [sigma_one_apply, sigma_one_apply]
  have h_divisors : (Nat.divisors a).image (λ d => d * b) ⊆ Nat.divisors (a * b) := by
    intro x hx; rcases Finset.mem_image.mp hx with ⟨d, hd, rfl⟩
    rw [Nat.mem_divisors]; have hdvd : d ∣ a := Nat.dvd_of_mem_divisors hd
    refine ⟨mul_dvd_mul hdvd (dvd_refl b), mul_pos ha hb |>.ne'⟩
  have h_sum : ∑ d ∈ (Nat.divisors a).image (λ d => d * b), d ≤ ∑ d ∈ Nat.divisors (a * b), d :=
    Finset.sum_le_sum_of_subset h_divisors
  have h_image_sum : ∑ d ∈ (Nat.divisors a).image (λ d => d * b), d = b * ∑ d ∈ Nat.divisors a, d := by
    simp [Finset.mul_sum]
  calc σ (a * b) = ∑ d ∈ Nat.divisors (a * b), d := rfl
    _ ≥ ∑ d ∈ (Nat.divisors a).image (λ d => d * b), d := h_sum
    _ = b * ∑ d ∈ Nat.divisors a, d := h_image_sum
    _ = b * σ a := by rw [sigma_one_apply]
    _ = σ a * b := by ring
lemma descent_32_45 (z : ℕ) (hz : z > 0) (h : 32 * σ z = 45 * z) : False := by
  rcases factor_2_pow_odd z hz with ⟨a, t, ht_odd, hz_eq⟩
  rw [hz_eq] at h
  have ht_pos : t > 0 := by by_contra! hle; have ht0 : t = 0 := by omega; rw [ht0, mul_zero] at hz_eq; omega
  have h_cop : Nat.Coprime (2 ^ a) t := by
    have hp2 : Nat.Prime 2 := by norm_num
    have h2t : ¬ 2 ∣ t := by intro h2t; have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2t; rw [ht_odd] at h2t_mod; omega
    have h_cop_2_t : Nat.Coprime 2 t := (Nat.Prime.coprime_iff_not_dvd hp2).mpr h2t
    exact h_cop_2_t.pow_left a
  have h_sigma_mul : σ (2 ^ a * t) = σ (2 ^ a) * σ t := sigma_mul_coprime h_cop
  rw [h_sigma_mul, sigma_two_pow a] at h
  by_cases ha0 : a = 0
  · subst ha0; simp at hz_eq h
    have h32_t : 32 ∣ t := factor_from_eq 32 45 t (by native_decide : Nat.Coprime 32 45) h
    have h2_t : 2 ∣ t := Nat.dvd_trans (by norm_num : 2 ∣ 32) h32_t
    have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2_t
    rw [ht_odd] at h2t_mod; omega
  · have ha_pos : a ≥ 1 := by omega
    have h_coeff : 32 * (2 ^ (a + 1) - 1) > 45 * 2 ^ a := by
      have hX_ge_2 : 2 ^ a ≥ 2 := by
        calc 2 ^ a ≥ 2 ^ 1 := Nat.pow_le_pow_right (by norm_num) ha_pos; _ = 2 := by norm_num
      have h_19X_ge_38 : 19 * 2 ^ a ≥ 38 := Nat.mul_le_mul_left 19 hX_ge_2
      have h_19X_ge_33 : 19 * 2 ^ a ≥ 33 := by omega
      have h_64X_ge : 64 * 2 ^ a ≥ 45 * 2 ^ a + 33 := by
        have h_eq : 64 * 2 ^ a = 45 * 2 ^ a + 19 * 2 ^ a := by ring; rw [h_eq]; omega
      have h_eq' : 32 * (2 ^ (a + 1) - 1) + 32 = 64 * 2 ^ a := by
        rw [pow_succ]; have hpos : 2 * 2 ^ a ≥ 1 := by have h := pow_pos (by norm_num : 0 < 2) a; omega; omega
      rw [← h_eq'] at h_64X_ge; omega
    have h_eq : (32 * (2 ^ (a + 1) - 1)) * σ t = (45 * 2 ^ a) * t := by
      calc (32 * (2 ^ (a + 1) - 1)) * σ t = 32 * ((2 ^ (a + 1) - 1) * σ t) := by ring
        _ = 45 * (2 ^ a * t) := h; _ = (45 * 2 ^ a) * t := by ring
    have h_sigma_t_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
    have h_contra : (32 * (2 ^ (a + 1) - 1)) * σ t > (45 * 2 ^ a) * t := by
      calc (32 * (2 ^ (a + 1) - 1)) * σ t ≥ (32 * (2 ^ (a + 1) - 1)) * t :=
          Nat.mul_le_mul_left (32 * (2 ^ (a + 1) - 1)) h_sigma_t_ge_t
        _ > (45 * 2 ^ a) * t := Nat.mul_lt_mul_of_pos_right h_coeff ht_pos
    rw [h_eq] at h_contra; exact lt_irrefl _ h_contra
lemma descent_331_chain (w : ℕ) (hw : w > 0) (h : 331 * σ w = 465 * w) : False := by
  by_cases h_cop_331_w : Nat.Coprime 331 w
  · have h_cop_331_465 : Nat.Coprime 331 465 := by
      have hp331 : Nat.Prime 331 := by native_decide
      exact (hp331.coprime_iff_not_dvd).mpr (by native_decide)
    have h331_w : 331 ∣ w := factor_from_eq 331 465 w h_cop_331_465 h
    rw [Nat.coprime_iff_gcd_eq_one] at h_cop_331_w
    have h_gcd1 : Nat.gcd 331 w = 1 := h_cop_331_w
    have h331_gcd : 331 ∣ Nat.gcd 331 w := Nat.dvd_gcd (dvd_refl 331) h331_w
    rw [h_gcd1] at h331_gcd
    have : 331 ∣ 1 := h331_gcd
    have : 331 ≤ 1 := Nat.le_of_dvd (by norm_num) this; omega

lemma coprime_332_465 : Nat.Coprime 332 465 := by native_decide
lemma coprime_41872_51305 : Nat.Coprime 41872 51305 := by native_decide
lemma coprime_52_75 : Nat.Coprime 52 75 := by native_decide
lemma coprime_31_45 : Nat.Coprime 31 45 := by native_decide
lemma sigma_31_val : σ 31 = 32 := by native_decide
lemma sigma_331_val : σ 331 = 332 := by native_decide
lemma sigma_31sq_val : σ (31^2) = 993 := by native_decide
lemma sigma_331sq_val : σ (331^2) = 109893 := by native_decide
lemma sigma_36631_val : σ 36631 = 41872 := by native_decide
lemma sigma_125_val : σ 125 = 156 := by native_decide
lemma sigma_5p5_val : σ (5^5) = 3906 := by native_decide
lemma sigma_781_val : σ 781 = 864 := by native_decide
lemma descent_332_465 (z : ℕ) (hz : z > 0) (h : 332 * σ z = 465 * z) : False :=
  descent_generic 332 465 (by norm_num) (by norm_num) (by norm_num) coprime_332_465 (by norm_num) z hz h
lemma descent_41872_51305 (z : ℕ) (hz : z > 0) (h : 41872 * σ z = 51305 * z) : False :=
  descent_generic 41872 51305 (by norm_num) (by norm_num) (by norm_num) coprime_41872_51305 (by norm_num) z hz h
lemma descent_52_75 (z : ℕ) (hz : z > 0) (h : 52 * σ z = 75 * z) : False :=
  descent_generic 52 75 (by norm_num) (by norm_num) (by norm_num) coprime_52_75 (by norm_num) z hz h
lemma product_bound : 5 * 32 * 332 * 41872 * 10939240 > 9 * 25 * 331 * 36631 * 7194483 := by
  native_decide
lemma sigma_div_mul_ge (a b : ℕ) (ha : a > 0) (hb : b > 0) : σ (a * b) ≥ σ a * b := by
  rw [sigma_one_apply, sigma_one_apply]
  have h_divisors : (Nat.divisors a).image (λ d => d * b) ⊆ Nat.divisors (a * b) := by
    intro x hx; rcases Finset.mem_image.mp hx with ⟨d, hd, rfl⟩
    rw [Nat.mem_divisors]; have hdvd : d ∣ a := Nat.dvd_of_mem_divisors hd
    refine ⟨mul_dvd_mul hdvd (dvd_refl b), mul_pos ha hb |>.ne'⟩
  have h_sum : ∑ d ∈ (Nat.divisors a).image (λ d => d * b), d ≤ ∑ d ∈ Nat.divisors (a * b), d :=
    Finset.sum_le_sum_of_subset h_divisors
  have h_image_sum : ∑ d ∈ (Nat.divisors a).image (λ d => d * b), d = b * ∑ d ∈ Nat.divisors a, d := by
    simp [Finset.mul_sum]
  calc σ (a * b) = ∑ d ∈ Nat.divisors (a * b), d := rfl
    _ ≥ ∑ d ∈ (Nat.divisors a).image (λ d => d * b), d := h_sum
    _ = b * ∑ d ∈ Nat.divisors a, d := h_image_sum
    _ = b * σ a := by rw [sigma_one_apply]
    _ = σ a * b := by ring
