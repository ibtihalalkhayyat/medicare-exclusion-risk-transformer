# Frozen Transformer — Public Synthetic Demonstration

This folder mirrors the **data and interface components** of the public [Medicare Hugging Face Static Space](https://huggingface.co/spaces/ibtihalalkhayyat/medicare-exclusion-risk-synthetic-demo).

## What the site does
- Displays **24 fictional** five-year provider activity profiles.
- Displays **504 precomputed outputs** from the **original frozen Transformer and Platt calibration** for 21 fixed multipliers per fictional profile.
- Uses static HTML/JavaScript without a live model server. The outputs are cached lookups and **not** live predictions.
- Does not include real CMS records, provider identifiers, original HHS–OIG outcome labels, checkpoints, or fitted parameters.

## Files
- `index.html` — static responsive website.
- `data/scenarios.json` — fictional feature vectors only.
- `data/synthetic_examples.csv` — equivalent fictional table.
- `data/inference_grid.json` — cached calibrated values, not measured real-world predictive performance.
- `data/model_output_provenance.json` — hashes and scientific limitations.
- Root `schema.json` — 140 model input columns, plus fictional example ID.

## Local preview

Run `python -m http.server 8000 --directory demo`, then open `http://localhost:8000`.

Validation: `python scripts/verify_public_release.py` and `python -m unittest discover -s tests -v`.

**Warning:** Fictional example scores do not represent validated probabilities, fraud findings, real provider rankings, causal changes, payment advice, or enforcement decisions. The sealed 2023 outcome set is not included.

Static demonstration files are imported from the exact audited Hugging Face commit through SHA-256 checks. The Space README on the Hub may have platform-adjusted metadata, so this GitHub documentation is not presented as a byte-for-byte copy of that README.
