#!/usr/bin/env python3
"""
verify_masses.py  --  Charged-fermion masses from a single input (Postulate P2)
===============================================================================
Framework: Entropy Driven Expansion Model (EDEM) -- Paper B.

WHAT THIS SCRIPT TESTS
----------------------
Postulate P2 states that every elementary particle is a frozen eddy whose mass
is fixed by m(P) = K / t(P), where

    * P      is the integer ("prime") identifying the particle,
    * t(P)   is the accumulated divisor cost of reaching P on the lattice,
    * K = m_top = 172,570 MeV is the SINGLE empirical input.

Every other mass is therefore an arithmetic consequence of one number.

THE DIVISOR RECURSION
---------------------
    S(2) = S(3) = 0
    S(n) = S(n-1) + 1/(d(n) - 2)   for composite n   (d(n) > 2)
    S(n) = S(n-1)                   for prime n        (recursion does not advance)
    t(P) = S(P)                     for a particle prime P
where d(n) is the number of positive divisors of n.  (Composite n always has
d(n) >= 3, so d(n)-2 >= 1 and the term is well defined.)

EXPECTED RESULTS (reproduce these)
----------------------------------
    * t(5) = 1.000000 exactly                     (Theorem T17; top = calibration)
    * proton (P=773): t ~ 184.17  ->  m ~ 937.0 MeV   (-0.13%)
    * The heavy sector (top, bottom, tau, charm, proton, muon, electron) is
      reproduced to <= ~1.4%.
    * The LIGHT QUARKS are the known open problem (README open problem #5):
      they reproduce the EDEM ratio m_d/m_s = 1/23.9 (i.e. -16% vs the PDG
      ratio 1/20.0), so down/up/strange carry the largest individual errors.
      This is a documented feature of EDEM, not a numerical defect here.

Standard library only.  Runs in a few seconds (it sieves divisor counts up to
~1.9 million, then sweeps the recursion once with a progress indicator).
"""

import sys

K = 172570.0  # MeV -- the single empirical input (top-quark mass)

# (name, prime P, PDG mass [MeV], note)
PARTICLES = [
    ("top",      5,        172570.0,  "calibration"),
    ("bottom",   157,        4180.0,  "PDG central"),
    ("tau",      389,        1776.86, "PDG central"),
    ("charm",    557,        1275.0,  "PDG central"),
    ("proton",   773,         938.272,"PDG central"),
    ("muon",     7649,        105.658,"PDG central"),
    ("strange",  8221,         93.5,  "PDG central"),
    ("down",     221873,        4.67, "PDG central"),
    ("up",       386993,        2.16, "PDG central"),
    ("electron", 1907573,       0.51100, "PDG central"),
]


def count_divisors_trial(n):
    """Number of positive divisors of n by trial division up to sqrt(n).
    (Reference implementation, used to validate the fast sieve below.)"""
    c, i = 0, 1
    while i * i <= n:
        if n % i == 0:
            c += 1 if i * i == n else 2
        i += 1
    return c


def divisor_count_sieve(N):
    """d[k] = number of divisors of k, for all k <= N (additive sieve)."""
    d = [0] * (N + 1)
    for step in range(1, N + 1):
        for m in range(step, N + 1, step):
            d[m] += 1
    return d


def main():
    N = max(P for _, P, _, _ in PARTICLES)  # 1,907,573

    print("=" * 76)
    print("  EDEM MASS FORMULA VERIFICATION  (verify_masses.py)")
    print("  Entropy Driven Expansion Model -- Postulate P2: m(P) = K / t(P)")
    print("  K = m_top = 172,570 MeV is the single empirical input.")
    print("=" * 76)

    print("\nComputing divisor counts up to N = %d (sieve)..." % N)
    d = divisor_count_sieve(N)
    # sanity-check the sieve against the trial-division reference on a sample
    for s in (4, 36, 900, 44100, 389, 773, 7649, N):
        assert d[s] == count_divisors_trial(s), "divisor mismatch at %d" % s
    print("Divisor sieve validated against trial division.")

    # Single sweep of the recursion from n=2..N with a progress indicator.
    print("Sweeping the divisor recursion n = 2 .. %d ..." % N)
    wanted = {P for _, P, _, _ in PARTICLES}
    t_of = {}
    S = 0.0
    for n in range(2, N + 1):
        if d[n] > 2:                  # composite -> recursion advances
            S += 1.0 / (d[n] - 2)
        if d[n] == 2 and n in wanted:  # prime particle -> record t(P) = S(P)
            t_of[n] = S
        if n % 200000 == 0:
            print("   ... n = %d  (S = %.3f)" % (n, S))
    print("Recursion complete.\n")

    # t(5) must be exactly 1 (Theorem T17).
    assert abs(t_of[5] - 1.0) < 1e-12, "t(5) is not 1.000000"

    # Results table.
    hdr = "%-9s %-10s %-13s %-14s %-13s %-9s" % (
        "Particle", "Prime P", "t(P)", "m_EDEM (MeV)", "m_PDG (MeV)", "Error")
    print(hdr)
    print("-" * len(hdr))
    max_err, max_name = 0.0, ""
    masses = {}
    for name, P, m_pdg, note in PARTICLES:
        t = t_of[P]
        m = K / t
        masses[name] = m
        if name == "top":
            err_str = "calibration"
        else:
            err = (m - m_pdg) / m_pdg * 100.0
            err_str = "%+.2f%%" % err
            if abs(err) > max_err:
                max_err, max_name = abs(err), name
        print("%-9s %-10d %-13.4f %-14.4f %-13.5f %-9s" %
              (name, P, t, m, m_pdg, err_str))

    print("\nAll 10 charged SM fermion masses generated from one constant K = m_top.")

    # Honest accounting of where EDEM is strong and where it is an open problem.
    heavy = ["top", "bottom", "tau", "charm", "proton", "muon", "electron"]
    heavy_max = max(abs((masses[n] - m) / m * 100.0)
                    for n, P, m, _ in PARTICLES if n in heavy and n != "top")
    print("Heavy sector (top, bottom, tau, charm, proton, muon, electron):")
    print("   largest error = %.2f%%" % heavy_max)
    print("Light quarks (strange, down, up) -- README open problem #5:")
    ratio = masses["down"] / masses["strange"]
    print("   m_d/m_s = %.5f = 1/%.1f  (EDEM value; PDG ratio is 1/20.0, -16%%)"
          % (ratio, 1.0 / ratio))
    print("   -> down/up/strange carry the largest individual errors by design.")
    print("Largest individual error (excluding calibration): %.2f%% (%s quark)"
          % (max_err, max_name))


if __name__ == "__main__":
    main()
