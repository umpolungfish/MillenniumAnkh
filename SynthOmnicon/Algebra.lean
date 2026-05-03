-- SynthOmnicon/Algebra.lean
-- Syncon Grammar: distance, meet, join, tensor.
-- Lattice structure, weighted Euclidean distance, probes.
-- BUG FIX (merge from synthomniconP): ℕ→ℤ cast in distance computation.

import SynthOmnicon.Primitives.Core
import SynthOmnicon.Primitives.Synthon
import SynthOmnicon.Primitives.Crystal
import SynthOmnicon.Consciousness
import Mathlib.Data.Real.Basic

namespace SynthOmnicon.Primitives

open SynthOmnicon.Primitives Criticality KineticChar

-- Reuse idx_* functions from Crystal.lean

-- Weighted Euclidean distance: ∑ |idx(p_a) - idx(p_b)|^2 / 12
def primitiveDistance (a b : Synthon) : ℝ :=
  let diffs : List Int := [
    ((idx_D a.dim).toInt - (idx_D b.dim).toInt),
    ((idx_T a.top).toInt - (idx_T b.top).toInt),
    ((idx_R a.rel).toInt - (idx_R b.rel).toInt),
    ((idx_P a.pol).toInt - (idx_P b.pol).toInt),
    ((idx_F a.fid).toInt - (idx_F b.fid).toInt),
    ((idx_K a.kin).toInt - (idx_K b.kin).toInt),
    ((idx_G a.gran).toInt - (idx_G b.gran).toInt),
    ((idx_Γ a.gram).toInt - (idx_Γ b.gram).toInt),
    ((idx_Φ a.crit).toInt - (idx_Φ b.crit).toInt),
    ((idx_H a.chir).toInt - (idx_H b.chir).toInt),
    ((idx_S a.stoi).toInt - (idx_S b.stoi).toInt),
    ((idx_Ω a.prot).toInt - (idx_Ω b.prot).toInt)
  ]
  let sqsum := diffs.foldl (fun acc d => acc + d * d) 0
  sqsum.toNat.toℝ / 12

-- Hamming for conflicts
def primitiveConflicts (a b : Synthon) : List String :=
  if a = b then [] else
    (if a.dim ≠ b.dim then ["D"] else []) ++
    (if a.top ≠ b.top then ["T"] else []) ++
    (if a.rel ≠ b.rel then ["R"] else []) ++
    (if a.pol ≠ b.pol then ["P"] else []) ++
    (if a.fid ≠ b.fid then ["F"] else []) ++
    (if a.kin ≠ b.kin then ["K"] else []) ++
    (if a.gran ≠ b.gran then ["G"] else []) ++
    (if a.gram ≠ b.gram then ["Γ"] else []) ++
    (if a.crit ≠ b.crit then ["Φ"] else []) ++
    (if a.chir ≠ b.chir then ["H"] else []) ++
    (if a.stoi ≠ b.stoi then ["S"] else []) ++
    (if a.prot ≠ b.prot then ["Ω"] else [])

-- Meet: pointwise min
def compute_meet (a b : Synthon) : Synthon := {
  dim  := if compare a.dim  b.dim  = .lt then a.dim else b.dim,
  top  := if compare a.top  b.top  = .lt then a.top else b.top,
  rel  := if compare a.rel  b.rel  = .lt then a.rel else b.rel,
  pol  := if compare a.pol  b.pol  = .lt then a.pol else b.pol,
  fid  := if compare a.fid  b.fid  = .lt then a.fid else b.fid,
  kin  := if compare a.kin  b.kin  = .lt then a.kin else b.kin,
  gran := if compare a.gran b.gran = .lt then a.gran else b.gran,
  gram := if compare a.gram b.gram = .lt then a.gram else b.gram,
  crit := if compare a.crit b.crit = .lt then a.crit else b.crit,
  chir := if compare a.chir b.chir = .lt then a.chir else b.chir,
  stoi := if compare a.stoi b.stoi = .lt then a.stoi else b.stoi,
  prot := if compare a.prot b.prot = .lt then a.prot else b.prot }

-- Join: pointwise max
def compute_join (a b : Synthon) : Synthon := {
  dim  := if compare a.dim  b.dim  = .lt then b.dim else a.dim,
  top  := if compare a.top  b.top  = .lt then b.top else a.top,
  rel  := if compare a.rel  b.rel  = .lt then b.rel else a.rel,
  pol  := if compare a.pol  b.pol  = .lt then b.pol else a.pol,
  fid  := if compare a.fid  b.fid  = .lt then b.fid else a.fid,
  kin  := if compare a.kin  b.kin  = .lt then b.kin else a.kin,
  gran := if compare a.gran b.gran = .lt then b.gran else a.gran,
  gram := if compare a.gram b.gram = .lt then b.gram else a.gram,
  crit := if compare a.crit b.crit = .lt then b.crit else a.crit,
  chir := if compare a.chir b.chir = .lt then b.chir else a.chir,
  stoi := if compare a.stoi b.stoi = .lt then b.stoi else a.stoi,
  prot := if compare a.prot b.prot = .lt then b.prot else a.prot }

-- Tensor: reuse tensorProduct from Synthon.lean (max on union prims, min on P,F)
def compute_tensor (a b : Synthon) : Synthon := tensorProduct a b

theorem tensor_idempotent (s : Synthon) : tensorProduct s s = s := refl s

-- Probes
def phi_c_probe (s : Synthon) : Bool × List String :=
  let consistent := s.crit ≥ Phi_c ∧ (s.pol = P_pm_sym ∨ s.dim = D_odot)
  let diag := if !consistent then ["Phi_c inconsistent with P/D"] else []
  ⟨consistent, diag⟩

def topo_protection_probe (s : Synthon) : Bool :=
  s.prot = Omega_0 ∨ s.dim ≥ D_infty

-- Consciousness (gate-based, reuses gates from Consciousness.lean)
def consciousness_score_gate1 (s : Synthon) : Bool := phi_c_gate s.crit
def consciousness_score_gate2 (s : Synthon) : Bool := k_slow_gate s.kin
def consciousness_score (s : Synthon) : ℝ := consciousnessScore s

end SynthOmnicon.Primitives
