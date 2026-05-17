-- Imscribing/Millennium/IGBarrierAnalysis.lean
-- Cross-pollination: IGMorphism protocols × Millennium barriers.

import Imscribing.IGMorphism
import Imscribing.Millennium.Barriers
import Imscribing.Millennium.BarrierFrobenius

namespace Millennium.IGBarrierAnalysis

open Imscribing
open Imscribing.Primitives
open Millennium.Barriers
open Millennium.BarrierFrobenius
open Millennium.Frobenius

theorem ym_not_eq_open_problem :
    millenniumBarrier .YM ≠ millenniumBarrier .RH := by
  simp [millenniumBarrier]

theorem odotOperator_is_O_inf :
    imscriptionTier odotOperator = .O_inf := by
  rfl

def barrierLiftDepth : MillenniumProblem → ℕ
  | .RH    => 1
  | .Hodge => 1
  | .PvsNP => 1
  | .NS    => 1
  | .YM    => 2
  | .BSD   => 2
  | .OPN   => 2

theorem barrierLiftDepth_eq_sorryDepth :
    ∀ p : MillenniumProblem, barrierLiftDepth p = sorryDepth p := by
  intro p; cases p <;> simp [barrierLiftDepth, sorryDepth]

def analysisBarrier : MillenniumProblem → Prop
  | .RH | .Hodge | .NS | .YM => true
  | _ => false

def arithmeticBarrier : MillenniumProblem → Prop
  | .PvsNP | .BSD | .OPN => true
  | _ => false

theorem analysis_is_full_frobenius :
    ∀ p : MillenniumProblem,
      analysisBarrier p → problemFrobenius p = .full := by
  intro p hp; cases p <;> simp [analysisBarrier, problemFrobenius] <;> trivial

theorem arithmetic_is_algebraOnly :
    ∀ p : MillenniumProblem,
      arithmeticBarrier p → problemFrobenius p = .algebraOnly := by
  intro p hp; cases p <;> simp [arithmeticBarrier, problemFrobenius] <;> trivial

theorem odot_vs_leeYang :
    leeYangFrobeniusType = .special := by
  simp [leeYangFrobeniusType]

end Millennium.IGBarrierAnalysis
