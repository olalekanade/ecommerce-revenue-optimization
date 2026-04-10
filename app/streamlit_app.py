"""
Ecommerce Revenue Optimization — Streamlit Dashboard
Run from repo root: streamlit run app/streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Ecommerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
PROC = ROOT / "data" / "processed"

# ── Palette ───────────────────────────────────────────────────────────────────
BG    = "#0A0E1A"
SURF  = "#111827"
CARD  = "#1A2236"
BORD  = "#1E3A5F"
TEAL  = "#00D4AA"
AMBER = "#F59E0B"
RED   = "#EF4444"
MUTED = "#64748B"
TXT   = "#F1F5F9"
TXT2  = "#94A3B8"

SEG_COLOR = {
    "Champions":           "#00D4AA",
    "Loyal Customers":     "#3B82F6",
    "Potential Loyalists": "#8B5CF6",
    "At Risk":             "#F59E0B",
    "Hibernating":         "#EF4444",
    "Others":              "#64748B",
}
SEG_ORDER = list(SEG_COLOR.keys())

# ── CSS injection ─────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

/* ── Hide Streamlit chrome ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
.stDeployButton { display: none; }

/* ── App shell ── */
.stApp { background-color: #0A0E1A; }
.main .block-container {
    padding-top: 1.2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1440px;
}

/* ── KPI cards ── */
.kpi-card {
    background: #1A2236;
    border: 1px solid #1E3A5F;
    border-top: 3px solid #00D4AA;
    border-radius: 6px;
    padding: 16px 18px 12px 18px;
}
.kpi-label {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 24px;
    font-weight: 600;
    color: #F1F5F9;
    line-height: 1.15;
}
.kpi-teal  { color: #00D4AA; }
.kpi-amber { color: #F59E0B; }
.kpi-muted { color: #94A3B8; }
.kpi-sub {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    color: #64748B;
    margin-top: 5px;
}

/* ── Section headers ── */
.sec-hdr {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: #00D4AA;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    border-left: 3px solid #00D4AA;
    padding-left: 10px;
    margin: 22px 0 14px 0;
    line-height: 1;
}

/* ── App title ── */
.app-title {
    font-family: 'Inter', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #F1F5F9;
}
.app-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #64748B;
    letter-spacing: 1px;
    margin-top: 2px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #111827;
    border-bottom: 1px solid #1E3A5F;
    gap: 0;
    padding: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #64748B !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    padding: 10px 26px !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #00D4AA !important;
    border-bottom: 2px solid #00D4AA !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 20px;
}

/* ── Segment def cards ── */
.seg-card {
    background: #1A2236;
    border: 1px solid #1E3A5F;
    border-radius: 6px;
    padding: 14px 16px;
}
.seg-card-name {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
}
.seg-card-rule {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #94A3B8;
    line-height: 1.5;
}
.seg-card-count {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #64748B;
    margin-top: 6px;
}

/* ── Callout box ── */
.callout {
    background: #071a16;
    border: 1px solid #00D4AA;
    border-left: 4px solid #00D4AA;
    border-radius: 6px;
    padding: 16px 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #00D4AA;
    line-height: 1.7;
    margin-top: 20px;
}
.callout-lbl {
    font-size: 9px;
    letter-spacing: 2.5px;
    color: #64748B;
    margin-bottom: 8px;
}

/* ── Summary bar ── */
.summary-bar {
    background: #1A2236;
    border: 1px solid #1E3A5F;
    border-radius: 6px;
    padding: 11px 18px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: #F1F5F9;
    margin-bottom: 14px;
}

/* ── Pagination ── */
.page-info {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #64748B;
    text-align: center;
    padding: 6px;
}

/* ── Model table rows ── */
.model-table { width: 100%; border-collapse: collapse; font-family: 'IBM Plex Mono', monospace; font-size: 12px; }
.model-table th { background: #0A0E1A; color: #64748B; font-size: 10px; letter-spacing: 1px; text-transform: uppercase; padding: 10px 14px; border-bottom: 1px solid #1E3A5F; text-align: left; }
.model-table td { padding: 10px 14px; border-bottom: 1px solid #1A2236; color: #F1F5F9; }
.model-table tr.naive-row td { background: #071a16; color: #00D4AA; }
.model-table tr.ets-row td { background: #1a0a0a; color: #64748B; }
.model-table tr:hover td { background: #1E3A5F22; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Data loaders ──────────────────────────────────────────────────────────────
@st.cache_data
def load_segment_summary() -> pd.DataFrame:
    return pd.read_csv(PROC / "rfm_segment_summary.csv")


@st.cache_data
def load_monthly() -> pd.DataFrame:
    df = pd.read_csv(PROC / "monthly_revenue_actual.csv", parse_dates=["month"])
    return df


@st.cache_data
def load_forecast() -> pd.DataFrame:
    df = pd.read_csv(PROC / "revenue_forecast_total.csv", index_col=0)
    df.index = pd.to_datetime(df.index)
    df = df.reset_index()
    df.columns = ["month", "forecast_revenue"]
    return df


@st.cache_data
def load_models() -> pd.DataFrame:
    return pd.read_csv(PROC / "forecast_model_comparison.csv")


@st.cache_data
def load_rfm() -> pd.DataFrame:
    return pd.read_csv(PROC / "rfm_segments.csv")


# ── Helper utilities ──────────────────────────────────────────────────────────
def fmt_m(v: float) -> str:
    if v >= 1_000_000:
        return f"R${v / 1_000_000:.1f}M"
    if v >= 1_000:
        return f"R${v / 1_000:.0f}K"
    return f"R${v:,.0f}"


def sec(text: str) -> None:
    st.markdown(f'<div class="sec-hdr">{text}</div>', unsafe_allow_html=True)


def kpi(label: str, value: str, sub: str = "", cls: str = "") -> str:
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value {cls}">{value}</div>'
        f'<div class="kpi-sub">{sub}</div>'
        f"</div>"
    )


def chart_base(fig: go.Figure, title: str = "") -> go.Figure:
    upd = dict(
        paper_bgcolor=SURF,
        plot_bgcolor=SURF,
        font=dict(family="IBM Plex Mono, monospace", color=TXT2, size=11),
        margin=dict(l=55, r=24, t=48 if title else 28, b=44),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TXT, size=11)),
    )
    if title:
        upd["title"] = dict(text=title, font=dict(color=TXT, size=14, family="Inter, sans-serif"))
    fig.update_layout(**upd)
    return fig


# ── Load all data once ────────────────────────────────────────────────────────
seg_sum  = load_segment_summary()
monthly  = load_monthly()
forecast = load_forecast()
models   = load_models()
rfm      = load_rfm()

seg_map        = seg_sum.set_index("segment").to_dict("index")
total_rev      = seg_sum["total_revenue"].sum()
total_cust     = seg_sum["customers"].sum()
champ_n        = int(seg_map["Champions"]["customers"])
atrisk_n       = int(seg_map["At Risk"]["customers"])
champ_pct      = champ_n  / total_cust * 100
atrisk_pct     = atrisk_n / total_cust * 100
valid_monthly  = monthly.dropna(subset=["revenue"])
total_orders   = valid_monthly["orders"].sum()
aov            = valid_monthly["revenue"].sum() / total_orders

# ── App header ────────────────────────────────────────────────────────────────
h_left, h_right = st.columns([3, 1])
with h_left:
    st.markdown(
        '<div class="app-title">Ecommerce Revenue Optimization</div>'
        '<div class="app-sub">OLIST BRAZIL · SEP 2016 – AUG 2018 · 93,358 CUSTOMERS</div>',
        unsafe_allow_html=True,
    )
with h_right:
    st.markdown(
        f'<div style="text-align:right; font-family:\'IBM Plex Mono\',monospace; '
        f'font-size:11px; color:{MUTED}; padding-top:8px;">'
        f'R${total_rev:,.0f} TOTAL REVENUE</div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr style="border:none; border-top:1px solid #1E3A5F; margin:8px 0 0 0;">', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "RFM Segments", "Revenue Forecast", "Customer Explorer"]
)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    # ── KPI row ──
    sec("KEY PERFORMANCE INDICATORS")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    cards = [
        (c1, "Total Revenue",     fmt_m(total_rev),       "All delivered orders", ""),
        (c2, "Total Customers",   f"{total_cust:,}",       "Unique buyers", ""),
        (c3, "Champions",         f"{champ_n:,}",          f"{champ_pct:.1f}% of base · highest LTV", "kpi-teal"),
        (c4, "At Risk",           f"{atrisk_n:,}",         f"{atrisk_pct:.1f}% of base · R$3.7M at stake", "kpi-amber"),
        (c5, "Avg Order Value",   f"R${aov:,.2f}",         "Revenue ÷ total orders", ""),
        (c6, "Repeat Buyer LTV",  "R$308.59",              "1.92× one-time buyer avg", "kpi-muted"),
    ]
    for col, label, value, sub, cls in cards:
        with col:
            st.markdown(kpi(label, value, sub, cls), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ──
    left, right = st.columns([6, 4])

    # ── Revenue trend chart ──────────────────────────────────────────────────
    with left:
        sec("MONTHLY REVENUE — ACTUAL VS FORECAST")

        # Combine actual + forecast
        actual_df = valid_monthly.copy()
        # bridge: repeat Aug 2018 as first forecast point for connected line
        bridge = pd.DataFrame({
            "month": [actual_df["month"].iloc[-1]],
            "forecast_revenue": [forecast["forecast_revenue"].iloc[0]],
        })
        fc_full = pd.concat([bridge, forecast], ignore_index=True)

        fig_rev = go.Figure()

        # Actual fill area
        fig_rev.add_trace(go.Scatter(
            x=actual_df["month"],
            y=actual_df["revenue"],
            name="Actual Revenue",
            mode="lines",
            line=dict(color=TEAL, width=2.5),
            fill="tozeroy",
            fillcolor="rgba(0,212,170,0.08)",
            hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: R$%{y:,.0f}<extra></extra>",
        ))

        # Forecast line (dashed amber)
        fig_rev.add_trace(go.Scatter(
            x=fc_full["month"],
            y=fc_full["forecast_revenue"],
            name="Forecast",
            mode="lines",
            line=dict(color=AMBER, width=2.5, dash="dash"),
            hovertemplate="<b>%{x|%b %Y}</b><br>Forecast: R$%{y:,.0f}<extra></extra>",
        ))

        # Forecast period shading
        fc_start = forecast["month"].iloc[0]
        fc_end   = forecast["month"].iloc[-1]
        fig_rev.add_vrect(
            x0=str(fc_start)[:10], x1=str(fc_end)[:10],
            fillcolor="rgba(245,158,11,0.07)",
            layer="below", line_width=0,
            annotation_text="FORECAST", annotation_position="top left",
            annotation=dict(font=dict(color=AMBER, size=10, family="IBM Plex Mono")),
        )

        fig_rev.update_xaxes(
            showgrid=False, color=TXT2, tickfont=dict(size=10),
            tickformat="%b %Y", tickangle=-30,
        )
        fig_rev.update_yaxes(
            showgrid=True, gridcolor=BORD, color=TXT2,
            tickfont=dict(size=10), tickprefix="R$", tickformat=",.0f",
        )
        chart_base(fig_rev)
        fig_rev.update_layout(height=340, showlegend=True)
        st.plotly_chart(fig_rev, use_container_width=True, config={"displayModeBar": False})

    # ── Segment donut chart ──────────────────────────────────────────────────
    with right:
        sec("REVENUE BY SEGMENT")

        # Sort by SEG_ORDER for consistent colour mapping
        donut_df = seg_sum.set_index("segment").loc[SEG_ORDER].reset_index()

        fig_donut = go.Figure(go.Pie(
            labels=donut_df["segment"],
            values=donut_df["revenue_share"],
            hole=0.52,
            marker=dict(
                colors=[SEG_COLOR[s] for s in donut_df["segment"]],
                line=dict(color=SURF, width=2),
            ),
            textinfo="label+percent",
            textposition="outside",
            textfont=dict(size=10, family="IBM Plex Mono, monospace", color=TXT2),
            hovertemplate="<b>%{label}</b><br>Share: %{percent}<br>Revenue: R$%{value:.2%}<extra></extra>",
            direction="clockwise",
            sort=False,
        ))

        fig_donut.update_layout(
            annotations=[dict(
                text=f"<b>{fmt_m(total_rev)}</b><br><span style='font-size:10px'>Total Revenue</span>",
                x=0.5, y=0.5, font_size=14, showarrow=False,
                font=dict(color=TXT, family="IBM Plex Mono"),
            )],
            showlegend=False,
            height=340,
            margin=dict(l=30, r=30, t=30, b=30),
        )
        chart_base(fig_donut)
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — RFM SEGMENTS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    sec("SEGMENT PERFORMANCE TABLE")

    # Build styled HTML table
    display_order = sorted(SEG_ORDER, key=lambda s: -seg_map[s]["total_revenue"])
    max_rev = max(seg_map[s]["total_revenue"] for s in display_order)

    rows_html = ""
    for i, seg in enumerate(display_order):
        r      = seg_map[seg]
        color  = SEG_COLOR[seg]
        bg     = CARD if i % 2 == 0 else SURF
        share  = r["revenue_share"]
        bar_w  = int(share * 200)  # px, max ~200 for 100%

        rows_html += f"""
        <tr style="background:{bg};">
          <td style="padding:11px 16px; border-bottom:1px solid #1A2236;">
            <span style="display:inline-block; width:8px; height:8px; border-radius:50%;
                         background:{color}; margin-right:8px; vertical-align:middle;"></span>
            <span style="font-family:'Inter',sans-serif; font-weight:600; color:{color};">{seg}</span>
          </td>
          <td style="padding:11px 16px; border-bottom:1px solid #1A2236; font-family:'IBM Plex Mono',monospace;
                     text-align:right; color:{TXT};">{int(r['customers']):,}</td>
          <td style="padding:11px 16px; border-bottom:1px solid #1A2236; font-family:'IBM Plex Mono',monospace;
                     text-align:right; color:{TXT2};">{r['avg_recency_days']:.0f}d</td>
          <td style="padding:11px 16px; border-bottom:1px solid #1A2236; font-family:'IBM Plex Mono',monospace;
                     text-align:right; color:{TXT2};">{r['avg_frequency']:.2f}</td>
          <td style="padding:11px 16px; border-bottom:1px solid #1A2236; font-family:'IBM Plex Mono',monospace;
                     text-align:right; color:{TXT};">R${r['avg_monetary']:,.2f}</td>
          <td style="padding:11px 16px; border-bottom:1px solid #1A2236; font-family:'IBM Plex Mono',monospace;
                     text-align:right; color:{TXT};">{fmt_m(r['total_revenue'])}</td>
          <td style="padding:11px 16px; border-bottom:1px solid #1A2236; text-align:right; color:{TXT2};">
            <span style="font-family:'IBM Plex Mono',monospace;">{r['customer_share']:.1%}</span>
          </td>
          <td style="padding:11px 24px 11px 16px; border-bottom:1px solid #1A2236;">
            <div style="display:flex; align-items:center; gap:8px; justify-content:flex-end;">
              <span style="font-family:'IBM Plex Mono',monospace; color:{TXT2}; font-size:12px;">{share:.1%}</span>
              <div style="width:{bar_w}px; height:6px; background:{color}; border-radius:3px; opacity:0.8;
                          min-width:4px;"></div>
            </div>
          </td>
        </tr>"""

    table_html = f"""
    <div style="overflow-x:auto; border:1px solid {BORD}; border-radius:8px;">
    <table style="width:100%; border-collapse:collapse; font-size:13px;">
      <thead>
        <tr style="background:{BG};">
          <th style="padding:10px 16px; text-align:left; font-family:'Inter',sans-serif; font-size:10px;
                     font-weight:600; color:{MUTED}; letter-spacing:1.2px; text-transform:uppercase;
                     border-bottom:1px solid {BORD};">Segment</th>
          <th style="padding:10px 16px; text-align:right; font-family:'Inter',sans-serif; font-size:10px;
                     font-weight:600; color:{MUTED}; letter-spacing:1.2px; text-transform:uppercase;
                     border-bottom:1px solid {BORD};">Customers</th>
          <th style="padding:10px 16px; text-align:right; font-family:'Inter',sans-serif; font-size:10px;
                     font-weight:600; color:{MUTED}; letter-spacing:1.2px; text-transform:uppercase;
                     border-bottom:1px solid {BORD};">Avg Recency</th>
          <th style="padding:10px 16px; text-align:right; font-family:'Inter',sans-serif; font-size:10px;
                     font-weight:600; color:{MUTED}; letter-spacing:1.2px; text-transform:uppercase;
                     border-bottom:1px solid {BORD};">Avg Freq</th>
          <th style="padding:10px 16px; text-align:right; font-family:'Inter',sans-serif; font-size:10px;
                     font-weight:600; color:{MUTED}; letter-spacing:1.2px; text-transform:uppercase;
                     border-bottom:1px solid {BORD};">Avg Monetary</th>
          <th style="padding:10px 16px; text-align:right; font-family:'Inter',sans-serif; font-size:10px;
                     font-weight:600; color:{MUTED}; letter-spacing:1.2px; text-transform:uppercase;
                     border-bottom:1px solid {BORD};">Total Revenue</th>
          <th style="padding:10px 16px; text-align:right; font-family:'Inter',sans-serif; font-size:10px;
                     font-weight:600; color:{MUTED}; letter-spacing:1.2px; text-transform:uppercase;
                     border-bottom:1px solid {BORD};">Cust %</th>
          <th style="padding:10px 24px 10px 16px; text-align:right; font-family:'Inter',sans-serif;
                     font-size:10px; font-weight:600; color:{MUTED}; letter-spacing:1.2px;
                     text-transform:uppercase; border-bottom:1px solid {BORD};">Rev Share</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    </div>"""
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ──────────────────────────────────────────────────────────
    ch_left, ch_right = st.columns(2)

    with ch_left:
        sec("REVENUE BY SEGMENT")
        sorted_segs = sorted(SEG_ORDER, key=lambda s: seg_map[s]["total_revenue"])
        revenues = [seg_map[s]["total_revenue"] for s in sorted_segs]
        max_revenue = max(revenues)
        fig_bar = go.Figure(go.Bar(
            x=revenues,
            y=sorted_segs,
            orientation="h",
            marker_color=[SEG_COLOR[s] for s in sorted_segs],
            text=[f"R${v/1e6:.1f}M" for v in revenues],
            textposition="outside",
            textfont=dict(family="IBM Plex Mono, monospace", size=11, color=TXT),
            hovertemplate="<b>%{y}</b><br>Revenue: R$%{x:,.0f}<extra></extra>",
        ))
        fig_bar.update_xaxes(showgrid=True, gridcolor=BORD, color=TXT2, tickprefix="R$",
                              tickformat=",.0f", range=[0, max_revenue * 1.15])
        fig_bar.update_yaxes(showgrid=False, color=TXT2)
        chart_base(fig_bar)
        fig_bar.update_layout(height=320, showlegend=False, bargap=0.25, margin=dict(r=120))
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with ch_right:
        sec("RECENCY vs MONETARY BY SEGMENT")
        sample = rfm.sample(2000, random_state=42)
        # Cap monetary at 95th pct for cleaner scatter
        cap = rfm["monetary"].quantile(0.95)
        sample = sample[sample["monetary"] <= cap]

        fig_scat = go.Figure()
        for seg in SEG_ORDER:
            s = sample[sample["segment"] == seg]
            if s.empty:
                continue
            fig_scat.add_trace(go.Scatter(
                x=s["recency_days"],
                y=s["monetary"],
                mode="markers",
                name=seg,
                marker=dict(color=SEG_COLOR[seg], size=4, opacity=0.6),
                hovertemplate=(
                    f"<b>{seg}</b><br>"
                    "Recency: %{x}d<br>Monetary: R$%{y:,.2f}<extra></extra>"
                ),
            ))
        fig_scat.update_xaxes(showgrid=False, color=TXT2, title_text="Recency (days)",
                               title_font=dict(size=11))
        fig_scat.update_yaxes(showgrid=True, gridcolor=BORD, color=TXT2,
                               title_text="Monetary (R$)", title_font=dict(size=11),
                               tickprefix="R$", tickformat=",.0f")
        chart_base(fig_scat)
        fig_scat.update_layout(height=320, legend=dict(orientation="h", y=-0.25,
                                                        font=dict(size=10)))
        st.plotly_chart(fig_scat, use_container_width=True, config={"displayModeBar": False})

    # ── Segment definition cards ─────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    sec("SEGMENT CLASSIFICATION RULES")

    seg_defs = [
        ("Champions",           "#00D4AA", "R ≥ 4  ·  F ≥ 4  ·  M ≥ 4",
         "Highest LTV · most recent · most frequent"),
        ("Loyal Customers",     "#3B82F6", "R ≥ 4  ·  F ≥ 3",
         "Recent with repeat behaviour"),
        ("Potential Loyalists", "#8B5CF6", "R ≥ 3  ·  F ≤ 2",
         "Recent first-time buyers — onboarding target"),
        ("At Risk",             "#F59E0B", "R ≤ 2  ·  F ≥ 3",
         "Were repeat buyers — >1 yr since purchase"),
        ("Hibernating",         "#EF4444", "R ≤ 2  ·  F ≤ 2",
         "Inactive one-time buyers — reactivation needed"),
        ("Others",              "#64748B", "All remaining",
         "Mixed profiles — secondary segmentation required"),
    ]

    r1, r2 = st.columns(3), st.columns(3)
    rows_of_cols = [r1, r2]
    for i, (seg, color, rule, desc) in enumerate(seg_defs):
        row_idx = i // 3
        col_idx = i % 3
        n = int(seg_map[seg]["customers"])
        with rows_of_cols[row_idx][col_idx]:
            st.markdown(
                f'<div class="seg-card" style="border-left:4px solid {color};">'
                f'<div class="seg-card-name" style="color:{color};">{seg}</div>'
                f'<div class="seg-card-rule">{rule}</div>'
                f'<div class="seg-card-rule" style="color:{MUTED}; margin-top:4px;">{desc}</div>'
                f'<div class="seg-card-count">{n:,} customers</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — REVENUE FORECAST
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    # ── Top metrics ──────────────────────────────────────────────────────────
    sec("FORECAST PARAMETERS")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(kpi("Training Period", "Sep 2016 – May 2018", "20 months of data"), unsafe_allow_html=True)
    with m2:
        st.markdown(kpi("Holdout Period", "Jun – Aug 2018", "3 months validation"), unsafe_allow_html=True)
    with m3:
        st.markdown(kpi("Model Selected", "Naive", "Lowest holdout error", "kpi-teal"), unsafe_allow_html=True)
    with m4:
        st.markdown(kpi("Holdout MAPE", "11.97%", "MAE: R$120,367", "kpi-amber"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("REVENUE — ACTUAL VS FORECAST")

    # Build combined figure (actual line + volume bars + forecast)
    actual_valid = monthly.dropna(subset=["revenue"])

    bridge_fc = pd.concat([
        pd.DataFrame({"month": [actual_valid["month"].iloc[-1]],
                      "forecast_revenue": [forecast["forecast_revenue"].iloc[0]]}),
        forecast,
    ], ignore_index=True)

    fc_start_dt = forecast["month"].iloc[0]

    fig_fc = go.Figure()

    # Volume bars (secondary axis)
    fig_fc.add_trace(go.Bar(
        x=actual_valid["month"],
        y=actual_valid["orders"],
        name="Order Volume",
        marker_color="rgba(59,130,246,0.15)",
        yaxis="y2",
        hovertemplate="<b>%{x|%b %Y}</b><br>Orders: %{y:,}<extra></extra>",
        showlegend=True,
    ))

    # Actual area + line
    fig_fc.add_trace(go.Scatter(
        x=actual_valid["month"],
        y=actual_valid["revenue"],
        name="Actual Revenue",
        mode="lines",
        line=dict(color=TEAL, width=2.5),
        fill="tozeroy",
        fillcolor="rgba(0,212,170,0.08)",
        yaxis="y1",
        hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: R$%{y:,.0f}<extra></extra>",
    ))

    # Forecast dashed line
    fig_fc.add_trace(go.Scatter(
        x=bridge_fc["month"],
        y=bridge_fc["forecast_revenue"],
        name="Forecast",
        mode="lines+markers",
        line=dict(color=AMBER, width=2.5, dash="dash"),
        marker=dict(color=AMBER, size=6),
        yaxis="y1",
        hovertemplate="<b>%{x|%b %Y}</b><br>Forecast: R$%{y:,.0f}<extra></extra>",
    ))

    # Vertical boundary line
    fig_fc.add_vline(
        x=str(fc_start_dt)[:10],
        line=dict(color=AMBER, width=1.5, dash="dot"),
    )

    # Forecast region shading
    fc_end_dt = forecast["month"].iloc[-1]
    fig_fc.add_vrect(
        x0=str(fc_start_dt)[:10], x1=str(fc_end_dt)[:10],
        fillcolor="rgba(245,158,11,0.06)", layer="below", line_width=0,
        annotation_text="← FORECAST",
        annotation_position="top left",
        annotation=dict(font=dict(color=AMBER, size=10, family="IBM Plex Mono")),
    )

    fig_fc.update_layout(
        yaxis=dict(
            title="Revenue (R$)", showgrid=True, gridcolor=BORD,
            color=TXT2, tickprefix="R$", tickformat=",.0f",
        ),
        yaxis2=dict(
            title="Order Volume", overlaying="y", side="right",
            showgrid=False, color=MUTED,
            tickformat=",", range=[0, actual_valid["orders"].max() * 4],
        ),
        xaxis=dict(showgrid=False, color=TXT2, tickformat="%b %Y", tickangle=-30),
        legend=dict(orientation="h", y=-0.18, font=dict(color=TXT, size=11)),
        height=400,
    )
    chart_base(fig_fc)
    st.plotly_chart(fig_fc, use_container_width=True, config={"displayModeBar": False})

    # ── Model comparison table ───────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    sec("MODEL COMPARISON — HOLDOUT EVALUATION")

    model_rows = ""
    for _, row in models.iterrows():
        is_naive = row["model"] == "Naive"
        is_ets   = str(row["model"]).startswith("ETS")
        row_cls  = "naive-row" if is_naive else ("ets-row" if is_ets else "")
        mae_str  = f"R${float(row['MAE']):,.0f}" if pd.notna(row["MAE"]) else "—"
        mape_str = f"{float(row['MAPE']):.2%}"   if pd.notna(row["MAPE"]) else "—"
        conv_ok  = str(row["convergence_warning"]) == "False"
        conv_str = "✓ PASS" if conv_ok else "⚠ FAIL"
        conv_col = TEAL if conv_ok else "#EF444488"
        sel_str  = " ← SELECTED" if is_naive else ""
        warn_str = " ⚠ convergence failure" if is_ets else ""
        model_rows += f"""
        <tr class="{row_cls}">
          <td><b>{row['model']}</b>{sel_str}{warn_str}</td>
          <td style="text-align:right;">{mae_str}</td>
          <td style="text-align:right;">{mape_str}</td>
          <td style="text-align:center; color:{conv_col};">{conv_str}</td>
        </tr>"""

    st.markdown(
        f"""
        <div style="border:1px solid {BORD}; border-radius:8px; overflow:hidden;">
        <table class="model-table">
          <thead>
            <tr>
              <th>Model</th>
              <th style="text-align:right;">MAE</th>
              <th style="text-align:right;">MAPE</th>
              <th style="text-align:center;">Convergence</th>
            </tr>
          </thead>
          <tbody>{model_rows}</tbody>
        </table>
        </div>""",
        unsafe_allow_html=True,
    )

    # ── Callout ──────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="callout">
          <div class="callout-lbl">▶ FORECAST INSIGHT</div>
          FORECAST MODEL: Naive selected — ETS convergence failure on ~20-point training set.<br>
          Flat projection of <b>R$985,414/month</b> for Sep–Nov 2018. Horizon: 3 months.<br>
          Holdout MAPE: <b>11.97%</b> (MAE R$120,367) on Jun–Aug 2018 validation window.<br>
          Recommended next step: ARIMA or Prophet with extended dataset for seasonal modelling.
        </div>""",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CUSTOMER EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    # ── Filter panel ─────────────────────────────────────────────────────────
    sec("FILTERS")
    f1, f2, f3 = st.columns([2, 2, 2])

    with f1:
        seg_filter = st.multiselect(
            "Segment",
            options=SEG_ORDER,
            default=SEG_ORDER,
            key="seg_filter",
        )
    with f2:
        rec_min, rec_max = st.slider(
            "Recency (days)",
            min_value=0, max_value=500,
            value=(0, 500), step=10,
            key="rec_filter",
        )
    with f3:
        mon_min, mon_max = st.slider(
            "Monetary (R$)",
            min_value=0, max_value=5000,
            value=(0, 5000), step=50,
            key="mon_filter",
        )

    # Apply filters
    filtered = rfm[rfm["segment"].isin(seg_filter)]
    filtered = filtered[
        (filtered["recency_days"] >= rec_min) &
        (filtered["recency_days"] <= rec_max)
    ]
    # When max is 5000, don't hard-cap (show all above 5000 too)
    if mon_max < 5000:
        filtered = filtered[filtered["monetary"] <= mon_max]
    filtered = filtered[filtered["monetary"] >= mon_min]

    n_shown   = len(filtered)
    rev_shown = filtered["monetary"].sum()
    pct_base  = n_shown / total_cust * 100

    # Summary bar
    st.markdown(
        f'<div class="summary-bar">'
        f'Showing <b style="color:{TEAL}">{n_shown:,}</b> customers · '
        f'<b style="color:{TEAL}">{fmt_m(rev_shown)}</b> total revenue · '
        f'<b style="color:{TXT2}">{pct_base:.1f}%</b> of total base'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Paginated table ──────────────────────────────────────────────────────
    PAGE_SIZE = 25

    if "page" not in st.session_state:
        st.session_state.page = 0

    # Reset page when filters change
    filter_key = (tuple(seg_filter), rec_min, rec_max, mon_min, mon_max)
    if st.session_state.get("_last_filter") != filter_key:
        st.session_state.page = 0
        st.session_state["_last_filter"] = filter_key

    total_pages = max(1, (n_shown - 1) // PAGE_SIZE + 1)
    page        = min(st.session_state.page, total_pages - 1)

    page_df = filtered.iloc[page * PAGE_SIZE : (page + 1) * PAGE_SIZE].copy()

    # Format display columns
    display_df = pd.DataFrame({
        "Customer ID":     page_df["customer_unique_id"].str[:12] + "…",
        "Recency (d)":     page_df["recency_days"],
        "Frequency":       page_df["frequency"],
        "Monetary (R$)":   page_df["monetary"].map(lambda x: f"R${x:,.2f}"),
        "RFM Code":        page_df["RFM_score"].astype(str),
        "Segment":         page_df["segment"],
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        height=min(650, 35 + len(display_df) * 35),
        hide_index=True,
        column_config={
            "Customer ID":   st.column_config.TextColumn("Customer ID", width="medium"),
            "Recency (d)":   st.column_config.NumberColumn("Recency (d)", format="%d"),
            "Frequency":     st.column_config.NumberColumn("Freq", format="%d"),
            "Monetary (R$)": st.column_config.TextColumn("Monetary", width="small"),
            "RFM Code":      st.column_config.TextColumn("RFM", width="small"),
            "Segment":       st.column_config.TextColumn("Segment", width="medium"),
        },
    )

    # Pagination controls
    pg_left, pg_mid, pg_right = st.columns([1, 2, 1])
    with pg_left:
        if st.button("← Prev", disabled=(page == 0), key="prev_btn"):
            st.session_state.page = max(0, page - 1)
            st.rerun()
    with pg_mid:
        start_row = page * PAGE_SIZE + 1
        end_row   = min((page + 1) * PAGE_SIZE, n_shown)
        st.markdown(
            f'<div class="page-info">Rows {start_row}–{end_row} of {n_shown:,} '
            f'· Page {page + 1} of {total_pages}</div>',
            unsafe_allow_html=True,
        )
    with pg_right:
        if st.button("Next →", disabled=(page >= total_pages - 1), key="next_btn"):
            st.session_state.page = min(total_pages - 1, page + 1)
            st.rerun()

    # Download button
    st.markdown("<br>", unsafe_allow_html=True)
    dl_col, _ = st.columns([2, 5])
    with dl_col:
        csv_data = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇  Download Filtered Data (.csv)",
            data=csv_data,
            file_name="rfm_filtered_customers.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ── RFM Score Heatmap ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    sec("AVG SPEND BY RFM SCORE COMBINATION")

    # Aggregate from FULL dataset (not filtered) for stable heatmap
    hmap_data = (
        rfm.groupby(["R_score", "F_score"])["monetary"]
        .mean()
        .reset_index()
        .rename(columns={"monetary": "avg_monetary"})
    )
    # Pivot: rows=F_score (5→1), cols=R_score (1→5)
    pivot = hmap_data.pivot(index="F_score", columns="R_score", values="avg_monetary")
    pivot = pivot.sort_index(ascending=False)   # F=5 on top
    pivot = pivot.reindex(columns=sorted(pivot.columns))  # R=1..5

    z      = pivot.values
    x_labs = [f"R={c}" for c in pivot.columns]
    y_labs = [f"F={r}" for r in pivot.index]

    text_vals = [[f"R${v:,.0f}" if not np.isnan(v) else "" for v in row] for row in z]

    fig_hmap = go.Figure(go.Heatmap(
        z=z,
        x=x_labs,
        y=y_labs,
        text=text_vals,
        texttemplate="%{text}",
        textfont=dict(size=11, family="IBM Plex Mono, monospace", color=TXT),
        colorscale=[[0, BG], [0.5, "#003D6B"], [1, TEAL]],
        showscale=True,
        colorbar=dict(
            tickfont=dict(color=TXT2, size=10, family="IBM Plex Mono"),
            tickprefix="R$",
            tickformat=",.0f",
        ),
        hovertemplate="R_score=%{x}<br>F_score=%{y}<br>Avg Spend=%{z:,.2f}<extra></extra>",
    ))
    fig_hmap.update_xaxes(showgrid=False, color=TXT2, side="bottom")
    fig_hmap.update_yaxes(showgrid=False, color=TXT2)
    chart_base(fig_hmap, title="Avg Spend by RFM Score Combination")
    fig_hmap.update_layout(height=380, margin=dict(l=60, r=60, t=50, b=50))
    st.plotly_chart(fig_hmap, use_container_width=True, config={"displayModeBar": False})
