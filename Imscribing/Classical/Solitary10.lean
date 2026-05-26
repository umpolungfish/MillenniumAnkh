import Mathlib.Tactic
import Mathlib.Data.Nat.GCD.Basic
import Mathlib.NumberTheory.ArithmeticFunction
open ArithmeticFunction

namespace Imscribing.Classical.Solitary10

local notation "σ" => ArithmeticFunction.sigma (1 : ℕ)

lemma sigma_apply (n : ℕ) : σ n = ∑ d ∈ divisors n, d := by
  simp [ArithmeticFunction.sigma_apply]

lemma sigma_ge_self (n : ℕ) (hn : n > 0) : σ n ≥ n := by
  rw [sigma_apply]
  have h_self : n ∈ divisors n := Nat.mem_divisors.mpr ⟨dvd_refl n, hn.ne'⟩
  exact Finset.single_le_sum_of_mem (fun d => Nat.zero_le d) h_self

lemma sigma_mul_coprime {a b : ℕ} (h : Coprime a b) : σ (a * b) = σ a * σ b :=
  (isMultiplicative_sigma (k := 1)).map_mul_of_coprime h

lemma sigma_ge_sigma_d_times_m_div_d (d m : ℕ) (hd : d ∣ m) (hd_pos : d > 0) : σ m ≥ σ d * (m / d) := by
  have hm_pos : m > 0 := Nat.pos_of_dvd_of_pos hd hd_pos
  have hm_div_d_pos : m / d > 0 := by
    have hm_ge_d : m ≥ d := Nat.le_of_dvd hm_pos hd
    exact Nat.div_pos hm_ge_d hd_pos
  have hsubset : (divisors d).image (λ δ => δ * (m / d)) ⊆ divisors m := by
    intro x hx
    rcases Finset.mem_image.mp hx with ⟨δ, hδ, rfl⟩
    have hδ_dvd : δ ∣ d := (Nat.mem_divisors.mp hδ).1
    have hx_dvd_m : δ * (m / d) ∣ m := by
      have : d * (m / d) = m := Nat.mul_div_cancel' hd
      calc δ * (m / d) ∣ d * (m / d) := mul_dvd_mul_right (m / d) hδ_dvd; _ = m := this
    refine Nat.mem_divisors.mpr ⟨hx_dvd_m, ?_⟩
    have hpos : δ * (m / d) > 0 := mul_pos (Nat.pos_of_mem_divisors hδ) hm_div_d_pos
    exact hpos.ne'
  have hinj : ∀ x y, x ∈ divisors d → y ∈ divisors d → x * (m / d) = y * (m / d) → x = y := by
    intro x y hx hy h; apply mul_right_cancel₀ hm_div_d_pos.ne' h
  have hsum_image : ∑ x ∈ (divisors d).image (λ δ => δ * (m / d)), x = σ d * (m / d) := by
    calc
      ∑ x ∈ (divisors d).image (λ δ => δ * (m / d)), x = ∑ δ ∈ divisors d, (δ * (m / d)) :=
        Finset.sum_image hinj
      _ = (∑ δ ∈ divisors d, δ) * (m / d) := by rw [Finset.sum_mul]
      _ = σ d * (m / d) := by rw [sigma_apply]
  have hsum_le : ∑ x ∈ (divisors d).image (λ δ => δ * (m / d)), x ≤ σ m := by
    calc
      ∑ x ∈ (divisors d).image (λ δ => δ * (m / d)), x ≤ ∑ x ∈ divisors m, x :=
        Finset.sum_le_sum_of_subset hsubset
      _ = σ m := by rw [sigma_apply]
  rw [hsum_image] at hsum_le; exact hsum_le

lemma coprime_five_nine : Coprime 5 9 := by native_decide
lemma coprime_two_three : Coprime 2 3 := by native_decide
lemma coprime_31_45 : Coprime 31 45 := by native_decide
lemma coprime_32_45 : Coprime 32 45 := by native_decide

lemma five_dvd_m (m : ℕ) (hm : m > 0) (h : σ m * 5 = 9 * m) : 5 ∣ m := by
  have h5_9m : 5 ∣ 9 * m := by rw [← h]; exact ⟨σ m, by ring⟩
  exact coprime_five_nine.dvd_of_dvd_mul_left h5_9m

lemma sigma_small : σ 5 = 6 := by native_decide
lemma sigma_25_val : σ 25 = 31 := by native_decide
lemma sigma_125_val : σ 125 = 156 := by native_decide
lemma sigma_6500_gt : σ 6500 * 5 > 9 * 6500 := by native_decide
lemma sigma_24800_gt : σ 24800 * 5 > 9 * 24800 := by native_decide
lemma sigma_2640155300_gt : σ 2640155300 * 5 > 9 * 2640155300 := by native_decide

lemma coprime_52_75 : Coprime 52 75 := by native_decide
lemma coprime_10261_14415 : Coprime 10261 14415 := by native_decide

theorem ten_is_solitary (m : ℕ) (hm : m > 0) (h : σ m * 5 = 9 * m) : m = 10 := by
  by_cases h25m : 25 ∣ m
  · -- Case B: 25|m
    by_cases h125m : 125 ∣ m
    · -- Subcase B2: 125|m (so v₅(m) ≥ 3)
      rcases h125m with ⟨u, hm_eq⟩
      have hu_pos : u > 0 := by
        by_contra! hz; rw [hz, mul_zero] at hm_eq; omega
      have h5u : ¬ 5 ∣ u := by
        intro h; have : 625 ∣ m := by
          rcases h with ⟨t, hu_eq⟩; rw [hu_eq] at hm_eq; exact ⟨5*t, by ring⟩
        have : 625 ∣ 125 := by exact ?_ -- impossible, contradiction
        sorry
      sorry
    · -- Subcase B1: 25∥m (v₅(m) = 2 exactly)
      rcases h25m with ⟨u, hm_eq⟩
      have hu_pos : u > 0 := by
        by_contra! hz; rw [hz, mul_zero] at hm_eq; omega
      have h5u : ¬ 5 ∣ u := by
        intro h; apply h125m; rcases h with ⟨t, hu_eq⟩
        rw [hu_eq] at hm_eq; exact ⟨5*t, by ring⟩
      rw [hm_eq] at h
      have h_sigma : σ (25 * u) = 9 * u := by omega
      have h_cop_25_u : Coprime 25 u := by
        have hp5 : Nat.Prime 5 := by native_decide
        have h5u_cop : Coprime 5 u := (Nat.Prime.coprime_iff_not_dvd hp5).mpr h5u
        exact Nat.Coprime.pow_left 2 h5u_cop
      have h_mul25 : σ (25 * u) = σ 25 * σ u := sigma_mul_coprime h_cop_25_u
      rw [h_mul25, sigma_25_val] at h_sigma
      have h_31su_45u : 31 * σ u = 45 * u := by omega
      have h31u : 31 ∣ u := by
        have h31_45u : 31 ∣ 45 * u := by
          rw [← h_31su_45u]; exact ⟨σ u, by ring⟩
        exact coprime_31_45.dvd_of_dvd_mul_left h31_45u
      rcases h31u with ⟨v, hu_eq⟩
      rw [hu_eq] at hm_eq h_sigma
      have hv_pos : v > 0 := by
        by_contra! hz; rw [hz, mul_zero] at hu_eq; rw [hu_eq] at hm_eq; omega
      by_cases h31v : 31 ∣ v
      · -- 31²|u → use N = 2640155300
        rcases h31v with ⟨w, hv_eq⟩
        rw [hv_eq] at hm_eq h_sigma
        have hw_pos : w > 0 := by
          by_contra! hz; rw [hz, mul_zero] at hv_eq; rw [hv_eq] at hm_eq; omega
        have h_cop_31sq_w : Coprime 31 w := by
          have hp31 : Nat.Prime 31 := by native_decide
          have h31w : ¬ 31 ∣ w := by
            intro h; have : 31^3 ∣ u := by
              rw [hu_eq, hv_eq]; exact ⟨31*w, by ring⟩
            -- This would mean 31^3|u, which is fine, but we only need 31∤w
            -- Actually, we should extract ALL 31-powers
            sorry
          exact (Nat.Prime.coprime_iff_not_dvd hp31).mpr h31w
        sorry
      · -- 31∥u → use N = 24800
        have h_cop_775_v : Coprime 775 v := by
          have hp5 : Nat.Prime 5 := by native_decide
          have hp31 : Nat.Prime 31 := by native_decide
          have h5v : ¬ 5 ∣ v := by
            intro h5v; apply h5u; rw [hu_eq]; exact mul_dvd_mul_left 31 h5v
          have h_cop5 : Coprime 5 v := (Nat.Prime.coprime_iff_not_dvd hp5).mpr h5v
          have h_cop31 : Coprime 31 v := (Nat.Prime.coprime_iff_not_dvd hp31).mpr h31v
          have h_cop25 : Coprime 25 v := Nat.Coprime.pow_left 2 h_cop5
          exact h_cop25.mul h_cop31
        have h_mul775 : σ (775 * v) = σ 775 * σ v := sigma_mul_coprime h_cop_775_v
        have sigma775 : σ 775 = 992 := by native_decide
        rw [hm_eq, show 775 * v = 775 * v by rfl] at h
        omit
        sorry
  · -- Case A: 25∤m
    have h5m : 5 ∣ m := five_dvd_m m hm h
    rcases h5m with ⟨k, hm_eq⟩
    have hk_pos : k > 0 := by
      by_contra! hz; rw [hz, mul_zero] at hm_eq; omega
    have h5k : ¬ 5 ∣ k := by
      intro h; apply h25m; rcases h with ⟨t, hk_eq⟩; rw [hk_eq] at hm_eq
      exact ⟨5*t, by ring⟩
    rw [hm_eq] at h
    have h_sk : σ (5 * k) = 9 * k := by omega
    have h_cop : Coprime 5 k := by
      have hp5 : Nat.Prime 5 := by native_decide
      exact (Nat.Prime.coprime_iff_not_dvd hp5).mpr h5k
    have h_mul : σ (5 * k) = σ 5 * σ k := sigma_mul_coprime h_cop
    rw [h_mul, sigma_small] at h_sk
    -- 6·σ(k) = 9·k → 2·σ(k) = 3·k
    sorry
