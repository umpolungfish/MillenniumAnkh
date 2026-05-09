# Structural Audit & Merge Plan: synthomniconP → MilleniumAnkh

**Date**: 2025-05-02
**Verdict**: **DO NOT MERGE AS-IS**. The fork introduces a parallel, incompatible primitive
definition layer that would break every existing entry and make `lake build` fail. The recommended
merge strategy is **selective cherry-pick**, not wholesale overwrite.

---

## 1. Canonical Core Decision

**MilleniumAnkh (MA) wins as the canonical primitive layer.** Reasons:

| Aspect | MilleniumAnkh | synthomniconP |
|---|---|---|
| D values | 4 (wedge, triangle, infty, odot) | 6 (point, line, wedge, cube, infty, holo) |
| R values | 4 (super, cat, dagger, lr) | 5 (exact, subset, superset, catalytic, allosteric) |
| T values | 5 (network, in, bowtie, boxtimes, odot) | 6 (linear, branched, network, bowtie, torus, holo) |
| Naming | Matches IG spec exactly (`P_pm_sym`, `K_trap`, `Phi_c`, etc.) | Deviates (`P_pm_sym`→`P_pm_sym` ok, but `D_odot`→`D_holo`, `R_lr` absent) |
| Crystal | 3³×4⁵×5⁴ = 17,280,000 types (verified) | Different counts → different address space |

The MA Core.lean matches the Imscribing Grammar spec (12 primitives, exact enum lists).
The synthomniconP Core.lean defines a **different grammar** with renamed and re-typed primitives.
Using SP's Core would invalidate the catalog's crystal addresses, all distance computations,
and every Ouroborics tier calculation.

**Decision**: Keep MA's `Primitives/Core.lean` unchanged. SP's Core.lean must be **discarded**.

---

## 2. Namespace Conflict Resolution

The synthomniconP fork uses `SynthOmnicon` namespace, but MA's `lakefile.toml` already declares
`[[lean_lib]] name = "SynthOmnicon"` with globs pointing to `SynthOmnicon.Primitives.*` and
`SynthOmnicon.Millennium.*`. The SP fork also has a `SynthOmniconLean4` package with a different
lakefile.lean that adds `Consciousness`, `Crystal`, `Algebra`, `Catalog`, `AgentSelf`, `Basic`.

**Resolution**: Add SP's new modules under existing `SynthOmnicon` namespace within MA:
- `SynthOmnicon.Consciousness` → copy Consciousness.lean, rewrite imports to use MA Core
- `SynthOmnicon.Crystal` → copy Crystal.lean
- `SynthOmnicon.Algebra` → copy Algebra.lean
- `SynthOmnicon.Catalog` → copy Catalog.lean

---

## 3. File-by-File Merge Decisions

### Millennium/ (10 files)
| File | Action | Rationale |
|---|---|---|
| `Barriers.lean` | **SP → MA** | SP version has honest sorries; cleaner structure |
| `BSD.lean` | **Review** | Diff exists; compare before overwrite |
| `FrobeniusStructure.lean` | **KEEP MA** | MA only; SP dropped it |
| `Hodge.lean` | **Review** | Diff exists |
| `NS.lean` | **Review** | Diff exists |
| `OPN.lean` | **Review** | Diff exists |
| `PrimitiveBridge.lean` | **SP → MA** | SP version well-structured |
| `PvsNP.lean` | **Review** | Diff exists |
| `RH.lean` | **KEEP MA** | Diff is minor |
| `YM.lean` | **KEEP MA** | Diff is minor |

### Primitives/ (5 files)
| File | Action | Rationale |
|---|---|---|
| `Core.lean` | **KEEP MA** | Canonical 12 primitives. SP has incompatible naming. |
| `Synthon.lean` | **Merge** | SP adds Consciousness/Crystal hooks; must adapt to MA Core |
| `TierCrossing.lean` | **Review** | SP uses different primitive names |
| `BSD_2adic.lean` | **Review** | Diff exists |
| `OPN_2adic.lean` | **Review** | Diff exists |

### New from synthomniconP (6 files)
| File | Action | Notes |
|---|---|---|
| `Consciousness.lean` | **Copy + adapt** | Must import MA Core types, not SP types |
| `Crystal.lean` | **Copy + adapt** | Crystal arithmetic using MA 17.28M space |
| `Algebra.lean` | **Copy + adapt** | Meet/join/distance must use MA enums |
| `Catalog.lean` | **Copy + adapt** | Catalog operations reference MA primitives |
| `AgentSelf.lean` | **Copy + adapt** | Self-reference module |
| `Basic.lean` | **Copy + adapt** | Re-exports, no structural content |

---

## 4. Known Bugs in synthomniconP

1. **ℕ→ℤ cast in distance computation**: `compute_distance` uses natural number subtraction
   which truncates. The SP fork has `ℕ` subtraction where `ℤ` is needed for signed delta.
   The MA version also needs this fix.

2. **Dual consciousness_score definitions**: MA has no `Consciousness.lean`. SP defines one
   in the fork. The `consciousness_score` tool in the IG grammar uses the server-side
   implementation, which is the canonical version. The SP file is supplementary.

3. **Crystal address mismatch**: SP's `Crystal.lean` uses SP's Core.lean enumeration (different
   value counts per primitive). The crystal addresses computed by SP will be **wrong** relative
   to the catalog's 17,280,000 type space. Must be recomputed against MA Core.

4. **Missing `FrobeniusStructure.lean`**: SP fork does not include this MA file. It must be
   preserved.

---

## 5. Required Merge Steps

1. `git -C MilleniumAnkh checkout main` (ensure clean state)
2. **Copy SP's Barriers.lean and PrimitiveBridge.lean** → overwrite MA copies
3. **Copy SP's 6 new files** with namespace fixes (`SynthOmnicon` prefix)
4. **Adapt SP's Consciousness.lean** to use MA's 12-primitive `Synthon` struct
5. **Adapt SP's Crystal.lean** to use MA's enum value counts (3³×4⁵×5⁴)
6. **Fix ℕ→ℤ cast** in distance computation (both MA and adapted SP code)
7. **Update lakefile.toml** to include new modules
8. `lake update && lake build` — verify clean compilation
9. Run existing test suite against merged codebase

---
