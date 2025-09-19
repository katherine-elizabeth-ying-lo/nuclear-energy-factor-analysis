# Nuclear Energy Factor Analysis

## Executive Summary
This project applies **Principal Component Analysis (PCA)** and a **residual z-score screen** to a basket of nuclear and utility stocks across the US, Canada, and UK.  

The goal is to test whether **nuclear is emerging as its own market driver**, distinct from broader utilities — highly relevant today as the US and UK announce nuclear partnerships and global uranium demand accelerates.

---

## Why these tickers?
The basket includes:
- **US utilities:** `CEG`, `VST`, `NRG`, `SO`, `DUK`, `NEE`, `EXC`  
- **Nuclear/uranium exposure:** `CCJ` (Cameco, Canada), `URA`, `URNM` (ETFs)  
- **UK exposure:** `CNA.L` (Centrica)  

This mix was chosen to:
- Capture **broad US utility beta**,  
- Add **direct uranium/nuclear exposure**,  
- Include **UK representation** (Centrica) to link with transatlantic policy news flow.

---

## Methodology
1. **Data collection** – daily adjusted closes via Yahoo Finance (`yfinance`).  
2. **Log returns** – compute daily returns, clean, and standardize.  
3. **PCA** – run on demeaned returns, retain enough PCs to explain ~80% variance.  
   - PC1: sector beta (common driver across all names)  
   - PC2: regional split (US vs non-US)  
   - PC3: uranium/nuclear factor (ETF + Cameco)  
   - PC4+: idiosyncratic company risk (e.g. NextEra renewables tilt, Centrica UK policy)  
4. **Residual z-score screen** – rolling 60-day z-scores of residuals.  
   - Positive = rich relative to peers → potential short  
   - Negative = cheap relative to peers → potential long  

---

## Results

### Variance Explained by PCs
By the fourth PC, ~85% of variance is explained.  
This suggests most movement is sector-wide, but a distinct **uranium factor** emerges by PC3.  


<img width="1200" height="600" alt="plot_pca_explained" src="https://github.com/user-attachments/assets/220cda0f-b573-41fb-be75-4b7e7ff1f55d" />


### Residual z-score screen
Example (latest run):  
- **Rich:** URA, CEG  
- **Cheap:** CCJ, SO, URNM  

This suggests uranium ETFs look extended vs Cameco and utilities.

---

## Why PCA?
- In markets, PCA helps **strip out beta** (common risk) and focus on **idiosyncratic alpha**.  
- For nuclear, the question is: *is it just utilities beta, or its own driver?*  
- PCA shows uranium names form a distinct component, supporting the idea that nuclear is now priced as a **separate theme**.  

---

## Relevance (2025 context)
- The **US-UK nuclear partnership** and broader “nuclear renaissance” make this question topical.  
- Utilities and uranium miners are moving in tandem with policy news, but PCA shows uranium is carving out its own factor.  
- This matters for trading desks: long/short screens can highlight which names are rich or cheap to the “nuclear factor,” not just general utilities.  

---

## Summary
- I ran PCA on a nuclear/utility basket, found 4 PCs explain ~85% of variance. PC1 was sector beta, PC3 was a uranium-specific driver. 
- I built a residual z-score screen: URA screened rich, CCJ and SO cheap. That’s the kind of RV idea PCA surfaces.  
- The project links to real-world context: US-UK nuclear partnerships, uranium pricing, and how traders separate systematic vs idiosyncratic risk.  

---

## Next steps
- Add **EWMA volatility scaling** or risk-parity weights.  
- Run **rolling PCA** to test stability of nuclear as a factor.  
- Overlay **event filters** (e.g., UK policy, uranium supply news).  

---

## License
MIT
