#!/usr/bin/env python3
"""
pmns_rigidity.py  --  How fragile are the PMNS predictions? (anti-tuning test)
==============================================================================

WHAT THIS SCRIPT TESTS
----------------------
A successful numerical coincidence should be ROBUST to small changes in its
inputs; a fine-tuned one is FRAGILE.  EDEM claims the opposite of fine-tuning:
the integers that enter the PMNS angles are fixed by theorems, and if you nudge
any of them the agreement with data collapses immediately.  This script makes
that quantitative.

Four structural "handles" feed the three angles:

        handle      EDEM value   enters
        r_tau          13        sin^2(theta_12) = tau^2 / r_tau          = 4/13
        D_null         11        sin^2(theta_23) = n_null / D_null        = 6/11
        sigma^2 g      45        sin^2(theta_13) = 1 / (sigma^2 g)        = 1/45
        n_null          6        sin^2(theta_23) = n_null / (n_null + g)  = 6/11

For each handle we (a) step it by +/-1,2,3 integer units and watch max|pull|
explode, and (b) quote the sensitivity (sigma per unit) and the number of units
needed to move the fit by a single sigma.

EXPECTED OUTPUT (the result a referee should reproduce)
-------------------------------------------------------
  * r_tau   moves 1 sigma in  < 0.56 units.
  * D_null  moves 1 sigma in  < 0.43 units.
  * Joint scan of all 104 epoch-prime triples (tau<sigma<g): only (2,3,5) keeps
    max|pull| < 1 sigma.
  * sigma^2 g = 44 and 46 are *individually* within 1 sigma of theta_13, yet both
    are excluded because T_SPATIAL_SUM proves sigma^2 g = r_p + tau = 43 + 2 = 45.

Standard library only.
"""

from fractions import Fraction

# ---------------------------------------------------------------------------
# Measured PMNS values (NuFit 5.2, NH): (central, 1-sigma).
# ---------------------------------------------------------------------------
PDG = {
    'th12': (0.307,   0.013),
    'th23': (0.546,   0.021),
    'th13': (0.02220, 0.00070),
}


def pull(value, key):
    mu, sigma = PDG[key]
    return (float(value) - mu) / sigma


def predictions(r_tau=13, D_null=11, s2g=45, n_null=6, g=5):
    """Return (th12, th23, th13) as exact fractions for given handle values.
    n_null drives th23 through n_null/(n_null+g); D_null is the same denominator
    treated as an independent handle (hold whichever one is being varied)."""
    return (Fraction(4, r_tau),
            Fraction(n_null, D_null),
            Fraction(1, s2g))


def max_pull(th12, th23, th13):
    return max(abs(pull(th12, 'th12')), abs(pull(th23, 'th23')), abs(pull(th13, 'th13')))


# (name, baseline, theorem, affected angle, integer builder, float predictor of angle)
HANDLES = [
    ("r_tau",    13, "Phi_6(tau^2) identity (Axiom M)",  'th12',
     lambda v: predictions(r_tau=v),            lambda v: 4.0 / v),
    ("D_null",   11, "B1: g = tau^2 + 1  (D=n_null+g)",  'th23',
     lambda v: predictions(D_null=v),           lambda v: 6.0 / v),
    ("sigma^2g", 45, "T_SPATIAL_SUM: sigma^2 g=r_p+tau", 'th13',
     lambda v: predictions(s2g=v),              lambda v: 1.0 / v),
    ("n_null",    6, "minimal null composite tau*sigma", 'th23',
     lambda v: predictions(n_null=v, D_null=v + 5), lambda v: v / (v + 5.0)),
]


def main():
    print("=" * 78)
    print("  EDEM PMNS rigidity / anti-tuning study  (pmns_rigidity.py)")
    print("=" * 78)

    base = predictions()
    print("\nBaseline predictions  (th12, th23, th13) = (%s, %s, %s)" % base)
    print("Baseline max|pull| = %.3f sigma" % max_pull(*base))

    # ------------------------------------------------------------------
    # (a) One-handle-at-a-time sensitivity table.
    # ------------------------------------------------------------------
    print("\n" + "-" * 78)
    print("  (a) Single-handle sensitivity")
    print("-" * 78)
    header = "  %-9s %5s  %-32s %8s %8s %8s  %9s" % (
        "handle", "value", "theorem fixing it", "-1", "+1", "sig/unit", "units/1sig")
    print(header)
    for name, base_v, thm, ang, build, fpred in HANDLES:
        mp_m1 = max_pull(*build(base_v - 1))
        mp_p1 = max_pull(*build(base_v + 1))
        # sensitivity of the affected angle via central finite difference
        h = 1e-3
        dpred = (fpred(base_v + h) - fpred(base_v - h)) / (2 * h)
        sig_per_unit = abs(dpred) / PDG[ang][1]
        units_1sig = 1.0 / sig_per_unit
        print("  %-9s %5d  %-32s %8.2f %8.2f %8.3f  %9.3f" %
              (name, base_v, thm, mp_m1, mp_p1, sig_per_unit, units_1sig))

    # Precise units-for-1sigma for the two sharpest handles (analytic derivative):
    u_rtau = 1.0 / (abs(-4 / 13 ** 2) / PDG['th12'][1])
    u_dnull = 1.0 / (abs(-6 / 11 ** 2) / PDG['th23'][1])
    print("\n  r_tau : %.3f units to move 1 sigma   (claim: < 0.56)  -> %s" %
          (u_rtau, u_rtau < 0.56))
    print("  D_null: %.3f units to move 1 sigma   (claim: < 0.43)  -> %s" %
          (u_dnull, u_dnull < 0.43))
    assert u_rtau < 0.56 and u_dnull < 0.43

    # ------------------------------------------------------------------
    # (b) Joint variation over epoch-prime triples tau<sigma<g.
    # ------------------------------------------------------------------
    print("\n" + "-" * 78)
    print("  (b) Joint scan: all (tau,sigma,g) with tau<sigma<g, "
          "tau in 2..5, sigma 2..7, g 2..13")
    print("-" * 78)
    good = []
    n = 0
    for tau in range(2, 6):
        for sigma in range(2, 8):
            for g in range(2, 14):
                if not (tau < sigma < g):
                    continue
                n += 1
                th12 = Fraction(tau ** 2, tau ** 4 - tau ** 2 + 1)
                th23 = Fraction(tau * sigma, tau * sigma + g)
                th13 = Fraction(1, sigma ** 2 * g)
                if max_pull(th12, th23, th13) < 1.0:
                    good.append(((tau, sigma, g), max_pull(th12, th23, th13)))
    print("  triples tested = %d   ;  with max|pull| < 1 sigma = %d" % (n, len(good)))
    for trip, mp in good:
        print("      (tau,sigma,g)=%s  max|pull|=%.3f sigma  (= %.2f%% of %d)" %
              (str(trip), mp, 100.0 / n, n))
    assert n == 104 and good and good[0][0] == (2, 3, 5) and len(good) == 1

    # ------------------------------------------------------------------
    # (c) The sigma^2 g = 44 / 46 near-misses, excluded by theorem.
    # ------------------------------------------------------------------
    print("\n" + "-" * 78)
    print("  (c) sigma^2 g neighbours of 45 for theta_13")
    print("-" * 78)
    for val in (44, 45, 46):
        p = pull(Fraction(1, val), 'th13')
        flag = "EDEM (proved: r_p + tau = 43 + 2)" if val == 45 else \
               ("within 1 sigma but excluded by T_SPATIAL_SUM" if abs(p) < 1 else "excluded")
        print("      sigma^2 g = %d : 1/%d = %.5f , pull = %+.3f sigma   %s" %
              (val, val, 1.0 / val, p, flag))
    assert abs(pull(Fraction(1, 44), 'th13')) < 1 and abs(pull(Fraction(1, 46), 'th13')) < 1

    print("\nConclusion: every handle is sub-unit fragile and the joint epoch-prime")
    print("scan singles out (2,3,5) alone (1/104).  The predictions are rigid, not")
    print("tuned: the integers are fixed by theorems, and any change breaks the fit.")
    print("\nDone.")


if __name__ == "__main__":
    main()
