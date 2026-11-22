"""Small tools for DNA sequences: your module from Module 1, lesson 7.

gc_content() returns a fraction between 0 and 1. Your tool prints GC% as a
percentage, so multiply by 100.
"""

COMPLEMENT = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}


def gc_content(seq):
    """Share of G and C bases, ignoring N."""
    seq = seq.upper()
    known = len(seq) - seq.count("N")
    if known == 0:
        raise ValueError("sequence has no A, C, G or T bases")
    return (seq.count("G") + seq.count("C")) / known


def reverse_complement(seq):
    """Reverse complement; N stays N."""
    try:
        return "".join(COMPLEMENT[base] for base in reversed(seq.upper()))
    except KeyError as err:
        raise ValueError(f"not a DNA base: {err.args[0]!r}") from None
