import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (9, 4.5)
plt.rcParams["axes.edgecolor"] = "#D8D8D6"
plt.rcParams["text.color"] = "#2A2A28"
plt.rcParams["axes.labelcolor"] = "#2A2A28"
plt.rcParams["xtick.color"] = "#2A2A28"
plt.rcParams["ytick.color"] = "#2A2A28"
plt.rcParams["font.family"] = "Calibri"

# ---- Charte graphique AfriMarket (couleurs extraites du logo officiel) ----
BRAND_RED = "#DC3D2A"
BRAND_DARK = "#2A2A28"
BRAND_GRAY = "#9A9A97"
BRAND_GOLD = "#E8A33D"
BRAND_GOOD = "#2E7D32"
CAT_PALETTE = [BRAND_RED, BRAND_DARK, BRAND_GOLD, BRAND_GRAY]

BASE = r"c:\Users\Lbzr\Desktop\FORMATION CLAUDE & AI BY AKSANTE\Jour 3\AfriMarket"
df = pd.read_csv(fr"{BASE}\data\df_clean.csv")
df["date_commande"] = pd.to_datetime(df["date_commande"])

FIG_DIR = fr"{BASE}\rapport\figures"
os.makedirs(FIG_DIR, exist_ok=True)

# 1. CA mensuel global
monthly = df.groupby("mois")["chiffre_affaires"].sum()
fig, ax = plt.subplots()
ax.plot(monthly.index, monthly.values, marker="o", linewidth=2.5, color=BRAND_RED, markerfacecolor=BRAND_DARK, markeredgecolor=BRAND_DARK)
ax.set_title("Évolution du chiffre d'affaires mensuel", fontweight="bold", fontsize=13, color=BRAND_DARK)
ax.set_ylabel("CA ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.tight_layout()
plt.savefig(fr"{FIG_DIR}\01_ca_mensuel.png", dpi=150)
plt.close()

# 2. CA et marge% par catégorie
cat_perf = df.groupby("categorie").agg(ca=("chiffre_affaires", "sum"),
                                        marge=("marge_brute_estimee", "sum"),
                                        taux_retour=("indicateur_retour", "mean")).sort_values("ca", ascending=False)
cat_perf["marge_pct"] = cat_perf["marge"] / cat_perf["ca"]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
bars = axes[0].bar(cat_perf.index, cat_perf["ca"], color=CAT_PALETTE[:len(cat_perf)])
axes[0].set_title("CA par catégorie", fontweight="bold", color=BRAND_DARK)
axes[0].set_ylabel("CA ($)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M" if x >= 1e6 else f"{x/1e3:.0f}k"))

bars2 = axes[1].bar(cat_perf.index, cat_perf["taux_retour"], color=CAT_PALETTE[:len(cat_perf)])
axes[1].set_title("Taux de retour par catégorie", fontweight="bold", color=BRAND_DARK)
axes[1].yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
for b in bars2:
    axes[1].text(b.get_x()+b.get_width()/2, b.get_height()+0.002, f"{b.get_height():.1%}", ha="center", fontsize=9, fontweight="bold")
plt.tight_layout()
plt.savefig(fr"{FIG_DIR}\02_categorie.png", dpi=150)
plt.close()

# 3. CA par ville
ville_perf = df.groupby("ville")["chiffre_affaires"].sum().sort_values()
fig, ax = plt.subplots(figsize=(9, 5))
n = len(ville_perf)
shades = [BRAND_RED if i == n - 1 else BRAND_DARK if i == n - 2 else BRAND_GRAY for i in range(n)]
ax.barh(ville_perf.index, ville_perf.values, color=shades)
ax.set_title("Chiffre d'affaires par ville", fontweight="bold", fontsize=13, color=BRAND_DARK)
ax.set_xlabel("CA ($)")
plt.tight_layout()
plt.savefig(fr"{FIG_DIR}\03_ville.png", dpi=150)
plt.close()

# 4. ROI par canal marketing
canal_perf = df.groupby("canal_marketing").agg(ca=("chiffre_affaires","sum"), cout=("cout_marketing","sum")).copy()
canal_perf["roi"] = (canal_perf["ca"] - canal_perf["cout"]) / canal_perf["cout"]
canal_perf = canal_perf.sort_values("roi")
fig, ax = plt.subplots(figsize=(9, 4.5))
colors = [BRAND_RED if v < 30 else BRAND_GOOD for v in canal_perf["roi"]]
bars = ax.barh(canal_perf.index, canal_perf["roi"], color=colors)
ax.set_title("ROI marketing par canal  (Revenus - Coût) / Coût", fontweight="bold", fontsize=13, color=BRAND_DARK)
ax.set_xlabel("ROI (x)")
for b, v in zip(bars, canal_perf["roi"]):
    ax.text(v + 3, b.get_y()+b.get_height()/2, f"{v:.0f}x", va="center", fontweight="bold")
plt.tight_layout()
plt.savefig(fr"{FIG_DIR}\04_roi_canal.png", dpi=150)
plt.close()

# 5. Pareto clients
clv = df.groupby("id_client")["chiffre_affaires"].sum().sort_values(ascending=False)
cum = clv.cumsum() / clv.sum()
x = np.arange(1, len(clv)+1) / len(clv) * 100
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(x, cum.values * 100, color=BRAND_RED, linewidth=2.5)
ax.axvline(20, color=BRAND_DARK, linestyle="--", alpha=0.6)
n20 = int(np.ceil(0.2*len(clv)))
ax.axhline(cum.iloc[n20-1]*100, color=BRAND_DARK, linestyle="--", alpha=0.6)
ax.set_title("Concentration du CA par client (Pareto)", fontweight="bold", fontsize=13, color=BRAND_DARK)
ax.set_xlabel("% des clients (triés par valeur décroissante)")
ax.set_ylabel("% du CA cumulé")
plt.tight_layout()
plt.savefig(fr"{FIG_DIR}\05_pareto.png", dpi=150)
plt.close()

print("Figures générées dans", FIG_DIR)
print(os.listdir(FIG_DIR))
