#I pulled daily prices for nuclear names (CEG, VST, CCJ, EDF, KAP) and for utilities/energy benchmarks (XLU, XLE, S&P). 
#I turned prices into returns, checked correlations, and ran PCA to see how many common forces drive the moves. 
#I also looked at rolling correlations to see if nuclear is de-linking over time. If nuclear names cluster together and load differently 
#from utilities/energy on the first PCs—and their correlation to XLU/XLE trends down—that’s evidence of an emerging ‘nuclear factor’.

# src/nuclear_factor_analysis.py
# Quick, self-contained script: downloads data, builds returns,
# saves CSVs, runs correlations + PCA, and exports charts.

from pathlib import Path
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
plt.rcParams["figure.dpi"] = 140

# ----------------------
# 1) Project paths
# ----------------------
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGS = ROOT / "figures"
DATA.mkdir(exist_ok=True)
FIGS.mkdir(exist_ok=True)

# ----------------------
# 2) Universe (edit as you like)
# ----------------------
NUCLEAR = {
    "CEG": "Constellation Energy (US)",
    "VST": "Vistra (US)",
    "CCJ": "Cameco (CA)",
    "EDF.PA": "EDF (FR)",
    "KAP.L": "Kazatomprom GDR (UK)",
}
BENCH = {
    "XLU": "US Utilities ETF",
    "XLE": "US Energy ETF",
    "^GSPC": "S&P 500",
}

TICKERS = list(NUCLEAR.keys()) + list(BENCH.keys())

# ----------------------
# 3) Download prices
# ----------------------
print("Downloading price history from Yahoo Finance…")
px = yf.download(TICKERS, start="2018-01-01", progress=False)["Adj Close"]
px = px.dropna(how="all")
px.to_csv(DATA / "adj_close.csv")

# Align and forward-fill occasional gaps, then compute log returns
px = px.ffill()
rets = np.log(px / px.shift(1)).dropna()
rets.to_csv(DATA / "log_returns.csv")
print(f"Saved data to {DATA}")

# ----------------------
# 4) Basic correlations
# ----------------------
corr = rets.corr()
corr.to_csv(DATA / "correlation_matrix.csv")

fig = plt.figure()
im = plt.imshow(corr.values, interpolation="nearest")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.index)), corr.index)
plt.title("Correlation matrix: Nuclear vs Utilities/Energy/Market")
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.tight_layout()
plt.savefig(FIGS / "correlation_matrix.png")
plt.close(fig)

# ----------------------
# 5) PCA on standardized returns
# ----------------------
# Standardize columns to equalize scale
X = StandardScaler().fit_transform(rets.fillna(0).values)
pca = PCA(n_components=min(6, X.shape[1]))
pcs = pca.fit_transform(X)

explained = pd.Series(
    pca.explained_variance_ratio_, name="explained_variance_ratio"
)
explained.index = [f"PC{i+1}" for i in range(len(explained))]
explained.to_csv(DATA / "pca_explained_variance.csv")

loadings = pd.DataFrame(
    pca.components_.T,
    index=rets.columns,
    columns=[f"PC{i+1}" for i in range(pca.n_components_)],
)
loadings.to_csv(DATA / "pca_loadings.csv")

# Scree plot
fig = plt.figure()
explained.plot(kind="bar")
plt.ylabel("Explained variance ratio")
plt.title("PCA Scree Plot")
plt.tight_layout()
plt.savefig(FIGS / "pca_scree.png")
plt.close(fig)

# Loadings plot for first two PCs
fig = plt.figure()
for t in rets.columns:
    x, y = loadings.loc[t, "PC1"], loadings.loc[t, "PC2"]
    plt.scatter(x, y, s=35)
    label = t
    if t in NUCLEAR:
        # visually tag nuclear names by annotating with "*"
        label = f"{t}*"
    plt.annotate(label, (x, y), xytext=(4, 4), textcoords="offset points")
plt.axhline(0, linewidth=0.8)
plt.axvline(0, linewidth=0.8)
plt.xlabel("PC1 loading")
plt.ylabel("PC2 loading")
plt.title("PCA Loadings (PC1 vs PC2)\n* = nuclear names")
plt.tight_layout()
plt.savefig(FIGS / "pca_loadings_pc1_pc2.png")
plt.close(fig)

# ----------------------
# 6) Rolling correlations (nuclear vs benchmarks)
# ----------------------
window = 60  # trading days ~ 3 months
pairs = [("CEG", "XLU"), ("CEG", "XLE"), ("VST", "XLU"), ("CCJ", "XLE")]
roll = {}
for a, b in pairs:
    roll[(a, b)] = (
        rets[a].rolling(window).corr(rets[b]).rename(f"{a}~{b}")
    )

roll_df = pd.concat(roll.values(), axis=1).dropna()
roll_df.to_csv(DATA / "rolling_corr_60d.csv")

fig = plt.figure()
roll_df.plot(ax=plt.gca())
plt.title("Rolling 60D Correlations (selected nuclear vs benchmarks)")
plt.ylabel("Correlation")
plt.tight_layout()
plt.savefig(FIGS / "rolling_corr_60d.png")
plt.close(fig)

# ----------------------
# 7) Simple textual takeaways in console
# ----------------------
print("\n=== Quick Takeaways ===")
print("Top correlations (last available day):")
last = corr.iloc[:, :].stack().sort_values(ascending=False)
print(last.head(10))

print("\nExplained variance ratios:")
print(explained.round(3))

print(f"\nFigures saved to: {FIGS}")
print("Done.")
