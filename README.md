# Entropic Discrete Emergence Model — Particle Sector
**Author:** J. Watson · Independent Researcher  
**Status:** Preprint — May 2026  
**Papers:** [Paper A (math note)](#paper-a) · [Paper B (physics)](#paper-b)

---

## Summary

EDEM is a theoretical physics framework proposing that the Standard Model
particle spectrum is the mathematical shadow of a {2,3,5,7}-smooth discrete
Minkowski lattice. Elementary particles are identified with prime integers
satisfying cooperative selection conditions on this lattice. Masses follow from
**m(P) = K/t(P)**, where t(P) is the accumulated divisor cost of reaching prime
P and **K = m_top = 172,570 MeV** is the single empirical input. The framework
derives — not fits — the masses of all ten charged SM fermions, the electroweak
mixing angle, the strong coupling, and the three PMNS neutrino mixing angles. It
asserts five explicit physical postulates, states kill conditions for each, and
identifies all open problems.

## Key predictions

| Observable | EDEM Prediction | PDG 2022 | Pull | Status |
|---|---|---|---|---|
| sin²θ₁₂ (solar) | 4/13 = 0.3077 | 0.307 ± 0.013 | +0.053σ | ✓ |
| sin²θ₂₃ (atmospheric) | 6/11 = 0.5455 | 0.546 ± 0.021 | −0.026σ | ✓ |
| sin²θ₁₃ (reactor) | 1/45 = 0.02222 | 0.02220 ± 0.00070 | +0.032σ | ✓ |
| Neutrino hierarchy | Normal (proved) | NH preferred | — | ✓ |
| sin²θ_W | ln(2)/3 = 0.23105 | 0.23122 | 0.07% | ✓ |
| τ mass | 1,768.9 MeV | 1,776.86 MeV | −0.45% | ✓ |
| μ mass | 105.64 MeV | 105.658 MeV | −0.02% | ✓ |
| e mass | 0.5106 MeV | 0.51100 MeV | −0.08% | ✓ |
| proton mass | 937.03 MeV | 938.272 MeV | −0.13% | ✓ |

All PMNS angles simultaneously within 0.053σ. Zero free parameters beyond
K = m_top.

## The five physical postulates

| Postulate | Physical claim | Key kill condition |
|---|---|---|
| **P1** | {2,3,5,7}-smooth discrete Minkowski lattice; p₁=2 temporal | Different null-cone structure giving a consistent particle sector |
| **P2** | Particles are frozen eddies; m(P) = K/t(P); K = m_top | Any SM fermion mass >5% from K/t(P) after RG |
| **P3** | Three generations from Φ₆ tower termination at n₁=4, n₂=36, n₃=900 | Fourth charged-fermion generation; confirmed inverted hierarchy |
| **P4** | Gauge couplings from epoch holonomy; g_k = ln(pₖ)/d(nₖ) | sin²θ_W outside [0.229, 0.233] at 3σ at M_Z |
| **P5** | PMNS = rotation from cooperative-fiber (charged-lepton) basis to path-eigenstate (neutrino) basis | Any mixing angle outside its 3σ PDG window; confirmed inverted hierarchy |

## Two-paper architecture

<a name="paper-a"></a>
**Paper A** (`papers/EDEM_Paper_A_Note_v2.docx`) — *math.NT*. Pure arithmetic.
Proves four theorems about the σ-lattice and the Φ₆-tower and their
intersection. No physical claims are made. It can be verified by a number
theorist with no knowledge of particle physics, and is suitable for the
**math.NT** or **math.CO** arXiv categories.

<a name="paper-b"></a>
**Paper B** (`papers/EDEM_Paper_B_v73.docx`) — *hep-ph / hep-th*. Physics. Maps
the arithmetic of Paper A onto the Standard Model under five explicit physical
postulates. Every claimed derivation is labelled **theorem**, **postulate**,
**conjecture**, or **open problem**, and the distinction is always marked.

The logical direction is:

> **physical postulate → mathematical consequence → experimental prediction**

This is *not* numerology. The physical interpretation is the axiom; the
arithmetic is its proof.

## Verification scripts

The `verification/` directory contains Python scripts that independently verify
the PMNS sector results. All scripts require only the Python 3 standard library
(plus NumPy for the floating-point matrix work in one script).

```bash
pip install -r requirements.txt
cd verification
python pmns_scan.py               # Hypothesis class H scan and uniqueness
python pmns_pairs.py              # Verifies all 8 non-EDEM pairs have no EDEM derivation
python pmns_sector_uniqueness.py  # 6-permutation exhaustive test
python pmns_unitary_embed.py      # Full 3x3 unitary matrix compatibility
python pmns_rigidity.py           # Rigidity study: 104 epoch prime triples
python pmns_mechanism.py          # Comparison with standard flavor symmetry models
```

All scripts are self-contained and print their results to stdout. See
[`verification/README.md`](verification/README.md) for what each one tests and
how to read its output.

## Citation

If you use this work, please cite:

> Watson, J. *"Entropic Discrete Emergence Model: The Particle Sector."* Preprint, 2026.

> Watson, J. *"A Note on the Intersection of the σ-Lattice and the Sixth Cyclotomic Tower."* Preprint, 2026.

## Open problems

1. **Series Resistance Theorem** (Step 4 of the α derivation) — the formal
   derivation that G(n₁→n₂) = 1/∑(d(nᵢ)−2) from □_disc for unique monotone
   paths. Completing this closes the derivation of the propagator decay constant
   α = log(12)/(2 log(3)).
2. **CP-violating phase δ** — the Jarlskog coefficient is J ≈ 0.0335·sin(δ) in
   EDEM notation. No current theorem determines sin(δ).
3. **Columns 1–2 of U_PMNS** — the μ and τ row elements in the ν₁, ν₂ columns are
   irrational (involving √5 and √6) and δ-dependent. Their derivation from P5 is
   open.
4. **Neutrino mass splittings** — Δm² from the path-node divisor structure is not
   yet computed.
5. **Light-quark mass ratio** — m_d/m_s = 1/23.9 vs PDG 1/20.0 (−16%); an open
   arithmetic problem in t(P_d)/t(P_s).
6. **P4 derivation** — full derivation of g_k = ln(pₖ)/d(nₖ) from P1 alone.

## License

MIT — see [`LICENSE`](LICENSE).
