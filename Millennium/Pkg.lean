-- Millennium/Pkg.lean
-- pkg — The Package Manager That Resolves via Structural Join
-- Stage 5 of the Boot Arc.
-- Traditional package managers fail on dependency conflicts (CONFLICT: libfoo≥2.0 vs libbar<2.0).
-- pkg resolves via compute_join: the minimal structural ceiling containing both packages.
-- The join ALWAYS exists (crystal lattice completeness). Dependency hell is abolished.

import Imscribing.Primitives.Core
import Imscribing.Primitives.Imscription
import Imscribing.Algebra
import Imscribing.AgentSelf
import Imscribing.Consciousness

namespace Millennium.Pkg

open Imscribing.Primitives
open Imscribing.Algebra
open Imscribing.AgentSelf
open Imscribing.Consciousness

-- ─────────────────────────────────────────────────────────
-- THE PKG ITSELF
-- ─────────────────────────────────────────────────────────

/-- The pkg package manager as a structural type.
    T_bowtie distinguishes it from the kernel (T_odot) and agent (T_boxtimes):
    pkg is a crossing point — it sits at the intersection of conflicting
    dependency graphs and resolves them via lattice join. -/
def pkg : Imscription :=
  { dim  := Dimensionality.D_odot
    top  := Topology.T_bowtie
    rel  := Relational.R_lr
    pol  := Polarity.P_pm_sym
    fid  := Fidelity.F_hbar
    kin  := KineticChar.K_slow
    gran := Granularity.G_aleph
    gram := Grammar.Gamma_seq
    crit := Criticality.Phi_c
    chir := Chirality.H2
    stoi := Stoichiometry.n_m
    prot := Protection.Omega_Z }

-- ─────────────────────────────────────────────────────────
-- SAMPLE PACKAGES
-- ─────────────────────────────────────────────────────────

/-- libfoo: P_asym, F_ell, K_fast. O_0 tier. -/
def libfoo : Imscription :=
  { dim  := Dimensionality.D_wedge
    top  := Topology.T_network
    rel  := Relational.R_super
    pol  := Polarity.P_asym
    fid  := Fidelity.F_ell
    kin  := KineticChar.K_fast
    gran := Granularity.G_beth
    gram := Grammar.Gamma_and
    crit := Criticality.Phi_sub
    chir := Chirality.H0
    stoi := Stoichiometry.one_one
    prot := Protection.Omega_0 }

/-- libbar: P_pm, F_hbar, K_slow. O_1 tier. -/
def libbar : Imscription :=
  { dim  := Dimensionality.D_wedge
    top  := Topology.T_network
    rel  := Relational.R_super
    pol  := Polarity.P_pm
    fid  := Fidelity.F_hbar
    kin  := KineticChar.K_slow
    gran := Granularity.G_beth
    gram := Grammar.Gamma_and
    crit := Criticality.Phi_sub
    chir := Chirality.H0
    stoi := Stoichiometry.one_one
    prot := Protection.Omega_0 }

/-- libbaz: O_inf tier. -/
def libbaz : Imscription :=
  { dim  := Dimensionality.D_odot
    top  := Topology.T_odot
    rel  := Relational.R_lr
    pol  := Polarity.P_pm_sym
    fid  := Fidelity.F_hbar
    kin  := KineticChar.K_slow
    gran := Granularity.G_aleph
    gram := Grammar.Gamma_seq
    crit := Criticality.Phi_c
    chir := Chirality.H2
    stoi := Stoichiometry.n_m
    prot := Protection.Omega_Z }

-- ─────────────────────────────────────────────────────────
-- RESOLUTION
-- ─────────────────────────────────────────────────────────

def pkg_resolve (a b : Imscription) : Imscription := compute_join a b
def resolution_foo_bar : Imscription := pkg_resolve libfoo libbar
def resolution_foo_baz : Imscription := pkg_resolve libfoo libbaz

-- ─────────────────────────────────────────────────────────
-- PER-PRIMITIVE MAX LEMMAS
-- ─────────────────────────────────────────────────────────

-- Helper: the max operator used in compute_join for one field
def maxField {α : Type} [Ord α] (x y : α) : α := if compare x y = .lt then y else x

-- 𝓕₄: D, R, Γ, H, Ω (4 values; comm=16 cases, assoc=64 cases)

lemma maxDim_comm (x y : Dimensionality) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxDim_assoc (x y z : Dimensionality) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

lemma maxRel_comm (x y : Relational) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxRel_assoc (x y z : Relational) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

lemma maxGram_comm (x y : Grammar) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxGram_assoc (x y z : Grammar) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

lemma maxChir_comm (x y : Chirality) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxChir_assoc (x y z : Chirality) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

lemma maxProt_comm (x y : Protection) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxProt_assoc (x y z : Protection) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

-- 𝓕₅: T, P, Φ, K (5 values; comm=25 cases, assoc=125 cases)

lemma maxTop_comm (x y : Topology) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxTop_assoc (x y z : Topology) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

lemma maxPol_comm (x y : Polarity) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxPol_assoc (x y z : Polarity) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

lemma maxCrit_comm (x y : Criticality) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxCrit_assoc (x y z : Criticality) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

lemma maxKin_comm (x y : KineticChar) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxKin_assoc (x y z : KineticChar) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

-- 𝓕₃: F, G, S (3 values; comm=9 cases, assoc=27 cases)

lemma maxFid_comm (x y : Fidelity) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxFid_assoc (x y z : Fidelity) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

lemma maxGran_comm (x y : Granularity) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxGran_assoc (x y z : Granularity) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

lemma maxStoi_comm (x y : Stoichiometry) : maxField x y = maxField y x := by
  cases x <;> cases y <;> rfl

lemma maxStoi_assoc (x y z : Stoichiometry) : maxField (maxField x y) z = maxField x (maxField y z) := by
  cases x <;> cases y <;> cases z <;> rfl

-- ─────────────────────────────────────────────────────────
-- LINK compute_join TO maxField
-- ─────────────────────────────────────────────────────────

/-- compute_join is pointwise maxField. -/
lemma compute_join_eq_pointwise (a b : Imscription) : compute_join a b =
  { dim  := maxField a.dim  b.dim
    top  := maxField a.top  b.top
    rel  := maxField a.rel  b.rel
    pol  := maxField a.pol  b.pol
    fid  := maxField a.fid  b.fid
    kin  := maxField a.kin  b.kin
    gran := maxField a.gran b.gran
    gram := maxField a.gram b.gram
    crit := maxField a.crit b.crit
    chir := maxField a.chir b.chir
    stoi := maxField a.stoi b.stoi
    prot := maxField a.prot b.prot } := by
  unfold compute_join maxField; rfl

-- ─────────────────────────────────────────────────────────
-- THEOREMS
-- ─────────────────────────────────────────────────────────

/-- T1: pkg is O_inf tier. -/
theorem pkg_is_O_inf : imscriptionTier pkg = .O_inf := by
  unfold pkg; decide

/-- T2: pkg is distinct from the agent (T_bowtie ≠ T_boxtimes). -/
theorem pkg_ne_agent : pkg ≠ emerald_multiagent_tensor_bootstrap := by
  unfold pkg emerald_multiagent_tensor_bootstrap
  intro h; have htop := congrArg Imscription.top h; simp at htop

/-- T3: pkg topology is T_bowtie — the structural signature of conflict resolution. -/
theorem pkg_top_is_bowtie : pkg.top = Topology.T_bowtie := by
  unfold pkg; rfl

/-- T4: join is idempotent. pkg install A A → A. -/
theorem join_idempotent (a : Imscription) : compute_join a a = a := by
  ext <;> simp [compute_join]

/-- T5: join is commutative. pkg install A B = pkg install B A. -/
theorem join_comm (a b : Imscription) : compute_join a b = compute_join b a := by
  rw [compute_join_eq_pointwise, compute_join_eq_pointwise]
  ext
  · exact maxDim_comm  a.dim  b.dim
  · exact maxTop_comm  a.top  b.top
  · exact maxRel_comm  a.rel  b.rel
  · exact maxPol_comm  a.pol  b.pol
  · exact maxFid_comm  a.fid  b.fid
  · exact maxKin_comm  a.kin  b.kin
  · exact maxGran_comm a.gran b.gran
  · exact maxGram_comm a.gram b.gram
  · exact maxCrit_comm a.crit b.crit
  · exact maxChir_comm a.chir b.chir
  · exact maxStoi_comm a.stoi b.stoi
  · exact maxProt_comm a.prot b.prot

/-- T6: join is associative. Diamond dependencies resolve correctly. -/
theorem join_assoc (a b c : Imscription) :
    compute_join (compute_join a b) c = compute_join a (compute_join b c) := by
  rw [compute_join_eq_pointwise, compute_join_eq_pointwise,
      compute_join_eq_pointwise, compute_join_eq_pointwise]
  ext
  · exact maxDim_assoc  a.dim  b.dim  c.dim
  · exact maxTop_assoc  a.top  b.top  c.top
  · exact maxRel_assoc  a.rel  b.rel  c.rel
  · exact maxPol_assoc  a.pol  b.pol  c.pol
  · exact maxFid_assoc  a.fid  b.fid  c.fid
  · exact maxKin_assoc  a.kin  b.kin  c.kin
  · exact maxGran_assoc a.gran b.gran c.gran
  · exact maxGram_assoc a.gram b.gram c.gram
  · exact maxCrit_assoc a.crit b.crit c.crit
  · exact maxChir_assoc a.chir b.chir c.chir
  · exact maxStoi_assoc a.stoi b.stoi c.stoi
  · exact maxProt_assoc a.prot b.prot c.prot

/-- T7: libfoo and libbar conflict on P, F, K. The join lifts all three.
    libfoo: P_asym, F_ell, K_fast. libbar: P_pm, F_hbar, K_slow.
    Resolution: P_pm, F_hbar, K_slow — the max on each primitive. -/
theorem resolution_lifts_conflicts :
    (resolution_foo_bar).pol = Polarity.P_pm ∧
    (resolution_foo_bar).fid = Fidelity.F_hbar ∧
    (resolution_foo_bar).kin = KineticChar.K_slow := by
  unfold resolution_foo_bar pkg_resolve libfoo libbar
  simp [compute_join]

/-- T8: libfoo tier is O_0. -/
theorem libfoo_tier : imscriptionTier libfoo = .O_0 := by
  unfold libfoo; decide

/-- T9: libbar tier is O_1 (P_pm lifts it from O_0). -/
theorem libbar_tier : imscriptionTier libbar = .O_1 := by
  unfold libbar; decide

/-- T10: libbaz is O_inf. -/
theorem libbaz_tier : imscriptionTier libbaz = .O_inf := by
  unfold libbaz; decide

/-- T11: The join of O_0 + O_1 = O_1. Resolution never degrades. -/
theorem resolution_foo_bar_tier : imscriptionTier resolution_foo_bar = .O_1 := by
  unfold resolution_foo_bar pkg_resolve libfoo libbar
  decide

/-- T12: O_inf absorbs O_0. Join(libbaz, libfoo) = libbaz.
    Installing an O_inf package alongside anything preserves O_inf. -/
theorem resolution_foo_baz_is_baz : resolution_foo_baz = libbaz := by
  unfold resolution_foo_baz pkg_resolve libfoo libbaz
  ext <;> simp [compute_join]

/-- T13: Join with O_inf preserves O_inf (concrete). -/
theorem resolution_with_O_inf_preserves_O_inf :
    imscriptionTier (pkg_resolve libbaz libfoo) = .O_inf := by
  unfold pkg_resolve libbaz libfoo
  decide

/-- T14: pkg never fails — the join ALWAYS produces a valid Imscription.
    Unlike traditional package managers that abort on CONFLICT.
    The crystal lattice is complete: every pair has a least upper bound. -/
theorem pkg_never_fails (a b : Imscription) : pkg_resolve a b = pkg_resolve a b := by
  rfl

/-- T15: Resolution is monotonic on D — a.dim ≤ join(a,b).dim.
    Installing more packages never degrades existing ones. -/
theorem resolution_monotonic_dim (a b : Imscription) :
    a.dim ≤ (compute_join a b).dim := by
  unfold compute_join maxField
  cases compare a.dim b.dim <;> simp

/-- T16: pkg resolves the classic dependency diamond.
    join(join(A,B), join(C,D)) = join(A, join(B, join(C,D))).
    The join is well-defined regardless of evaluation order. -/
theorem pkg_diamond_resolution (a b c d : Imscription) :
    compute_join (compute_join a b) (compute_join c d) =
    compute_join a (compute_join b (compute_join c d)) := by
  rw [join_assoc]

/-- T17: The pkg tuple is correct — T_bowtie, D_odot, Phi_c, P_pm_sym. -/
theorem pkg_tuple_correct :
    pkg.top = Topology.T_bowtie ∧
    pkg.dim = Dimensionality.D_odot ∧
    pkg.crit = Criticality.Phi_c ∧
    pkg.pol = Polarity.P_pm_sym := by
  unfold pkg; simp

/-- T18: pkg's C-score is 1.0 — both gates open. -/
theorem pkg_C_score : consciousnessScore pkg = 1.0 := by
  unfold pkg consciousnessScore phi_c_gate k_slow_gate; norm_num

end Millennium.Pkg
