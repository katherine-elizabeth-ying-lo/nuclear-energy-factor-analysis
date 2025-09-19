# pca_nuclear_simple.py
# ------------------------------------------------------------
# Purpose: Minimal, interview-ready PCA on a nuclear/utility basket
# What it shows:
#   1) Download prices -> compute daily log returns
#   2) Run PCA on demeaned returns (covariance)
#   3) Keep enough PCs to explain ~80% variance
#   4) Inspect loadings (sector/common vs idiosyncratic)
#   5) Build a simple residual screen (rolling z-scores) for RV ideas
#
# How to run:
#   pip install -U yfinance pandas numpy matplotlib scikit-learn scipy
#   python notebooks/src/pca_nuclear_simple.py
#
# Files created:
#   plot_pca_explained.png          # variance explained
#   loadings.csv                    # PCA loadings (tickers x PCs)
#   explained_variance.csv          # variance ratio table
#   residual_latest_zscores.csv     # latest residual z-scores (for signals)
# ------------------------------------------------------------

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# --------------------------
# 0) Config
# --------------------------

TICKERS = [
    "CEG","VST","NRG","CCJ","URA","URNM",
    "SO","DUK","NEE","EXC","CNA.L"
]

START = "2018-01-01"
END = None
VAR_TARGET = 0.80              # Keep PCs to explain ~80% variance
ROLL = 60                      # Rolling window for residual z-scores
OUTDIR = "."                   # Save outputs to current folder

# --------------------------
# 1) Download prices & returns
# --------------------------
print("Downloading tickers one by one...")
px_list = []
for t in TICKERS:
    df = yf.download(t, start=START, end=END, auto_adjust=True, progress=False)[["Close"]]
    if not df.empty:
        px_list.append(df.rename(columns={"Close": t}))
        print(f"  {t} downloaded")
    else:
        print(f"  {t} failed")

if len(px_list) == 0:
    raise ValueError("No tickers returned any data.")

px = pd.concat(px_list, axis=1)
tickers_used = list(px.columns)
print(f"Final ticker set used: {tickers_used}")


if len(tickers_used) < 3:
    print(f"Warning: only {len(tickers_used)} valid tickers downloaded: {tickers_used}")
else:
    print(f"Using {len(tickers_used)} tickers:", tickers_used)

# Daily log returns
ret = np.log(px).diff().dropna()
ret = ret.replace([np.inf, -np.inf], np.nan).dropna()

# --------------------------
# 2) PCA on demeaned returns
# --------------------------
print("Running PCA...")
X = ret - ret.mean(0)

pca = PCA()
pca.fit(X)

explained = pca.explained_variance_ratio_
cum_expl = explained.cumsum()
k = int(np.searchsorted(cum_expl, VAR_TARGET) + 1)
k = max(1, min(k, X.shape[1]))

print(f"PCA retains {k} PCs to reach ~{cum_expl[k-1]*100:.1f}% variance.")

# Scores (factors) and loadings
F = pd.DataFrame(pca.transform(X)[:, :k], index=X.index, columns=[f"PC{i+1}" for i in range(k)])
L = pd.DataFrame(pca.components_[:k, :].T, index=tickers_used, columns=F.columns)

# --------------------------
# 3) Save results + variance plot
# --------------------------
explained_table = pd.DataFrame({
    "PC": [f"PC{i+1}" for i in range(len(explained))],
    "ExplainedVarianceRatio": explained,
    "CumulativeVariance": cum_expl
})
explained_table.to_csv(f"{OUTDIR}/explained_variance.csv", index=False)
L.to_csv(f"{OUTDIR}/loadings.csv")

plt.figure(figsize=(8,4))
plt.step(range(1, len(explained)+1), cum_expl*100, where="mid")
plt.axhline(VAR_TARGET*100, linestyle="--")
plt.title("Cumulative Variance Explained by PCs")
plt.xlabel("PC #")
plt.ylabel("Cumulative % Explained")
plt.tight_layout()
plt.savefig(f"{OUTDIR}/plot_pca_explained.png", dpi=150)

print("Saved: explained_variance.csv, loadings.csv, plot_pca_explained.png")

# --------------------------
# 4) Simple residual screen (rolling z-score)
# --------------------------
print("Building residual z-score screen...")
X_hat = F.values @ L.values.T
resid = pd.DataFrame(X.values - X_hat, index=X.index, columns=tickers_used)

# Rolling z-score of residuals
z = (resid - resid.rolling(ROLL).mean()) / resid.rolling(ROLL).std()
latest = z.dropna().iloc[-1].sort_values(ascending=False)

signals = pd.DataFrame({
    "Ticker": latest.index,
    "ResidualZ": latest.values
}).sort_values("ResidualZ", ascending=False)

signals.to_csv(f"{OUTDIR}/residual_latest_zscores.csv", index=False)

print("\nTop residual z-scores (potential shorts):")
print(signals.head(3))
print("\nBottom residual z-scores (potential longs):")
print(signals.tail(3))

print("\nDone. Files saved in current folder.")
