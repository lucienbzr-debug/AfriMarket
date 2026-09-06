<p align="center">
  <img src="Logo AfriMarket.png" alt="AfriMarket" width="220">
</p>

<h1 align="center">AfriMarket — Analyse Commerciale & Dashboard Stratégique</h1>

<p align="center">
  Analyse des données e-commerce d'AfriMarket (Juillet–Décembre 2025) : nettoyage des données,
  analyse stratégique, dashboard interactif et livrables de direction (PDF, PowerPoint, Word).
</p>

---

## Sommaire

- [Contexte](#contexte)
- [Résultats clés](#résultats-clés)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Lancer le dashboard en local](#lancer-le-dashboard-en-local)
  - [Publier le dashboard sur Streamlit Community Cloud](#publier-le-dashboard-sur-streamlit-community-cloud)
  - [Régénérer les livrables (figures, PDF, PowerPoint, Word)](#régénérer-les-livrables-figures-pdf-powerpoint-word)
- [Données](#données)
  - [Source et dictionnaire des données](#source-et-dictionnaire-des-données)
  - [Nettoyage appliqué](#nettoyage-appliqué)
  - [Hypothèses et règles métier](#hypothèses-et-règles-métier)
- [Charte graphique](#charte-graphique)
- [Stack technique](#stack-technique)

---

## Contexte

AfriMarket est une entreprise e-commerce panafricaine opérant dans **8 villes** d'Afrique francophone,
vendant des produits dans **4 catégories** : Électronique, Mode, Beauté et Maison.

La direction a constaté quatre signaux à investiguer :
1. Des variations importantes du chiffre d'affaires selon les mois.
2. Un taux de retour préoccupant sur certains produits.
3. Des dépenses marketing élevées, avec un retour sur investissement (ROI) incertain par canal.
4. Des écarts de performance importants selon les villes.

Ce projet répond à ces quatre signaux à partir de **6 mois de données commerciales** (10 100 commandes
brutes, réduites à 9 400 commandes après nettoyage), avec des analyses chiffrées, un dashboard interactif
et des recommandations actionnables pour le comité de direction.

## Résultats clés

| Indicateur | Valeur |
|---|---|
| Chiffre d'affaires total | **2,51 M$** |
| Profit net estimé | **430 k$** |
| Panier moyen | 272,03 $ |
| Taux d'annulation | 1,9 % |
| Taux de retour | 8,1 % |

**5 recommandations stratégiques** ressortent de l'analyse (détaillées dans le
[rapport PDF](rapport/AfriMarket_Rapport_Strategique.pdf) et la
[présentation PowerPoint](rapport/AfriMarket_Presentation_Direction.pptx)) :

1. Sécuriser la marge sur Électronique (74,6 % du CA, marge la plus faible : 20 %).
2. Réduire le taux de retour Électronique (13,8 %, cause principale du taux de retour global).
3. Réallouer le budget marketing vers Email (ROI 225x) et Google Ads (ROI 49x), au détriment d'Instagram Ads (ROI 24x).
4. Corriger l'anomalie opérationnelle de Douala (taux d'annulation de 12,9 % malgré +76 % de croissance) et réévaluer Libreville (-46 %).
5. Lancer un programme de fidélisation VIP pour les 350 clients Pareto qui génèrent 64,5 % du CA total.

## Structure du projet

```
AfriMarket/
├── Logo AfriMarket.png                 # Logo officiel (source de la charte graphique)
├── requirements.txt                    # Dépendances complètes (analyse + génération de rapports)
│
├── data/
│   ├── afrimarket_dataset_senior.csv   # Données brutes (10 100 commandes)
│   └── df_clean.csv                    # Données nettoyées et enrichies (9 400 commandes)
│
├── notebook/
│   ├── AfriMarket_Analyse.ipynb        # Notebook d'analyse complet (audit, nettoyage, KPIs, insights)
│   ├── AfriMarket_Analyse.py           # Version script (jupytext) du notebook ci-dessus
│   ├── generate_report_figures.py      # Génère les 5 graphiques de rapport/figures (palette de marque)
│   ├── build_executive_summary.py      # Génère rapport/Resume_Executif_AfriMarket.docx
│   ├── build_presentation.py           # Génère rapport/AfriMarket_Presentation_Direction.pptx
│   └── build_pdf_report.py             # Génère rapport/AfriMarket_Rapport_Strategique.pdf
│
├── dashboard/
│   ├── app.py                          # Dashboard Streamlit interactif
│   └── requirements.txt                # Dépendances minimales pour le déploiement Streamlit Cloud
│
└── rapport/
    ├── figures/                        # Graphiques PNG utilisés dans le PDF et le PowerPoint
    ├── Resume_Executif_AfriMarket.docx # Résumé exécutif (Word)
    ├── AfriMarket_Rapport_Strategique.pdf         # Rapport stratégique complet (PDF)
    └── AfriMarket_Presentation_Direction.pptx     # Présentation de direction (PowerPoint)
```

## Installation

Prérequis : **Python 3.10+**.

```bash
git clone <url-du-repo>
cd AfriMarket
pip install -r requirements.txt
```

> `requirements.txt` (racine) installe tout l'outillage du projet : analyse de données, notebook,
> dashboard et génération de rapports (Word/PDF/PowerPoint). Pour déployer uniquement le dashboard,
> voir [dashboard/requirements.txt](dashboard/requirements.txt).

## Utilisation

### Lancer le dashboard en local

```bash
streamlit run dashboard/app.py
```

Le dashboard s'ouvre sur `http://localhost:8501` et propose :
- des filtres (ville, catégorie, canal marketing, statut de commande, période) ;
- des KPIs globaux (CA, profit, panier moyen, taux d'annulation, taux de retour) ;
- 5 onglets d'analyse : Catégorie, Géographie, Marketing, Clients, Données ;
- un export CSV des données filtrées.

### Publier le dashboard sur Streamlit Community Cloud

1. Pousser le projet sur un dépôt GitHub (public ou privé).
2. Sur [share.streamlit.io](https://share.streamlit.io), créer une nouvelle app en pointant vers
   `dashboard/app.py` comme fichier principal.
3. Streamlit Cloud détecte automatiquement [dashboard/requirements.txt](dashboard/requirements.txt)
   (placé dans le même dossier que `app.py`, il est prioritaire sur celui de la racine).
4. Le chemin vers `data/df_clean.csv` est résolu **dynamiquement** depuis l'emplacement du script
   (`dashboard/app.py`), donc aucune configuration supplémentaire n'est nécessaire.

### Régénérer les livrables (figures, PDF, PowerPoint, Word)

Les scripts doivent être exécutés depuis la racine du projet, dans cet ordre si `df_clean.csv` a changé :

```bash
# 1. Régénère les 5 graphiques (rapport/figures/) avec la palette de marque
python notebook/generate_report_figures.py

# 2. Régénère le rapport PDF stratégique
python notebook/build_pdf_report.py

# 3. Régénère la présentation PowerPoint de direction
python notebook/build_presentation.py

# 4. Régénère le résumé exécutif Word
python notebook/build_executive_summary.py
```

Chaque script est autonome et réécrit son livrable dans `rapport/`. Si les chiffres clés (CA, profit,
ROI, etc.) évoluent suite à une mise à jour des données, ils doivent être mis à jour manuellement dans
`build_pdf_report.py`, `build_presentation.py` et `build_executive_summary.py` (les valeurs y sont
codées en dur à partir des résultats du notebook d'analyse).

## Données

### Source et dictionnaire des données

- **Brutes** : [data/afrimarket_dataset_senior.csv](data/afrimarket_dataset_senior.csv) — 10 100 lignes, 14 colonnes.
- **Nettoyées** : [data/df_clean.csv](data/df_clean.csv) — 9 400 lignes, 21 colonnes.

| Colonne | Description |
|---|---|
| `id_commande` | Identifiant unique de commande |
| `date_commande` | Date de la commande (YYYY-MM-DD) |
| `id_client` | Identifiant unique du client |
| `ville` | Ville de livraison (8 valeurs : Kinshasa, Abidjan, Douala, Dakar, Lomé, Cotonou, Libreville, Brazzaville) |
| `categorie` | Catégorie produit (Électronique, Mode, Beauté, Maison) |
| `nom_produit` | Nom du produit |
| `prix_unitaire` | Prix unitaire ($) |
| `quantite` | Quantité commandée |
| `remise` | Taux de remise appliqué (0 à 0,30) |
| `cout_livraison` | Coût de livraison ($) |
| `methode_paiement` | Méthode de paiement |
| `canal_marketing` | Canal marketing d'acquisition |
| `cout_marketing` | Coût marketing attribué à la commande ($) |
| `statut_commande` | Statut (Livrée, Retournée, Annulée) |
| `chiffre_affaires`* | CA généré (0 si Annulée) |
| `marge_brute_estimee`* | Marge brute estimée par catégorie |
| `indicateur_retour`* | 1 si Retournée, sinon 0 |
| `profit_net_estime`* | Profit net après marge, coûts logistiques/marketing et retours |
| `mois`* | Mois de la commande (YYYY-MM) |
| `nombre_commandes_par_client`* | Nombre total de commandes du client |
| `valeur_vie_client`* | CA cumulé généré par le client (CLV) |

*Colonnes calculées lors du feature engineering (absentes du fichier brut).

### Nettoyage appliqué

L'audit du fichier brut a révélé les problèmes suivants, corrigés dans [notebook/AfriMarket_Analyse.py](notebook/AfriMarket_Analyse.py) :

| Problème | Détail | Volume | Correction |
|---|---|---|---|
| Doublons exacts | Même `id_commande` répété | 100 lignes | Suppression (conservation de la 1ère occurrence) |
| Ville mal orthographiée | `Kinshassa` → `Kinshasa` | 605 lignes | Harmonisation par mapping |
| Catégorie incohérente | `electronique` → `Électronique` | 606 lignes | Harmonisation par mapping |
| Statut incohérent | `retournée` → `Retournée` | 826 lignes | Harmonisation par mapping |
| Remises négatives | `remise` < 0 (impossible) | 614 lignes | Valeur absolue, plafonnée à 0,30 |
| Prix aberrants | `prix_unitaire` négatif | 632 lignes | Remplacé par la médiane de la catégorie |
| Quantités nulles | `quantite` = 0 (pas d'activité économique réelle) | 608 lignes | Commandes supprimées |

Le nettoyage est validé par une série d'assertions automatiques (unicité des `id_commande`, absence de
valeurs négatives, cohérence des catégories/villes/statuts) avant l'export vers `df_clean.csv`.

### Hypothèses et règles métier

Le dataset ne fournit pas de coût d'achat produit : un **taux de marge brute par catégorie** a donc été
estimé à partir de références sectorielles e-commerce classiques :

| Catégorie | Marge brute estimée |
|---|---|
| Électronique | 20 % (marché concurrentiel) |
| Mode | 45 % |
| Beauté | 50 % |
| Maison | 35 % |

**Règles de calcul du chiffre d'affaires et du profit** :
- Une commande **Annulée** ne génère aucun chiffre d'affaires.
- Une commande **Retournée** génère un CA (elle a été livrée puis retournée), mais son profit net est
  pénalisé : la marge brute est annulée alors que les coûts de livraison et marketing restent à charge
  (perte sèche), pour refléter l'impact réel d'un retour sur la rentabilité.

## Charte graphique

La charte graphique utilisée dans le dashboard, le rapport PDF et la présentation PowerPoint est extraite
directement des couleurs officielles du logo AfriMarket :

| Couleur | Code hex | Usage |
|---|---|---|
| 🔴 Rouge AfriMarket | `#DC3D2A` | Couleur principale, accents, alertes |
| ⚫ Anthracite | `#2A2A28` | Texte, fonds sombres, titres |
| ⚪ Gris neutre | `#9A9A97` | Éléments secondaires |
| 🟡 Or | `#E8A33D` | Accents, mise en valeur |

## Stack technique

| Usage | Bibliothèques |
|---|---|
| Analyse de données | `pandas`, `numpy` |
| Visualisation (notebook & rapports) | `matplotlib`, `seaborn` |
| Dashboard interactif | `streamlit`, `plotly` |
| Notebook | `jupyter`, `nbformat` |
| Export Word | `python-docx` |
| Export PowerPoint | `python-pptx` |
| Export PDF | `reportlab` |
| Export d'images statiques Plotly | `kaleido` |
| Lecture/inspection de PDF | `pymupdf` |
