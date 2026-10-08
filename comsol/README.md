# COMSOL rebuild lessons

Start with [the first 0D benchmark](lessons/M1.html#p0). Read [M1](lessons/M1.html) → [M2](lessons/M2.html) → [M3](lessons/M3.html) → [M4](lessons/M4.html) after the existing J/L course. The route has 328 numbered GUI steps, with exact input fields, save points and observation/error checks.

Read [GUI basics](reference/gui-basics.html) for panels and imports. The [worked theory](reference/worked-theory.html) includes governing assumptions, symbol tables, complete derivations and dimensional/limiting checks; download its [LaTeX source](reference/worked-theory.tex).

Use the [blank-model recipe](reference/rebuild.html), exact imports and `rebuild/Run-Rebuild.ps1` with COMSOL 6.4. Sources use a portable root; the runner substitutes the extracted project location. Rebuilding creates the native models and complete settings locally. Install the Python reference dependencies from `rebuild/requirements-reference.txt` for independent calculations. Native model files, original PDFs and private recovery/learning records are outside the public lesson edition. The four chapters remain awaiting independent learner demonstration.
