# market-regime-research
# Market Regime Research

This repository is dedicated to **objective research into market regimes**, specifically:
- Trend
- Compression / Range

The purpose of this project is **measurement, not strategy**.

## Data
Raw daily FX data lives in the `data/` directory.
- One CSV per symbol
- Data is treated as immutable truth
- No indicators or labels are assumed

Schema:

`MarketState` is intentionally left as `UNKNOWN` at this stage.

## Analysis
All analysis scripts live in `analysis/`.

Initial focus:
- Volatility compression
- Price overlap
- Directional efficiency
- Behavioural patterns over rolling windows

No trading logic.
No optimisation.
No thresholds.

## Outputs
Generated research outputs are written to `outputs/`.

These are **derived artefacts** and may be regenerated at any time.

## Philosophy
- Observe first
- Measure behaviour
- Derive rules only after evidence
- Separate regime detection from strategy execution

This repo supports a broader market-structure framework but stands alone as a **pure research environment**.
