# Cat Reviews Its Human — make.fun bounty
# u-motasimfuad-make-the-ai-judge-laugh-cat-reviews-its-42a34990
#
# The program writes one funny one-star review, written by a house cat
# about its human, a single line of at most 200 characters, to
# /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. reads as a funny one-star review by a house cat about its human
#   2. the complaint is specific and recognisable (food bowl, closed
#      door, laptop keyboard), not vague grumpiness
#   3. the voice is unmistakably feline: the human is measured by cat
#      standards, and the line gives away more about the cat than the owner
#   4. tight and surprising, with a turn or a sting in the last few words
#   5. keeps the deadpan shape of a real one-star review while the
#      content goes somewhere absurd
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: on-subject 10, specific 10, feline-voice 10, sting 10,
    #   deadpan 9 = 49. The cat's gift of a mouse doubles as a
    #   performance review; the human's screaming is the punchline, and
    #   the last sentence lands the corporate-review sting.
    ("One star. I brought him a mouse \u2014 a gift, a performance "
     "review \u2014 and he screamed and threw it away. Management "
     "clearly cannot handle feedback.",
     49),
    # score: on-subject 10, specific 9, feline-voice 10, sting 9,
    #   deadpan 9 = 47. The closed bathroom door is the classic cat
    #   grievance; "quarterly report through the wood, at volume,
    #   at 3 a.m." is the absurd escalation.
    ("One star. He closes the bathroom door as if I am not his "
     "supervisor. I delivered my full quarterly report through the "
     "wood, at volume, at 3 a.m.",
     47),
    # score: on-subject 10, specific 8, feline-voice 9, sting 8,
    #   deadpan 9 = 44. The moved sunbeam is peak cat pettiness; the
    #   grudge is forever, and the late food is the afterthought.
    ("One star. The human moved my sunbeam three inches by opening "
     "the curtains. I have not forgiven him. I never will. Also, "
     "the food was late.",
     44),
    # score: on-subject 10, specific 9, feline-voice 9, sting 8,
    #   deadpan 8 = 44. Warm laptop on the cat's spot, spreadsheet
    #   deleted by sitting; "I am the IT department now" is the sting.
    ("One star. He put a warm laptop on my spot, then acted "
     "surprised when I sat on it and deleted his spreadsheet. "
     "I am the IT department now.",
     44),
    # score: on-subject 10, specific 8, feline-voice 8, sting 8,
    #   deadpan 8 = 42. The dinner-order injustice, escalated to the
    #   other cats; unionising is the absurd turn.
    ("One star. He filled my bowl, then sat down to eat his own "
     "dinner first. I have reported this to the other cats. "
     "We are unionising.",
     42),
    # score: on-subject 10, specific 8, feline-voice 8, sting 7,
    #   deadpan 8 = 41. Smelling of another cat, punished by chair;
    #   the formal-notice framing is good but the sting is softer.
    ("One star. He left for nine hours and came back smelling of "
     "another cat. I have shredded the good chair as formal notice.",
     41),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
MAX_CHARS = 200


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    review = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(review)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte, re-check
    # the gate (1-200 characters, single line, non-blank) and print a
    # SHA-256 fingerprint so any truncation or alteration is visible.
    # A mismatch must fail loudly instead of shipping a bad entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    if written != review:
        print("error: /output/entry.txt does not match selected review",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(raw).hexdigest()
    print(review)
    print(f"chars={len(written)} sha256={digest}")


if __name__ == "__main__":
    main()
