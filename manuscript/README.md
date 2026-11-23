# Sun's difference-permanent conjectures

**Alternative proofs for Sun's difference-permanent conjectures and Kunisky–Spielman–Yu's sign identity**

Haobo Ma — ChronoAI Pte Ltd, Singapore  
Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore

## Statements

For `a(n) = per[i-j]` on `1,...,2n`, the note proves `(-1)^n a(n) > 0` and divisibility by `2n+1` whenever that modulus is composite. The sign is also a consequence of Kunisky–Spielman–Yu's skew rank-two identity, arXiv:2608.28520v1, Section 5, pages 24–25. A coefficient proof supplies the equality criterion for arbitrary real inputs.

For all integer additive matrices of order `q-1`, divisibility by `q` holds exactly for composite `q != 4`. The exact common divisor at order `N` is `(N+1)!/lcm(1,...,N+1)`, using Farhi's identity. Marcus's Lemma 4 supplies the equivalent elementary-symmetric expansion. The note credits the earliest sources located for these ingredients and the reciprocal assertions, without a priority claim.

## Files and build

- `note.tex` is the single self-contained LaTeX source, including the bibliography.
- `note.pdf` is its readable rendering.
- `metadata.json` states authorship, license, source locators and mathematical coverage.
- `verify.py` contains exact finite checks using only the Python 3 standard library.
- `checks.json` is the expected checker output.
- `oeis-a346934.txt` contains the 130 values from the OEIS b-file.
- `manifest.json` binds the other package members by size and SHA-256.

Build with **Tectonic 0.17.0**:

```sh
tectonic note.tex
```

Alternatively use a standard TeX installation:

```sh
pdflatex note.tex
pdflatex note.tex
```

The bibliography is included in `note.tex`; no separate BibTeX database is needed.

Run the exact finite checks and compare with the supplied output:

```sh
python3 verify.py > checks-new.json
cmp checks.json checks-new.json
```

## Coverage

The written proofs cover the additive expansion and universal modulus classification, exact gcd, sign identity and equality criterion, centered positive formula, sum comparison, order-`q-1` power matrices, the prime and root-of-unity corollaries, and Jovovic's squared-sum expansion. The reciprocal assertions are cited to Guo–Li–Tao–Wei (arXiv:2206.02592v1, equation (1.1), Section 3) and Yang–Zhang (arXiv:2605.19502v1, Theorem 2(12)).

The [pinned Lean file](https://github.com/the-omega-institute/trureturing/blob/eac52692d71b89f89bd7c0d8c734ddc9c5d9e61d/D5/S3/Combinatorics/Permanental/SunA346934CompositeModulus.lean), declaration `D5.S3.Combinatorics.Permanental.SunA346934CompositeModulus.result`, states the odd-composite difference-permanent divisibility for `n>=1`. The other statements have the written or cited proofs specified above. The checker output records finite ranges and is distinct from these unrestricted proofs.

The order-`(q-1)/2` composite conjecture and reciprocal square-difference conjecture in A278847, both conjectures in A085807, and the asymptotic formulas are outside this note's coverage.

## License and data credit

The note and its original accompanying text and code are licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**, identifier `cc-by-4.0`.

The sequence values in `oeis-a346934.txt` are from [OEIS A346934's b-file](https://oeis.org/A346934/b346934.txt), credited in the entry to Vaclav Kotesovec. OEIS material remains under its separate **CC BY-SA 4.0** terms and [OEIS End-User License Agreement](https://oeis.org/wiki/The_OEIS_End-User_License_Agreement). This data notice is not a change to the note's CC BY 4.0 license.
