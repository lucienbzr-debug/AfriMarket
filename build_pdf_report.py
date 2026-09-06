"""Génère le rapport PDF de direction AfriMarket (charte graphique officielle)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table,
    TableStyle, NextPageTemplate, PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader

BASE = r"c:\Users\Lbzr\Desktop\FORMATION CLAUDE & AI BY AKSANTE\Jour 3\AfriMarket"
FIG = fr"{BASE}\rapport\figures"
LOGO = fr"{BASE}\Logo AfriMarket.png"
OUT = fr"{BASE}\rapport\AfriMarket_Rapport_Strategique.pdf"

# ---------- Charte graphique officielle (couleurs extraites du logo) ----------
RED = colors.HexColor("#DC3D2A")
DARK = colors.HexColor("#2A2A28")
GRAY = colors.HexColor("#6B6B68")
LIGHT_GRAY = colors.HexColor("#F3F2F1")
GOLD = colors.HexColor("#E8A33D")
WHITE = colors.white

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm


# ---------------------------------------------------------------------------
# Page decoration : header (logo + fil rouge) + footer (pagination)
# ---------------------------------------------------------------------------
def draw_header_footer(c: pdfcanvas.Canvas, doc):
    c.saveState()
    page_num = c.getPageNumber()

    if page_num == 1:
        # Couverture pleine page
        c.setFillColor(DARK)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        c.setFillColor(RED)
        c.rect(0, PAGE_H - 0.35 * cm, PAGE_W, 0.35 * cm, fill=1, stroke=0)
        c.setFillColor(RED)
        c.rect(0, 0, PAGE_W, 0.35 * cm, fill=1, stroke=0)

        logo = ImageReader(LOGO)
        lw, lh = logo.getSize()
        target_h = 4.6 * cm
        target_w = target_h * lw / lh
        c.drawImage(logo, (PAGE_W - target_w) / 2, PAGE_H - 8.2 * cm, width=target_w, height=target_h,
                    mask='auto')

        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 25)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 12.4 * cm, "Rapport Stratégique")
        c.setFont("Helvetica-Bold", 25)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 13.25 * cm, "Analyse Commerciale AfriMarket")

        c.setFillColor(GOLD)
        c.setFont("Helvetica-Oblique", 13)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 14.4 * cm, "Résumé exécutif à destination de la Direction")

        c.setStrokeColor(colors.HexColor("#4A4A47"))
        c.setLineWidth(0.8)
        c.line(PAGE_W / 2 - 2.4 * cm, PAGE_H - 15.4 * cm, PAGE_W / 2 + 2.4 * cm, PAGE_H - 15.4 * cm)

        info_rows = [
            ("Période analysée", "Juillet — Décembre 2025"),
            ("Commandes analysées", "9 400 (nettoyées, sur 10 100 brutes)"),
            ("Couverture", "8 villes · 4 catégories · 1 747 clients"),
            ("Destinataire", "Comité de direction AfriMarket"),
        ]
        y0 = PAGE_H - 17.2 * cm
        for label, val in info_rows:
            c.setFillColor(colors.HexColor("#8A8A87"))
            c.setFont("Helvetica", 9.5)
            c.drawRightString(PAGE_W / 2 - 0.3 * cm, y0, label.upper())
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 9.5)
            c.drawString(PAGE_W / 2 + 0.3 * cm, y0, val)
            y0 -= 0.85 * cm

        c.setFillColor(colors.HexColor("#8A8A87"))
        c.setFont("Helvetica", 9)
        c.drawCentredString(PAGE_W / 2, 2.3 * cm, "Document confidentiel — usage interne AfriMarket")
        c.restoreState()
        return

    # Header (pages 2+)
    c.setFillColor(WHITE)
    c.rect(0, PAGE_H - 1.7 * cm, PAGE_W, 1.7 * cm, fill=1, stroke=0)
    c.setFillColor(RED)
    c.rect(0, PAGE_H - 1.72 * cm, PAGE_W, 0.06 * cm, fill=1, stroke=0)

    logo = ImageReader(LOGO)
    lw, lh = logo.getSize()
    target_h = 0.95 * cm
    target_w = target_h * lw / lh
    c.drawImage(logo, PAGE_W - MARGIN - target_w, PAGE_H - 1.35 * cm, width=target_w, height=target_h,
                mask='auto')
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, PAGE_H - 1.05 * cm, "AFRIMARKET")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8.5)
    c.drawString(MARGIN, PAGE_H - 1.35 * cm, "Rapport stratégique — Direction")

    # Footer
    c.setFillColor(DARK)
    c.rect(0, 0, PAGE_W, 1.0 * cm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#C9C9C6"))
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 0.38 * cm, "AfriMarket — Analyse stratégique des données commerciales (Juil.–Déc. 2025)")
    c.drawRightString(PAGE_W - MARGIN, 0.38 * cm, f"Page {page_num - 1}")
    c.restoreState()


# ---------------------------------------------------------------------------
# Document + styles
# ---------------------------------------------------------------------------
doc = BaseDocTemplate(OUT, pagesize=A4,
                       topMargin=2.0 * cm, bottomMargin=1.4 * cm,
                       leftMargin=MARGIN, rightMargin=MARGIN)

cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover", leftPadding=0, rightPadding=0,
                     topPadding=0, bottomPadding=0)
content_frame = Frame(MARGIN, 1.25 * cm, PAGE_W - 2 * MARGIN, PAGE_H - 3.1 * cm, id="content")

doc.addPageTemplates([
    PageTemplate(id="Cover", frames=[cover_frame], onPage=draw_header_footer),
    PageTemplate(id="Content", frames=[content_frame], onPage=draw_header_footer),
])

styles = {
    "H1": dict(fontName="Helvetica-Bold", fontSize=17, textColor=DARK, spaceAfter=10, spaceBefore=4, leading=21),
    "H2": dict(fontName="Helvetica-Bold", fontSize=12.5, textColor=RED, spaceAfter=6, spaceBefore=14, leading=16),
    "Body": dict(fontName="Helvetica", fontSize=9.7, textColor=DARK, spaceAfter=8, leading=14.5, alignment=TA_JUSTIFY),
    "BodyBold": dict(fontName="Helvetica-Bold", fontSize=9.7, textColor=DARK, spaceAfter=8, leading=14.5, alignment=TA_JUSTIFY),
    "Bullet": dict(fontName="Helvetica", fontSize=9.7, textColor=DARK, spaceAfter=5, leading=14, leftIndent=14,
                    bulletIndent=0),
    "Caption": dict(fontName="Helvetica-Oblique", fontSize=8.3, textColor=GRAY, spaceAfter=10, alignment=TA_CENTER),
    "RecoTitle": dict(fontName="Helvetica-Bold", fontSize=11.5, textColor=RED, spaceAfter=2, spaceBefore=10, leading=14),
}


def P(text, style="Body"):
    from reportlab.lib.styles import ParagraphStyle
    return Paragraph(text, ParagraphStyle(style, **styles[style]))


def bullet(text):
    from reportlab.lib.styles import ParagraphStyle
    return Paragraph(f"<bullet>&#9679;</bullet>{text}", ParagraphStyle("b", **styles["Bullet"]))


def img_fit(path, max_w, max_h):
    ir = ImageReader(path)
    iw, ih = ir.getSize()
    ratio = min(max_w / iw, max_h / ih)
    return Image(path, width=iw * ratio, height=ih * ratio, hAlign="CENTER")


def kpi_table(kpis):
    data = [[Paragraph(f'<font color="#DC3D2A" size="15"><b>{v}</b></font><br/>'
                        f'<font color="#6B6B68" size="7.6">{l}</font>', styles_center())
             for v, l in kpis]]
    t = Table(data, colWidths=[(PAGE_W - 2 * MARGIN) / len(kpis)] * len(kpis))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E3E2E0")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E3E2E0")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def styles_center():
    from reportlab.lib.styles import ParagraphStyle
    return ParagraphStyle("kpi", alignment=TA_CENTER, leading=16)


def hr():
    return HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#E3E2E0"), spaceBefore=2, spaceAfter=10)


# ---------------------------------------------------------------------------
# Contenu
# ---------------------------------------------------------------------------
flow = []
flow.append(NextPageTemplate("Content"))
flow.append(PageBreak())

# --- Page 2 : Contexte + KPIs ---
flow.append(P("Contexte", "H1"))
flow.append(P(
    "AfriMarket est une entreprise e-commerce panafricaine opérant dans 8 villes d'Afrique francophone, "
    "vendant des produits dans 4 catégories : Électronique, Mode, Beauté et Maison. La direction a constaté "
    "des variations importantes du chiffre d'affaires, un taux de retour préoccupant sur certains produits, "
    "des dépenses marketing élevées, et des différences de performance selon les villes. Cette analyse "
    "couvre 6 mois d'activité commerciale (10 100 commandes brutes, réduites à 9 400 commandes après "
    "nettoyage) et répond à ces quatre signaux avec des recommandations chiffrées.", "Body"))

flow.append(P("Chiffres clés (KPIs globaux)", "H2"))
flow.append(kpi_table([
    ("2,51 M$", "CA total"),
    ("430 k$", "Profit net estimé"),
    ("272,03 $", "Panier moyen"),
    ("1,9 %", "Taux d'annulation"),
    ("8,1 %", "Taux de retour"),
]))
flow.append(Spacer(1, 16))
flow.append(P("Évolution mensuelle du chiffre d'affaires", "H2"))
flow.append(img_fit(fr"{FIG}\01_ca_mensuel.png", PAGE_W - 2 * MARGIN, 9.5 * cm))
flow.append(Spacer(1, 10))
flow.append(P(
    "Après un repli en novembre (391 k$, -6,5 % vs. moyenne mensuelle), le CA rebondit fortement en "
    "décembre (463 k$, +10,9 % vs. moyenne) — un effet saisonnier de fin d'année à anticiper dans le "
    "pilotage des stocks et du budget marketing pour la période équivalente l'an prochain.", "Body"))

flow.append(PageBreak())

# --- Page 3 : Catégorie + Ville ---
flow.append(P("Analyse par catégorie — quelle catégorie prioriser ?", "H1"))
flow.append(P(
    "Électronique génère <b>74,6 %</b> du CA total (1,87 M$) mais affiche la marge la plus faible (20 %) "
    "et le taux de retour le plus élevé (13,8 %, contre 2,8 % à 7,4 % pour les autres catégories). Beauté "
    "est à l'inverse la catégorie la plus rentable en marge (50 %) et la plus fiable (2,8 % de retour) mais "
    "reste marginale en volume (3 % du CA).", "Body"))
flow.append(img_fit(fr"{FIG}\02_categorie.png", PAGE_W - 2 * MARGIN, 6.0 * cm))

flow.append(P("Analyse géographique — où investir davantage ?", "H1"))
flow.append(P(
    "Kinshasa domine largement (752 k$ de CA, 130 k$ de profit) et reste la priorité d'investissement. "
    "Douala combine la meilleure croissance du réseau (+76 %) et un taux d'annulation anormal de 12,9 % "
    "(quasi 0 % partout ailleurs) : un problème opérationnel local freine probablement un marché à fort "
    "potentiel. Libreville recule (-46 %) et doit être réévaluée avant tout nouvel investissement marketing. "
    "Brazzaville (+60 %) est un marché émergent à surveiller.", "Body"))
flow.append(img_fit(fr"{FIG}\03_ville.png", PAGE_W - 2 * MARGIN, 6.6 * cm))

flow.append(PageBreak())

# --- Page 4 : Marketing + Clients ---
flow.append(P("Analyse marketing — quel canal mérite plus de budget ?", "H1"))
flow.append(P(
    "Email affiche un ROI de <b>225x</b> pour seulement 2 349 $ investis — le plus petit budget des 4 "
    "canaux. À l'inverse, Instagram Ads consomme le plus gros budget (37 637 $) pour un ROI de seulement "
    "24x, et Influenceur affiche le ROI le plus faible (21x). Google Ads est solide (ROI 49x). Un "
    "rééquilibrage progressif du budget vers Email et Google Ads, sans couper Instagram (premier "
    "contributeur de CA en volume), maximiserait le retour marginal du budget marketing.", "Body"))
flow.append(img_fit(fr"{FIG}\04_roi_canal.png", PAGE_W - 2 * MARGIN, 6.0 * cm))

flow.append(P("Analyse clients — comment améliorer la rétention ?", "H1"))
flow.append(P(
    "AfriMarket compte 1 747 clients, dont <b>74 %</b> sont déjà récurrents (plus d'une commande) — un "
    "socle de fidélité solide. Cependant, les 350 clients les plus rentables (20 % de la base) concentrent "
    "<b>64,5 %</b> du CA total : la valeur de l'entreprise repose sur une minorité de clients qu'il est "
    "prioritaire de protéger et développer via un programme de fidélisation dédié.", "Body"))
flow.append(img_fit(fr"{FIG}\05_pareto.png", PAGE_W - 2 * MARGIN, 6.0 * cm))

flow.append(PageBreak())

# --- Page 5 : Recommandations ---
flow.append(P("5 recommandations stratégiques", "H1"))
recos = [
    ("1. Sécuriser la marge sur Électronique",
     "Pilier du CA (74,6 %) mais marge la plus faible (20 %) et retours les plus fréquents (13,8 %). "
     "Négocier les coûts fournisseurs et traiter la cause des retours en priorité : effet de levier le "
     "plus élevé sur le profit total."),
    ("2. Réduire le taux de retour Électronique",
     "Cause principale du taux de retour global (8,1 %). Un audit qualité/SAV ciblé (fiabilité produit, "
     "clarté des fiches produit, réactivité du SAV) est le levier de rentabilité le plus direct identifié."),
    ("3. Réallouer le budget marketing vers Email et Google Ads",
     "Email : ROI 225x pour 2 349 $ investis (sous-financé). Instagram Ads : ROI 24x pour 37 637 $ investis "
     "(sur-financé). Transférer 15-20 % du budget Instagram/Influenceur vers Email/Google Ads, en test A/B "
     "avant généralisation."),
    ("4. Corriger l'anomalie opérationnelle de Douala et réévaluer Libreville",
     "Douala (+76 % de croissance) subit un taux d'annulation de 12,9 % à investiguer en urgence (paiement, "
     "stock, livraison). Libreville recule de 46 % et ne doit pas recevoir de budget supplémentaire tant "
     "que la cause du déclin n'est pas identifiée."),
    ("5. Lancer un programme de fidélisation VIP",
     "Les 350 clients Pareto (20 % de la base, 64,5 % du CA) doivent être protégés par un programme dédié "
     "(offres exclusives, service prioritaire) : le ROI de rétention y est supérieur à celui de l'acquisition."),
]
for title, detail in recos:
    flow.append(KeepTogether([P(title, "RecoTitle"), P(detail, "Body")]))

flow.append(Spacer(1, 12))
flow.append(hr())
flow.append(P("Priorisation par effet de levier estimé", "H2"))
priority_data = [
    ["Priorité", "Recommandation", "Levier principal", "Délai"],
    ["1", "Sécuriser la marge Électronique", "Profit (marge 20 % sur 74,6 % du CA)", "30-60 j"],
    ["2", "Réduire le retour Électronique", "Profit + satisfaction client", "30-45 j"],
    ["3", "Réallouer le budget marketing", "ROI marketing (9x d'écart Email/Instagram)", "15-30 j"],
    ["4", "Corriger l'anomalie de Douala", "CA (ville à plus forte croissance)", "15 j"],
    ["5", "Programme de fidélisation VIP", "Rétention (64,5 % du CA sur 20 % clients)", "30 j"],
]
t = Table(priority_data, colWidths=[2.0 * cm, 5.4 * cm, 6.3 * cm, 2.5 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), DARK),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.7),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ("TEXTCOLOR", (0, 1), (0, -1), RED),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("ALIGN", (3, 0), (3, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E3E2E0")),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
flow.append(t)

flow.append(PageBreak())

# --- Page 6 : Conclusion + plan d'action ---
flow.append(P("Conclusion business orientée action", "H1"))
flow.append(P(
    "Avec 2,51 M$ de CA et 430 k$ de profit net estimé sur 6 mois, AfriMarket a un modèle rentable mais "
    "avec trois fuites de rentabilité claires et quantifiées : un taux de retour Électronique presque double "
    "de la moyenne qui érode la marge de sa catégorie la plus vendue, un budget marketing mal réparti (Email "
    "sous-investi malgré un ROI 9x supérieur à Instagram Ads), et un problème opérationnel localisé à Douala "
    "qui freine la ville à plus forte croissance du réseau.", "Body"))

flow.append(P("Plan d'action à 30 jours", "H2"))
flow.append(bullet("<b>Semaine 1</b> : audit qualité/SAV Électronique + audit opérationnel des annulations à Douala."))
flow.append(bullet("<b>Semaine 2</b> : transfert de 15-20 % du budget Instagram Ads/Influenceur vers "
                    "Email/Google Ads, en test A/B sur un mois avant généralisation."))
flow.append(bullet("<b>Semaines 3-4</b> : lancement pilote du programme de fidélisation VIP sur les 350 "
                    "clients Pareto identifiés."))
flow.append(Spacer(1, 10))
flow.append(hr())
flow.append(P(
    "Ces trois actions ciblent directement les 4 signaux remontés par la direction (variations de CA, taux "
    "de retour, dépenses marketing, écarts de performance géographique) avec un impact mesurable dès le mois "
    "suivant, sans investissement supplémentaire net : il s'agit de réallocation de ressources existantes, "
    "pas d'une augmentation de budget.", "BodyBold"))
flow.append(P("Source : afrimarket_dataset_senior.csv, nettoyé et enrichi (df_clean). Hypothèses de marge "
              "par catégorie documentées dans le notebook d'analyse.", "Caption"))

flow.append(Spacer(1, 18))
next_step = Table(
    [[Paragraph('<font color="#FFFFFF" size="11.5"><b>Prochaine étape</b></font><br/>'
                '<font color="#D9D9D6" size="9.3">Validation en comité de direction des 3 actions prioritaires '
                'et lancement de la semaine 1 du plan d\'action.</font>', styles_center())]],
    colWidths=[PAGE_W - 2 * MARGIN])
next_step.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK),
    ("TOPPADDING", (0, 0), (-1, -1), 14),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
]))
flow.append(next_step)

doc.build(flow)
print("Rapport PDF sauvegardé :", OUT)
