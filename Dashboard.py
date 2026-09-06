import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="AfriMarket — Dashboard", page_icon="📊", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "df_clean.csv")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date_commande"] = pd.to_datetime(df["date_commande"])
    return df


df = load_data()

# ---------------- SIDEBAR : FILTRES ----------------
st.sidebar.title("📊 AfriMarket")
st.sidebar.caption("Dashboard stratégique — 6 mois d'activité")

villes = st.sidebar.multiselect("Ville", sorted(df["ville"].unique()), default=sorted(df["ville"].unique()))
categories = st.sidebar.multiselect("Catégorie", sorted(df["categorie"].unique()), default=sorted(df["categorie"].unique()))
canaux = st.sidebar.multiselect("Canal marketing", sorted(df["canal_marketing"].unique()), default=sorted(df["canal_marketing"].unique()))
statuts = st.sidebar.multiselect("Statut commande", sorted(df["statut_commande"].unique()), default=sorted(df["statut_commande"].unique()))

date_min, date_max = df["date_commande"].min(), df["date_commande"].max()
date_range = st.sidebar.date_input("Période", (date_min, date_max), min_value=date_min, max_value=date_max)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start, end = date_min, date_max

mask = (
    df["ville"].isin(villes)
    & df["categorie"].isin(categories)
    & df["canal_marketing"].isin(canaux)
    & df["statut_commande"].isin(statuts)
    & df["date_commande"].between(start, end)
)
dff = df[mask]

st.title("Dashboard Stratégique — AfriMarket")
st.caption(f"{len(dff):,} commandes sélectionnées sur {len(df):,} au total (données nettoyées `df_clean`)")

if dff.empty:
    st.warning("Aucune donnée pour les filtres sélectionnés.")
    st.stop()

# ---------------- KPIs ----------------
ca_total = dff["chiffre_affaires"].sum()
profit_total = dff["profit_net_estime"].sum()
panier_moyen = dff.loc[dff["statut_commande"] != "Annulée", "chiffre_affaires"].mean()
taux_annulation = (dff["statut_commande"] == "Annulée").mean()
taux_retour = (dff["statut_commande"] == "Retournée").mean()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("CA total", f"{ca_total:,.0f} $")
k2.metric("Profit net estimé", f"{profit_total:,.0f} $")
k3.metric("Panier moyen", f"{panier_moyen:,.2f} $")
k4.metric("Taux d'annulation", f"{taux_annulation:.1%}")
k5.metric("Taux de retour", f"{taux_retour:.1%}")

st.divider()

tab_cat, tab_geo, tab_mkt, tab_client, tab_data = st.tabs(
    ["📦 Catégorie", "🌍 Géographie", "📣 Marketing", "👥 Clients", "🔍 Données"]
)

# ---------------- TAB CATEGORIE ----------------
with tab_cat:
    st.subheader("Performance par catégorie")
    cat_perf = dff.groupby("categorie").agg(
        ca=("chiffre_affaires", "sum"),
        marge=("marge_brute_estimee", "sum"),
        profit=("profit_net_estime", "sum"),
        taux_retour=("indicateur_retour", "mean"),
        n_commandes=("id_commande", "count"),
    ).reset_index()
    cat_perf["marge_pct"] = cat_perf["marge"] / cat_perf["ca"]

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(cat_perf.sort_values("ca"), x="ca", y="categorie", orientation="h",
                     title="CA par catégorie", labels={"ca": "CA ($)", "categorie": ""}, color="categorie")
        st.plotly_chart(fig, width="stretch")
    with c2:
        fig = px.bar(cat_perf.sort_values("taux_retour"), x="taux_retour", y="categorie", orientation="h",
                     title="Taux de retour par catégorie", labels={"taux_retour": "Taux de retour", "categorie": ""},
                     color="categorie")
        fig.update_layout(xaxis_tickformat=".0%")
        st.plotly_chart(fig, width="stretch")

    evol = dff.groupby(["mois", "categorie"])["chiffre_affaires"].sum().reset_index()
    fig = px.line(evol, x="mois", y="chiffre_affaires", color="categorie", markers=True,
                  title="Évolution mensuelle du CA par catégorie")
    st.plotly_chart(fig, width="stretch")

    st.markdown("**Question stratégique :** Électronique domine le CA mais avec la marge la plus faible "
                "et le taux de retour le plus élevé — priorité de rentabilité, pas seulement de volume.")
    st.dataframe(cat_perf.style.format({"ca": "{:,.0f}", "marge": "{:,.0f}", "profit": "{:,.0f}",
                                        "taux_retour": "{:.1%}", "marge_pct": "{:.0%}"}), width="stretch")

# ---------------- TAB GEOGRAPHIE ----------------
with tab_geo:
    st.subheader("Performance géographique")
    ville_perf = dff.groupby("ville").agg(
        ca=("chiffre_affaires", "sum"),
        profit=("profit_net_estime", "sum"),
        taux_annulation=("statut_commande", lambda s: (s == "Annulée").mean()),
        n_commandes=("id_commande", "count"),
    ).sort_values("ca", ascending=False).reset_index()

    c1, c2 = st.columns([1.3, 1])
    with c1:
        fig = px.bar(ville_perf.sort_values("ca"), x="ca", y="ville", orientation="h",
                     title="CA par ville", color="ca", color_continuous_scale="Teal")
        st.plotly_chart(fig, width="stretch")
    with c2:
        fig = px.bar(ville_perf.sort_values("taux_annulation"), x="taux_annulation", y="ville", orientation="h",
                     title="Taux d'annulation par ville", color="taux_annulation", color_continuous_scale="Reds")
        fig.update_layout(xaxis_tickformat=".0%")
        st.plotly_chart(fig, width="stretch")

    pivot = dff.pivot_table(index="ville", columns="mois", values="chiffre_affaires", aggfunc="sum").fillna(0)
    fig = px.imshow(pivot, text_auto=".0f", color_continuous_scale="YlGnBu", aspect="auto",
                     title="Heatmap CA mensuel par ville")
    st.plotly_chart(fig, width="stretch")

    st.markdown("**Question stratégique :** Kinshasa reste la priorité d'investissement ; Douala combine "
                "forte croissance et taux d'annulation anormal à corriger en priorité.")
    st.dataframe(ville_perf.style.format({"ca": "{:,.0f}", "profit": "{:,.0f}", "taux_annulation": "{:.1%}"}),
                 width="stretch")

# ---------------- TAB MARKETING ----------------
with tab_mkt:
    st.subheader("Performance marketing")
    canal_perf = dff.groupby("canal_marketing").agg(
        ca=("chiffre_affaires", "sum"),
        cout_marketing_total=("cout_marketing", "sum"),
        taux_retention=("nombre_commandes_par_client", lambda s: (s > 1).mean()),
    ).reset_index()
    canal_perf["roi"] = (canal_perf["ca"] - canal_perf["cout_marketing_total"]) / canal_perf["cout_marketing_total"]

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(canal_perf.sort_values("roi"), x="roi", y="canal_marketing", orientation="h",
                     title="ROI par canal marketing", color="roi", color_continuous_scale="Purples")
        st.plotly_chart(fig, width="stretch")
    with c2:
        fig = px.bar(canal_perf.sort_values("cout_marketing_total"), x="cout_marketing_total", y="canal_marketing",
                     orientation="h", title="Coût marketing total par canal", color="cout_marketing_total",
                     color_continuous_scale="Oranges")
        st.plotly_chart(fig, width="stretch")

    st.markdown("**Question stratégique :** quel canal mérite plus de budget ? Comparez le ROI (gauche) au "
                "coût investi (droite) — un canal à faible coût et fort ROI est sous-investi.")
    st.dataframe(canal_perf.style.format({"ca": "{:,.0f}", "cout_marketing_total": "{:,.0f}",
                                           "taux_retention": "{:.1%}", "roi": "{:.1f}x"}), width="stretch")

# ---------------- TAB CLIENTS ----------------
with tab_client:
    st.subheader("Analyse clients")
    n_clients = dff["id_client"].nunique()
    pct_recurrents = (dff.groupby("id_client")["id_commande"].count() > 1).mean()

    c1, c2 = st.columns(2)
    c1.metric("Nombre total de clients", f"{n_clients:,}")
    c2.metric("% clients récurrents (>1 commande)", f"{pct_recurrents:.1%}")

    clv = dff.groupby("id_client")["chiffre_affaires"].sum().sort_values(ascending=False)
    cum = clv.cumsum() / clv.sum()
    n20 = max(1, int(np.ceil(0.2 * len(clv))))
    part_top20 = cum.iloc[n20 - 1] if len(cum) else 0

    st.info(f"Les **{n20} clients les plus rentables** ({n20/len(clv):.0%} de la base) génèrent "
            f"**{part_top20:.1%} du CA total** (analyse Pareto 80/20).")

    c1, c2 = st.columns([1.3, 1])
    with c1:
        pareto_df = pd.DataFrame({"pct_clients": np.arange(1, len(clv)+1)/len(clv)*100, "pct_ca_cumule": cum.values*100})
        fig = px.line(pareto_df, x="pct_clients", y="pct_ca_cumule", title="Courbe de Pareto — concentration du CA")
        fig.add_vline(x=20, line_dash="dash", line_color="gray")
        st.plotly_chart(fig, width="stretch")
    with c2:
        seg = pd.cut(clv, bins=[-0.01, clv.quantile(0.5), clv.quantile(0.8), clv.max()],
                      labels=["Occasionnel", "Régulier", "VIP"])
        seg_counts = seg.value_counts().reindex(["Occasionnel", "Régulier", "VIP"]).reset_index()
        seg_counts.columns = ["segment", "n_clients"]
        fig = px.bar(seg_counts, x="segment", y="n_clients", title="Segmentation simple des clients",
                     color="segment", color_discrete_map={"Occasionnel": "#90A4AE", "Régulier": "#42A5F5", "VIP": "#FFB300"})
        st.plotly_chart(fig, width="stretch")

    st.markdown("**Top 10 clients par valeur vie client (CLV)**")
    top10 = clv.head(10).rename("valeur_vie_client").reset_index()
    st.dataframe(top10.style.format({"valeur_vie_client": "{:,.0f} $"}), width="stretch")

# ---------------- TAB DONNEES ----------------
with tab_data:
    st.subheader("Exploration des données nettoyées (df_clean)")
    st.dataframe(dff, width="stretch", height=500)
    st.download_button("Télécharger les données filtrées (CSV)", dff.to_csv(index=False).encode("utf-8"),
                        "afrimarket_filtre.csv", "text/csv")

st.divider()
st.caption("Source : afrimarket_dataset_senior.csv, nettoyé et enrichi (df_clean). "
           "Hypothèses de marge par catégorie documentées dans le notebook d'analyse.")
