#!/usr/bin/env python3
"""
pmns_pairs.py  --  Are the 8 non-EDEM (theta_12, theta_23) pairs derivable?
===========================================================================

WHAT THIS SCRIPT TESTS
----------------------
pmns_scan.py found that, within 0.1 sigma of the data, the hypothesis class H
contains exactly three candidates for each of the two well-measured angles:

        sin^2(theta_12) within 0.1 sigma :  26/85, 15/49, 4/13
        sin^2(theta_23) within 0.1 sigma :   6/11, 65/119, 23/42

Their Cartesian product is 3 x 3 = 9 candidate PAIRS, all numerically acceptable.
EDEM uses exactly one of them, (4/13, 6/11).  This script asks the obvious
follow-up question: of the other EIGHT pairs, does ANY have a genuine EDEM
*structural* derivation -- i.e. does it appear in the EDEM theorem register, the
closed list of fractions that the five postulates actually prove?

THE DISTINCTION THAT MATTERS
----------------------------
All nine pairs live in H *by construction* -- that is what "candidate" means.
Being in H is cheap (their numerators/denominators are just products of G, e.g.
85 = 5*17, 49 = 7*7, 119 = 7*17, 42 = 6*7).  The expensive, falsifiable property
is being in the THEOREM REGISTER: a fraction that some postulate P1-P5 forces.

EXPECTED OUTPUT (the result a referee should reproduce)
-------------------------------------------------------
  * 9 pairs enumerated.
  * Exactly 1 pair, (4/13, 6/11), has both members in the theorem register.
  * The four "foreign" fractions {26/85, 15/49, 65/119, 23/42} are NOT in the
    register and have no structural derivation -> the other 8 pairs are excluded.
  * EDEM-internal uniqueness check:
        - closest competing register value to sin^2(theta_12) is 4/9 (~10.6 sigma)
        - closest competing register value to sin^2(theta_23) is 8/15 (~0.6 sigma,
          and that value is already spoken for as |U_mu3|^2).

Standard library only.
"""

from fractions import Fraction
from itertools import combinations_with_replacement

# ---------------------------------------------------------------------------
# EDEM primitive set G  (see pmns_scan.py for the per-element provenance).
# ---------------------------------------------------------------------------
G = [
    2,    # tau    : temporal prime p1
    3,    # sigma  : spatial prime p2
    5,    # g      : generation constant, tau^2 + 1
    6,    # n_null : minimal null composite, tau * sigma
    7,    # p4     : fourth lattice prime
    13,   # r_tau  : temporal resonance, tau^4 - tau^2 + 1
    17,   # tau^4 + 1 lattice resonance
    43,   # r_p    : spatial/proton resonance (sigma^2*g = r_p + tau = 45)
]

PDG = {
    'th12': (0.307, 0.013),     # sin^2(theta_12)
    'th23': (0.546, 0.021),     # sin^2(theta_23)
}

# ---------------------------------------------------------------------------
# EDEM theorem register: fractions actually PROVED by postulates P1-P5.
# (membership here -- not membership in H -- is the falsifiable property.)
# ---------------------------------------------------------------------------
EDEM_REGISTER = {
    Fraction(4, 13):   'tau^2 / r_tau            -- temporal sector (T_SECTOR_ASSIGN)',
    Fraction(6, 11):   'n_null / (n_null + g)    -- null sector (T_SECTOR_ASSIGN)',
    Fraction(1, 45):   '1 / (sigma^2 * g)        -- spatial residue (T_UNIT_RESIDUE)',
    Fraction(4, 9):    'tau^2 / sigma^2          = |U_tau3|^2',
    Fraction(8, 15):   'tau^2*n_null/(sigma^2*g) = |U_mu3|^2',
    Fraction(44, 65):  'tau^2*(n_null+g)/(g*r_tau)         = |U_e1|^2',
    Fraction(176, 585):'tau^2*(n_null+g-1)/(r_tau*sigma^2*g) = |U_e2|^2',
    Fraction(2, 3):    'tau / sigma              -- bare epoch-prime ratio',
}


def build_H(elements):
    """Hypothesis class H: reduced fractions in (0,1) whose numerator and
    denominator are each a singleton, pairwise product, or pairwise sum of G."""
    atoms = set(elements)
    for a, b in combinations_with_replacement(elements, 2):
        atoms.add(a * b)
        atoms.add(a + b)
    H = set()
    for a in atoms:
        for b in atoms:
            if 0 < a < b:
                H.add(Fraction(a, b))
    return H


def members_within(H, mu, sigma, k=0.1):
    return sorted((f for f in H if abs(float(f) - mu) <= k * sigma), key=float)


def pull(value, mu, sigma):
    return (float(value) - mu) / sigma


def main():
    print("=" * 74)
    print("  EDEM PMNS pair analysis  (pmns_pairs.py)")
    print("=" * 74)

    H = build_H(G)
    cand12 = members_within(H, *PDG['th12'])
    cand23 = members_within(H, *PDG['th23'])

    print("\n0.1-sigma candidates regenerated from H:")
    print("  theta_12 :", ", ".join(str(f) for f in cand12))
    print("  theta_23 :", ", ".join(str(f) for f in cand23))

    # Self-check against the values quoted in the paper.
    assert set(cand12) == {Fraction(26, 85), Fraction(15, 49), Fraction(4, 13)}
    assert set(cand23) == {Fraction(6, 11), Fraction(65, 119), Fraction(23, 42)}

    # ------------------------------------------------------------------
    # Enumerate all 9 pairs and test theorem-register membership.
    # ------------------------------------------------------------------
    print("\n" + "-" * 74)
    print("  All %d candidate pairs : is each member in the EDEM theorem register?" %
          (len(cand12) * len(cand23)))
    print("-" * 74)
    print("  %-9s %-9s  %-7s %-7s  %s" % ("th12", "th23", "reg12?", "reg23?", "verdict"))
    edem_pairs = []
    for f12 in cand12:
        for f23 in cand23:
            in12 = f12 in EDEM_REGISTER
            in23 = f23 in EDEM_REGISTER
            verdict = "EDEM-DERIVED" if (in12 and in23) else "no derivation"
            if in12 and in23:
                edem_pairs.append((f12, f23))
            print("  %-9s %-9s  %-7s %-7s  %s" %
                  (f12, f23, "yes" if in12 else "no", "yes" if in23 else "no", verdict))

    print("\n  EDEM-derived pairs : %d  ->  %s" %
          (len(edem_pairs), ", ".join("(%s, %s)" % p for p in edem_pairs)))
    assert edem_pairs == [(Fraction(4, 13), Fraction(6, 11))], \
        "expected the unique EDEM pair (4/13, 6/11)"

    # ------------------------------------------------------------------
    # The four "foreign" fractions: in H, but not provable.
    # ------------------------------------------------------------------
    print("\n" + "-" * 74)
    print("  The non-EDEM fractions: present in H, absent from the register")
    print("-" * 74)
    foreign = [Fraction(26, 85), Fraction(15, 49), Fraction(65, 119), Fraction(23, 42)]
    fact = {26: "2*13", 85: "5*17", 15: "3*5", 49: "7*7",
            65: "5*13", 119: "7*17", 23: "17+6", 42: "6*7"}
    for f in foreign:
        n, d = f.numerator, f.denominator
        print("  %-7s = %s / %s   in H (yes), in register (%s)  -> no structural derivation" %
              (str(f), fact.get(n, str(n)), fact.get(d, str(d)),
               "yes" if f in EDEM_REGISTER else "no"))
    assert not any(f in EDEM_REGISTER for f in foreign)

    # ------------------------------------------------------------------
    # EDEM-internal uniqueness: closest competing register value per angle,
    # excluding values that are algebraic consequences of the assigned angle.
    # ------------------------------------------------------------------
    print("\n" + "-" * 74)
    print("  EDEM-internal uniqueness (closest INDEPENDENT register competitor)")
    print("-" * 74)
    # Quantities that are direct functions of a given angle are degenerate with it
    # and do not count as independent competitors for that angle's slot.
    derived_from = {
        'th12': {Fraction(176, 585), Fraction(44, 65)},  # = s12^2*c13^2 etc.
        'th23': set(),
    }
    assigned = {'th12': Fraction(4, 13), 'th23': Fraction(6, 11)}
    for ang in ('th12', 'th23'):
        mu, sigma = PDG[ang]
        comp = []
        for fr in EDEM_REGISTER:
            if fr == assigned[ang] or fr in derived_from[ang]:
                continue
            comp.append((abs(pull(fr, mu, sigma)), fr))
        comp.sort()
        best_d, best_f = comp[0]
        note = "  (already assigned as |U_mu3|^2)" if best_f == Fraction(8, 15) else ""
        print("  %-6s assigned %-5s (pull %+.3f sig).  closest competitor: %-5s at %.1f sig%s" %
              (ang, str(assigned[ang]), pull(assigned[ang], mu, sigma),
               str(best_f), best_d, note))

    print("\nConclusion: of the 9 numerically-allowed pairs, exactly one -- (4/13, 6/11) --")
    print("is forced by the postulates.  The other eight are arithmetic coincidences in H")
    print("with no EDEM derivation.")
    print("\nDone.")


if __name__ == "__main__":
    main()
