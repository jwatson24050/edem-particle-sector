#!/usr/bin/env python3
"""
pmns_mechanism.py  --  EDEM vs standard discrete-flavour-symmetry models
========================================================================

WHAT THIS SCRIPT TESTS
----------------------
Before the reactor angle theta_13 was measured (Daya Bay, 2012), the leading
theoretical mixing patterns -- Tribimaximal (A4), Bimaximal, Golden-Ratio --
all PREDICTED theta_13 = 0.  EDEM instead predicts sin^2(theta_13) = 1/45, a
nonzero rational.  This script:

  1. tabulates each pattern's three angles and their pulls against the data;
  2. shows every theta_13 = 0 pattern is excluded at > 30 sigma by the measured
     reactor angle;
  3. shows the flagship Tribimaximal point misses on ALL three angles
     (+2.0 sigma, -2.2 sigma, -31.7 sigma) -- so EDEM is NOT a small perturbative
     correction sitting on top of TBM, but a different point entirely;
  4. prints the vocabulary translation table mapping standard HEP flavour-model
     language onto its EDEM realisation.

EXPECTED OUTPUT (the result a referee should reproduce)
-------------------------------------------------------
  * EDEM max|pull| ~ 0.05 sigma; TBM/BM/GR all have a theta_13 pull near -31.7 sigma.
  * TBM pulls: theta_12 = +2.0, theta_23 = -2.2, theta_13 = -31.7 sigma.
  * EDEM's shifts away from TBM are comparable across all three angles -> not
    perturbative in theta_13 alone.

Standard library only.
"""

# ---------------------------------------------------------------------------
# Measured PMNS values (NuFit 5.2 / PDG 2022, NH): (central, 1-sigma).
# ---------------------------------------------------------------------------
PDG = {
    'th12': (0.307,   0.013),
    'th23': (0.546,   0.021),
    'th13': (0.02220, 0.00070),
}
KEYS = ['th12', 'th23', 'th13']

# (label, sin2_12, sin2_23, sin2_13, origin)
PATTERNS = [
    ("EDEM (proved)",     4 / 13, 6 / 11, 1 / 45,  "P5: Layer-1/Layer-3 basis mismatch"),
    ("Tribimaximal (A4)", 1 / 3,  1 / 2,  0.0,     "Harrison-Perkins-Scott 2002"),
    ("Bimaximal (BM)",    1 / 2,  1 / 2,  0.0,     "Barger et al. 1998"),
    ("Golden ratio (GR)", 0.276,  1 / 2,  0.0,     "Romanino 2004 (approx)"),
    ("PDG 2022 best-fit", 0.307,  0.546,  0.02220, "NuFit 5.2 NH"),
]

TRANSLATION = [
    ("Flavor symmetry group G",   "{2,3}-smooth multiplicative semigroup (derived)"),
    ("Residual G_nu",             "Unique monotone path 4->12->36 (T_PATH_EIGENSTATES)"),
    ("Residual G_l",              "Cooperative fiber positions {4, 6, 5} (T_COOP_ANTIPODAL)"),
    ("Vacuum alignment",          "No alignment problem; path unique by theorem"),
    ("Mass hierarchy",            "NH from monotone divisor growth d(4)=1, d(12)=4, d(36)=7"),
    ("Reactor angle suppression", "gcd(5,36)=1: electron off-path isolation (structural)"),
    ("CP phase delta",            "Open: Jarlskog involves sqrt(30) = sqrt(tau*sigma*g)"),
]


def pull(value, key):
    mu, sigma = PDG[key]
    return (value - mu) / sigma


def main():
    print("=" * 78)
    print("  EDEM vs standard flavour-symmetry patterns  (pmns_mechanism.py)")
    print("=" * 78)

    # ------------------------------------------------------------------
    # (1) Pattern comparison table.
    # ------------------------------------------------------------------
    print("\n" + "-" * 78)
    print("  (1) Predicted angles and pulls vs data")
    print("-" * 78)
    print("  %-19s %22s %22s" % ("pattern", "sin^2(angle) [pull sig]", ""))
    print("  %-19s %10s %12s %12s %10s" %
          ("", "th12", "th23", "th13", "max|pull|"))
    for label, s12, s23, s13, origin in PATTERNS:
        vals = {'th12': s12, 'th23': s23, 'th13': s13}
        pulls = {k: pull(vals[k], k) for k in KEYS}
        maxp = max(abs(p) for p in pulls.values())
        print("  %-19s %6.4f[%+5.1f] %6.4f[%+5.1f] %6.4f[%+6.1f] %9.2f" %
              (label, s12, pulls['th12'], s23, pulls['th23'],
               s13, pulls['th13'], maxp))
        print("  %-19s   %s" % ("", "(" + origin + ")"))

    # ------------------------------------------------------------------
    # (2) The theta_13 = 0 catastrophe (Daya Bay 2012).
    # ------------------------------------------------------------------
    print("\n" + "-" * 78)
    print("  (2) Patterns with theta_13 = 0 vs the measured reactor angle")
    print("-" * 78)
    zero13 = [p for p in PATTERNS if p[3] == 0.0]
    p13 = pull(0.0, 'th13')
    for label, *_ in zero13:
        print("      %-19s : sin^2(theta_13)=0  ->  pull = %+.1f sigma  (excluded)" %
              (label, p13))
    print("  All theta_13=0 patterns are excluded at |pull| = %.1f sigma (> 30 sigma)." % abs(p13))
    assert abs(p13) > 30

    # ------------------------------------------------------------------
    # (3) TBM is missed on all three angles; EDEM is not a perturbation of it.
    # ------------------------------------------------------------------
    print("\n" + "-" * 78)
    print("  (3) Tribimaximal misses on all three angles; EDEM is a different point")
    print("-" * 78)
    tbm = {'th12': 1 / 3, 'th23': 1 / 2, 'th13': 0.0}
    edem = {'th12': 4 / 13, 'th23': 6 / 11, 'th13': 1 / 45}
    for k in KEYS:
        print("      %-6s : TBM pull = %+6.1f sigma ;  EDEM-minus-TBM shift = %+.4f" %
              (k, pull(tbm[k], k), edem[k] - tbm[k]))
    shifts = [abs(edem[k] - tbm[k]) for k in KEYS]
    print("  EDEM shifts away from TBM: %s" % ["%.4f" % s for s in shifts])
    print("  These are comparable in magnitude across all three angles, so EDEM is NOT")
    print("  a perturbative (theta_13-only) correction to Tribimaximal.")
    # a genuine perturbation would leave th12,th23 ~ TBM and only switch on th13:
    assert abs(edem['th12'] - tbm['th12']) > 0.2 * abs(edem['th13'] - tbm['th13'])
    # TBM key pulls match the quoted values
    assert round(pull(tbm['th12'], 'th12'), 1) == 2.0
    assert round(pull(tbm['th23'], 'th23'), 1) == -2.2
    assert round(pull(tbm['th13'], 'th13'), 1) == -31.7

    # ------------------------------------------------------------------
    # (4) Vocabulary translation table.
    # ------------------------------------------------------------------
    print("\n" + "-" * 78)
    print("  (4) Translation: standard HEP flavour concept  <->  EDEM realisation")
    print("-" * 78)
    print("  %-28s %s" % ("Standard HEP concept", "EDEM realisation"))
    print("  " + "-" * 74)
    for concept, realisation in TRANSLATION:
        print("  %-28s %s" % (concept, realisation))

    print("\nConclusion: EDEM is not a tweak of Tribimaximal or any theta_13=0 ansatz.")
    print("It predicts a nonzero rational reactor angle from structure, and lands")
    print("within ~0.05 sigma on all three angles where the classic patterns fail.")
    print("\nDone.")


if __name__ == "__main__":
    main()
