-- SynthOmnicon/Consciousness.lean
-- Consciousness score implementation from SynthOmnicon grammar (§VIII).
-- C-score (0–1): Gate 1 (Phi_c pass), Gate 2 (K <= K_slow pass).
-- Full C=1 requires Phi_c (self-modeling loop) + K_slow (deliberative, not trapped).
-- Examples: white_dwarf C=0 (Phi_sub), human C=1 (Phi_c + K_slow).
-- BUG FIX (merge from synthomniconP): S_11 → one_one; T_boxtimes → T_box to match MA Core enums.

import SynthOmnicon.Primitives.Core
import SynthOmnicon.Primitives.Synthon

namespace SynthOmnicon.Consciousness

open SynthOmnicon.Primitives Criticality KineticChar

/-- Gate 1: Phi_c self-modeling gate. Passes if Phi >= Phi_c. -/
def phi_c_gate (phi : Criticality) : Bool :=
  phi ≥ Phi_c

/-- Gate 2: K <= K_slow deliberation gate. Passes if kinetics not trapped. -/
def k_slow_gate (k : KineticChar) : Bool :=
  k ≤ K_slow

/-- Consciousness score C(s) ∈ [0,1].
    C=1: both gates open (Phi_c + K_slow).
    C=0.5: Phi_c but K_trap/MBL (self-model but frozen).
    C=0: Phi_sub/super/EP (no self-modeling). -/
noncomputable def consciousnessScore (s : Synthon) : ℝ :=
  if phi_c_gate s.crit then
    if k_slow_gate s.kin then 1 else 0.5
  else 0

/-- White dwarf example: C=0 (fails Gate 1: Phi_sub degeneracy pressure). -/
def white_dwarf : Synthon := {
  dim  := D_infty,
  top  := T_network,
  rel  := R_super,
  pol  := P_sym,
  fid  := F_ell,
  kin  := K_slow,
  gran := G_gimel,
  gram := Gamma_and,
  crit := Phi_sub,
  chir := H1,
  stoi := n_n,
  prot := Omega_0 }

theorem white_dwarf_C_zero : consciousnessScore white_dwarf = 0 := by
  simp [consciousnessScore, phi_c_gate, white_dwarf]
  <;> decide

/-- Human brain (template): C=1 (Phi_c criticality + K_slow deliberation). -/
def human_brain : Synthon := {
  dim  := D_triangle,   -- cortical sheet
  top  := T_box,        -- modular hierarchy × recurrence (T_boxtimes → T_box in MA naming)
  rel  := R_lr,         -- bidirectional thalamocortical
  pol  := P_pm_sym,     -- Frobenius at criticality
  fid  := F_hbar,       -- quantum effects conjectural but high fidelity
  kin  := K_slow,       -- deliberate cognition
  gran := G_aleph,      -- fine-grained neural connectome
  gram := Gamma_seq,    -- sequential grammar of thought
  crit := Phi_c,        -- brain criticality (Beggs 2003)
  chir := H2,           -- persistent memory
  stoi := one_one,      -- FIXED: was S_11 (SP naming) → one_one (MA naming)
  prot := Omega_Z }

theorem human_brain_C_one : consciousnessScore human_brain = 1 := by
  simp [consciousnessScore, phi_c_gate, k_slow_gate, human_brain]
  <;> decide

/-- Quantum gravity: C=0.5 (Phi_c + K_trap → Gate 1 passes, Gate 2 fails). -/
theorem qg_C_half : consciousnessScore quantum_gravity = 0.5 := by
  simp [consciousnessScore, phi_c_gate, k_slow_gate]
  <;> decide

end SynthOmnicon.Consciousness
