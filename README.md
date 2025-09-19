# nuclear-energy-factor-analysis
PCA and correlation analysis of nuclear energy stocks against utilities and energy benchmarks, exploring whether nuclear is emerging as its own market driver.


# PCA on Nuclear/Utilities (Minimal, Trading-Oriented)

**What this shows**
- PCA on a nuclear/utility basket to separate **sector/common** drivers from **idiosyncratic** ones.
- A **simple residual screen** using rolling z-scores to suggest long/short ideas (RV lens).
- Clean, explainable pipeline you can discuss in interviews.

## Why PCA (trading lens)
- Strip out the **sector beta** and see what’s left (idiosyncratic signals).
- If the “nuclear renaissance” is broadly priced into the sector, **alpha** likely sits in residuals.
- Loadings tell you which names are **beta-heavy** vs **residual-rich**.

## How to run
```bash
pip install -U yfinance pandas numpy matplotlib scikit-learn scipy
python pca_nuclear_simple.py
```

## What to look at
- `plot_pca_explained.png` – Cumulative variance explained; you’ll mention you kept PCs to ~80%.
- `loadings.csv` – Which names load on PC1 (sector/macro) vs later PCs (idiosyncratic).
- `residual_latest_zscores.csv` – Top (rich) vs bottom (cheap) residual z-scores (rolling 60-day).

## Talking points (interviews)
- “I ran PCA on a nuclear/utility basket, retained PCs to explain ~80% variance. **PC1** read as the sector driver; later PCs captured **stock-specific** effects. I then built a **rolling residual z-score screen**: **top** = potentially rich (short), **bottom** = potentially cheap (long). Next step would be **risk-controls** (e.g., equal risk weights or a light EWMA sizing) and a quick **event/risk sanity check** (policy headlines, outages).”

## Tickers
Editable in the script:
- `CEG`, `VST`, `NRG` (US utilities)
- `CCJ` (Cameco), `URA` (uranium ETF)
- `CNA.L` (Centrica, UK)

## Keep it simple
This repo intentionally avoids heavier volatility models. If asked about risk, mention you can add **EWMA sizing** or a **t-GARCH + VaR** appendix.
