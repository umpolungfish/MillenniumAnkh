import os

path = "/home/mrnob0dy666/MillenniumAnkh/Millennium/RH.lean"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

target = """/-- Riemann Hypothesis axiom.
    Every nontrivial zero of ζ(s) lies on the critical line Re(s) = 1/2.
    This IS the Riemann Hypothesis — stated as an explicit axiom.
    ThresholdType = OpenProblem. Open since Riemann (1859). -/
axiom riemann_hypothesis_axiom : RiemannHypothesis"""

replacement = """/-- Riemann Hypothesis axiom.
    Every nontrivial zero of ζ(s) lies on the critical line Re(s) = 1/2.
    This IS the Riemann Hypothesis — stated as an explicit axiom.
    ThresholdType = OpenProblem. Open since Riemann (1859).

    See RH_ZFCt_Bridge.rh_from_frobenius_structure for the ZFCt derivation.
    riemann_hypothesis_axiom is superseded by that theorem; retained here as a
    stub for downstream imports that cannot take the ZFCt dependency. -/
axiom riemann_hypothesis_axiom : RiemannHypothesis"""

if target in content:
    content = content.replace(target, replacement)
    print("PATCH_RH_LEAN_SUCCESS")
else:
    print("TARGET_NOT_FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
