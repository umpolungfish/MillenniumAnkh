import Mathlib.Tactic
import Mathlib.NumberTheory.ArithmeticFunction.Defs
import Mathlib.NumberTheory.ArithmeticFunction.Misc
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Algebra.Ring.GeomSum

open Nat ArithmeticFunction

namespace Imscribing.Classical.OPN

def Perfect (n : ℕ) : Prop := sigma 1 n = 2 * n

private lemma geom_sum_mod2 (q n : ℕ) (hq : q % 2 = 1) :
    (∑ i ∈ Finset.range n, q ^ i) % 2 = n % 2 := by
  induction n with
  | zero => simp
  | succ k ih =>
    rw [Finset.sum_range_succ, Nat.add_mod]
    have h_pow_odd : q ^ k % 2 = 1 := by
      induction k with
      | zero => simp
      | succ k ih' =>
        rw [pow_succ, Nat.mul_mod, hq, ih']
        norm_num
    rw [h_pow_odd, ih]
    simp
