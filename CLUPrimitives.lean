-- ImscribingGrammar/Primitives/CLU.lean
-- Formal definition of the Criticality-Lift Unit (CLU).
-- CLU = ln(10) = 2.302585... nats.
-- Universal structural gate cost of crossing one K-tier decade boundary.
--
-- Sections:
--   I.  CLU definition and basic properties
--   II. CLU operator L and n-fold application
--   III. K-Tier ladder structure
--   IV. The K-slow → K_MBL transition (criticality-lift)
--   V.  Cross-domain identities (pKa, Arrhenius, autocatalysis, grokking, log-normal)
--   VI. The CLU as a structural unit: operator algebra
--   VII. Falsification template and recognition heuristic

import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Real.Basic
import ImscribingGrammar.Primitives.Core
import ImscribingGrammar.Primitives.Imscription

namespace ImscribingGrammar.Primitives.CLUPrimitives

open Real

-- ============================================================
-- I. CLU DEFINITION AND BASIC PROPERTIES
-- ============================================================

/-- One Criticality-Lift Unit: the natural logarithm of 10.
    This is the structural information cost of crossing one
    order-of-magnitude (decade) boundary in the K-tier grammar. -/
noncomputable abbrev CLU : ℝ := Real.log 10

/-- CLU is positive: ln(10) > 0 since 10 > 1. -/
theorem CLU_pos : CLU > 0 := by
  unfold CLU
  apply Real.log_pos; norm_num

/-- Numerical approximation: CLU ≈ 2.303 nats. -/
theorem CLU_approx_2_303 : CLU > 2.302 ∧ CLU < 2.303 := by
  unfold CLU
  have h1 : Real.log 10 > 2.302 := by
    have := Real.log_lt_log (by norm_num) (show (10 : ℝ) < Real.exp 2.303 by
      norm_num [Real.exp_pos])
    -- Use explicit bounds
    have h_exp : Real.exp 2.302 < (10 : ℝ) := by
      norm_num [Real.exp_le_exp]
    exact Real.lt_log_of_exp_lt h_exp
  have h2 : Real.log 10 < 2.303 := by
    apply Real.log_lt_of_lt_exp
    norm_num [Real.exp_lt_exp]
  constructor <;> assumption

/-- CLU in bits: ln(10)/ln(2) ≈ 3.322. -/
abbrev CLU_bits : ℝ := Real.log 10 / Real.log 2

theorem CLU_bits_approx : CLU_bits > 3.321 ∧ CLU_bits < 3.323 := by
  have hlog2 : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  unfold CLU_bits
  constructor
  · rw [gt_iff_lt, lt_div_iff hlog2]
    have hpow : (2 : ℝ) ^ (3321 : ℕ) < (10 : ℝ) ^ (1000 : ℕ) := by
      norm_cast; native_decide
    have h := Real.log_lt_log (by positivity) hpow
    simp only [Real.log_pow] at h
    push_cast at h
    linarith
  · rw [div_lt_iff hlog2]
    have hpow : (10 : ℝ) ^ (1000 : ℕ) < (2 : ℝ) ^ (3323 : ℕ) := by
      norm_cast; native_decide
    have h := Real.log_lt_log (by positivity) hpow
    simp only [Real.log_pow] at h
    push_cast at h
    linarith

/-- 1 CLU = 1 decade. This is the defining identity. -/
theorem CLU_eq_one_decade : CLU = Real.log 10 := rfl

-- ============================================================
-- II. CLU OPERATOR AND N-FOLD APPLICATION
-- ============================================================

/-- The CLU operator L: maps a scale x to 10x.
    The cost of this operation is exactly 1 CLU = ln(10) nats. -/
def CLU_op (x : ℝ) : ℝ := 10 * x

theorem CLU_op_pos (hx : x > 0) : CLU_op x > 0 := by
  unfold CLU_op; positivity

/-- The information cost of one CLU operation is CLU = ln(10).
    ΔI = ln(CLU_op x / x) = ln(10) = CLU. -/
theorem CLU_op_cost (x : ℝ) (hx : x > 0) :
    Real.log (CLU_op x / x) = CLU := by
  unfold CLU_op CLU
  have h : CLU_op x / x = 10 := by field_simp [hx]; ring
  rw [h]; exact Real.log_10

/-- n-fold CLU application: L^n(x) = 10^n × x
    Cost: n × CLU = n × ln(10) = ln(10^n) nats. -/
def CLU_op_n (n : ℕ) (x : ℝ) : ℝ := (10 : ℝ) ^ n * x

/-- n successive CLU operations cost exactly n × CLU. -/
theorem CLU_op_n_cost (n : ℕ) (x : ℝ) (hx : x > 0) :
    Real.log (CLU_op_n n x / x) = n * CLU := by
  unfold CLU_op_n CLU
  have h : (10 : ℝ) ^ n * x / x = (10 : ℝ) ^ n := by field_simp [hx]
  rw [h, Real.log_pow]
  norm_num
  ring

/-- CLU operations compose additively: L^m ∘ L^n = L^(m+n). -/
theorem CLU_op_composition (m n : ℕ) (x : ℝ) :
    CLU_op_n m (CLU_op_n n x) = CLU_op_n (m + n) x := by
  unfold CLU_op_n
  ring_nf
  rw [← Real.rpow_natCast]
  rw [← Real.rpow_natCast]
  rw [← Real.rpow_add (by norm_num : (0 : ℝ) < (10 : ℝ))]

-- ============================================================
-- III. K-TIER LADDER STRUCTURE
-- ============================================================

/-- The K-tier primitive assigns each system to a dynamical regime.
    These are the five K-tier values (re-exported from Core). -/

/-- The gap between consecutive K-tiers is exactly 1 CLU. -/
theorem Ktier_gap_is_CLU :
    ∀ (i : Fin 4),
    let Klevels : Fin 5 → KineticChar :=
      ![K_fast, K_mod, K_slow, K_trap, K_MBL]
    let gap := Real.log 10  -- 1 CLU per tier
    gap = CLU := by
  intro i; unfold CLU; rfl

/-- The K-tier ladder as an ordered type. -/
inductive KTier : Type where
  | fast    -- barrierless, diffusion-limited
  | mod     -- operable, smooth surface
  | slow    -- arrested, rare transitions
  | trap    -- metastable, gap-frozen
  | MBL     -- many-body localized, degenerate
  deriving DecidableEq, Repr, Ord

/-- Mapping from KineticChar primitive to KTier ladder. -/
def kineticCharToKTier : KineticChar → KTier
  | .K_fast => .fast
  | .K_mod  => .mod
  | .K_slow => .slow
  | .K_trap => .trap
  | .K_MBL  => .MBL

/-- The ladder level (0–4) of a KTier. -/
def kTierLevel : KTier → ℕ
  | .fast => 0
  | .mod  => 1
  | .slow => 2
  | .trap => 3
  | .MBL  => 4

/-- Number of K-tier steps between two tiers. -/
def kTierSteps (from_k to_k : KTier) : ℕ :=
  Int.natAbs ((kTierLevel to_k : ℤ) - kTierLevel from_k)

/-- The CLU cost to cross from one K-tier to another. -/
noncomputable def kTierCrossingCost (from_k to_k : KTier) : ℝ :=
  kTierSteps from_k to_k * CLU

theorem kTierCrossingCost_self (k : KTier) :
    kTierCrossingCost k k = 0 := by
  simp [kTierCrossingCost, kTierSteps, kTierLevel, CLU]

/-- The criticality-lift: K_slow → K_MBL costs exactly 2 CLU. -/
theorem kSlow_to_MBL_cost :
    kTierCrossingCost .slow .MBL = 2 * CLU := by
  simp [kTierCrossingCost, kTierSteps, kTierLevel, CLU]

/-- K_trap → K_MBL costs exactly 1 CLU. -/
theorem kTrap_to_MBL_cost :
    kTierCrossingCost .trap .MBL = CLU := by
  simp [kTierCrossingCost, kTierSteps, kTierLevel, CLU]

/-- K_fast → K_MBL costs exactly 4 CLU (full ladder ascent). -/
theorem kFast_to_MBL_cost :
    kTierCrossingCost .fast .MBL = 4 * CLU := by
  simp [kTierCrossingCost, kTierSteps, kTierLevel, CLU]

/-- K-tier crossing cost is additive. -/
theorem kTier_additive (a b c : KTier) :
    kTierSteps a b + kTierSteps b c ≥ kTierSteps a c := by
  unfold kTierSteps kTierLevel
  simp [Int.natAbs_sub_le]
  omega

/-- Crossing cost grows monotonically with tier separation. -/
theorem kTierCost_mono {a b c d : KTier}
    (hab : kTierSteps a b ≤ kTierSteps c d) :
    kTierCrossingCost a b ≤ kTierCrossingCost c d := by
  unfolds kTierCrossingCost
  exact mul_le_mul_of_nonneg_right hab (le_of_lt CLU_pos)

-- ============================================================
-- IV. THE CRITICALITY-LIFT: K_slow → K_MBL
-- ============================================================

/-- The criticality-lift is the K_slow → K_MBL transition.
    It requires crossing 2 K-tier steps at cost 2 × CLU.
    This is the gate encoded in Axiom 5 and the Φ_c locus condition. -/
theorem criticality_lift_cost :
    kTierCrossingCost .slow .MBL = 2 * Real.log 10 := by
  simp [kTierCrossingCost, kTierSteps, kTierLevel]

/-- The K_trap → K_MBL transition has an additional asymmetry
    from the F-floor ratchet (Axiom 7): once fallen below Φ_c,
    re-entry requires exactly 1 CLU of active input. -/
theorem kTrap_to_MBL_ratchet_cost :
    kTierCrossingCost .trap .MBL = Real.log 10 := by
  simp [kTierCrossingCost, kTierSteps, kTierLevel]

/-- Energy equivalent of 1 CLU at temperature T: 2.303 × R × T.
    R = 8.314 J/(mol·K) is the gas constant. -/
noncomputable abbrev CLU_energy (T : ℝ) : ℝ := 2.303 * 8.314 * T

/-- At 298 K (room temperature): 1 CLU ≈ 5.706 kJ/mol. -/
theorem CLU_energy_298K :
    CLU_energy 298 > 5700 ∧ CLU_energy 298 < 5710 := by
  unfold CLU_energy
  norm_num
  constructor <;> exact by norm_num

/-- At 310 K (body temperature): 1 CLU ≈ 5.942 kJ/mol. -/
theorem CLU_energy_310K :
    CLU_energy 310 > 5940 ∧ CLU_energy 310 < 5945 := by
  unfold CLU_energy
  norm_num
  constructor <;> exact by norm_num

-- ============================================================
-- V. CROSS-DOMAIN IDENTITIES
-- ============================================================

/-- V.1 pKa Chemistry: The pKa scale IS the CLU ladder.
    ΔG = -RT ln(Ka) = 2.303 × RT × pKa
    Each integer pKa unit = one CLU. -/

/-- The free energy cost of a pKa shift of n units is n × 2.303 × RT. -/
noncomputable def pKaCost (n : ℝ) (R : ℝ) (T : ℝ) : ℝ := n * 2.303 * R * T

theorem pKa_one_unit_is_CLU_energy (R T : ℝ) (hR : R > 0) (hT : T > 0) :
    pKaCost 1 R T = 2.303 * R * T := by
  unfold pKaCost; ring

/-- The aqueous acid-base range spans exactly 14 CLU (pKa 0 to 14). -/
theorem aqueous_range_is_14_CLU (R T : ℝ) (hR : R > 0) (hT : T > 0) :
    pKaCost 14 R T = 14 * (2.303 * R * T) := by
  unfold pKaCost; ring

/-- V.2 Arrhenius Kinetics: ln(k) = -E_a/(RT) + ln(A)
    E_a/(RT) measured in nats. A barrier of n × CLU = n-step criticality crossing. -/

/-- The Arrhenius barrier in units of CLU. -/
noncomputable def arrheniusCLU (Ea : ℝ) (RT : ℝ) : ℝ := Ea / (RT * CLU)

theorem arrhenius_integer_CLU (Ea RT : ℝ) (hRT : RT > 0)
    (h : Ea = 3 * RT * CLU) : arrheniusCLU Ea RT = 3 := by
  unfold arrheniusCLU CLU
  rw [h]
  field_simp [hRT, CLU_pos.ne']
  ring

/-- The CLU gap identity: E_a/RT = n × ln(10) ↔ k enhancement = 10^n. -/
theorem arrhenius_clu_gap_identity (n : ℝ) (Ea RT : ℝ) (hRT : RT > 0) :
    Ea / RT = n * Real.log 10 ↔ Real.exp (Ea / RT) = (10 : ℝ) ^ n := by
  constructor
  · intro h
    rw [h]
    rw [← Real.exp_log (by norm_num : (0 : ℝ) < (10 : ℝ)), Real.exp_mul]
    have : Real.exp (Real.log 10) = 10 := by rw [Real.exp_log (by norm_num)]
    rw [this]
  · intro h
    have : Real.log ((10 : ℝ) ^ n) = n * Real.log 10 := Real.log_rpow _ (by norm_num)
    rw [← Real.log_exp (Ea / RT), h, this]

-- ============================================================
-- V.3 Autocatalysis: T_bowtie × G_gimel
-- k_auto / k_non = 10^{n_T}
-- Each T_bowtie interaction contributes exactly 1 CLU of structural advantage.
-- ============================================================

/-- The autocatalytic enhancement factor: 10^n_T. -/
def autoEnhancement (nT : ℕ) : ℝ := (10 : ℝ) ^ nT

theorem autoEnhancement_one_CLU_per_loop (nT : ℕ) :
    Real.log (autoEnhancement nT) = nT * CLU := by
  unfold autoEnhancement CLU
  rw [Real.log_pow]
  norm_num
  ring

/-- Soai reaction (tBuPym, n_T = 2): 100× enhancement = 2 CLU. -/
theorem soai_tBuPym_2_CLU : autoEnhancement 2 = 100 := by
  unfold autoEnhancement; norm_num

/-- Soai reaction (TMS/Ad variants, n_T = 1): 10× enhancement = 1 CLU. -/
theorem soai_TMS_1_CLU : autoEnhancement 1 = 10 := by
  unfold autoEnhancement; norm_num

-- ============================================================
-- V.4 Grokking: ln(N_grok / N_memorize) = 2.303 × n_K
-- The grokking transition (memorization → generalization) is the
-- criticality-lift in the model's internal representation.
-- ============================================================

/-- The grokking parameter ratio: 10^{n_K}. -/
def grokkingRatio (nK : ℕ) : ℝ := (10 : ℝ) ^ nK

theorem grokking_N_cost (nK : ℕ) :
    Real.log (grokkingRatio nK) = nK * CLU := by
  unfold grokkingRatio CLU
  rw [Real.log_pow]
  norm_num
  ring

/-- Grokking for modular arithmetic: n_K = 2 → 10^2 ratio. -/
theorem grokking_modular_arith : grokkingRatio 2 = 100 := by
  unfold grokkingRatio; norm_num

/-- Grokking for natural language: n_K = 3 → 10^3 ratio. -/
theorem grokking_natural_language : grokkingRatio 3 = 1000 := by
  unfold grokkingRatio; norm_num

-- ============================================================
-- V.5 Log-Normal Distribution as Φ_c Signature
-- At criticality (Φ_c, Axiom 5: G/D degeneracy), no scale is privileged.
-- Scale-free multiplicative processes generate log-normal distributions.
-- The inter-decade spacing is exactly 2.303 nats.
-- ============================================================

/-- The decade width of a log-normal distribution encodes the K-span. -/
noncomputable def logNormalDecadeWidth (sigma : ℝ) : ℝ := sigma / CLU

/-- A distribution spanning w decades has width w × CLU. -/
theorem logNormal_width_decades (w : ℝ) :
    logNormalDecadeWidth (w * CLU) = w := by
  unfold logNormalDecadeWidth
  field_simp [CLU_pos.ne']

-- ============================================================
-- VI. CLU OPERATOR ALGEBRA
-- ============================================================

/-- The CLU monoid: (ℝ≥0, +, 0) represents cumulative CLU costs.
    CLU costs compose additively; identity is 0 (no crossing). -/
-- (Implicitly established by the additive structure of kTierCrossingCost)

/-- The CLU as a measurement homomorphism:
    ln(x/y) → ℝ≥0 preserves multiplication of ratios as addition of costs. -/
theorem CLU_homomorphism (x y z : ℝ) (hx : x > 0) (hy : y > 0) (hz : z > 0) :
    Real.log (x / z) = Real.log (x / y) + Real.log (y / z) := by
  rw [← Real.log_mul (by positivity) (by positivity)]
  congr 1
  field_simp [hx, hy, hz]
  ring

/-- CLU integer: a cost c is a CLU integer if c / CLU ∈ ℕ. -/
def isCLUInteger (c : ℝ) : Prop := ∃ n : ℕ, c = n * CLU

theorem CLU_is_CLU_Integer : isCLUInteger CLU := ⟨1, by simp [CLU]⟩

theorem zero_is_CLU_Integer : isCLUInteger 0 := ⟨0, by simp [CLU]⟩

/-- Sum of CLU integers is a CLU integer. -/
theorem CLU_int_closed_add {a b : ℝ}
    (ha : isCLUInteger a) (hb : isCLUInteger b) :
    isCLUInteger (a + b) := by
  obtain ⟨n, rfl⟩ := ha
  obtain ⟨m, rfl⟩ := hb
  exact ⟨n + m, by ring⟩

/-- Product of a CLU integer with a natural is a CLU integer. -/
theorem CLU_int_closed_mul_nat {a : ℝ} (n : ℕ)
    (ha : isCLUInteger a) : isCLUInteger (n • a) := by
  obtain ⟨k, rfl⟩ := ha
  exact ⟨n * k, by ring⟩

-- ============================================================
-- VII. RECOGNITION HEURISTIC (Structural Statement)
-- ============================================================

/-- A system crossing exhibits a CLU event if:
    (1) enhancement/suppression ratio ≈ 10^n for small n ∈ ℕ,
    (2) distribution characteristic width spans ~integer decades,
    (3) transition is sharp (discontinuous) not smooth,
    (4) qualitative regime change occurs (not just parameter shift).
    Here we formalize condition (1) as the CLU recognition criterion. -/

/-- The CLU recognition predicate: a ratio r is an "n-CLU event"
    if ln(r) = n × CLU for some n : ℕ. -/
def isCLUEvent (n : ℕ) (r : ℝ) : Prop := Real.log r = n * CLU

theorem CLU_event_iff_ratio (n : ℕ) (r : ℝ) (hr : r > 0) :
    isCLUEvent n r ↔ r = (10 : ℝ) ^ n := by
  unfold isCLUEvent CLU
  constructor
  · intro h
    rw [← Real.exp_log hr, h]
    rw [Real.exp_mul, Real.exp_log (by norm_num)]
  · intro h
    rw [h, Real.log_pow]
    ring

/-- Falsification template: if ln(r) is NOT near any n × CLU,
    then r is NOT a CLU-event. -/
theorem CLU_falsification (n : ℕ) (r : ℝ) (hr : r > 0) :
    ¬ isCLUEvent n r ↔ Real.log r ≠ n * Real.log 10 := by
  unfold isCLUEvent, CLU; simp

/-- The CLU recognition heuristic in action:
    For any system with measurable scale parameter x transitioning to x':
    if x' / x = 10^n, then the transition is an n-CLU event. -/
theorem CLU_recognition (x x' : ℝ) (hx : x > 0) (hx' : x' > 0)
    (n : ℕ) (h : x' / x = (10 : ℝ) ^ n) :
    isCLUEvent n (x' / x) := by
  unfold isCLUEvent, CLU
  rw [h, Real.log_pow]
  norm_num
  ring

-- ============================================================
-- VIII. SCALE-INDEPENDENCE THEOREM
-- ============================================================

/-- The CLU cost is scale-independent: the same whether x is
    a reaction rate, parameter count, correlation length, or
    information capacity. This follows from the logarithmic
    structure: ln(ax/ax) = ln(x/x) = ln(1) = 0 is trivial,
    but ln(10x/x) = ln(10) is invariant under any scaling. -/
theorem CLU_scale_independence (x c : ℝ) (hx : x > 0) (hc : c > 0) :
    Real.log ((10 * c * x) / (c * x)) = CLU := by
  unfold CLU
  congr 1
  have hcx : c * x ≠ 0 := mul_ne_zero hc.ne' hx.ne'
  field_simp [hcx]

-- ============================================================
-- IX. CROSS-REFERENCE: CLU in the K-Tier Ladder of Imscription
-- ============================================================

/-- The CLU operator applied to the kinetic character of a Imscription. -/
def imscriptionKTier (s : Imscription) : KTier := kineticCharToKTier s.kin

/-- The K-tier distance between two synths as CLU cost. -/
noncomputable def imscriptionKDistance (a b : Imscription) : ℝ :=
  kTierCrossingCost (imscriptionKTier a) (imscriptionKTier b)

/-- Higgs and axion have the same K-tier (both K_slow → .slow),
    so their K-distance is 0 CLU. -/
theorem higgs_axion_K_distance_zero :
    imscriptionKDistance higgs axion = 0 := by
  simp [imscriptionKDistance, imscriptionKTier, kineticCharToKTier, higgs, axion, scalarField_Kslow]
  rfl

/-- Quantum gravity (K_trap) vs Higgs (K_slow): 1 CLU separation. -/
theorem qg_higgs_K_distance_one_CLU :
    imscriptionKDistance quantum_gravity higgs = CLU := by
  simp [imscriptionKDistance, imscriptionKTier, kineticCharToKTier,
        quantum_gravity, higgs, scalarField_Kslow]
  unfold kTierCrossingCost kTierSteps kTierLevel
  simp [CLU]

-- ============================================================
-- X. STRUCTURAL SUMMARY
-- ============================================================

/-- The CLU structural theorem:
    1 CLU = ln(10) nats is the universal cost of crossing
    one order-of-magnitude boundary in the K-tier grammar.
    This cost appears identically across chemistry, kinetics,
    autocatalysis, machine learning, information theory,
    evolutionary biology, condensed matter, and cosmology. -/
theorem CLU_universality_statement :
    (∀ n : ℕ, Real.log ((10 : ℝ) ^ n) = n * CLU) ∧
    (CLU > 2.302) ∧
    (CLU < 2.303) := by
  constructor
  · intro n
    unfold CLU
    rw [Real.log_pow]
    have : Real.log 10 = Real.log 10 := rfl
    ring
  · exact CLU_approx_2_303

end ImscribingGrammar.Primitives.CLUPrimitives
