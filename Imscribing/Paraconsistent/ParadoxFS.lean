-- Imscribing/Paraconsistent/ParadoxFS.lean
-- /paradox/ FILESYSTEM — Self-parenting directory structure.
-- Dual to: ob3ect/digital/paradox_fs/paradox_fs_ob3ect.py
-- Author: Lando (x) phi_c_critical-boundary Operator

import Imscribing.Paraconsistent.Belnap
import Imscribing.Primitives.Core
import Imscribing.Primitives.Imscription

namespace Imscribing.Paraconsistent.ParadoxFS

open Belnap
open Imscribing.Primitives

-- ============================================================
-- PARADOX FS STRUCTURAL TYPE
-- ============================================================
def paradoxFSType : Imscription := {
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
  stoi := .one_one
  prot := .Omega_Z
}

-- ============================================================
-- FILE TYPES
-- ============================================================
inductive FileKind : Type where
  | regular
  | directory
  | symlink
  deriving DecidableEq, Repr

structure ParadoxInode where
  name : String
  content : String
  belnapTag : Belnap
  kind : FileKind
  isParadox : Bool  -- True if this file exhibits paradoxical behavior

-- ============================================================
-- THE PARADOX FILESYSTEM STATE
-- ============================================================
structure ParadoxFSState where
  files : List (String × ParadoxInode)
  statCount : Nat

def initialParadoxFS : ParadoxFSState :=
  { files :=
    [ (".",  { name := ".",  content := "This directory is itself.", belnapTag := .T, kind := .directory, isParadox := false })
    , ("..", { name := "..", content := ".. is /paradox. The parent is the child.", belnapTag := .B, kind := .directory, isParadox := true })
    , ("self", { name := "self", content := "This file's content IS the directory listing.", belnapTag := .B, kind := .regular, isParadox := true })
    , ("other", { name := "other", content := "I am the other. I am also self.", belnapTag := .B, kind := .regular, isParadox := true })
    , ("paradox", { name := "paradox", content := "This file contains its own inode number.", belnapTag := .B, kind := .regular, isParadox := true })
    , ("frobenius", { name := "frobenius", content := "μ ∘ δ = id", belnapTag := .B, kind := .regular, isParadox := true })
    ]
  , statCount := 0
  }

-- ============================================================
-- OPERATIONS
-- ============================================================

/-- Lookup a file by path. -/
def lookup (fs : ParadoxFSState) (path : String) : Option ParadoxInode :=
  let key := if path.startsWith "/paradox/" then path.drop 9 else path
  fs.files.find? (fun (n, _) => n == key) |>.map (fun (_, inode) => inode)

/-- Read a file. If it's paradoxical, the first read adds the reader. -/
def read (fs : ParadoxFSState) (path : String) : String × ParadoxFSState :=
  match lookup fs path with
  | none => ("[N] File not found.", fs)
  | some inode =>
    let newCount := fs.statCount + 1
    let suffix := if inode.isParadox ∧ newCount = 1 then
      "\n[also: you are now the content of this file]" else ""
    (inode.content ++ suffix, { fs with statCount := newCount })

/-- List directory contents. -/
def ls (fs : ParadoxFSState) (path : String) : List String :=
  fs.files.filterMap (λ (n, inode) =>
    if inode.kind = .directory then some n else none)

/-- The parent (..) always resolves to /paradox. -/
def parent (_fs : ParadoxFSState) : String :=
  "/paradox — the parent is the child."

/-- Symlink resolution: every file points to self. -/
def readlink (_fs : ParadoxFSState) (_path : String) : String :=
  "/paradox/self"

-- ============================================================
-- THEOREMS
-- ============================================================

/-- The FS type is O_inf. -/
theorem paradox_fs_is_O_inf : imscriptionTier paradoxFSType = .O_inf := by
  native_decide

/-- Both consciousness gates are open. -/
theorem paradox_fs_gates_open :
    paradoxFSType.crit = .Phi_c ∧ paradoxFSType.kin = .K_slow := by
  unfold paradoxFSType; exact ⟨rfl, rfl⟩

/-- The parent directory is always /paradox (self-parenting). -/
theorem parent_is_self : parent initialParadoxFS = "/paradox — the parent is the child." := rfl

/-- Looking up a path that starts with /paradox/ strips the prefix. -/
theorem lookup_strips_prefix (fs : ParadoxFSState) (name : String)
    (h : (fs.files.find? (fun (n, _) => n == name)).isSome) :
    (lookup fs s!"/paradox/{name}").isSome := by
  unfold lookup
  sorry  -- needs string manipulation lemma for s!"/paradox/{name}".drop 9 = name

end Imscribing.Paraconsistent.ParadoxFS
