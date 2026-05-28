#!/usr/bin/env python3
"""
pmns_unitary_embed.py  --  Embedding the EDEM angles in a full 3x3 PMNS matrix
==============================================================================

WHAT THIS SCRIPT TESTS
----------------------
EDEM fixes the three mixing angles exactly,

        sin^2(theta_12) = 4/13,  sin^2(theta_23) = 6/11,  sin^2(theta_13) = 1/45,

but says nothing (yet) about the Dirac CP phase delta.  This script builds the
full 3x3 lepton mixing matrix in the standard PDG parametrisation from those
angles, and checks three things:

  1. COMPATIBILITY.  Is |U_EDEM|^2 consistent, element-by-element, with the PDG
     central matrix for *every* value of delta?  (Expected: max deviation over
     all 9 elements and all delta is below 0.001.)

  2. EXACT RATIONAL SUB-BLOCKS.  Two parts of |U|^2 are delta-INDEPENDENT and
     come out as exact rationals predicted by EDEM theorems:
         third column : (|U_e3|^2, |U_mu3|^2, |U_tau3|^2) = (1/45, 8/15, 4/9)
         first  row   : (|U_e1|^2, |U_e2|^2, |U_e3|^2)    = (44/65, 176/585, 1/45)
     Each triple sums to 1 (unitarity).

  3. THE sqrt(6) STRUCTURE.  sqrt(6) = sqrt(tau*sigma) = sqrt(n_null) is the
     characteristic surd of the columns-1&2 block.  It enters the delta-dependent
     |U|^2 entries (the mu and tau rows of columns 1 and 2) as a cos(delta) cross
     term whose coefficient is exactly (rational)*sqrt(6); everywhere in the
     third column and first row it squares away to a rational.  Finally the
     Jarlskog invariant is J = (8*sqrt(6)/585) * sin(delta) = 0.0335 * sin(delta).

(The "only the tau row" wording sometimes attached to sqrt(6) is too strong: the
paper's own open-problems list notes both the mu and tau rows of columns 1-2 are
irrational in sqrt(5) and sqrt(6).  This script reports the true distribution.)

Requires numpy.
"""

import numpy as np
from fractions import Fraction

# ---------------------------------------------------------------------------
# EDEM exact angles, and the best-fit phase.
# ---------------------------------------------------------------------------
S2_12 = Fraction(4, 13)     # tau^2 / r_tau
S2_23 = Fraction(6, 11)     # n_null / (n_null + g)
S2_13 = Fraction(1, 45)     # 1 / (sigma^2 * g)
DELTA_BESTFIT = 197.0       # degrees (NuFit 5.2 NH best fit)

# PDG central angles, for the compatibility comparison.
PDG_12, PDG_23, PDG_13 = 0.307, 0.546, 0.02220


def pmns_matrix(delta_deg, sin2_12, sin2_23, sin2_13):
    """Standard PDG parametrisation of the 3x3 lepton mixing matrix."""
    c12, s12 = np.sqrt(1 - sin2_12), np.sqrt(sin2_12)
    c23, s23 = np.sqrt(1 - sin2_23), np.sqrt(sin2_23)
    c13, s13 = np.sqrt(1 - sin2_13), np.sqrt(sin2_13)
    d = np.deg2rad(delta_deg)
    eid, emid = np.exp(1j * d), np.exp(-1j * d)
    return np.array([
        [c12 * c13,                       s12 * c13,                       s13 * emid],
        [-s12 * c23 - c12 * s23 * s13 * eid,  c12 * c23 - s12 * s23 * s13 * eid,  s23 * c13],
        [s12 * s23 - c12 * c23 * s13 * eid,  -c12 * s23 - s12 * c23 * s13 * eid,  c23 * c13],
    ], dtype=complex)


def absq(U):
    return np.abs(U) ** 2


def main():
    print("=" * 74)
    print("  EDEM PMNS unitary embedding  (pmns_unitary_embed.py)")
    print("=" * 74)

    e12, e23, e13 = float(S2_12), float(S2_23), float(S2_13)

    U = pmns_matrix(DELTA_BESTFIT, e12, e23, e13)
    P = absq(U)
    print("\n|U_EDEM|^2 at delta = %.0f deg  (rows e/mu/tau, cols 1/2/3):" % DELTA_BESTFIT)
    for r, name in enumerate(["e  ", "mu ", "tau"]):
        print("  %s  %s" % (name, "  ".join("%.5f" % x for x in P[r])))
    print("  row sums : %s    col sums : %s" %
          (np.round(P.sum(axis=1), 6), np.round(P.sum(axis=0), 6)))

    # ------------------------------------------------------------------
    # (1) Compatibility with PDG central matrix, scanned over all delta.
    # ------------------------------------------------------------------
    print("\n" + "-" * 74)
    print("  (1) Element-wise deviation |U_EDEM|^2 vs |U_PDG|^2, scanned over delta")
    print("-" * 74)
    worst = 0.0
    worst_delta = None
    for delta in np.arange(0, 360, 1.0):
        Pe = absq(pmns_matrix(delta, e12, e23, e13))
        Pp = absq(pmns_matrix(delta, PDG_12, PDG_23, PDG_13))
        m = np.max(np.abs(Pe - Pp))
        if m > worst:
            worst, worst_delta = m, delta
    print("  max |deviation| over 9 elements and all delta = %.2e  (at delta=%.0f deg)" %
          (worst, worst_delta))
    print("  threshold 0.001 satisfied : %s" % (worst < 1e-3))
    assert worst < 1e-3, "EDEM and PDG matrices differ by more than 0.001"

    # ------------------------------------------------------------------
    # (2) Exact rational, delta-independent sub-blocks.
    # ------------------------------------------------------------------
    print("\n" + "-" * 74)
    print("  (2) Exact rational sub-blocks (delta-independent)")
    print("-" * 74)
    col3_exact = [S2_13,                          # |U_e3|^2   = s13^2
                  S2_23 * (1 - S2_13),            # |U_mu3|^2  = s23^2 c13^2
                  (1 - S2_23) * (1 - S2_13)]      # |U_tau3|^2 = c23^2 c13^2
    row1_exact = [(1 - S2_12) * (1 - S2_13),      # |U_e1|^2   = c12^2 c13^2
                  S2_12 * (1 - S2_13),            # |U_e2|^2   = s12^2 c13^2
                  S2_13]                          # |U_e3|^2   = s13^2

    print("  third column |U_i3|^2 :")
    for lbl, fr, num in zip(["e3 ", "mu3", "tau3"], col3_exact, P[:, 2]):
        print("      |U_%s|^2 = %-6s = %.6f   (numeric %.6f)" %
              (lbl, str(fr), float(fr), num))
        assert abs(float(fr) - num) < 1e-12
    print("      sum = %s = %d" % (str(sum(col3_exact)), sum(col3_exact)))
    assert sum(col3_exact) == 1

    print("  first row    |U_1j|^2 :")
    for lbl, fr, num in zip(["e1", "e2", "e3"], row1_exact, P[0, :]):
        print("      |U_%s|^2 = %-7s = %.6f   (numeric %.6f)" %
              (lbl, str(fr), float(fr), num))
        assert abs(float(fr) - num) < 1e-12
    print("      sum = %s = %d" % (str(sum(row1_exact)), sum(row1_exact)))
    assert sum(row1_exact) == 1

    # Confirm these blocks really are delta-independent.
    P0 = absq(pmns_matrix(0.0, e12, e23, e13))
    P90 = absq(pmns_matrix(90.0, e12, e23, e13))
    assert np.allclose(P0[:, 2], P90[:, 2]) and np.allclose(P0[0, :], P90[0, :])
    print("  (verified delta-independent: column 3 and row 1 identical at delta=0 and 90)")

    # ------------------------------------------------------------------
    # (3) sqrt(6) structure of the columns-1&2 block.
    # ------------------------------------------------------------------
    print("\n" + "-" * 74)
    print("  (3) sqrt(6) = sqrt(tau*sigma) = sqrt(n_null) structure")
    print("-" * 74)
    sqrt6 = np.sqrt(6.0)
    # |U_ij(delta)|^2 = A_ij - B_ij cos(delta) for the lower-left 2x2 block.
    P0 = absq(pmns_matrix(0.0, e12, e23, e13))
    P180 = absq(pmns_matrix(180.0, e12, e23, e13))
    B = (P180 - P0) / 2.0   # coefficient of cos(delta)
    print("  cos(delta) cross-term coefficient B_ij and B_ij / sqrt(6):")
    block = [(1, 0, "mu1"), (1, 1, "mu2"), (2, 0, "tau1"), (2, 1, "tau2")]
    for i, j, name in block:
        ratio = B[i, j] / sqrt6
        rat = Fraction(ratio).limit_denominator(1000)
        print("      U_%-4s : B = %+.6f   B/sqrt(6) = %+.6f = %s  (rational)" %
              (name, B[i, j], ratio, str(rat)))
        # B/sqrt(6) must be a clean rational -> sqrt(6) is the only surd present
        assert abs(float(rat) - ratio) < 1e-9
    # third column / first row carry no sqrt(6) (B = 0 there)
    print("  third column & first row : B = %s (no cos-delta term -> sqrt(6) squared away)"
          % np.round([B[0, 2], B[1, 2], B[2, 2], B[0, 0], B[0, 1]], 9).tolist())

    # ------------------------------------------------------------------
    # Jarlskog invariant J = s12 c12 s23 c23 s13 c13^2 sin(delta).
    # ------------------------------------------------------------------
    print("\n" + "-" * 74)
    print("  Jarlskog invariant")
    print("-" * 74)

    def jarlskog(U):
        # J defined via Im(U_e1 U_mu2 U_e2* U_mu1*)
        return np.imag(U[0, 0] * U[1, 1] * np.conj(U[0, 1]) * np.conj(U[1, 0]))

    coeffs = []
    for delta in (30.0, 90.0, 150.0, 197.0):
        Jd = jarlskog(pmns_matrix(delta, e12, e23, e13))
        s = np.sin(np.deg2rad(delta))
        coeffs.append(Jd / s)
        print("      delta=%6.1f deg : J = %+.6f ,  J/sin(delta) = %.6f" % (delta, Jd, Jd / s))
    coeff = np.mean(coeffs)
    # exact coefficient = 8*sqrt(6)/585
    exact = 8 * sqrt6 / 585
    print("  J coefficient (numeric)  = %.6f" % coeff)
    print("  J coefficient (8*sqrt(6)/585) = %.6f  ->  J = %.4f * sin(delta)" % (exact, exact))
    assert abs(coeff - exact) < 1e-9
    print("  At best-fit delta=197 deg : J = %.5f" %
          jarlskog(pmns_matrix(197.0, e12, e23, e13)))

    print("\nDone.")


if __name__ == "__main__":
    main()
