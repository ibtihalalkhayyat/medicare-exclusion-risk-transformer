# Medicare Administrative Exclusion Risk — Temporal Transformer Research

**Status: Research code release and synthetic demonstration (November 2026).**

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

## Release boundaries

Only independently screened **source-only inference logic, synthetic input schema, static demo files, synthetic examples, cached output displays, and aggregate scientific documentation** are intended for public release. No original CMS/LEIE provider-level records, NPI labels, provider predictions, real source data, private model weights, preprocessing statistics, calibration coefficients, or sealed 2023 outcomes may be published here.

## Scientific limitations

The outcome is an observed administrative exclusion, not verified fraud. Historic LEIE coverage is incomplete and temporal provenance limits exact historical real-time emulation. Fictional inputs do not support valid probability statements about real providers. The full training pipeline and prespecified explainability work are **not** included in this initial public release.

## Next steps

Publish the independently verified synthetic demonstration source files and release checks; complete the remaining scientific governance, explanation analyses, and manuscript, without opening the 2023 final-test outcomes.

## Citation and license

The final paper and a software license have not yet been approved by the research owner. **Do not assume an open-source code license.** The public synthetic dataset is separately licensed on Hugging Face.
