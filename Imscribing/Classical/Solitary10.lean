import Mathlib.Tactic
import Mathlib.Data.Nat.GCD.Basic
import Mathlib.NumberTheory.ArithmeticFunction.Defs
import Mathlib.NumberTheory.ArithmeticFunction.Misc
import Mathlib.NumberTheory.ArithmeticFunction.Moebius
import Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt
import Mathlib.NumberTheory.ArithmeticFunction.Zeta

open ArithmeticFunction

set_option linter.style.nativeDecide false
set_option linter.style.induction false
set_option linter.style.whitespace false
set_option linter.style.longLine false

namespace Imscribing.Classical.Solitary10

local notation "σ" => ArithmeticFunction.sigma (1 : ℕ)

lemma sigma_one_apply (n : ℕ) : σ n = ∑ d ∈ Nat.divisors n, d := by
  simp [ArithmeticFunction.sigma_apply]

lemma sigma_ge_self (n : ℕ) (hn : n > 0) : σ n ≥ n := by
  rw [sigma_one_apply]
  have h_self : n ∈ Nat.divisors n := Nat.mem_divisors.mpr ⟨dvd_refl n, hn.ne'⟩
  refine Finset.single_le_sum (fun d _ => Nat.zero_le d) h_self

lemma sigma_mul_coprime {a b : ℕ} (h : Nat.Coprime a b) : σ (a * b) = σ a * σ b :=
  (ArithmeticFunction.isMultiplicative_sigma (k := 1)).map_mul_of_coprime h

lemma geom_two (e : ℕ) : (∑ k ∈ Finset.range (e + 1), (2 : ℕ) ^ k) = 2 ^ (e + 1) - 1 := by
  induction e with
  | zero => norm_num
  | succ k ih =>
    rw [Finset.sum_range_succ, ih, pow_succ]
    omega

lemma sigma_two_pow (e : ℕ) : σ (2 ^ e) = 2 ^ (e + 1) - 1 := by
  have hp : Nat.Prime 2 := by native_decide
  rw [ArithmeticFunction.sigma_one_apply_prime_pow hp]
  exact geom_two e

lemma factor_2_pow_odd (n : ℕ) (hn : n > 0) : ∃ (e : ℕ) (u : ℕ), u % 2 = 1 ∧ n = 2 ^ e * u := by
  induction n using Nat.strong_induction_on with
  | h m ih =>
    by_cases h2m : 2 ∣ m
    · rcases h2m with ⟨t, hm_eq⟩
      have ht_pos : t > 0 := by subst hm_eq; omega
      have ht_lt_m : t < m := by subst hm_eq; omega
      rcases ih t ht_lt_m ht_pos with ⟨e, u, hu, ht_eq⟩
      refine ⟨e + 1, u, hu, ?_⟩
      rw [hm_eq, ht_eq, pow_succ]
      ring
    · refine ⟨0, m, ?_, by simp⟩
      rcases Nat.mod_two_eq_zero_or_one m with (h | h)
      · exfalso; apply h2m; exact Nat.dvd_of_mod_eq_zero h
      · exact h

lemma factor_from_eq (a q x : ℕ) (hcop : Nat.Coprime a q) (h : a * σ x = q * x) : a ∣ x := by
  have ha_qx : a ∣ q * x := by rw [← h]; apply dvd_mul_right
  have : a ∣ x * q := by rwa [mul_comm]
  exact hcop.dvd_of_dvd_mul_right this

lemma coeff_ineq_pow {a b : ℕ} (ha : a > 0) (hineq : a * 3 > b * 2) (e : ℕ) (he : e ≥ 1) : a * (2 ^ (e + 1) - 1) > b * 2 ^ e := by
  induction e, he using Nat.le_induction with
  | base =>
    calc a * (2 ^ (1 + 1) - 1) = a * 3 := by norm_num
      _ > b * 2 := hineq
      _ = b * 2 ^ 1 := by norm_num
  | succ k _ ih =>
    have h_pow_step : 2 ^ (k + 2) - 1 = 2 * (2 ^ (k + 1) - 1) + 1 := by
      have h1 : 1 ≤ 2 ^ (k + 1) := Nat.one_le_two_pow
      rw [pow_succ]; omega
    calc a * (2 ^ (k + 2) - 1) = a * (2 * (2 ^ (k + 1) - 1) + 1) := by rw [h_pow_step]
      _ = 2 * (a * (2 ^ (k + 1) - 1)) + a := by ring
      _ > 2 * (b * 2 ^ k) + a := by
        have h_mul : 2 * (a * (2 ^ (k + 1) - 1)) > 2 * (b * 2 ^ k) := Nat.mul_lt_mul_of_pos_left ih (by norm_num)
        exact Nat.add_lt_add_right h_mul a
      _ = b * 2 ^ (k + 1) + a := by ring
      _ > b * 2 ^ (k + 1) := by apply Nat.lt_add_of_pos_right; exact ha

lemma descent_generic (a b : ℕ) (ha_pos : a > 0) (ha_even : a % 2 = 0) (hcop : Nat.Coprime a b)
    (hineq : a * 3 > b * 2) (z : ℕ) (hz : z > 0) (h : a * σ z = b * z) : False := by
  rcases factor_2_pow_odd z hz with ⟨e, t, ht_odd, hz_eq⟩
  have ht_pos : t > 0 := by
    subst hz_eq
    exact Nat.pos_of_ne_zero (fun ht0 => by simp [ht0] at hz)
  have h_cop : Nat.Coprime (2 ^ e) t := by
    have hp2 : Nat.Prime 2 := by native_decide
    have h2t : ¬ 2 ∣ t := by intro h2t; have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2t; rw [ht_odd] at h2t_mod; omega
    have h_cop_2_t : Nat.Coprime 2 t := (Nat.Prime.coprime_iff_not_dvd hp2).mpr h2t
    exact h_cop_2_t.pow_left e
  have h_sigma_mul : σ (2 ^ e * t) = σ (2 ^ e) * σ t := sigma_mul_coprime h_cop
  rw [hz_eq, h_sigma_mul, sigma_two_pow e] at h
  by_cases he0 : e = 0
  · subst he0
    simp only [pow_zero, zero_add, pow_one, Nat.reduceSub, one_mul] at h
    have ha_t : a ∣ t := factor_from_eq a b t hcop h
    have h2_a : 2 ∣ a := Nat.dvd_of_mod_eq_zero ha_even
    have h2_t : 2 ∣ t := Nat.dvd_trans h2_a ha_t
    have h2t_mod : t % 2 = 0 := Nat.mod_eq_zero_of_dvd h2_t
    rw [ht_odd] at h2t_mod
    omega
  · have he_pos : e ≥ 1 := by omega
    have h_coeff : a * (2 ^ (e + 1) - 1) > b * 2 ^ e := coeff_ineq_pow ha_pos hineq e he_pos
    have h_sigma_t_ge_t : σ t ≥ t := sigma_ge_self t ht_pos
    have h_contra : a * (2 ^ (e + 1) - 1) * σ t > b * 2 ^ e * t := by
      calc a * (2 ^ (e + 1) - 1) * σ t ≥ a * (2 ^ (e + 1) - 1) * t :=
          Nat.mul_le_mul_left (a * (2 ^ (e + 1) - 1)) h_sigma_t_ge_t
        _ > (b * 2 ^ e) * t := Nat.mul_lt_mul_of_pos_right h_coeff ht_pos
    have h_eq : a * (2 ^ (e + 1) - 1) * σ t = b * 2 ^ e * t := by
      calc a * (2 ^ (e + 1) - 1) * σ t = a * ((2 ^ (e + 1) - 1) * σ t) := by ring
        _ = b * (2 ^ e * t) := h
        _ = b * 2 ^ e * t := by ring
    rw [h_eq] at h_contra
    exact lt_irrefl _ h_contra

lemma descent_332_465 (z : ℕ) (hz : z > 0) (h : 332 * σ z = 465 * z) : False :=
  descent_generic 332 465 (by norm_num) (by norm_num) (by native_decide) (by norm_num) z hz h

end Solitary10
end Classical
end Imscribing
