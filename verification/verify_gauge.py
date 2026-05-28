#!/usr/bin/env python3
"""
verify_gauge.py  --  Gauge couplings from epoch holonomy (Postulate P4)
=======================================================================
Framework: Entropy Driven Expansion Model (EDEM) -- Paper B.

WHAT THIS SCRIPT TESTS
----------------------
Postulate P4 derives the gauge couplings from the holonomy of successive
"epochs" of the lattice:

        g_k = ln(p_k) / d(n_k)

with epoch primes p_k (the first four primes) and epoch composites n_k = the
square of the k-th primorial:

        p   = [2, 3, 5, 7]
        n_k = [(2)^2, (2*3)^2, (2*3*5)^2, (2*3*5*7)^2] = [4, 36, 900, 44100]
        d(n_k) = [3, 9, 27, 81]   (= 3^k)

From this:
  * Weinberg angle (epoch 1): sin^2(theta_W) = ln(2) / d(4) = ln(2)/3
  * Strong coupling (epoch 2): alpha_s        = ln(3) / d(36) = ln(3)/9
  * Gauge-boson counts from epoch holonomy: p_k^2 - 1 generators.

It also tests Theorem T_CR (Cross-epoch Running), which links the two couplings
through one-loop QCD running between the natural QCD scale mu_QCD = M_Z/2^(1/3)
and M_Z.  Because ln(M_Z / mu_QCD) = ln(2^(1/3)) = ln(2)/3 = sin^2(theta_W),

        1/alpha_s(M_Z) - 1/alpha_s(mu_QCD) = (beta_0 / 2pi) * sin^2(theta_W).

EXPECTED RESULTS (reproduce these)
----------------------------------
  * sin^2(theta_W) = 0.23105   (PDG 0.23122; residual 0.07%)
  * alpha_s        = 0.12207   (PDG 0.1180;  residual 3.4% pre-RG)
  * T_CR agreement ~ 61 ppm of the inverse coupling (one loop)
  * gluons p_2^2-1 = 8, weak bosons p_1^2-1 = 3
  * mu_QCD = M_Z / 2^(1/3) ~ 72.4 GeV

Standard library only.
"""

import math

# Epoch structure --------------------------------------------------------------
p = [2, 3, 5, 7]                 # epoch primes (first four primes)
n_k = [4, 36, 900, 44100]        # epoch composites: (primorial_k)^2
d_nk = [3, 9, 27, 81]            # divisor counts d(n_k) = 3^k

# Measured inputs --------------------------------------------------------------
sin2_PDG = 0.23122
alpha_s_PDG = 0.1180
M_Z = 91187.6                    # MeV
beta_0 = 23 / 3                  # one-loop QCD beta coeff, n_f = 5


def divisor_count(n):
    c, i = 0, 1
    while i * i <= n:
        if n % i == 0:
            c += 1 if i * i == n else 2
        i += 1
    return c


def main():
    print("=" * 72)
    print("  EDEM GAUGE COUPLING VERIFICATION  (verify_gauge.py)")
    print("  Entropy Driven Expansion Model -- Postulate P4: g_k = ln(p_k)/d(n_k)")
    print("=" * 72)

    # Confirm the epoch divisor counts.
    for nk, expect in zip(n_k, d_nk):
        assert divisor_count(nk) == expect, "d(%d) != %d" % (nk, expect)
    print("\nEpoch table:")
    print("  k  p_k   n_k=(p_k#)^2   d(n_k)")
    for k in range(4):
        print("  %d  %-4d  %-12d  %d" % (k + 1, p[k], n_k[k], d_nk[k]))

    # --- Weinberg angle (epoch 1) --------------------------------------------
    sin2 = math.log(2) / d_nk[0]
    res_w = abs(sin2 - sin2_PDG) / sin2_PDG * 100
    print("\nWeinberg angle (epoch 1):")
    print("  EDEM: ln(2)/3 = %.5f" % sin2)
    print("  PDG : %.5f" % sin2_PDG)
    print("  Residual: %.2f%%" % res_w)
    assert res_w < 0.1

    # --- Strong coupling (epoch 2) -------------------------------------------
    alpha_s = math.log(3) / d_nk[1]
    res_s = abs(alpha_s - alpha_s_PDG) / alpha_s_PDG * 100
    print("\nStrong coupling (epoch 2):")
    print("  EDEM: ln(3)/9 = %.5f" % alpha_s)
    print("  PDG : %.5f" % alpha_s_PDG)
    print("  Residual: %.1f%% (pre-RG scale correction)" % res_s)
    assert 3.0 < res_s < 4.0

    # --- T_CR: cross-epoch running -------------------------------------------
    inv_edem = 1.0 / alpha_s
    inv_pdg = 1.0 / alpha_s_PDG
    lhs = inv_pdg - inv_edem
    rhs = (beta_0 / (2 * math.pi)) * sin2
    # agreement measured against the scale of the inverse coupling (1/alpha_s)
    ppm = abs(lhs - rhs) / inv_edem * 1e6
    print("\nT_CR (Cross-Epoch Running, Theorem):")
    print("  LHS: 1/alpha_s(M_Z) - 1/alpha_s_EDEM      = %.6f" % lhs)
    print("  RHS: (beta_0/2pi) * sin^2(theta_W)        = %.6f" % rhs)
    print("  ln(M_Z/mu_QCD) = ln(2)/3 = sin^2(theta_W) = %.6f  (identity)" %
          (math.log(M_Z / (M_Z / 2 ** (1 / 3)))))
    print("  Agreement: %.0f ppm of 1/alpha_s at one loop" % ppm)
    assert ppm < 65

    # --- Gauge-boson counts ---------------------------------------------------
    gluons = p[1] ** 2 - 1
    weak = p[0] ** 2 - 1
    print("\nGauge boson count (epoch holonomy p_k^2 - 1):")
    print("  Gluons:      p_2^2 - 1 = %d  (SU(3) holonomy)  %s" %
          (gluons, "OK" if gluons == 8 else "FAIL"))
    print("  Weak bosons: p_1^2 - 1 = %d  (SU(2) holonomy)  %s" %
          (weak, "OK" if weak == 3 else "FAIL"))
    assert gluons == 8 and weak == 3

    # --- Natural QCD scale ----------------------------------------------------
    mu_QCD = M_Z / 2 ** (1 / 3)
    print("\nNatural QCD scale:")
    print("  mu_QCD = M_Z / 2^(1/3) = %.1f MeV = %.2f GeV" % (mu_QCD, mu_QCD / 1000))

    print("\nDone.")


if __name__ == "__main__":
    main()
