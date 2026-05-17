-- Imscribing/Millennium/BarrierFrobenius.lean
-- Integration: connects Barrier taxonomy with Frobenius tier structure.

import Imscribing.Millennium.Barriers
import Imscribing.Millennium.FrobeniusStructure

namespace Millennium.BarrierFrobenius

open Imscribing.Primitives

def problemFrobenius : Millennium.Barriers.MillenniumProblem → Millennium.Frobenius.FrobeniusType
  | .RH    => .full
  | .Hodge => .full
  | .PvsNP => .algebraOnly
  | .NS    => .full
  | .YM    => .full
  | .BSD   => .algebraOnly
  | .OPN   => .algebraOnly

theorem analysis_problems_full_frobenius :
    problemFrobenius .RH = .full ∧
    problemFrobenius .Hodge = .full ∧
    problemFrobenius .NS = .full ∧
    problemFrobenius .YM = .full := by
  simp [problemFrobenius]

theorem layered_problems_algebraOnly :
    problemFrobenius .PvsNP = .algebraOnly ∧
    problemFrobenius .BSD = .algebraOnly ∧
    problemFrobenius .OPN = .algebraOnly := by
  simp [problemFrobenius]

theorem leeYang_above_all :
    ∀ p : Millennium.Barriers.MillenniumProblem,
      (problemFrobenius p).rank < (Millennium.Frobenius.leeYangFrobeniusType).rank := by
  intro p; cases p <;>
    simp [problemFrobenius, Millennium.Frobenius.leeYangFrobeniusType, Millennium.Frobenius.FrobeniusType.rank]
  <;> norm_num

theorem ym_barrier_frobenius_cross :
    Millennium.Barriers.millenniumBarrier .YM = .MissingFoundation ∧
    problemFrobenius .YM = .full := by
  simp [Millennium.Barriers.millenniumBarrier, problemFrobenius]

theorem c13_gap_is_frobenius_one :
    (Millennium.Frobenius.leeYangFrobeniusType).rank - (problemFrobenius .RH).rank = 1 := by
  simp [problemFrobenius, Millennium.Frobenius.leeYangFrobeniusType, Millennium.Frobenius.FrobeniusType.rank]

end Millennium.BarrierFrobenius
