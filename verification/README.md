# PMNS verification scripts

These six scripts independently reproduce the PMNS (neutrino mixing) results of
Paper B. They are written to **referee-response quality**: each is
self-contained, prints clearly labelled output, and asserts its own headline
numbers so that a silent regression cannot pass unnoticed. A non-zero exit code
means a check failed.

```bash
pip install -r ../requirements.txt   # only NumPy, only for pmns_unitary_embed.py
python pmns_scan.py
```

The three EDEM predictions under test are

| angle | EDEM | formula | PDG 2022 (NH) | pull |
|---|---|---|---|---|
| sin²θ₁₂ | 4/13 = 0.30769 | τ²/r_τ | 0.307 ± 0.013 | +0.053σ |
| sin²θ₂₃ | 6/11 = 0.54545 | n_null/(n_null+g) | 0.546 ± 0.021 | −0.026σ |
| sin²θ₁₃ | 1/45 = 0.02222 | 1/(σ²g) | 0.02220 ± 0.00070 | +0.032σ |

with epoch primes (τ, σ, g) = (2, 3, 5).

## Quick start — run these three first

These three answer the questions a sceptical reader asks first: *could this have
happened by chance, is the assignment unique, and is it fine-tuned?*

```bash
python pmns_scan.py               # 1. Could three random fractions have fit? (|H| = 983)
python pmns_sector_uniqueness.py  # 2. Is the sector->angle assignment unique? (1 of 6, 1 of 104)
python pmns_rigidity.py           # 3. Is it fine-tuned? (every handle is sub-unit fragile)
```

## What each script tests

### `pmns_scan.py` — hypothesis-class scan
Builds **H**, the class of all fractions whose numerator and denominator are each
reachable from at most two elements of the primitive set
`G = {2,3,5,6,7,13,17,43}`. Reports `|H| = 983`, then counts how many members lie
within 0.1σ / 0.5σ / 1σ of each measured angle.
**Read it as:** θ₁₂ and θ₂₃ each have exactly 3 candidates within 0.1σ; θ₁₃ has
**none** — because 1/45 = 1/(σ²g) is a degree-three product outside H. So θ₁₃ is a
*derivation* (theorem T_UNIT_RESIDUE), not a fished-out coincidence.

### `pmns_pairs.py` — are the rival pairs derivable?
The 3 × 3 = 9 candidate (θ₁₂, θ₂₃) pairs are all numerically allowed. Tests which
have both members in the **EDEM theorem register** (the closed list of fractions
the postulates actually prove).
**Read it as:** exactly one pair, (4/13, 6/11), is theorem-derived. The four
foreign fractions {26/85, 15/49, 65/119, 23/42} live in H but have no derivation,
so the other 8 pairs are arithmetic coincidences.

### `pmns_sector_uniqueness.py` — is the assignment unique?
(A) Tries all 6 ways to attach the three sector formulas to the three angles.
(B) Varies the epoch primes over all 104 ordered triples τ<σ<g.
**Read it as:** the EDEM assignment is the only good fit — max|pull| = 0.053σ vs a
next-best of 18.3σ (others 400–748σ); and only (τ,σ,g) = (2,3,5) survives the
104-triple scan.

### `pmns_unitary_embed.py` — full 3×3 unitary embedding *(needs NumPy)*
Builds the complete PMNS matrix from the EDEM angles in the standard
parametrisation.
**Read it as:** |U|² agrees with the PDG matrix to < 0.001 for any δ; the third
column (1/45, 8/15, 4/9) and first row (44/65, 176/585, 1/45) are exact rationals
that sum to 1; √6 = √(τσ) = √(n_null) is the characteristic surd of the columns-1&2
block; and the Jarlskog invariant is J = 0.0335·sin(δ).

### `pmns_rigidity.py` — anti-tuning / rigidity study
Nudges each structural handle (r_τ = 13, D_null = 11, σ²g = 45, n_null = 6) and
watches the fit degrade; then runs the joint 104-triple scan.
**Read it as:** r_τ moves 1σ in < 0.56 units, D_null in < 0.43 units; only (2,3,5)
keeps max|pull| < 1σ. The predictions are rigid, not tuned. (σ²g = 44 and 46 are
individually within 1σ of θ₁₃ but are excluded because T_SPATIAL_SUM proves
σ²g = r_p + τ = 43 + 2 = 45.)

### `pmns_mechanism.py` — EDEM vs standard flavour models
Compares EDEM against Tribimaximal (A4), Bimaximal, Golden-Ratio and the PDG
best fit, and prints a vocabulary translation table.
**Read it as:** every classic θ₁₃ = 0 pattern is excluded at 31.7σ by the measured
reactor angle; Tribimaximal misses on all three angles (+2.0σ, −2.2σ, −31.7σ), so
EDEM is a different point, not a perturbative correction to TBM.

## Notes
- Python 3.8+ (uses f-strings and `fractions.Fraction`).
- Only `pmns_unitary_embed.py` imports NumPy; the rest are standard library only.
- Each script exits 0 on success; an `AssertionError` (exit 1) flags a broken
  invariant.
