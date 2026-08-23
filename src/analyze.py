"""
analyze.py — Análisis comparativo TikTok vs Instagram @aroaxinping
Periodo: 24 Feb – 24 Mar 2026

Genera visualizaciones cross-platform en visuals/ y el notebook
de análisis comparativo.
"""

import os
import sys
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

warnings.filterwarnings("ignore")

BASE   = Path(__file__).resolve().parent.parent
VIS    = BASE / "visuals"
VIS.mkdir(exist_ok=True)

TT_ENG = BASE / "data" / "tiktok" / "videos_engagement.csv"
TT_OVR = BASE / "data" / "tiktok" / "overview_metrics.csv"
IG_REE = BASE / "data" / "instagram" / "reels_metricas.csv"
IG_DAI = BASE / "data" / "instagram" / "metricas_diarias.csv"

# ── Paleta ────────────────────────────────────────────────────────────────────
BG      = "#0F0F1A"
CARD    = "#16213E"
TT_COL  = "#FF2D55"   # rojo TikTok
IG_COL  = "#C13584"   # morado Instagram
GOLD    = "#FCD34D"
TEXT    = "#E2E8F0"
GRID    = "#1E293B"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": CARD,
    "axes.edgecolor": "#334155", "axes.labelcolor": TEXT,
    "text.color": TEXT, "xtick.color": TEXT, "ytick.color": TEXT,
    "grid.color": GRID, "grid.linestyle": "--", "grid.alpha": 0.5,
    "font.family": "sans-serif", "font.size": 10,
})

# ── Carga ─────────────────────────────────────────────────────────────────────
print("📂 Cargando datos...")
tt  = pd.read_csv(TT_ENG)
ig  = pd.read_csv(IG_REE)
ig  = ig[ig["visualizaciones"] > 0].copy()

# Normalizar nombres para comparación
tt["platform"]       = "TikTok"
tt["views"]          = tt["views"]
tt["engagement_rate"]= tt["engagement_rate_pct"]
tt["share_rate"]     = tt["share_rate_pct"]
tt["save_rate"]      = tt["save_rate_pct"]
tt["new_followers"]  = tt["new_followers"].fillna(0)
tt["completion"]     = tt["completion_pct"]
tt["desc"]           = tt["title"].str[:40]

ig["platform"]       = "Instagram"
ig["views"]          = ig["visualizaciones"]
ig["engagement_rate"]= ig["engagement_rate"]
ig["share_rate"]     = ig["share_rate"]
ig["save_rate"]      = ig["save_rate"]
ig["new_followers"]  = ig["seguidores_ganados"]
ig["completion"]     = None   # no disponible en Instagram
ig["desc"]           = ig["descripcion_corta"].str[:40]

TT_FOLLOWERS = 30000
IG_FOLLOWERS = 8728

# Clasificar temática para TikTok desde el título
def classify_topic_tt(title: str) -> str:
    t = str(title).lower()
    if "sql" in t or "select" in t:                  return "SQL"
    if "python" in t or "pyth" in t:                 return "Python"
    if "terminal" in t or "bash" in t:               return "Terminal/Bash"
    if "excel" in t:                                 return "Excel"
    if "linux" in t:                                 return "Linux"
    if "git" in t:                                   return "Git"
    if any(x in t for x in ["chico", "relaci", "informátic", "informatico", "apodo"]):
        return "Humor personal"
    if any(x in t for x in ["programad", "codigo", "código", "code"]):
        return "Programación general"
    if any(x in t for x in ["tech", "informatica", "informática"]):
        return "Tech humor"
    return "Otro"

tt["topic"] = tt["title"].apply(classify_topic_tt)

print(f"  TikTok:    {len(tt)} vídeos")
print(f"  Instagram: {len(ig)} reels")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 1: KPIs COMPARATIVOS — Barras enfrentadas
# ─────────────────────────────────────────────────────────────────────────────
print("\n📊 Chart 1: KPIs comparativos...")

kpis = {
    "Vistas totales":         (tt["views"].sum(),            ig["views"].sum()),
    "Engagement rate medio %":(tt["engagement_rate"].mean(), ig["engagement_rate"].mean()),
    "Save rate medio %":      (tt["save_rate"].mean(),       ig["save_rate"].mean()),
    "Share rate medio %":     (tt["share_rate"].mean(),      ig["share_rate"].mean()),
    "Seg. ganados":           (tt["new_followers"].sum(),    ig["new_followers"].sum()),
    "Follower Rate/1K (avg)": (
        (tt["new_followers"] / tt["views"].replace(0, np.nan) * 1000).mean(),
        (ig["new_followers"] / ig["views"].replace(0, np.nan) * 1000).mean()
    ),
}

labels = list(kpis.keys())
tt_raw = [v[0] for v in kpis.values()]
ig_raw = [v[1] for v in kpis.values()]

# Normalize each metric to 0-100 scale for visual comparison
def normalize_pair(a, b):
    mx = max(abs(a), abs(b), 1)
    return a / mx * 100, b / mx * 100

tt_norm = []; ig_norm = []
for a, b in zip(tt_raw, ig_raw):
    an, bn = normalize_pair(a, b)
    tt_norm.append(an); ig_norm.append(bn)

fig, axes = plt.subplots(1, 2, figsize=(15, 7), gridspec_kw={"width_ratios": [1.6, 1]})
fig.patch.set_facecolor(BG)

ax = axes[0]
ax.set_facecolor(CARD)
y = np.arange(len(labels))
h = 0.35
bars_tt = ax.barh(y + h/2, tt_norm, h, color=TT_COL, alpha=0.88, label="TikTok")
bars_ig = ax.barh(y - h/2, ig_norm, h, color=IG_COL, alpha=0.88, label="Instagram")
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=10)
ax.set_xlabel("Valor normalizado (100 = mejor en esa métrica)")
ax.set_title("Rendimiento comparativo (normalizado)", fontweight="bold", fontsize=12, pad=12)
ax.legend(loc="lower right")
ax.grid(axis="x")

# Annotate actual values
for bar, val in zip(bars_tt, tt_raw):
    txt = f"{val:,.0f}" if val > 10 else f"{val:.2f}"
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            txt, va="center", fontsize=8, color=TT_COL)
for bar, val in zip(bars_ig, ig_raw):
    txt = f"{val:,.0f}" if val > 10 else f"{val:.2f}"
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            txt, va="center", fontsize=8, color=IG_COL)

# Right panel: winner badges
ax2 = axes[1]; ax2.set_facecolor(CARD); ax2.axis("off")
ax2.set_title("Ganador por métrica", fontweight="bold", fontsize=12, pad=12)
for i, (label, (tv, iv)) in enumerate(kpis.items()):
    winner = "TikTok" if tv >= iv else "Instagram"
    color  = TT_COL if winner == "TikTok" else IG_COL
    y_pos  = 0.92 - i * 0.14
    ax2.text(0.05, y_pos, f"  {label}", transform=ax2.transAxes,
             fontsize=9, color=TEXT, va="center")
    ax2.text(0.72, y_pos, f"▶ {winner}", transform=ax2.transAxes,
             fontsize=9, color=color, fontweight="bold", va="center")

plt.tight_layout()
plt.savefig(VIS / "01_kpis_comparativos.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# CHART 2: ENGAGEMENT RATE — Distribución por plataforma (violin/box)
# ─────────────────────────────────────────────────────────────────────────────
print("📊 Chart 2: Distribución engagement rate...")

fig, axes = plt.subplots(1, 2, figsize=(13, 6))
fig.patch.set_facecolor(BG)

for ax, df, color, plat, followers in [
    (axes[0], tt, TT_COL, "TikTok",    TT_FOLLOWERS),
    (axes[1], ig, IG_COL, "Instagram", IG_FOLLOWERS),
]:
    ax.set_facecolor(CARD)
    er = df["engagement_rate"].dropna().sort_values()
    ax.bar(range(len(er)), er.values, color=color, alpha=0.75, width=0.8)
    ax.axhline(er.mean(), color=GOLD, linestyle="--", linewidth=1.5,
               label=f"Media: {er.mean():.1f}%")
    ax.axhline(er.median(), color=TEXT, linestyle=":", linewidth=1.2,
               label=f"Mediana: {er.median():.1f}%")
    ax.set_ylabel("Engagement Rate (%)")
    ax.set_title(f"{plat} — ER por publicación\n({len(er)} posts)", fontweight="bold", pad=10)
    ax.legend(fontsize=9)
    ax.grid(axis="y")

plt.suptitle("Distribución del Engagement Rate — TikTok vs Instagram",
             fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(VIS / "02_engagement_distribucion.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# CHART 3: FOLLOWER CONVERSION — seg. ganados por 1K vistas
# ─────────────────────────────────────────────────────────────────────────────
print("📊 Chart 3: Follower conversion rate/1K...")

tt["fol_per_1k"] = tt["new_followers"] / tt["views"].replace(0, np.nan) * 1000
ig["fol_per_1k"] = ig["new_followers"] / ig["views"].replace(0, np.nan) * 1000

fig, ax = plt.subplots(figsize=(13, 6))
ax.set_facecolor(CARD)

x = np.arange(2)
means  = [tt["fol_per_1k"].mean(), ig["fol_per_1k"].mean()]
maxes  = [tt["fol_per_1k"].max(),  ig["fol_per_1k"].max()]
colors = [TT_COL, IG_COL]

bars_m = ax.bar(x - 0.2, means, 0.35, color=colors, alpha=0.9, label="Media")
bars_x = ax.bar(x + 0.2, maxes, 0.35, color=colors, alpha=0.45, label="Máximo")

ax.set_xticks(x); ax.set_xticklabels(["TikTok", "Instagram"], fontsize=12)
ax.set_ylabel("Seguidores ganados por 1K vistas")
ax.set_title("Follower Conversion Rate por 1K vistas — ¿Cuál convierte mejor?",
             fontweight="bold", fontsize=13, pad=12)
ax.legend()
ax.grid(axis="y")

for bar, val in zip(list(bars_m) + list(bars_x), means + maxes):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f"{val:.2f}", ha="center", fontsize=10, fontweight="bold")

# Insight annotation
winner_conv = "TikTok" if means[0] >= means[1] else "Instagram"
ax.annotate(f"✦ {winner_conv} convierte\nmás seguidores\npor vista",
            xy=(0 if winner_conv=="TikTok" else 1, means[0 if winner_conv=="TikTok" else 1]),
            xytext=(1.3, max(means)*0.7),
            fontsize=9, color=GOLD,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.2))

plt.tight_layout()
plt.savefig(VIS / "03_follower_conversion.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# CHART 4: SAVE RATE — señal de calidad (guardados / alcance)
# ─────────────────────────────────────────────────────────────────────────────
print("📊 Chart 4: Save rate comparativo...")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.patch.set_facecolor(BG)

for ax, df, color, plat in [
    (axes[0], tt, TT_COL, "TikTok"),
    (axes[1], ig, IG_COL, "Instagram"),
]:
    ax.set_facecolor(CARD)
    sr = df["save_rate"].dropna().sort_values(ascending=False)
    ax.bar(range(len(sr)), sr.values, color=color, alpha=0.8, width=0.8)
    ax.axhline(sr.mean(), color=GOLD, linestyle="--", lw=1.5,
               label=f"Media: {sr.mean():.2f}%")
    ax.set_ylabel("Save Rate (%)")
    ax.set_title(f"{plat} — Save Rate por publicación", fontweight="bold", pad=10)
    ax.legend(fontsize=9)
    ax.grid(axis="y")

plt.suptitle("Save Rate (Guardados / Alcance) — Señal de valor del contenido",
             fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(VIS / "04_save_rate.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# CHART 5: SHARE RATE — viralidad
# ─────────────────────────────────────────────────────────────────────────────
print("📊 Chart 5: Share rate comparativo...")

fig, ax = plt.subplots(figsize=(11, 6))
ax.set_facecolor(CARD)

categories = ["Share rate\nmedio %", "Share rate\nmáximo %", "Share rate\nmediana %"]
tt_vals = [tt["share_rate"].mean(), tt["share_rate"].max(), tt["share_rate"].median()]
ig_vals = [ig["share_rate"].mean(), ig["share_rate"].max(), ig["share_rate"].median()]

x2 = np.arange(len(categories))
ax.bar(x2 - 0.2, tt_vals, 0.35, color=TT_COL, alpha=0.88, label="TikTok")
ax.bar(x2 + 0.2, ig_vals, 0.35, color=IG_COL, alpha=0.88, label="Instagram")
ax.set_xticks(x2); ax.set_xticklabels(categories, fontsize=11)
ax.set_ylabel("Share Rate (%)")
ax.set_title("Share Rate (Compartidos) — ¿Dónde se viraliza más?",
             fontweight="bold", fontsize=13, pad=12)
ax.legend()
ax.grid(axis="y")

for bars, vals in [(ax.containers[0], tt_vals), (ax.containers[1], ig_vals)]:
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f"{val:.2f}%", ha="center", fontsize=9, fontweight="bold")

plt.tight_layout()
plt.savefig(VIS / "05_share_rate.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# CHART 6: RENDIMIENTO POR TEMÁTICA — ambas plataformas
# ─────────────────────────────────────────────────────────────────────────────
print("📊 Chart 6: Rendimiento por temática...")

tt_topic = tt.groupby("topic")["engagement_rate"].agg(["mean","count"]).rename(
    columns={"mean":"er_tt","count":"n_tt"}).reset_index().rename(columns={"topic":"tema"})
ig_topic = ig.groupby("tema")["engagement_rate"].agg(["mean","count"]).rename(
    columns={"mean":"er_ig","count":"n_ig"}).reset_index()

topics_merged = pd.merge(tt_topic, ig_topic, on="tema", how="outer").fillna(0)
topics_merged = topics_merged[
    (topics_merged["n_tt"] >= 1) | (topics_merged["n_ig"] >= 1)
].sort_values("er_tt", ascending=False)

fig, ax = plt.subplots(figsize=(13, 7))
ax.set_facecolor(CARD)
y3 = np.arange(len(topics_merged))
ax.barh(y3 + 0.2, topics_merged["er_tt"], 0.35, color=TT_COL, alpha=0.85, label="TikTok ER %")
ax.barh(y3 - 0.2, topics_merged["er_ig"], 0.35, color=IG_COL, alpha=0.85, label="Instagram ER %")
ax.set_yticks(y3); ax.set_yticklabels(topics_merged["tema"], fontsize=10)
ax.set_xlabel("Engagement Rate medio (%)")
ax.set_title("Engagement Rate por Temática — ¿Qué funciona en cada plataforma?",
             fontweight="bold", fontsize=13, pad=12)
ax.legend()
ax.grid(axis="x")
plt.tight_layout()
plt.savefig(VIS / "06_tematica_comparativa.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# CHART 7: PASSIVE VS ACTIVE RATIO
# ─────────────────────────────────────────────────────────────────────────────
print("📊 Chart 7: Passive vs Active ratio...")

tt["passive_active"] = (tt["likes"] + tt["saves"]) / (
    (tt["comments"] + tt["shares"]).replace(0, np.nan))
ig["passive_active"] = (ig["me_gustas"] + ig["guardados"]) / (
    (ig["comentarios"] + ig["compartidos"]).replace(0, np.nan))

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor(CARD)

data_pa = [tt["passive_active"].dropna().values, ig["passive_active"].dropna().values]
bp = ax.boxplot(data_pa, patch_artist=True, widths=0.4,
                medianprops=dict(color=GOLD, linewidth=2))
bp["boxes"][0].set_facecolor(TT_COL); bp["boxes"][0].set_alpha(0.7)
bp["boxes"][1].set_facecolor(IG_COL); bp["boxes"][1].set_alpha(0.7)
for whisker in bp["whiskers"]: whisker.set_color(TEXT)
for cap in bp["caps"]:         cap.set_color(TEXT)

ax.set_xticks([1, 2]); ax.set_xticklabels(["TikTok", "Instagram"], fontsize=12)
ax.set_ylabel("Ratio (Likes + Saves) / (Comments + Shares)")
ax.set_title("Passive vs Active Ratio — ¿Consumen o interactúan activamente?",
             fontweight="bold", fontsize=13, pad=12)
ax.axhline(5, color=GOLD, linestyle="--", alpha=0.5, label="Umbral pasivo (>5)")
ax.axhline(2, color="#6EE7B7", linestyle=":", alpha=0.5, label="Umbral activo (<2)")
ax.legend(fontsize=9)
ax.grid(axis="y")

for i, (data, color) in enumerate([(tt["passive_active"].dropna(), TT_COL),
                                    (ig["passive_active"].dropna(), IG_COL)], 1):
    ax.text(i, data.median() + 0.3, f"Med: {data.median():.1f}",
            ha="center", fontsize=9, color=GOLD, fontweight="bold")

plt.tight_layout()
plt.savefig(VIS / "07_passive_vs_active.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# CHART 8: RESUMEN EJECUTIVO — scorecard visual
# ─────────────────────────────────────────────────────────────────────────────
print("📊 Chart 8: Scorecard ejecutivo...")

fig, ax = plt.subplots(figsize=(13, 7))
ax.set_facecolor(BG); ax.axis("off")
ax.set_title("Scorecard Comparativo — @aroaxinping | Feb–Mar 2026",
             fontweight="bold", fontsize=14, pad=20, color=TEXT)

scorecard = [
    ("Vistas totales",         f"{tt['views'].sum():,.0f}",       f"{ig['views'].sum():,.0f}",         "TikTok"),
    ("Engagement rate medio",  f"{tt['engagement_rate'].mean():.1f}%", f"{ig['engagement_rate'].mean():.1f}%","TikTok"),
    ("Save rate medio",        f"{tt['save_rate'].mean():.2f}%",  f"{ig['save_rate'].mean():.2f}%",    "Instagram" if ig["save_rate"].mean() > tt["save_rate"].mean() else "TikTok"),
    ("Share rate medio",       f"{tt['share_rate'].mean():.2f}%", f"{ig['share_rate'].mean():.2f}%",   "TikTok" if tt["share_rate"].mean() > ig["share_rate"].mean() else "Instagram"),
    ("Seg. ganados",           f"{int(tt['new_followers'].sum()):,}", f"{int(ig['new_followers'].sum()):,}", "TikTok" if tt['new_followers'].sum() > ig['new_followers'].sum() else "Instagram"),
    ("Follower Rate/1K (avg)", f"{tt['fol_per_1k'].mean():.2f}",  f"{ig['fol_per_1k'].mean():.2f}",   "TikTok" if tt['fol_per_1k'].mean() > ig['fol_per_1k'].mean() else "Instagram"),
    ("Posts publicados",       str(len(tt)),                       str(len(ig)),                        "—"),
]

headers = ["Métrica", "TikTok", "Instagram", "Ganador"]
col_x   = [0.02, 0.30, 0.55, 0.78]
row_h   = 0.10
start_y = 0.85

for j, h in enumerate(headers):
    ax.text(col_x[j], start_y + 0.04, h, transform=ax.transAxes,
            fontsize=11, fontweight="bold", color=GOLD, va="center")

for i, (metric, tt_v, ig_v, winner) in enumerate(scorecard):
    y_pos = start_y - i * row_h
    bg_color = "#1A1A2E" if i % 2 == 0 else "#16213E"
    rect = plt.Rectangle((0, y_pos - 0.035), 1, row_h - 0.01,
                          transform=ax.transAxes, color=bg_color, zorder=0)
    ax.add_patch(rect)
    ax.text(col_x[0], y_pos, metric, transform=ax.transAxes, fontsize=10, color=TEXT, va="center")
    ax.text(col_x[1], y_pos, tt_v,  transform=ax.transAxes, fontsize=10,
            color=TT_COL if winner=="TikTok" else TEXT, fontweight="bold" if winner=="TikTok" else "normal", va="center")
    ax.text(col_x[2], y_pos, ig_v,  transform=ax.transAxes, fontsize=10,
            color=IG_COL if winner=="Instagram" else TEXT, fontweight="bold" if winner=="Instagram" else "normal", va="center")
    w_color = TT_COL if winner == "TikTok" else IG_COL if winner == "Instagram" else TEXT
    ax.text(col_x[3], y_pos, winner, transform=ax.transAxes, fontsize=10,
            color=w_color, fontweight="bold", va="center")

plt.tight_layout()
plt.savefig(VIS / "08_scorecard.png", dpi=150, bbox_inches="tight")
plt.close()

print(f"\n✅ 8 gráficas guardadas en {VIS}/")
print("   01_kpis_comparativos · 02_engagement_distribucion · 03_follower_conversion")
print("   04_save_rate · 05_share_rate · 06_tematica_comparativa")
print("   07_passive_vs_active · 08_scorecard")
