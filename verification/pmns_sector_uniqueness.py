#!/usr/bin/env python3
"""
pmns_sector_uniqueness.py  --  Is the sector->angle assignment unique?
======================================================================

WHAT THIS SCRIPT TESTS
----------------------
EDEM does not merely produce three fractions; it assigns each to a specific
angle on physical grounds (postulate P5):

        temporal sector  ->  theta_12 :  tau^2 / r_tau          = 4/13
        null     sector  ->  theta_23 :  n_null / (n_null + g)  = 6/11
        spatial  sector  ->  theta_13 :  1 / (sigma^2 * g)      = 1/45

Two independent uniqueness questions are tested:

  (A) PERMUTATION TEST.  Of the 3! = 6 ways to attach the three sector formulas
      to the three measured angles, how many fit the data?

  (B) STRUCTURAL ROBUSTNESS.  If we leave the *form* of the three formulas fixed
      but vary the underlying epoch primes (tau, sigma, g) over all ordered
      triples tau<sigma<g with tau in 2..5, sigma in 2..7, g in 2..13
      (104 triples in total), how many reproduce the data?

EXPECTED OUTPUT (the result a referee should reproduce)
-------------------------------------------------------
  (A) Only the EDEM assignment fits: max|pull| = 0.053 sigma.
      The next-best permutation is 18.3 sigma; the remaining four are 400-748 sigma.
  (A') The EDEM sector value is the single closest register expression to each
       measured angle.
  (B) Exactly 1 of the 104 epoch-prime triples gives max|pull| < 1 sigma, namely
      (tau, sigma, g) = (2, 3, 5).

Standard library only.
"""

from itertools import permutations
from fractions import Fraction

# ---------------------------------------------------------------------------
# Measured PMNS values (NuFit 5.2, NH): (central, 1-sigma), in canonical order.
# ---------------------------------------------------------------------------
PDG = [
    (0.307,   0.013),    # 0: sin^2(theta_12)
    (0.546,   0.021),    # 1: sin^2(theta_23)
    (0.02220, 0.00070),  # 2: sin^2(theta_13)
]
ANGLE_NAMES = ["theta_12", "theta_23", "theta_13"]

# ---------------------------------------------------------------------------
# EDEM epoch primes (the {2,3,5} that the framework selects) and the three
# sector formulas written as functions of (tau, sigma, g).
# ---------------------------------------------------------------------------
TAU, SIGMA, GG = 2, 3, 5


def r_tau(tau):
    """Temporal resonance  r_tau = Phi_6(tau^2) = tau^4 - tau^2 + 1."""
    return tau ** 4 - tau ** 2 + 1


def temporal(tau, sigma, g):
    return Fraction(tau ** 2, r_tau(tau))            # 4/13 for (2,3,5)


def null(tau, sigma, g):
    n_null = tau * sigma
    return Fraction(n_null, n_null + g)              # 6/11 for (2,3,5)


def spatial(tau, sigma, g):
    return Fraction(1, sigma ** 2 * g)               # 1/45 for (2,3,5)


SECTORS = [("temporal", temporal), ("null", null), ("spatial", spatial)]


def pull(value, target):
    mu, sigma = target
    return (float(value) - mu) / sigma


def main():
    print("=" * 74)
    print("  EDEM PMNS sector-assignment uniqueness  (pmns_sector_uniqueness.py)")
    print("=" * 74)

    sector_vals = [(name, f(TAU, SIGMA, GG)) for name, f in SECTORS]
    print("\nSector formulas at (tau,sigma,g) = (%d,%d,%d):" % (TAU, SIGMA, GG))
    for name, val in sector_vals:
        print("  %-9s = %-5s = %.5f" % (name, str(val), float(val)))

    # ------------------------------------------------------------------
    # (A) Permutation test: 6 ways to map {temporal,null,spatial} -> angles.
    # ------------------------------------------------------------------
    print("\n" + "-" * 74)
    print("  (A) Permutation test  (6 assignments of sectors to angles)")
    print("-" * 74)
    print("  %-34s %-12s %s" % ("assignment (th12, th23, th13)", "max|pull|", "is EDEM?"))
    results = []
    edem_order = ("temporal", "null", "spatial")
    for perm in permutations(sector_vals):
        names = tuple(n for n, _ in perm)
        pulls = [pull(val, PDG[i]) for i, (_, val) in enumerate(perm)]
        maxp = max(abs(p) for p in pulls)
        is_edem = (names == edem_order)
        results.append((maxp, names, is_edem))
        label = " -> ".join(n[:4] for n in names)
        print("  %-34s %10.3f   %s" % (label, maxp, "<== EDEM" if is_edem else ""))

    results.sort()
    print("\n  Ranked max|pull| (sigma): %s" %
          ", ".join("%.3f" % r[0] for r in results))
    best, second = results[0], results[1]
    print("  Best       : %.3f sigma  (%s)  EDEM=%s" %
          (best[0], " -> ".join(best[1]), best[2]))
    print("  Next-best  : %.3f sigma" % second[0])
    print("  Worst four : %s sigma" %
          ", ".join("%.0f" % r[0] for r in results[2:]))
    assert best[2] and best[0] < 0.1, "EDEM assignment should be the unique good fit"
    assert second[0] > 10, "next-best should be many sigma away"

    # ------------------------------------------------------------------
    # (A') Closest register expression per angle.
    # ------------------------------------------------------------------
    print("\n" + "-" * 74)
    print("  (A') Is the EDEM sector value the closest register expression?")
    print("-" * 74)
    register = {
        Fraction(4, 13): "tau^2/r_tau", Fraction(6, 11): "n_null/(n_null+g)",
        Fraction(1, 45): "1/(sigma^2*g)", Fraction(4, 9): "|U_tau3|^2",
        Fraction(8, 15): "|U_mu3|^2", Fraction(44, 65): "|U_e1|^2",
        Fraction(176, 585): "|U_e2|^2", Fraction(2, 3): "tau/sigma",
    }
    assigned = [Fraction(4, 13), Fraction(6, 11), Fraction(1, 45)]
    for i, target in enumerate(PDG):
        ranked = sorted(register, key=lambda fr: abs(pull(fr, target)))
        closest = ranked[0]
        within3 = [fr for fr in register if abs(pull(fr, target)) <= 3.0]
        print("  %-9s : closest register value = %-6s (%+.3f sig) ; assigned = %-6s ; %d within 3 sig"
              % (ANGLE_NAMES[i], str(closest), pull(closest, target),
                 str(assigned[i]), len(within3)))
        assert closest == assigned[i], "assigned sector value is not the closest register expr"

    # ------------------------------------------------------------------
    # (B) Structural robustness over epoch-prime triples tau<sigma<g.
    # ------------------------------------------------------------------
    print("\n" + "-" * 74)
    print("  (B) Structural robustness: vary (tau,sigma,g), tau<sigma<g")
    print("      tau in 2..5, sigma in 2..7, g in 2..13")
    print("-" * 74)
    good = []
    n_triples = 0
    for tau in range(2, 6):
        for sigma in range(2, 8):
            for g in range(2, 14):
                if not (tau < sigma < g):
                    continue
                n_triples += 1
                vals = [temporal(tau, sigma, g), null(tau, sigma, g), spatial(tau, sigma, g)]
                maxp = max(abs(pull(vals[i], PDG[i])) for i in range(3))
                if maxp < 1.0:
                    good.append(((tau, sigma, g), maxp))
    print("  triples tested            : %d   (expected 104)" % n_triples)
    print("  triples with max|pull|<1s : %d" % len(good))
    for trip, mp in good:
        print("      (tau,sigma,g) = %s   max|pull| = %.3f sigma" % (str(trip), mp))
    assert n_triples == 104, "triple count changed -- expected 104"
    assert len(good) == 1 and good[0][0] == (2, 3, 5), \
        "only (2,3,5) should fit within 1 sigma"

    print("\nConclusion: the assignment temporal->th12, null->th23, spatial->th13 with")
    print("epoch primes (2,3,5) is the unique choice (1 of 6 permutations, 1 of 104")
    print("triples) compatible with the measured PMNS angles.")
    print("\nDone.")


if __name__ == "__main__":
    main()
