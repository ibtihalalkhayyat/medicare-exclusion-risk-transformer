# Stage23-B code release scope

**Included:** Original frozen inference architecture and validation logic (`src/frozen_stage8_inference.py`), public static HTML/JavaScript, fictional examples, cached model outputs on those fictional inputs, integrity-checking scripts, and unit tests.

**Not included:** Model checkpoint, fitted preprocessing or calibration files, NPI identifiers, real CMS/LEIE provider-level data, original training notebooks, credentials, unpublished individual-level scores, or sealed 2023 outcomes.

## Reproducibility limits

The public code **cannot reproduce original training or private inference outputs independently** without authorized access to immutable private files. Public checks validate the synthetic release and its provenance, not real-provider scientific performance.

## External source linkage

Space: https://huggingface.co/spaces/ibtihalalkhayyat/medicare-exclusion-risk-synthetic-demo

Dataset: https://huggingface.co/datasets/ibtihalalkhayyat/medicare-l5-synthetic-schema-demo

The frozen private-model repository is access-restricted; do not copy its private weights into this public repository. No standalone code license is designated at this stage.
