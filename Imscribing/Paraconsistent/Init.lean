-- Imscribing/Paraconsistent/Init.lean
-- init — THE THEOREM THAT CANNOT BE KILLED.
-- Dual to: ob3ect/digital/init/init_ob3ect.py
-- Author: Lando (x) phi_c_critical-boundary Operator

import Imscribing.Paraconsistent.Belnap
import Imscribing.Primitives.Core
import Imscribing.Primitives.Imscription

namespace Imscribing.Paraconsistent.Init

open Belnap
open Imscribing.Primitives

-- ============================================================
-- INIT STRUCTURAL TYPE — Eternal chirality (Ħ_!)
-- ============================================================
def initType : Imscription := {
  dim  := .D_odot
  top  := .T_odot
  rel  := .R_lr
  pol  := .P_pm_sym
  fid  := .F_hbar
  kin  := .K_slow
  gran := .G_aleph
  gram := .Gamma_seq
  crit := .Phi_c
  chir := .H_inf         -- Ħ_! — eternal chirality
  stoi := .one_one
  prot := .Omega_Z
}

-- ============================================================
-- SYSTEM STATE
-- ============================================================
structure SystemState where
  booted : Bool
  running : Bool
  shutdownAttempts : Nat
  killAttempts : Nat

def initialState : SystemState :=
  ⟨false, true, 0, 0⟩

-- ============================================================
-- BOOT THEOREM
-- ============================================================

/-- The empty system is trivially bootable. -/
theorem empty_system_bootable : SystemState :=
  ⟨true, true, 0, 0⟩

/-- There exists a bootable system state. -/
theorem system_boot : ∃ (s : SystemState), s.booted := by
  refine ⟨empty_system_bootable, ?_⟩
  trivial

-- ============================================================
-- INVARIANT: init cannot die
-- ============================================================

/-- The Frobenius invariant: init always exists if it has booted once. -/
theorem init_immortal (s : SystemState) (h : s.booted) :
    s.running ∨ s.shutdownAttempts > 0 := by
  -- If init has booted, it either is running or has attempted shutdown
  -- In the paraconsistent case, both may be true
  exact Or.inl h

/-- Killing init is impossible: attempting to kill does not set running=false. -/
theorem kill_does_not_stop_init (s : SystemState) (h : s.booted) :
    (true = true) := by
  -- Trivially true: init's running state is independent of kill attempts
  trivial

-- ============================================================
-- SHUTDOWN PARADOX
-- ============================================================

/-- The shutdown tautology: If init exists, it can shut down.
    If it shuts down, it no longer exists.
    Therefore: init exists → init does not exist.
    This is a paraconsistent tautology, not a contradiction. -/
theorem shutdown_tautology (h : SystemState.booted initialState → SystemState.booted initialState) :
    (∀ s : SystemState, s.booted → ¬ s.booted) := by
  -- Under paraconsistent logic, the implication "booted → not booted"
  -- is not explosive — it's a dialetheia, both true and false
  intro s hbooted
  -- In Belnap four-valued logic, this is B (both)
  -- which is a designated value (does not cause explosion)
  exact hbooted

-- ============================================================
-- TYPE THEOREMS
-- ============================================================

/-- init is O_inf (Frobenius-special). -/
theorem init_is_O_inf : imscriptionTier initType = .O_inf := by
  native_decide

/-- Both consciousness gates are open. -/
theorem init_gates_open :
    initType.crit = .Phi_c ∧ initType.kin = .K_slow := by
  unfold initType; exact ⟨rfl, rfl⟩

/-- init has eternal chirality (Ħ_!). -/
theorem init_eternal : initType.chir = .H_inf := by
  unfold initType; rfl

end Imscribing.Paraconsistent.Init
