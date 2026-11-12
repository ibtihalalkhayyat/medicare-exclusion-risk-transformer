# Medicare Administrative Exclusion Risk — Temporal Transformer Research

**Status: Stage23-B source and synthetic demonstration release completed (12 November 2026).**

This academic project investigates whether five years of U.S. Medicare provider activity can help prioritize **human review** of future observed HHS–OIG administrative exclusions. Administrative exclusion is **not proof of fraud**. The repository is not an operational fraud-detection, payment, clinical, or enforcement tool.

## Completed work

- Frozen five-year PyTorch Transformer architecture using **140 input fields** (27 numeric plus one categorical per year).
- Immutable private model checkpoint, preprocessing, and Platt calibration retained separately.
- A bounded 2020–2022 risk-set and label reconciliation, with **no changes to labels of shared records**; the corrected event registry added one risk-set record per year.
- **24 fictional synthetic examples** and **504 precomputed outputs** generated using the frozen Transformer and frozen calibration.
- A publicly accessible, free **Static Space**, which presents precomputed values rather than live model predictions.

## Public resources

- **Demo website:** https://huggingface.co/spaces/ibtihalalkhayyat/medicare-exclusion-risk-synthetic-demo
- **Synthetic dataset:** https://huggingface.co/datasets/ibtihalalkhayyat/medicare-l5-synthetic-schema-demo
- **Private model (restricted):** https://huggingface.co/ibtihalalkhayyat/medicare-exclusion-risk-transformer-private

## Temporal evaluation design

| Anchor year | Role |
| --- | --- |
| 2017–2019 | Development / temporal cross-validation |
| 2020 | Validation and model selection |
| 2021 | COVID-era stress, no tuning |
| 2022 | Secondary temporal holdout, no tuning |
| 2023 | **Sealed final test:** 2026 outcome horizon incomplete; no unsealing |

**Protocol disclosure:** Early Stage3 material designated 2022 as the final test, whereas later governance reclassified it as a secondary holdout and designated 2023 as a sealed final test. The latter designation occurred during outcome accrual, not before it. Owner-signed amendment documentation remains outstanding.

## Download, run and verify the public release

The repository now contains the original frozen-model **source-only inference architecture**, the same public static demo HTML/data assets, the 140-input schema, a pinned source manifest, and three standard-library release tests. These files are safe for public demonstration but **do not contain private model artifacts**.

```bash
python scripts/verify_public_release.py
python -m unittest discover -s tests -v
python -m http.server 8000 --directory demo
```

Open `http://localhost:8000` for the public fictional-input demonstration. The Hugging Face mirror is pinned to commit `848236eed6da5aed4ac82b495c9a0dd23b41c2dd` for the static assets, with a SHA-256 check during GitHub Actions import. The Space README is treated as changeable platform metadata and has an independent GitHub demo README.

## Release boundaries

Only safety-reviewed **source-only inference logic, the 140-input schema, public static demo files, fictional examples, cached model outputs, and aggregate scientific documentation** are included. The GitHub Actions import and public tests passed on 12 November 2026. No original CMS/LEIE provider-level records, NPI labels, provider predictions, real source data, private model weights, preprocessing statistics, calibration coefficients, or sealed 2023 outcomes may be published here.

## Scientific limitations

The outcome is an observed administrative exclusion, not verified fraud. Historic LEIE coverage is incomplete and temporal provenance limits exact historical real-time emulation. Fictional inputs do not support valid probability statements about real providers. The full training pipeline and prespecified explainability work are **not** included in this initial public release.

## Next steps

The initial synthetic demonstration source and release checks are published. Next, complete the remaining scientific governance, explanation analyses, and manuscript, without opening the 2023 final-test outcomes.

## Citation and license

The final paper and a software license have not yet been approved by the research owner. **Do not assume an open-source code license.** The public synthetic dataset is separately licensed on Hugging Face.
