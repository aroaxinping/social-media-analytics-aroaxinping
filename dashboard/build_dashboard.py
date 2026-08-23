"""
Cross-Platform Analytics Dashboard — TikTok vs Instagram @aroaxinping
Genera un dashboard interactivo HTML con Plotly.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── Rutas ──────────────────────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TT_CSV = os.path.join(BASE, "data", "tiktok",    "videos_engagement.csv")
IG_CSV = os.path.join(BASE, "data", "instagram", "reels_metricas.csv")
IG_DAY = os.path.join(BASE, "data", "instagram", "metricas_diarias.csv")
OUT    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crossplatform_dashboard.html")

# ── Datos ──────────────────────────────────────────────────────────────────
tt = pd.read_csv(TT_CSV)
ig = pd.read_csv(IG_CSV)
ig_daily = pd.read_csv(IG_DAY)

ig["fecha"] = pd.to_datetime(ig["fecha"])
ig_daily["fecha"] = pd.to_datetime(ig_daily["fecha"])

# Unificar columnas para comparacion
tt_unified = pd.DataFrame({
    "plataforma": "TikTok",
    "vistas":          tt["views"],
    "engagement_rate": tt["engagement_rate_pct"],
    "save_rate":       tt["save_rate_pct"],
    "share_rate":      tt["share_rate_pct"],
    "seguidores":      tt["new_followers"],
})
ig_unified = pd.DataFrame({
    "plataforma": "Instagram",
    "vistas":          ig["visualizaciones"],
    "engagement_rate": ig["engagement_rate"],
    "save_rate":       ig["save_rate"],
    "share_rate":      ig["share_rate"],
    "seguidores":      ig["seguidores_ganados"],
})
combined = pd.concat([tt_unified, ig_unified], ignore_index=True)

# Colores
TT_COLOR = "#FF2D55"
IG_COLOR = "#E1306C"
IG_GRAD  = "#833ab4"
DARK     = "#0f0f1a"
CARD     = "#1a1a2e"
LIGHT    = "#e2e8f0"
MUTED    = "#94a3b8"

# ── Figura ──────────────────────────────────────────────────────────────────
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        "Vistas medias por plataforma",
        "Engagement Rate medio (%)",
        "Distribucion de vistas (box plot)",
        "Save Rate vs Share Rate",
        "Seguidores ganados por publicacion",
        "ER vs Vistas — TikTok vs Instagram",
    ),
    vertical_spacing=0.12,
    horizontal_spacing=0.12,
    specs=[[{"type":"xy"},{"type":"xy"}],
           [{"type":"xy"},{"type":"xy"}],
           [{"type":"xy"},{"type":"xy"}]],
)

kpis = combined.groupby("plataforma").agg(
    vistas_medias=("vistas","mean"),
    er_medio=("engagement_rate","mean"),
    save_medio=("save_rate","mean"),
    share_medio=("share_rate","mean"),
    seg_total=("seguidores","sum"),
).reset_index()

colors_map = {"TikTok": TT_COLOR, "Instagram": IG_GRAD}
bar_colors = [colors_map[p] for p in kpis["plataforma"]]

# 1. Vistas medias
fig.add_trace(go.Bar(
    x=kpis["plataforma"],
    y=kpis["vistas_medias"],
    marker=dict(color=bar_colors),
    text=[f'{v/1000:.0f}K' for v in kpis["vistas_medias"]],
    textposition="outside",
    name="Vistas medias",
), row=1, col=1)

# 2. ER medio
fig.add_trace(go.Bar(
    x=kpis["plataforma"],
    y=kpis["er_medio"],
    marker=dict(color=bar_colors),
    text=[f'{v:.1f}%' for v in kpis["er_medio"]],
    textposition="outside",
    name="ER medio",
), row=1, col=2)

# 3. Box plot vistas
for plat, color in [("TikTok", TT_COLOR), ("Instagram", IG_GRAD)]:
    sub = combined[combined["plataforma"] == plat]
    fig.add_trace(go.Box(
        y=sub["vistas"],
        name=plat,
        marker=dict(color=color),
        line=dict(color=color),
        boxmean=True,
    ), row=2, col=1)

# 4. Save Rate vs Share Rate (scatter)
for plat, color, sym in [("TikTok", TT_COLOR, "circle"), ("Instagram", IG_GRAD, "diamond")]:
    sub = combined[combined["plataforma"] == plat]
    fig.add_trace(go.Scatter(
        x=sub["share_rate"],
        y=sub["save_rate"],
        mode="markers",
        name=plat,
        marker=dict(size=10, color=color, symbol=sym, opacity=0.8),
    ), row=2, col=2)

# 5. Seguidores por publicacion
fig.add_trace(go.Bar(
    x=kpis["plataforma"],
    y=kpis["seg_total"] / kpis.apply(
        lambda r: len(tt) if r["plataforma"]=="TikTok" else len(ig), axis=1
    ),
    marker=dict(color=bar_colors),
    text=[f'{v:.0f}' for v in kpis["seg_total"] / kpis.apply(
        lambda r: len(tt) if r["plataforma"]=="TikTok" else len(ig), axis=1
    )],
    textposition="outside",
    name="Seg/publicacion",
), row=3, col=1)

# 6. ER vs Vistas scatter (ambas plataformas)
for plat, color, sym in [("TikTok", TT_COLOR, "circle"), ("Instagram", IG_GRAD, "diamond")]:
    sub = combined[combined["plataforma"] == plat]
    fig.add_trace(go.Scatter(
        x=sub["vistas"],
        y=sub["engagement_rate"],
        mode="markers",
        name=plat,
        marker=dict(size=10, color=color, symbol=sym, opacity=0.8),
    ), row=3, col=2)

# ── Layout ──────────────────────────────────────────────────────────────────
fig.update_layout(
    height=1300,
    paper_bgcolor=DARK,
    plot_bgcolor=CARD,
    font=dict(color=LIGHT, family="Inter, system-ui, sans-serif", size=11),
    title=dict(
        text="<b>TikTok vs Instagram — Cross-Platform Analytics</b> · @aroaxinping · Feb–Mar 2026",
        font=dict(size=18, color=LIGHT),
        x=0.5,
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0.4)", bordercolor="#4a5568", borderwidth=1,
        font=dict(color=LIGHT),
    ),
    margin=dict(t=80, b=40, l=20, r=20),
    barmode="group",
)

for i in range(1, 4):
    for j in range(1, 3):
        fig.update_xaxes(showgrid=True, gridcolor="#2d3748", gridwidth=0.5,
                         zeroline=False, linecolor="#4a5568",
                         tickfont=dict(color=MUTED, size=9), row=i, col=j)
        fig.update_yaxes(showgrid=True, gridcolor="#2d3748", gridwidth=0.5,
                         zeroline=False, linecolor="#4a5568",
                         tickfont=dict(color=MUTED, size=9), row=i, col=j)

for ann in fig.layout.annotations:
    ann.font.color = LIGHT
    ann.font.size = 12

fig.update_xaxes(title_text="Share Rate (%)", row=2, col=2)
fig.update_yaxes(title_text="Save Rate (%)", row=2, col=2)
fig.update_yaxes(title_text="Seguidores / publicacion", row=3, col=1)
fig.update_xaxes(title_text="Vistas", row=3, col=2)
fig.update_yaxes(title_text="Engagement Rate (%)", row=3, col=2)

# KPIs summary
tt_views = tt["views"].sum()
ig_views = ig["visualizaciones"].sum()
tt_er    = tt["engagement_rate_pct"].mean()
ig_er    = ig["engagement_rate"].mean()
kpi_text = (
    f"<b>TikTok:</b> {tt_views/1e6:.1f}M vistas · ER {tt_er:.1f}%  |  "
    f"<b>Instagram:</b> {ig_views/1e6:.2f}M vistas · ER {ig_er:.1f}%  |  "
    f"<b>Periodo:</b> 24 Feb – 24 Mar 2026"
)
fig.add_annotation(
    text=kpi_text, x=0.5, y=1.04, xref="paper", yref="paper",
    showarrow=False, font=dict(size=11, color="#f093fb"), align="center",
)

# ── Exportar ─────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.write_html(OUT, include_plotlyjs="cdn", full_html=True)
print(f"Dashboard guardado en: {OUT}")
