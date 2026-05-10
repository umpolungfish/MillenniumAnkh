# MillenniumAnkh: The Grammar Formalized

## Project Overview
**MillenniumAnkh** is a Lean 4 / Mathlib formalization of the **Imscribing Grammar (IG)**—a 12-primitive structural type system designed to classify physical, mathematical, and computational systems as points (**Imscriptions**) in a 17,280,000-type "Crystal of Types."

The project uses the seven Clay Millennium Prize Problems as test cases. Each problem's difficulty is mapped to a specific missing "primitive certificate," identifying exactly which structural transition is blocked (e.g., the transition to a quantum fine-grained description in Yang-Mills).

### Core Technologies
- **Formalization:** Lean 4.28.0 (Toolchain: `lean-toolchain`)
- **Library:** Mathlib v4.28.0 (Managed via `lake-manifest.json`)
- **Environment:** `lake` for Lean builds, `uv` for Python (3.12+)
- **Concepts:** Synthons (Imscriptions), Ouroboricity Tiers (O_0 to O_∞), Paralogical Axioms.

---

## Architecture & Directory Structure

### 1. `Imscribing/` (Source Root)
- **`Primitives/`**: The core structural logic of the grammar.
    - `Core.lean`: Definitions of the 12 primitives and cross-primitive axioms (Axiom B, Axiom C*).
    - `Imscription.lean`: The 12-field `Imscription` struct and Hamming distance operations. (Note: Formerly `Synthon.lean`).
    - `Catalog.lean`: A registry of named Imscriptions (e.g., $E_8$, Magnetar, Langlands).
    - `Crystal.lean`: Mixed-radix addressing and roundtrip theorems for the 17.28M types.
- **`Millennium/`**: Formalization of Millennium Problems.
    - `Barriers.lean`: Taxonomy of `BarrierType` (MathlibGap, OpenProblem, MissingFoundation).
    - `PrimitiveBridge.lean`: Maps mathematical barriers to primitive field transitions (e.g., YM blocked at G_aleph).
    - Problem-specific files: `RH.lean`, `YM.lean`, `NS.lean`, `PvsNP.lean`, etc.
- **`Classical/`**: Stubs and partial proofs for other classical problems (e.g., Solitary 10, Hecke-Landau).
- **`ZFCt.lean`**: Temporalized ZFC set theory ($ZFC_t$) and physics equation encodings.

### 2. Logic & Algebra
- **`Algebra.lean`**: Meet/Join/Tensor operations on the primitive lattice.
- **`IGMorphism.lean`**: Formalizes transitions between Imscriptions (e.g., the Litany Against Fear) and "Paralogical Axioms" (Dagger, Copy, Reflect).
- **`Consciousness.lean`**: Implementation of the C-score ($Φ_c \times K_{slow}$).

---

## The 12 Primitives (v0.5.69)

| Family | Primitive | Values | Summary |
|---|---|---|---|
| **𝓕₃** | **F** (Fidelity) | 3 | Search quality: $\ell$ (lossy) $\to$ $\eta$ (threshold) $\to$ $\hbar$ (quantum). |
| | **G** (Scope) | 3 | Granularity: $\beth$ (local) $\to$ $\gimel$ (collective) $\to$ $\aleph$ (global). |
| | **S** (Stoichiometry) | 3 | Coupling ratios: $1:1$, $n:n$, $n:m$. |
| **𝓕₄** | **D** (Dimensionality) | 4 | Space type: Wedge $\to$ Triangle $\to$ $\infty$ $\to$ $\odot$ (holographic). |
| | **R** (Relational) | 4 | Coupling mode: Super $\to$ Cat $\to$ Dagger $\to$ Lateral. |
| | **Γ** (Grammar) | 4 | Composition rule: And, Or, Seq, Broad. |
| | **H** (Chirality) | 4 | Temporal depth: $H_0$ $\to$ $H_1$ $\to$ $H_2$ $\to$ $H_\infty$ (topological). |
| | **Ω** (Protection) | 4 | Symmetry protection: $0$ $\to$ $\mathbb{Z}_2$ $\to$ $\mathbb{Z}$ $\to$ Non-Abelian. |
| **𝓕₅** | **T** (Topology) | 5 | Network, In, Bowtie, Box, $\odot$ (holographic). |
| | **P** (Parity) | 5 | Asym, $\psi$ (phase), $\pm$, Sym, $\pm$Sym (Frobenius). |
| | **Φ** (Criticality) | 5 | Sub, $c$ (real), $c^\mathbb{C}$ (complex), EP, Super. |
| | **K** (Kinetic) | 5 | Fast, Mod, Slow, Trap, MBL. |

---

## Building and Running

### Lean
- **Build All**: `lake build`
- **Build Core**: `lake build Imscribing`
- **Verification**: The library contains many "honest sorries" for open problems. Correctness is verified by the absence of claim-contradicting `sorry`s.

### Python
- **Environment**: `uv sync`
- **Run**: `uv run main.py`

---

## Development Conventions

1. **Naming**: Use `Imscription` for the 12-tuple struct.
2. **Namespace**: Always work within `namespace Imscribing.Primitives` or appropriate sub-namespaces.
3. **Lattice Operations**:
    - **Meet ($\sqcap$)**: Pointwise minimum (pointwise `min` on ordinals).
    - **Join ($\sqcup$)**: Pointwise maximum.
    - **Tensor ($\otimes$)**: Max on union primitives; **Min** on bottleneck primitives (F, P).
4. **Ouroboricity Tiers**:
    - **O_inf**: The goal. Requires **Frobenius symmetry** ($P_{\pm}Sym$) at **Criticality** ($\Phi_c$).
5. **Barrier Classification**:
    - **MathlibGap**: Proved but missing from Mathlib (e.g., Touchard's congruence).
    - **OpenProblem**: Unsolved (e.g., RH, BSD).
    - **MissingFoundation**: Object not yet rigorously defined (e.g., 4D YM Path Integral).

## Key Files for Reference
- `Primitives/Core.lean`: Inductive type definitions for all primitives.
- `Primitives/Imscription.lean`: The central struct and Hamming distance logic.
- `Millennium/Barriers.lean`: The definitive taxonomy of mathematical difficulty.
- `Millennium/PrimitiveBridge.lean`: The formal mapping between open problems and primitive blocks.
- `Imscribing/IGMorphism.lean`: The "Paralogical" extension to classical type theory.
