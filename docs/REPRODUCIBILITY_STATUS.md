# Reproducibility status

## What is reproducible publicly today

1. A **static** interactive web demonstration hosted on [Hugging Face Spaces](https://huggingface.co/spaces/ibtihalalkhayyat/medicare-exclusion-risk-synthetic-demo).
2. The format of **24 wholly synthetic** provider-history examples from [the public dataset](https://huggingface.co/datasets/ibtihalalkhayyat/medicare-l5-synthetic-schema-demo).
3. A display grid of **504 cached values** calculated offline using the frozen original Transformer plus frozen Platt calibration.
4. The disclosed temporal design, limited label-reconciliation aggregates and public source-release decisions.

## What is NOT independently reproducible from public assets

- Training the original Transformer from source CMS/LEIE data.
- Reproducing the 504 outputs from weights: the checkpoint, fitted preprocessing and calibrator are **private**.
- Evaluating real-provider metrics without restricted original data and stage-specific audit approval.
- Running new prediction requests in the static Space: there is **no live model server**.
- Using 2023 held-out test labels, which remain sealed until the outcome window and authorization gates are complete.

## Scientific next steps

Preserve and document environment locks, original-source hashes, frozen model/artifact versions and release manifests; complete the owner-signed protocol amendment, prespecified explainability work, full manuscript reporting, and rights/PII review before any wider release.

No public repository integrity check can be described as an independent validation of real-provider predictive performance.
