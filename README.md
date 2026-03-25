# 📊 Social Media Analytics — TikTok vs Instagram

> Análisis comparativo cross-platform @aroaxinping · Período: 24 Feb – 24 Mar 2026

---

## ¿De qué trata este proyecto?

Después de construir proyectos de analytics individuales para [TikTok](https://github.com/aroaxinping/tiktok-analytics-aroaxinping) e [Instagram](https://github.com/aroaxinping/instagram-analytics-aroaxinping), el siguiente paso natural fue compararlos directamente: ¿qué plataforma convierte mejor? ¿dónde tiene más impacto el contenido de datos/tech? ¿qué métricas clave difieren entre ambos algoritmos?

**Mismo período, mismo creador, dos algoritmos distintos.**

---

## Datos utilizados

| Plataforma | Fuente | Posts analizados | Período |
|---|---|---|---|
| TikTok | TikTok Studio (manual) | 10 vídeos | 24 Feb – 24 Mar 2026 |
| Instagram | Meta Business Suite (manual) | 30 reels | 24 Feb – 24 Mar 2026 |

---

## Resultados principales

### KPIs Comparativos

![KPIs comparativos](visuals/01_kpis_comparativos.png)

### Distribución del Engagement Rate

![Distribución ER](visuals/02_engagement_distribucion.png)

### Follower Conversion Rate / 1K Vistas

![Follower conversion](visuals/03_follower_conversion.png)

### Save Rate — Calidad del contenido

![Save rate](visuals/04_save_rate.png)

### Share Rate — Viralidad

![Share rate](visuals/05_share_rate.png)

### Rendimiento por Temática

![Temática comparativa](visuals/06_tematica_comparativa.png)

### Passive vs Active Engagement

![Passive vs Active](visuals/07_passive_vs_active.png)

### Scorecard Ejecutivo

![Scorecard](visuals/08_scorecard.png)

---

## Hallazgos clave

- **TikTok lidera en alcance absoluto**: 3.1M vistas en 10 vídeos vs ~200K en 30 reels en Instagram — el algoritmo de TikTok distribuye mucho más agresivamente contenido nuevo.
- **Instagram convierte mejor a seguidores**: mayor follower conversion rate relativo al alcance, lo que indica una audiencia más alineada con el perfil.
- **El contenido de humor personal bate a SQL/Python en ambas plataformas** en engagement rate puro — aunque el contenido técnico genera más guardados (calidad).
- **Save rate de Instagram es notablemente alto** (~5–8% medio), señal de que el contenido técnico se guarda para consultar después.
- **Passive vs Active ratio**: TikTok muestra ratios más extremos (vídeos virales con muchos likes pero poco comentario), Instagram es más consistente.

---

## Estructura del proyecto

```
social-media-analytics-aroaxinping/
├── data/
│   ├── tiktok/
│   │   ├── videos_engagement.csv
│   │   └── overview_metrics.csv
│   └── instagram/
│       ├── reels_metricas.csv
│       └── metricas_diarias.csv
├── src/
│   └── analyze.py          # Script principal de análisis comparativo
├── visuals/                # 8 gráficas generadas
├── notebooks/
│   └── cross_platform_analysis.ipynb
├── requirements.txt
└── README.md
```

---

## Cómo reproducir

```bash
git clone https://github.com/aroaxinping/social-media-analytics-aroaxinping
cd social-media-analytics-aroaxinping
pip install -r requirements.txt
python src/analyze.py
```

---

## Proyectos individuales

- [instagram-analytics-aroaxinping](https://github.com/aroaxinping/instagram-analytics-aroaxinping) — análisis profundo de Instagram con métricas diarias, por reel y Excel avanzado
- [tiktok-analytics-aroaxinping](https://github.com/aroaxinping/tiktok-analytics-aroaxinping) — análisis de TikTok con 8 visualizaciones y Excel con fórmulas de social media

---

`Python` `pandas` `matplotlib` `numpy` · *Período: 24 Feb – 24 Mar 2026*
