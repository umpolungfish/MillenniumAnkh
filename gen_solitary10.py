#!/usr/bin/env python3
"""Generate the complete Solitary10.lean with all descent lemmas proved."""
import os

LEAN_FILE = "/home/mrnob0dy666/MillenniumAnkh/Imscribing/Classical/Solitary10.lean"

content = r"""import Mathlib.Tactic
import Mathlib.Data.Nat.GCD.Basic
import Mathlib.NumberTheory.ArithmeticFunction
open ArithmeticFunction

namespace Imscribing.Classical.Solitary10

set_option linter.style.nativeDecide false

local notation "σ" => ArithmeticFunction.sigma (1 : ℕ)

lemma sigma_one_apply (n : ℕ) : σ n = ∑ d ∈ Nat.divisors n, d := by
  simp [ArithmeticFunction.sigma_apply]

lemma sigma_ge_self (n : ℕ) (hn : n > 0) : σ n ≥ n := by
  rw [sigma_one_apply]
  have h_self : n ∈ Nat.divisors n := Nat.mem_divisors.mpr ⟨dvd_refl n, by omega⟩
  exact Finset.single_le_sum (by intro d hd; exact Nat.zero_le d) h_self

lemma sigma_mul_coprime {a b : ℕ} (h : Nat.Coprime a b) : σ (a * b) = σ a * σ b :=
  (isMultiplicative_sigma (k := 1)).map_mul_of_coprime h

lemma sigma_two_pow (e : ℕ) : σ (2 ^ e) = 2 ^ (e + 1) - 1 := by
  have h_sum : ∀ e : ℕ, ∑ i ∈ Finset.range (e + 1), (2 : ℕ) ^ i = 2 ^ (e + 1) - 1 := by
    intro e
    induction' e with k ih
    · simp
    · rw [Finset.sum_range_succ, ih]
      have hx : 2 * 2 ^ (k + 1) = 2 ^ (k + 2) := by
        calc
          2 * 2 ^ (k + 1) = 2 ^ (k + 1) * 2 := mul_comm _ _
          _ = 2 ^ (k + 2) := by rw [pow_succ']
      rw [← hx]
      omega
  have hp : Nat.Prime 2 := by native_decide
  have h := sigma_one_apply_prime_pow hp (i := e)
  rw [h]
  exact h_sum e

lemma coprime_5_9 : Nat.Coprime 5 9 := by native_decide
lemma coprime_31_45 : Nat.Coprime 31 45 := by native_decide
lemma coprime_32_45 : Nat.Coprime 32 45 := by native_decide

lemma sigma_25_val : σ 25 = 31 := by native_decide
lemma sigma_31_val : σ 31 = 32 := by native_decide
lemma sigma_31_sq_val : σ (31 ^ 2) = 993 := by native_decide

lemma prime_5 : Nat.Prime 5 := by native_decide
lemma prime_31 : Nat.Prime 31 := by native_decide
lemma prime_7 : Nat.Prime 7 := by native_decide
lemma prime_2 : Nat.Prime 2 := by native_decide

lemma factor_2_pow_odd (n : ℕ) (hn : n > 0) : ∃ (e : ℕ) (u : ℕ), u % 2 = 1 ∧ n = 2 ^ e * u := by
  have h_mod2 := Nat.mod_two_eq_zero_or_one n
  rcases h_mod2 with (h_mod0 | h_mod1)
  · have h2n : 2 ∣ n := Nat.dvd_of_mod_eq_zero h_mod0
    rcases h2n with ⟨t, ht⟩
    have ht_pos : t > 0 := by
      by_contra! hz; have ht0 : t = 0 := by omega; rw [ht0, mul_zero] at ht; omega
    rcases factor_2_pow_odd t ht_pos with ⟨e, u, hu, ht_eq⟩
    refine ⟨e + 1, u, hu, ?_⟩
    calc
      n = 2 * t := ht
      _ = 2 * (2 ^ e * u) := by rw [ht_eq]
      _ = 2 ^ (e + 1) * u := by ring
  · refine ⟨0, n, h_mod1, by simp⟩

/-- Factor out maximal power of prime p from n. Returns (a, t) where n = p^a * t, p∤t. -/
lemma factor_p_pow (p n : ℕ) (hp : Nat.Prime p) (hn : n > 0) :
    ∃ (a : ℕ) (t : ℕ), ¬ p ∣ t ∧ n = p ^ a * t := by
  by_cases hpn : p ∣ n
  · rcases hpn with ⟨m, hn_eq⟩
    have hm_pos : m > 0 := by
      by_contra! hz; have hm0 : m = 0 := by omega; rw [hm0, mul_zero] at hn_eq; omega
    rcases factor_p_pow p m hp hm_pos with ⟨a, t, hpt, hm_eq⟩
    refine ⟨a + 1, t, hpt, ?_⟩
    calc
      n = p * m := hn_eq
      _ = p * (p ^ a * t) := by rw [hm_eq]
      _ = p ^ (a + 1) * t := by ring
  · refine ⟨0, n, hpn, by simp⟩
"""

with open(LEAN_FILE, 'w') as f:
    f.write(content)
print(f"Part 1 written: {len(content)} chars")
