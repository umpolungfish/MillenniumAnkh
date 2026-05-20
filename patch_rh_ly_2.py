import os

path = "/home/mrnob0dy666/MillenniumAnkh/Millennium/RH_LeeYang_Bridge.lean"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the incorrectly placed rh_from_zfct theorem
incorrect_str = """theorem lee_yang_template :
    lee_yang_C13.polar = P_doublebarpipe →
    lee_yang_C13.crit  = odot_Ae →
    lee_yang_C13.claim :=
  fun _ _ => lee_yang_proved

  /-- RiemannHypothesis_as_C13 derived from the ZFCt Frobenius structure.
      rh_C13.claim = ∀ s, IsZetaZero s → s.re = 1/2, which follows from
      zeta_zeros_frobenius_fixed + theta_fixed_iff_critical. -/
  theorem rh_from_zfct :
      RiemannHypothesis_as_C13 :=
    fun s hs => (Millennium.RH_ZFCt.theta_fixed_iff_critical s).mp
      (Millennium.RH_ZFCt.zeta_zeros_frobenius_fixed s hs)"""

correct_template_str = """theorem lee_yang_template :
    lee_yang_C13.polar = P_doublebarpipe →
    lee_yang_C13.crit  = odot_Ae →
    lee_yang_C13.claim :=
  fun _ _ => lee_yang_proved"""

content = content.replace(incorrect_str, correct_template_str)

# Place it correctly after def RiemannHypothesis_as_C13
rh_c13_def = "def RiemannHypothesis_as_C13 : Prop := rh_C13.claim"
rh_c13_with_theorem = """def RiemannHypothesis_as_C13 : Prop := rh_C13.claim

  /-- RiemannHypothesis_as_C13 derived from the ZFCt Frobenius structure.
      rh_C13.claim = ∀ s, IsZetaZero s → s.re = 1/2, which follows from
      zeta_zeros_frobenius_fixed + theta_fixed_iff_critical. -/
  theorem rh_from_zfct :
      RiemannHypothesis_as_C13 :=
    fun s hs => (Millennium.RH_ZFCt.theta_fixed_iff_critical s).mp
      (Millennium.RH_ZFCt.zeta_zeros_frobenius_fixed s hs)"""

content = content.replace(rh_c13_def, rh_c13_with_theorem)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("PATCH_SUCCESS_2")
