# Scientific status — November 2026

## Research question
Can a frozen five-year (L5) Transformer rank future **observed** HHS–OIG administrative-exclusion events among U.S. Medicare providers for human review?

**Not** a verified fraud diagnosis, a causal finding, or permission for automated payment denial or enforcement.

## Frozen study design

| Period | Role |
| --- | --- |
| 2017–2019 | Development; temporal cross-validation |
| 2020 | Validation / model selection |
| 2021 | COVID-era temporal stress; no tuning |
| 2022 | Secondary temporal holdout; no tuning |
| 2023 | Sealed outcome-blind final test; 2026 outcomes not yet complete |

The five-year input has **140 model fields**: 27 numeric and 1 categorical field for each of five years. The model, fitted preprocessing, and temporal Platt calibrator remain frozen in a **private** repository.

## Confirmed bounded label reconciliation

| Anchor | Originally frozen risk set | Revised registry risk set | Observed positives | Shared-row label changes |
| --- | ---: | ---: | ---: | ---: |
| 2020 | 757,095 | 757,096 | 52 | 0 |
| 2021 | 770,227 | 770,228 | 59 | 0 |
| 2022 | 781,607 | 781,608 | 32 | 0 |

These are aggregate audit counts **not recomputed predictive performance**. The revised event registry was not available before the initial Stage3 protocol freeze.

## Protocol amendment disclosure

The earliest Stage3 protocol designated **2022** as the locked final test. Later Stage3/Stage4.5 governance designated it as a secondary holdout and **2023** as the sealed final test. The latter designation occurred during outcome accrual, not before accrual began. Documenting the rationale and obtaining owner-signed amendment evidence remain pending.

## Limitations

- Historical LEIE evidence is incomplete, and reinstated records may be absent from current public registries.
- No observed exclusion is **not** confirmed legitimate conduct.
- Exact point-in-time CMS historical data-vintage reconstruction was not established.
- Full prespecified explainability analysis is still incomplete.
- Do not expose or inspect the sealed 2023 outcomes before the 2026 outcome window ends and release is authorized.

## What the public website shows

The [public Static Space](https://huggingface.co/spaces/ibtihalalkhayyat/medicare-exclusion-risk-synthetic-demo) presents 504 **cached** model outputs for 24 **fictional** profiles and 21 fixed input multipliers. It does not compute live predictions or establish real-world risk probabilities for synthetic examples.
