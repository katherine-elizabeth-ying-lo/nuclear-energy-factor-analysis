# Nuclear Energy Factor Analysis


## Key Findings


The analysis shows that **nuclear equities (CCJ, URA, URNM) and merchant utilities (CEG, VST, NRG) are not the same trade**.  

- PCA separated them into a distinct **“see-saw” factor (PC2):** uranium trades like a **commodity cycle** (supply deficits, policy), while merchant utilities move with **wholesale power market tightness** (ERCOT/PJM prices).  

- The **residual screen flagged URA as rich (+2.9σ)** compared to Cameco and URNM, which screened cheap. This suggests the ETF’s basket effect (smaller uranium names outperforming) pulled URA ahead of the main producer.  

- **Relative-value lens:** traders could frame this as **short URA vs long Cameco/URNM** to capture a potential convergence, while recognising risks (liquidity, borrow costs, event headlines).  

**Why this matters:**  
Even though uranium ultimately fuels nuclear power (and thus electricity generation), markets are not yet pricing it like merchant utilities. Instead, uranium trades as a **stand-alone commodity theme**, while merchant utilities track power price cycles. That separation means uranium is emerging as its **own factor**, so relative-value trades only make sense after hedging out the shared utilities beta.


---

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
4. **Residual z-score screen** – rolling 60-day z-scores of residuals.  
   - Positive = rich relative to peers → potential short  
   - Negative = cheap relative to peers → potential long  

---

## Results

### Variance Explained by PCs
By the fourth PC, ~85% of variance is explained.  
This suggests most movement is sector-wide, but distinct **uranium** and **regulated-utility** components also emerge.  


<img width="1200" height="600" alt="plot_pca_explained" src="https://github.com/user-attachments/assets/220cda0f-b573-41fb-be75-4b7e7ff1f55d" />

<img width="667" height="291" alt="Screen Shot 2025-09-19 at 17 03 11" src="https://github.com/user-attachments/assets/1864b185-6eff-4dce-b906-74eece10c4e4" />

---

### PC1 – Sector Beta (~51% variance explained)
The first component captures the broad market/sector driver. High loadings on **CEG (0.39), VST (0.44), CCJ (0.46), URA (0.40), and URNM (0.42)** show that both merchant utilities and uranium names swing together under macro and sector conditions. By contrast, regulated names like **SO (0.04), DUK (0.04), CNA.L (0.04)** load only lightly, consistent with their rate-base insulation: regulated utilities pass through fuel costs and earn capped returns, so they are structurally less exposed to commodity volatility. This lines up with policy support such as the U.S. **Inflation Reduction Act’s 45U production credit** for nuclear plants, which further stabilises cashflows. PC1 is thus the “sector wind” lifting most nuclear and utility names, with regulated stocks less sensitive to the tide.

---

### PC2 – Uranium vs Merchant Utilities (~19% variance explained)
The second component emerges as a **see-saw between uranium equities and U.S. merchant utilities**. Uranium names (**CCJ –0.40, URA –0.34, URNM –0.42**) load strongly negative, while merchant utilities (**CEG 0.42, VST 0.48, NRG 0.36**) load strongly positive. Regulated utilities remain near zero, indicating they are not part of this tug-of-war. Economically, this reflects how **uranium trades more like a commodity cycle**, while merchant utilities benefit when wholesale power markets tighten.

**Why?**

- Uranium trades more like a commodity cycle (spot uranium price, supply shocks, mine restarts, policy).

- Merchant utilities make money from selling electricity into wholesale markets → they benefit from power price tightening (like Texas heatwaves, gas price spikes).

As of **August 2025, spot uranium was around $59.58/lb** (not yet $100). Banks such as **Citi** and **Morgan Stanley** have published forecasts that prices could **approach or exceed $100/lb** given tight supply and policy tailwinds, and a Forbes piece (Sept 2025) described uranium as “marching towards $100.” The **2025 U.S.–UK civil nuclear partnership** further reinforced uranium as a distinct investment theme. PC2 therefore isolates a factor that traders actively track: the performance gap between uranium exposures and merchant utilities.

---

### PC3 – Regulated & Renewables Utilities (~10% variance explained)
The third component clusters the regulated and renewables-tilted names: **SO (0.43), DUK (0.41), NEE (0.60), EXC (0.45), CNA.L (0.24)**. This is a coherent group of companies whose earnings are **policy-linked and rate-sensitive**. Unlike uranium or merchant names, these stocks move together on regulatory cycles, interest-rate expectations, and renewables investment policy. **NextEra’s outsized loading (0.60)** is consistent with its renewables tilt (via NEER) alongside its regulated Florida utility arm. Similarly, UK utilities like **Centrica** are tied into government policy decisions, with **Sizewell C receiving final investment approval in 2025**. PC3 thus represents a defensive, policy-driven axis distinct from commodity swings — the “regulated/renewables cluster.”

---

### PC4 – Pair-trade Axis (~5% variance explained)
The fourth component is narrower, with **CEG (0.72)** and **NRG (–0.63)** showing strong opposing loadings. This looks less like a sector factor and more like an **idiosyncratic spread between two merchant names**. Traders could read this as a statistical justification for **pair-trading Constellation vs NRG**, but it doesn’t carry broad sector interpretation.

---
### Residual z-score screen
The residual screen highlights which names trade rich/cheap versus their factor-implied fair value.  
Example (latest run):  

<img width="259" height="288" alt="Screen Shot 2025-09-19 at 17 07 35" src="https://github.com/user-attachments/assets/023d8975-23f3-4188-984d-eed92a860f90" />

**Interpretation:**  
- **URA (+2.9σ)** screened rich. This reflects uranium equities rallying on a structural supply deficit (~35m lbs in 2025), financial buying (SPUT), and policy tailwinds (U.S.–UK partnership, EU taxonomy). This isn’t from new inflows (1Y flows are –$67.7m) but from uranium equities inside the ETF (Cameco, Oklo, UEC) rallying hard in 2025. 
- **URNM and CCJ screened cheap** despite being direct uranium exposures, suggesting ETF demand may have run ahead of single-name performance.
- URA screened rich vs Cameco/URNM. That suggests the ETF’s basket effect — small-cap uranium names rallying hard — pulled the ETF above what the larger producer implied. In relative-value terms, URA looks extended while CCJ/URNM lag, which could justify a **pairs idea: short URA vs long Cameco.**
- **SO (–1.1σ)** cheap vs **CEG/VST (+0.4–0.5σ rich)** fits the merchant vs regulated split. Merchant names benefit when wholesale markets tighten — as seen in ERCOT and PJM during U.S. summer 2025, which lifted VST and CEG earnings — while regulated names lag since their returns are capped by regulators.

---

## Why PCA?
- PCA helps **strip out beta** (common risk) and focus on **idiosyncratic alpha**.  
- The question here is: *is nuclear just utilities beta, or its own driver?*  
- The decomposition shows uranium names form a distinct component, supporting the idea that nuclear is now priced as a **separate theme**.

---

## Relevance (2025 context)
- The **US–UK nuclear partnership** and broader “nuclear renaissance” make this question topical.  
- Utilities and uranium miners are moving with policy news, but PCA shows uranium is carving out its own factor.  
- For trading desks, relative-value screens can identify which names are rich or cheap to the **nuclear factor**, not just general utilities beta.

---

## Summary
- PCA on a nuclear/utility basket finds four components explaining ~85% of variance.  
- **PC1:** sector beta; **PC2:** uranium vs merchant utilities; **PC3:** regulated/renewables cluster; **PC4:** pair-trade spread.  
- A residual z-score screen highlights potential relative-value ideas after neutralising the main factors.

---

## Next steps
- Add **EWMA volatility scaling** or risk-parity weights.  
- Run **rolling PCA** to test factor stability through time.  
- Overlay **event filters** (e.g., UK policy, uranium supply news).

---

## License
MIT
