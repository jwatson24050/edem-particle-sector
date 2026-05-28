#!/usr/bin/env python3
"""
verify_cooperative_moduli.py  --  Null-cone origin of {13, 17, 43} (Postulate P1)
=================================================================================
Framework: Entropy Driven Expansion Model (EDEM) -- Paper B.

WHAT THIS SCRIPT TESTS
----------------------
The cooperative moduli {r_tau, r_mu, r_p} = {13, 17, 43} are NOT fitted to data.
They are forced by the metric of the {2,3,5,7}-smooth discrete Minkowski lattice
(Postulate P1).  This script verifies each step of that derivation:

  1. Null-cone condition.  With X_p = v_p(n) the p-adic valuation,
         ds^2(n) = -X_2^2 + X_3^2 + X_5^2 + X_7^2,
     and n = 6 is the MINIMAL null composite (ds^2 = 0); no composite below 6 is
     null.
  2. The sixth cyclotomic map Phi_6(n) = n^2 - n + 1, the iterated tower it
     generates, and its termination at Phi_6(43) = 1807 = 13 x 139 (composite).
  3. Intersection Identity (Theorem 1): Phi_6(n) = 6n + 1 has the unique positive
     solution n = 7.
  4. The cooperative moduli r_tau = Phi_6(4) = 13, r_p = Phi_6(7) = 43, and
     r_mu = r_p - 2 r_tau = 17.
  5. Corollary 1: ord_43(7) = 6 (the multiplicative order of 7 mod 43).
  6. Three-generation theorem: the iterated Phi_6 tower yields exactly three
     cooperative primes (3, 7, 43) before terminating -> three generations.

Standard library only.
"""


def v_p(n, prime):
    """p-adic valuation of n."""
    if n == 0:
        return float("inf")
    c = 0
    while n % prime == 0:
        n //= prime
        c += 1
    return c


def ds_squared(n):
    """Lattice interval ds^2(n) = -X2^2 + X3^2 + X5^2 + X7^2."""
    X2, X3, X5, X7 = v_p(n, 2), v_p(n, 3), v_p(n, 5), v_p(n, 7)
    return -X2 ** 2 + X3 ** 2 + X5 ** 2 + X7 ** 2


def phi6(n):
    return n * n - n + 1


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def factor(n):
    """Return a short 'a x b x ...' factorisation string (small n)."""
    fs, d, m = [], 2, n
    while d * d <= m:
        while m % d == 0:
            fs.append(d)
            m //= d
        d += 1
    if m > 1:
        fs.append(m)
    return " x ".join(map(str, fs)) if len(fs) > 1 else str(n)


def kind(x):
    return "timelike" if x < 0 else ("spacelike" if x > 0 else "NULL")


def main():
    print("=" * 74)
    print("  COOPERATIVE MODULI VERIFICATION  (verify_cooperative_moduli.py)")
    print("  Entropy Driven Expansion Model -- Postulate P1: {2,3,5,7} lattice")
    print("=" * 74)

    # 1. Null-cone scan -------------------------------------------------------
    print("\nNull-cone condition  ds^2(n) = -X2^2 + X3^2 + X5^2 + X7^2 :")
    for n in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]:
        flag = "  <-- MINIMAL NULL COMPOSITE (forced by P1)" if n == 6 else ""
        print("  n=%-3d ds^2 = %+d  (%s)%s" % (n, ds_squared(n), kind(ds_squared(n)), flag))
    assert ds_squared(6) == 0
    # no composite below 6 is null (only composite < 6 is 4)
    assert all(ds_squared(n) != 0 for n in range(4, 6) if not is_prime(n))
    print("  -> n=6 is null; the only composite below 6 (n=4) is not null.")

    # 2. Phi_6 values + iterated tower ---------------------------------------
    print("\nPhi_6(n) = n^2 - n + 1 :")
    labels = {2: "= p_2", 3: "= p_4", 4: "= r_tau (tau modulus)",
              5: "no prime tower value at p_3", 7: "= r_p (proton modulus)",
              43: "TOWER TERMINATES"}
    for n in [2, 3, 4, 5, 7, 43]:
        val = phi6(n)
        tag = "prime " if is_prime(val) else "COMPOSITE = %s" % factor(val)
        print("  Phi_6(%-2d) = %-5d (%s)  %s" % (n, val, tag, labels[n]))

    print("\nIterated Phi_6 tower (seed 2):")
    chain, a = [2], 2
    while True:
        a = phi6(a)
        chain.append(a)
        if not is_prime(a):
            break
    primes_in_tower = [x for x in chain[1:] if is_prime(x)]
    print("  " + " -> ".join(str(x) for x in chain) +
          "   (last = %s, composite -> terminate)" % factor(chain[-1]))
    print("  cooperative primes produced: %s  (%d of them)"
          % (primes_in_tower, len(primes_in_tower)))
    assert chain == [2, 3, 7, 43, 1807] and primes_in_tower == [3, 7, 43]

    # 3. Intersection Identity (Theorem 1) -----------------------------------
    sols = [n for n in range(1, 101) if phi6(n) == 6 * n + 1]
    print("\nTheorem 1 (Intersection Identity): Phi_6(n) = 6n + 1")
    print("  scanning n = 1..100 ... solutions: %s" % sols)
    assert sols == [7]
    print("  unique solution n = 7  (OK)")

    # 4. Cooperative moduli ---------------------------------------------------
    r_tau, r_p = phi6(4), phi6(7)
    r_mu = r_p - 2 * r_tau
    print("\nCooperative moduli (resonant frequencies of the null cone):")
    print("  r_tau = Phi_6(4)         = %d" % r_tau)
    print("  r_p   = Phi_6(7)         = %d" % r_p)
    print("  r_mu  = r_p - 2*r_tau    = %d" % r_mu)
    print("  -> {13, 17, 43} forced by P1, not tuned to data.")
    assert (r_tau, r_mu, r_p) == (13, 17, 43)

    # 5. Corollary 1: ord_43(7) = 6 ------------------------------------------
    print("\nCorollary 1: multiplicative order of 7 modulo 43")
    order = None
    for k in range(1, 8):
        val = pow(7, k, 43)
        note = ""
        if val == 6:
            note = "  (= sigma, the lattice constant n_null = tau*sigma = 6)"
        elif val == 42:
            note = "  (= -1 mod 43)"
        elif val == 1 and order is None:
            order = k
            note = "  <-- order = %d" % k
        print("  7^%d = %2d mod 43%s" % (k, val, note))
    assert order == 6
    print("  ord_43(7) = 6 = sigma  (OK)")

    # 6. Three-generation theorem --------------------------------------------
    print("\nThree-generation theorem:")
    print("  Phi_6 tower produces primes at {3, 7, 43}, then Phi_6(43) = 1807")
    print("  = 13 x 139 (composite) terminates the tower.")
    print("  => exactly three cooperative prime generations.  This is a theorem.")

    print("\nDone.")


if __name__ == "__main__":
    main()
