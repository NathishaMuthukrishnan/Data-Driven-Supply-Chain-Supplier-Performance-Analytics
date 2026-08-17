# ================================================================
# SUPPLY CHAIN ANALYTICS — Charts Module (Plotly)
# ================================================================

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import data as D

# ── Common theme ─────────────────────────────────────────────────
LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, Segoe UI, sans-serif', color='#8b949e', size=12),
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        borderwidth=0,
        font=dict(size=11, color='#8b949e'),
        orientation='h',
        yanchor='bottom', y=1.02,
        xanchor='left',   x=0,
    ),
    hoverlabel=dict(
        bgcolor='#1c2128',
        bordercolor='#30363d',
        font=dict(color='#e6edf3', size=12),
    ),
)

AXIS = dict(
    showgrid=True,
    gridcolor='rgba(255,255,255,0.05)',
    linecolor='rgba(255,255,255,0.1)',
    tickcolor='rgba(0,0,0,0)',
    color='#8b949e',
    zeroline=False,
)

C = dict(
    green='#1D9E75', blue='#185FA5', amber='#BA7517',
    red='#E24B4A', purple='#7F77DD', teal='#5DCAA5',
    green_a='rgba(29,158,117,0.15)', blue_a='rgba(24,95,165,0.15)',
    amber_a='rgba(186,117,23,0.15)', red_a='rgba(226,75,74,0.15)',
    green_fill='rgba(29,158,117,0.08)', blue_fill='rgba(24,95,165,0.08)',
)

def _fig(**kwargs):
    fig = go.Figure(**kwargs)
    fig.update_layout(**LAYOUT)
    fig.update_xaxes(**AXIS)
    fig.update_yaxes(**AXIS)
    return fig

# ── 1. OTD & POR Trend ────────────────────────────────────────
def chart_otd():
    fig = _fig()
    fig.add_trace(go.Scatter(
        x=D.MONTHS, y=D.OTD_2024, name='OTD 2024',
        line=dict(color=C['green'], width=2.5),
        fill='tozeroy', fillcolor=C['green_fill'],
        mode='lines+markers', marker=dict(size=5, color=C['green']),
    ))
    fig.add_trace(go.Scatter(
        x=D.MONTHS, y=D.OTD_2023, name='OTD 2023',
        line=dict(color='#4dcfa8', width=1.5, dash='dot'),
        mode='lines+markers', marker=dict(size=3, color='#4dcfa8'),
    ))
    fig.add_trace(go.Scatter(
        x=D.MONTHS, y=D.POR_2024, name='POR 2024',
        line=dict(color=C['blue'], width=2.5),
        mode='lines+markers', marker=dict(size=5, color=C['blue']),
    ))
    fig.add_trace(go.Scatter(
        x=D.MONTHS, y=D.POR_2023, name='POR 2023',
        line=dict(color='#6bb3f5', width=1.5, dash='dot'),
        mode='lines+markers', marker=dict(size=3, color='#6bb3f5'),
    ))
    fig.update_yaxes(range=[82, 97], ticksuffix='%')
    fig.update_layout(hovermode='x unified', height=250)
    return fig

# ── 2. Cost Donut ────────────────────────────────────────────
def chart_cost_donut():
    fig = go.Figure(go.Pie(
        labels=D.COST_LABELS, values=D.COST_VALUES,
        marker=dict(colors=D.COST_COLORS, line=dict(width=0)),
        hole=0.65,
        textinfo='label+percent',
        textfont=dict(size=11, color='#8b949e'),
        hovertemplate='%{label}: %{value}% of revenue<extra></extra>',
    ))
    fig.update_layout(**LAYOUT, height=230,
        annotations=[dict(text='9.4%<br><span style="font-size:10px">of revenue</span>',
                          x=0.5, y=0.5, font=dict(size=14, color='#e6edf3'), showarrow=False)])
    return fig

# ── 3. Inventory Turnover Bar ────────────────────────────────
def chart_inv_turnover():
    fig = _fig()
    fig.add_trace(go.Bar(
        x=D.INV_CATEGORIES, y=D.INV_ACTUAL, name='Actual 2024',
        marker=dict(color=C['blue'], line=dict(width=0)),
    ))
    fig.add_trace(go.Bar(
        x=D.INV_CATEGORIES, y=D.INV_BENCHMARK, name='Benchmark',
        marker=dict(color=C['blue_a'], line=dict(color=C['blue'], width=1)),
    ))
    fig.update_layout(barmode='group', height=230, bargap=0.25)
    fig.update_yaxes(ticksuffix='×')
    return fig

# ── 4. Forecast Accuracy ─────────────────────────────────────
def chart_forecast():
    fig = _fig()
    fig.add_trace(go.Scatter(
        x=D.MONTHS, y=D.FORECAST_2024, name='2024',
        line=dict(color=C['green'], width=2.5),
        fill='tozeroy', fillcolor=C['green_fill'],
        mode='lines+markers', marker=dict(size=4),
    ))
    fig.add_trace(go.Scatter(
        x=D.MONTHS, y=D.FORECAST_2023, name='2023',
        line=dict(color=C['amber'], width=1.5, dash='dot'),
        mode='lines', opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=D.MONTHS, y=[85]*12, name='85% Target',
        line=dict(color=C['red'], width=1.2, dash='dash'),
        mode='lines', opacity=0.5,
    ))
    fig.update_yaxes(range=[70, 90], ticksuffix='%')
    fig.update_layout(hovermode='x unified', height=220)
    return fig

# ── 5. Supplier Rating Distribution ─────────────────────────
def chart_supplier_rating():
    fig = _fig()
    fig.add_trace(go.Bar(
        y=D.RATING_LABELS, x=D.RATING_COUNTS, orientation='h',
        marker=dict(color=D.RATING_COLORS, line=dict(width=0)),
        text=D.RATING_COUNTS, textposition='outside',
        textfont=dict(color='#8b949e', size=11),
    ))
    fig.update_layout(height=220, margin=dict(l=10,r=50,t=10,b=10))
    return fig

# ── 6. Lead Time vs Defect Rate Scatter ─────────────────────
def chart_scatter():
    color_map = {'A': C['green'], 'B': C['blue'], 'C': C['red']}
    colors = [color_map.get(r, C['amber']) for r in D.df_suppliers['Rating']]
    sizes  = [max(10, s * 1.4) for s in D.df_suppliers['Spend_M']]
    fig = _fig()
    for rating, color in color_map.items():
        mask = D.df_suppliers['Rating'] == rating
        sub  = D.df_suppliers[mask]
        fig.add_trace(go.Scatter(
            x=sub['Lead_Days'], y=sub['Defect_Pct'],
            mode='markers', name=f'Rating {rating}',
            marker=dict(
                size=[max(10, s * 1.4) for s in sub['Spend_M']],
                color=color, opacity=0.6,
                line=dict(color=color, width=1.5),
            ),
            customdata=sub[['Supplier','Spend_M']].values,
            hovertemplate='<b>%{customdata[0]}</b><br>Lead: %{x}d | Defect: %{y}%<br>Spend: $%{customdata[1]}M<extra></extra>',
        ))
    fig.update_xaxes(title_text='Lead Time (days)', range=[0, 25])
    fig.update_yaxes(title_text='Defect Rate (%)', range=[0, 4])
    fig.update_layout(height=250)
    return fig

# ── 7. Inventory Trend ────────────────────────────────────
def chart_inv_trend():
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(
        x=D.MONTHS, y=D.INV_VALUE_2024, name='Inventory ($M)',
        marker=dict(color=C['blue_a'], line=dict(color=C['blue'], width=1)),
    ), secondary_y=False)
    fig.add_trace(go.Bar(
        x=D.MONTHS, y=D.STOCKOUT_EVENTS, name='Stockout Events',
        marker=dict(color='rgba(226,75,74,0.7)', line=dict(width=0)),
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=D.MONTHS, y=D.SALES_VELOCITY, name='Sales Velocity',
        line=dict(color=C['green'], width=2.5),
        mode='lines+markers', marker=dict(size=5),
    ), secondary_y=True)
    fig.update_layout(**LAYOUT, hovermode='x unified', height=250,
        barmode='overlay',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0,
                    font=dict(size=11, color='#8b949e'), bgcolor='rgba(0,0,0,0)'),
    )
    fig.update_xaxes(**AXIS)
    fig.update_yaxes(**AXIS, title_text='Inventory Value ($M)', secondary_y=False)
    fig.update_yaxes(**AXIS, title_text='Velocity / Events', secondary_y=True)
    return fig

# ── 8. Cash-to-Cash ──────────────────────────────────────────
def chart_c2c():
    fig = _fig()
    fig.add_trace(go.Bar(
        x=D.C2C_COMPONENTS, y=D.C2C_2024, name='2024',
        marker=dict(color=C['blue'], line=dict(width=0)),
        text=D.C2C_2024, textposition='outside',
        textfont=dict(color='#8b949e', size=11),
    ))
    fig.add_trace(go.Bar(
        x=D.C2C_COMPONENTS, y=D.C2C_2023, name='2023',
        marker=dict(color=C['blue_a'], line=dict(color=C['blue'], width=1)),
        text=D.C2C_2023, textposition='outside',
        textfont=dict(color='#8b949e', size=11),
    ))
    fig.update_layout(barmode='group', height=240, bargap=0.25)
    fig.update_yaxes(ticksuffix='d')
    return fig

# ── 9. Freight Cost ──────────────────────────────────────────
def chart_freight():
    bar_colors = [C['red'] if v >= 4 else C['amber'] if v >= 3 else C['green']
                  for v in D.FREIGHT_COSTS]
    fig = _fig()
    fig.add_trace(go.Bar(
        y=D.FREIGHT_LANES, x=D.FREIGHT_COSTS, orientation='h',
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[f'${v}' for v in D.FREIGHT_COSTS],
        textposition='outside', textfont=dict(color='#8b949e', size=11),
    ))
    fig.update_xaxes(tickprefix='$')
    fig.update_layout(height=260, margin=dict(l=10,r=50,t=10,b=10))
    return fig

# ── 10. Geographic Concentration Pie ─────────────────────────
def chart_geo():
    fig = go.Figure(go.Pie(
        labels=D.GEO_LABELS, values=D.GEO_VALUES,
        marker=dict(colors=D.GEO_COLORS, line=dict(width=0)),
        textinfo='label+percent',
        textfont=dict(size=11, color='#e6edf3'),
        hovertemplate='%{label}: %{value}% of spend<extra></extra>',
    ))
    fig.update_layout(**LAYOUT, height=240)
    return fig

# ── 11. Resilience Score ─────────────────────────────────────
def chart_resilience():
    fig = _fig()
    fig.add_trace(go.Scatter(
        x=D.QUARTERS, y=D.RESILIENCE_SCORES, name='Resilience Score',
        line=dict(color=C['purple'], width=2.5),
        fill='tozeroy', fillcolor='rgba(127,119,221,0.08)',
        mode='lines+markers',
        marker=dict(size=8, color=C['purple'],
                    line=dict(color='#0d1117', width=2)),
        text=D.RESILIENCE_SCORES, textposition='top center',
        textfont=dict(color=C['purple'], size=11),
    ))
    fig.update_yaxes(range=[50, 85])
    fig.update_layout(height=240, showlegend=False)
    return fig
