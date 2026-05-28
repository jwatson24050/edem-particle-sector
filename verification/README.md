# EDEM Verification Scripts

Independent computational verification of results from:
**Entropy Driven Expansion Model — Particle Sector** (Paper B).

Each script is self-contained, prints clearly labelled output, and asserts its
own headline numbers, so a silent regression cannot pass unnoticed — a non-zero
exit code means a check failed. All scripts use the Python 3 standard library;
only `pmns_unitary_embed.py` additionally needs NumPy.

```bash
pip install -r ../requirements.txt   # NumPy, for pmns_unitary_embed.py only
```

## Quick start

Run the three most important scripts first — the core mass claim, the null-cone
origin of the moduli, and the PMNS uniqueness scan:

```bash
python verify_masses.py              # Core claim: all 10 masses from one constant
python verify_cooperative_moduli.py  # Null cone forces {13,17,43}
python pmns_scan.py                  # PMNS angles: 1 triple in 983 fractions
```

## All scripts

### Core framework verification

| Script | Tests | Key result |
|---|---|---|
| `verify_masses.py` | Postulate P2: m(P) = K/t(P) | 10 masses from K = m_top alone |
| `verify_gauge.py` | Postulate P4: gauge holonomy | sin²θ_W = 0.2310; T_CR to 61 ppm |
| `verify_cooperative_moduli.py` | P1: null cone → {13,17,43} | Moduli forced, not tuned |
| `verify_electron_selection.py` | T_ELECTRON: unique electron prime | competitors → 0 via 3 steps |

### PMNS sector verification

| Script | Tests | Key result |
|---|---|---|
| `pmns_scan.py` | Hypothesis class H uniqueness | 1 of 983 fractions matches all 3 angles |
| `pmns_pairs.py` | 8 non-EDEM pairs | None have an EDEM derivation |
| `pmns_sector_uniqueness.py` | 6-permutation exhaustive test | Only EDEM assignment < 1σ |
| `pmns_unitary_embed.py` | Full 3×3 matrix compatibility | Compatible for any δ |
| `pmns_rigidity.py` | 104 epoch-prime triples | Only {2,3,5} achieves < 1σ |
| `pmns_mechanism.py` | vs. standard flavor models | TBM excluded 30σ; EDEM correct |

---

## Script details

### `verify_masses.py`
- **Tests:** Postulate P2 — every charged fermion mass is `m(P) = K/t(P)` with
  the divisor recursion `S(n) = S(n-1) + 1/(d(n)-2)` at composites, and the one
  empirical input `K = m_top = 172,570 MeV`.
- **Runtime:** ~1–2 s (sieves divisor counts to ≈1.9 M, then one recursion sweep
  with a progress line every 200,000 steps).
- **Key output to check:** `t(5) = 1.000000` exactly (Theorem T17); the heavy
  sector (top, bottom, tau, charm, proton, muon, electron) reproduced to ≤ ~1.4 %.
- **Caveat — light quarks (open problem #5):** strange/down/up carry the largest
  individual errors (down ≈ −12 %, up ≈ +11 %). This is the *documented* EDEM
  open problem: the script reproduces the known ratio `m_d/m_s = 1/23.9` (vs the
  PDG ratio 1/20.0, −16 %). It is a feature of the framework, not a code defect.

### `verify_gauge.py`
- **Tests:** Postulate P4 — `g_k = ln(p_k)/d(n_k)` over the epochs
  `n_k = (primorial_k)²`, plus Theorem T_CR (cross-epoch running).
- **Runtime:** instant.
- **Key output to check:** `sin²θ_W = ln(2)/3 = 0.23105` (PDG 0.23122, 0.07 %);
  `α_s = ln(3)/9 = 0.12207` (PDG 0.1180, 3.4 % pre-RG); gluons `p₂²−1 = 8`, weak
  bosons `p₁²−1 = 3`; natural QCD scale `μ_QCD = M_Z/2^(1/3) ≈ 72.4 GeV`.
- **Caveat — T_CR metric:** the one-loop identity
  `1/α_s(M_Z) − 1/α_s,EDEM = (β₀/2π)·sin²θ_W` holds to **61 ppm of the inverse
  coupling** `1/α_s` (equivalently, the absolute discrepancy is ≈0.006 % of
  `1/α_s`). The α_s residual of 3.4 % is the expected pre-RG scale offset.

### `verify_cooperative_moduli.py`
- **Tests:** Postulate P1 — the cooperative moduli {13, 17, 43} forced by the
  null cone `ds²(n) = −X₂² + X₃² + X₅² + X₇²`; the Φ₆ tower; Theorem 1
  (`Φ₆(n) = 6n+1 ⇔ n = 7`); Corollary 1 (`ord₄₃(7) = 6`); and the
  three-generation theorem (Φ₆ tower terminates at Φ₆(43)=1807=13×139).
- **Runtime:** instant.
- **Key output to check:** `ds²(6) = 0` is the minimal null composite; iterated
  tower `2→3→7→43→1807` yields the three primes {3,7,43}; `r_tau, r_mu, r_p =
  13, 17, 43`.
- **Caveat — naming:** in this script `σ` denotes the *lattice constant*
  `n_null = τ·σ = 6` (so `ord₄₃(7) = 6 = σ`). This is distinct from the *spatial
  prime* `σ = 3` used in the PMNS scripts — two different uses of the symbol in
  Paper B.

### `verify_electron_selection.py`
- **Tests:** Paper B §3.6 — the electron prime `P_e = 6·23²·601 − 1 =
  1,907,573` is the unique electron-class survivor of a three-step modular
  cascade: Step A (QR mod 23), Step B (43 ∣ s+1), Step C (7 ∣ s+1).
- **Runtime:** < 1 s (trial-division primality; largest P ≈ 5.3 M).
- **Key output to check:** **zero** competitors survive all three steps, while
  `P_e` (secondary `s = 601`) passes A, B and C, and 601 is prime → unique
  survivor.
- **Caveat — counts:** this script uses the *simplified* lepton/electron-class
  checks specified for it, which admit a larger candidate pool (≈105
  electron-class candidates → 104 competitors) than Paper B's full enumeration
  (309 lepton candidates → 8 electron-class competitors). The cascade and the
  unique-survivor conclusion are identical; the intermediate counts differ
  because the full epoch/foam conditions are not reproduced here.

### `pmns_scan.py`
- **Tests:** builds the hypothesis class **H** of fractions reachable from ≤ 2
  elements of `G = {2,3,5,6,7,13,17,43}`; counts members near each measured angle.
- **Runtime:** instant. **Key output:** `|H| = 983`; θ₁₂ and θ₂₃ have exactly 3
  candidates within 0.1σ, θ₁₃ has **0** (1/45 is degree-3, a derivation not a fit).

### `pmns_pairs.py`
- **Tests:** the 3×3 = 9 candidate (θ₁₂, θ₂₃) pairs against the EDEM theorem
  register. **Key output:** only (4/13, 6/11) is theorem-derived; the four
  foreign fractions {26/85, 15/49, 65/119, 23/42} have no derivation.

### `pmns_sector_uniqueness.py`
- **Tests:** all 6 sector→angle permutations and all 104 epoch-prime triples.
  **Key output:** EDEM assignment 0.053σ vs next-best 18.3σ; only (2,3,5) fits.

### `pmns_unitary_embed.py` *(requires NumPy)*
- **Tests:** the full 3×3 PMNS matrix from the EDEM angles. **Key output:** |U|²
  agrees with PDG to < 0.001 for any δ; third column (1/45, 8/15, 4/9) and first
  row (44/65, 176/585, 1/45) are exact rationals; Jarlskog J = 0.0335·sin δ.

### `pmns_rigidity.py`
- **Tests:** sensitivity of each structural handle and the joint 104-triple scan.
  **Key output:** r_tau moves 1σ in < 0.56 units, D_null in < 0.43; only (2,3,5)
  keeps max|pull| < 1σ.

### `pmns_mechanism.py`
- **Tests:** EDEM vs Tribimaximal (A4), Bimaximal, Golden-Ratio, PDG best fit,
  plus a vocabulary translation table. **Key output:** every θ₁₃ = 0 pattern is
  excluded at 31.7σ; TBM misses all three angles (+2.0σ, −2.2σ, −31.7σ).

---

## Notes
- Python 3.8+ (uses f-strings and `fractions.Fraction`).
- Only `pmns_unitary_embed.py` imports NumPy; the rest are standard library only.
- Each script exits 0 on success; an `AssertionError` (exit 1) flags a broken
  invariant.
