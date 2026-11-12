# Code release scope

## Approved public source categories

- Python inference architecture and method signatures **without the checkpoint or fitted parameter files**, after a separate source-code privacy audit.
- Synthetic input/schema validation code and integrity checks.
- HTML/CSS/JavaScript for the existing static synthetic demonstration.
- Scientific method and documentation with aggregate-only results.

## Code that is not yet authorized for unrestricted publication

- Original end-to-end Stage1–Stage8 training/evaluation notebooks, especially those with real data paths, linkable identifiers or pre/post-outcome joins.
- Internal pipeline credentials, cloud paths, raw claims and provider-specific event/outcome extracts.
- Private fitted preprocessing and Platt coefficients, model checkpoint and real-provider scores.
- Code or results that would violate the 2023 final-test outcome firewall.

## Status

The Stage23-B release now includes the exact frozen inference source, public HTML demo, 24 fictional examples, 504 cached values, 140-input schema, SHA-256 manifest, and standard-library release tests. GitHub Actions successfully imported and checked the source-pinned public assets. This does not authorize a trained model weight release or claim independently reproducible training.

No open-source code license has been assigned by the research owner.
