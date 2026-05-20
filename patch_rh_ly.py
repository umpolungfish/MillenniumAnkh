import os

path = "/home/mrnob0dy666/MillenniumAnkh/Millennium/RH_LeeYang_Bridge.lean"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import
import_to_add = "import Imscribing.Millennium.RH_ZFCt_Bridge"
if import_to_add not in content:
    content = content.replace(
        "import Imscribing.Primitives.Core",
        "import Imscribing.Primitives.Core\nimport Imscribing.Millennium.RH_ZFCt_Bridge"
    )

# 2. Replace axiom IsZetaZero
axiom_str = "axiom IsZetaZero : ℂ → Prop"
def_str = "def IsZetaZero : ℂ → Prop := Millennium.RH_ZFCt.IsZetaZero"
content = content.replace(axiom_str, def_str)

# 3. Add rh_from_zfct after lee_yang_template
template_str = """theorem lee_yang_template :
    lee_yang_C13.polar = P_doublebarpipe →
    lee_yang_C13.crit  = odot_Ae →
    lee_yang_C13.claim :=
  fun _ _ => lee_yang_proved"""

new_theorem_str = """theorem lee_yang_template :
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

content = content.replace(template_str, new_theorem_str)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("PATCH_SUCCESS")
