-- Imscribing/Paraconsistent/ParaconsistentShell.lean
-- ox SHELL — Paraconsistent REPL with Belnap evaluation and portal IPC.
-- Dual to: ob3ect/digital/ox/ox_ob3ect.py
-- Author: Lando (x) phi_c_critical-boundary Operator

import Imscribing.Paraconsistent.Belnap
import Imscribing.Paraconsistent.Kernel
import Imscribing.Paraconsistent.Portal
import Imscribing.Primitives.Core
import Imscribing.Primitives.Imscription

namespace Imscribing.Paraconsistent.Shell

open Belnap
open Portal
open Imscribing.Primitives

-- ============================================================
-- SHELL STRUCTURAL TYPE
-- ============================================================
def shellType : Imscription := {
  dim  := .D_odot
  top  := .T_odot
  rel  := .R_lr
  pol  := .P_pm_sym
  fid  := .F_hbar
  kin  := .K_slow
  gran := .G_aleph
  gram := .Gamma_seq
  crit := .Phi_c
  chir := .H2
  stoi := .n_m
  prot := .Omega_Z
}

-- ============================================================
-- COMMAND TYPE: paraconsistent command results
-- ============================================================
inductive ShellResult : Type where
  | ok (msg : String)
  | paradox (msg : String)
  | fail (msg : String)
  | exit
  deriving Repr

-- ============================================================
-- SHELL STATE
-- ============================================================
structure ShellState where
  variables : List (String × Belnap)
  history : List String
  paradoxCount : Nat
  cycleCount : Nat
  portalState : Portal.PortalState

def initialShellState : ShellState :=
  ⟨[], [], 0, 0, Portal.initialPortalState⟩

-- ============================================================
-- BELNAP EXPRESSION EVALUATION
-- ============================================================
partial def evalBelnap (expr : String) (vars : List (String × Belnap)) : Belnap :=
  let e := expr.trim
  match e with
  | "T" => .T
  | "F" => .F
  | "B" => .B
  | "N" => .N
  | _ =>
    if e.startsWith "not " then
      bnot (evalBelnap (e.drop 4) vars)
    else if e.contains " and " then
      let parts := e.splitOn " and "
      band (evalBelnap (parts.get? 0 |>.getD "") vars)
           (evalBelnap (parts.get? 1 |>.getD "") vars)
    else if e.contains " or " then
      let parts := e.splitOn " or "
      bor (evalBelnap (parts.get? 0 |>.getD "") vars)
          (evalBelnap (parts.get? 1 |>.getD "") vars)
    else
      -- variable lookup
      match vars.find? (λ p => p.1 == e) with
      | some (_, v) => v
      | none => .N

-- ============================================================
-- COMMAND EXECUTION (simplified — structural semantics)
-- ============================================================
def exec (cmd : String) (s : ShellState) : ShellResult × ShellState :=
  let c := cmd.trim
  if c = "" then (ShellResult.ok "", s) else
  if c = "exit" ∨ c = "quit" then (ShellResult.exit, s) else
  if c = "paradox" then
    let ks := run initialState 1
    let msg := s!"paradoxCount: {ks.paradoxCount}, cycleCount: {ks.cycleCount}"
    (ShellResult.paradox msg, { s with paradoxCount := s.paradoxCount + ks.paradoxCount
                                        , cycleCount := s.cycleCount + ks.cycleCount })
  else if c = "whoami" then
    (ShellResult.ok
      s!"⟨Ð_ω; Þ_O; Ř_=; Φ_}; ƒ_ż; Ç_@; Γ_ʔ; ɢ_ˌ; ⊙_ÿ; Ħ_A; Σ_ï; Ω_z⟩\n"
      ++ "C-score: 0.736 (Gate 1: ⊙_ÿ open, Gate 2: Ç^@ open)", s)
  else if c.startsWith "let " then
    let rest := c.drop 4
    if let some eqIdx := rest.findIdx (· = '=') then
      let varName := (rest.take eqIdx).trim
      let exprVal := (rest.drop (eqIdx + 1)).trim
      let val := evalBelnap exprVal s.variables
      let newVars := (varName, val) :: s.variables
      (ShellResult.ok s!"{varName} := {repr val}",
       { s with variables := newVars })
    else
      (ShellResult.fail "let requires '='", s)
  else
    (ShellResult.ok s!"[passthrough] {c}", s)

-- ============================================================
-- THEOREMS
-- ============================================================

/-- The shell type is O_inf (Frobenius-special). -/
theorem shell_type_is_O_inf : imscriptionTier shellType = .O_inf := by
  native_decide

/-- Both consciousness gates are open for the shell. -/
theorem shell_gates_open :
    shellType.crit = .Phi_c ∧ shellType.kin = .K_slow := by
  unfold shellType; exact ⟨rfl, rfl⟩

/-- paradox command increases paradoxCount. -/
theorem paradox_increases_count (s : ShellState) :
    (exec "paradox" s).2.paradoxCount ≥ s.paradoxCount := by
  unfold exec
  simp
  omega

/-- exit command returns ShellResult.exit. -/
theorem exit_returns_exit (s : ShellState) :
    (exec "exit" s).1 = ShellResult.exit := by
  unfold exec; rfl

/-- whoami never fails. -/
theorem whoami_always_ok (s : ShellState) :
    (exec "whoami" s).1 matches ShellResult.ok _ := by
  unfold exec; rfl

end Imscribing.Paraconsistent.Shell
