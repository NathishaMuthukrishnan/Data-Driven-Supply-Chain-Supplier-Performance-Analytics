# ================================================================
# SUPPLY CHAIN ANALYTICS DASHBOARD
# Data-Driven Optimization of Supply Chain Operations
# and Supplier Performance Analysis
#
# Run:  python app.py
# Open: http://localhost:8050
# ================================================================

import dash
from dash import dcc, html, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

import data as D
import charts as CH

# ── App init ─────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap',
    ],
    suppress_callback_exceptions=True,
    title='Supply Chain Analytics Dashboard',
)
server = app.server

# ── Colour helpers ────────────────────────────────────────────────
DELTA_COLORS = {'up': '#1D9E75', 'down': '#E24B4A', 'neutral': '#BA7517'}

BADGE_STYLE = {
    'A':        {'background':'rgba(29,158,117,.15)',  'color':'#4dcfa8'},
    'B':        {'background':'rgba(24,95,165,.15)',   'color':'#6bb3f5'},
    'C':        {'background':'rgba(186,117,23,.15)',  'color':'#f0b042'},
    'D':        {'background':'rgba(226,75,74,.15)',   'color':'#f07575'},
    'Low':      {'background':'rgba(29,158,117,.15)',  'color':'#4dcfa8'},
    'Medium':   {'background':'rgba(186,117,23,.15)',  'color':'#f0b042'},
    'High':     {'background':'rgba(226,75,74,.15)',   'color':'#f07575'},
    'Critical': {'background':'rgba(226,75,74,.35)',   'color':'#f07575'},
    'Completed':{'background':'rgba(29,158,117,.15)',  'color':'#4dcfa8'},
    'In Progress':{'background':'rgba(24,95,165,.15)', 'color':'#6bb3f5'},
    'Planned':  {'background':'rgba(186,117,23,.15)',  'color':'#f0b042'},
}

def badge(text, extra_style=None):
    style = {**BADGE_STYLE.get(text, {'background':'rgba(255,255,255,.05)','color':'#8b949e'}),
             'padding':'3px 10px','borderRadius':'4px','fontSize':'11px',
             'fontWeight':'600','display':'inline-block'}
    if extra_style:
        style.update(extra_style)
    return html.Span(text, style=style)

# ── KPI Card ─────────────────────────────────────────────────────
def kpi_card(key):
    k = D.KPIS[key]
    color = DELTA_COLORS[k['delta_dir']]
    arrow = '▲ ' if k['delta_dir'] == 'up' else ('▼ ' if k['delta_dir'] == 'down' else '– ')
    val = f"{k['unit']}{k['value']}" if k['unit'] == '$' else f"{k['value']}{k['unit']}"
    return html.Div([
        html.Div(style={'height':'2px','background':color,'borderRadius':'2px 2px 0 0','margin':'-1px -1px 0'}),
        html.Div([
            html.Div(k['label'].upper(), style={'fontSize':'10px','fontWeight':'600','letterSpacing':'.06em','color':'#8b949e','marginBottom':'8px'}),
            html.Div(val, style={'fontSize':'26px','fontWeight':'700','color':'#e6edf3','lineHeight':'1','fontVariantNumeric':'tabular-nums'}),
            html.Div([
                html.Span(arrow + k['delta'], style={'color': color, 'fontSize':'11px'}),
                html.Span(' ' + k['note'], style={'color':'#484f58','fontSize':'11px'}),
            ], style={'marginTop':'6px'}),
        ], style={'padding':'14px 16px'}),
    ], style={
        'background':'#161b22', 'borderRadius':'10px',
        'border':'1px solid rgba(48,54,61,0.8)',
        'overflow':'hidden', 'transition':'border-color .2s',
    })

# ── Chart card wrapper ────────────────────────────────────────────
def chart_card(title, subtitle, content, height_class=''):
    return html.Div([
        html.Div([
            html.Div(title, style={'fontSize':'14px','fontWeight':'600','color':'#e6edf3','marginBottom':'3px'}),
            html.Div(subtitle, style={'fontSize':'12px','color':'#8b949e'}),
        ], style={'marginBottom':'14px'}),
        content,
    ], style={
        'background':'#161b22','borderRadius':'14px',
        'border':'1px solid rgba(48,54,61,0.8)','padding':'20px',
    })

def dcc_graph(fig_fn, graph_id):
    return dcc.Graph(
        id=graph_id,
        figure=fig_fn(),
        config={'displayModeBar': False},
        style={'width':'100%'},
    )

# ─────────────────────────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────────────────────────

def page_overview():
    kpi_keys = ['otd','por','inv_turnover','c2c','forecast_acc','sc_cost']
    return html.Div([
        # KPI Row
        html.Div([kpi_card(k) for k in kpi_keys],
            style={'display':'grid','gridTemplateColumns':'repeat(auto-fill, minmax(160px, 1fr))','gap':'14px','marginBottom':'24px'}),
        # OTD Full width
        chart_card('On-time delivery & perfect order rate — 2023 vs 2024',
                   'Monthly tracking of fulfilment reliability across both measurement years',
                   dcc_graph(CH.chart_otd, 'graph-otd')),
        html.Div(style={'height':'16px'}),
        # Cost + Inv Turnover
        html.Div([
            chart_card('Supply chain cost breakdown','% of total revenue, FY 2024',
                       dcc_graph(CH.chart_cost_donut, 'graph-cost')),
            chart_card('Inventory turnover by category','FY 2024 actual vs industry benchmark',
                       dcc_graph(CH.chart_inv_turnover, 'graph-inv-turn')),
        ], style={'display':'grid','gridTemplateColumns':'1fr 1fr','gap':'16px','marginTop':'0'}),
        html.Div(style={'height':'16px'}),
        # Forecast
        chart_card('Demand forecast accuracy trend','Monthly % accuracy vs 85% target — 2023 vs 2024',
                   dcc_graph(CH.chart_forecast, 'graph-forecast')),
    ])


def page_suppliers():
    kpi_keys = ['active_suppliers','otd','avg_lead','defect_rate']
    return html.Div([
        html.Div([kpi_card(k) for k in kpi_keys],
            style={'display':'grid','gridTemplateColumns':'repeat(auto-fill, minmax(160px, 1fr))','gap':'14px','marginBottom':'24px'}),
        html.Div([
            chart_card('Supplier rating distribution','Count by composite performance grade — FY 2024',
                       dcc_graph(CH.chart_supplier_rating, 'graph-rating')),
            chart_card('Lead time vs defect rate','Bubble = annual spend · Colour = rating',
                       dcc_graph(CH.chart_scatter, 'graph-scatter')),
        ], style={'display':'grid','gridTemplateColumns':'1fr 1fr','gap':'16px','marginBottom':'24px'}),
        # Supplier Table Card
        html.Div([
            html.Div([
                html.Div([
                    html.Div('Supplier performance register', style={'fontSize':'14px','fontWeight':'600','color':'#e6edf3','marginBottom':'3px'}),
                    html.Div('Click column headers to sort · Use filters to narrow results', style={'fontSize':'12px','color':'#8b949e'}),
                ]),
                html.Button('⬇ Export CSV', id='btn-export-csv',
                    style={'fontSize':'12px','padding':'6px 14px',
                           'background':'rgba(29,158,117,.1)','border':'1px solid rgba(29,158,117,.3)',
                           'color':'#1D9E75','borderRadius':'6px','cursor':'pointer'}),
            ], style={'display':'flex','justifyContent':'space-between','alignItems':'center','marginBottom':'14px','flexWrap':'wrap','gap':'10px'}),
            # Filters
            html.Div([
                dcc.Input(id='filter-search', type='text', placeholder='🔍 Search supplier or region…',
                    style={'flex':'1','minWidth':'180px','background':'#1c2128','border':'1px solid rgba(48,54,61,0.8)',
                           'borderRadius':'6px','color':'#e6edf3','fontSize':'13px','padding':'7px 12px',
                           'fontFamily':'Inter, sans-serif','outline':'none'}),
                dcc.Dropdown(id='filter-rating', placeholder='All Ratings',
                    options=[{'label':'A — Excellent','value':'A'},{'label':'B — Good','value':'B'},
                             {'label':'C — Needs improvement','value':'C'}],
                    clearable=True, style={'minWidth':'160px'},
                    className='dash-dropdown-dark'),
                dcc.Dropdown(id='filter-risk', placeholder='All Risk Levels',
                    options=[{'label':'Low Risk','value':'Low'},{'label':'Medium Risk','value':'Medium'},
                             {'label':'High Risk','value':'High'}],
                    clearable=True, style={'minWidth':'160px'},
                    className='dash-dropdown-dark'),
                html.Span(id='supplier-count', style={'fontSize':'12px','color':'#8b949e'}),
            ], style={'display':'flex','gap':'10px','marginBottom':'16px','flexWrap':'wrap','alignItems':'center'}),
            # Table
            html.Div(id='supplier-table-container'),
            dcc.Download(id='download-csv'),
        ], style={'background':'#161b22','borderRadius':'14px','border':'1px solid rgba(48,54,61,0.8)','padding':'20px'}),
    ])


def page_inventory():
    kpi_keys = ['dio','stockout_rate','gmroi','c2c']
    return html.Div([
        html.Div([kpi_card(k) for k in kpi_keys],
            style={'display':'grid','gridTemplateColumns':'repeat(auto-fill, minmax(160px, 1fr))','gap':'14px','marginBottom':'24px'}),
        chart_card('Inventory value vs sales velocity — 2024',
                   'Identifying overstocking and demand-driven stockout windows',
                   dcc_graph(CH.chart_inv_trend, 'graph-inv-trend')),
        html.Div(style={'height':'16px'}),
        html.Div([
            chart_card('Cash-to-cash cycle breakdown','DIO + DSO − DPO comparison: 2023 vs 2024',
                       dcc_graph(CH.chart_c2c, 'graph-c2c')),
            chart_card('Freight cost per unit by lane','Top 8 shipping corridors — FY 2024 (USD)',
                       dcc_graph(CH.chart_freight, 'graph-freight')),
        ], style={'display':'grid','gridTemplateColumns':'1fr 1fr','gap':'16px','marginBottom':'24px'}),
        # ABC-XYZ Table
        html.Div([
            html.Div('ABC-XYZ inventory classification', style={'fontSize':'14px','fontWeight':'600','color':'#e6edf3','marginBottom':'4px'}),
            html.Div('Segmentation by revenue contribution and demand variability', style={'fontSize':'12px','color':'#8b949e','marginBottom':'16px'}),
            _abc_table(),
        ], style={'background':'#161b22','borderRadius':'14px','border':'1px solid rgba(48,54,61,0.8)','padding':'20px'}),
    ])


def _abc_table():
    rows = []
    risk_color = {'Low':'#4dcfa8','Medium':'#f0b042','High':'#f07575','Variable':'#a9a3f0'}
    for _, r in D.df_abc.iterrows():
        rows.append(html.Tr([
            html.Td(html.Strong(r['Class']), style={'padding':'10px 12px','color':'#e6edf3','borderBottom':'1px solid rgba(48,54,61,0.4)'}),
            html.Td(r['SKUs'], style={'padding':'10px 12px','color':'#e6edf3','borderBottom':'1px solid rgba(48,54,61,0.4)'}),
            html.Td(f"{r['Revenue_Pct']}%", style={'padding':'10px 12px','color':'#e6edf3','borderBottom':'1px solid rgba(48,54,61,0.4)'}),
            html.Td(f"{r['Avg_Turnover']}×", style={'padding':'10px 12px','color':'#e6edf3','borderBottom':'1px solid rgba(48,54,61,0.4)'}),
            html.Td(f"{r['Holding_Cost_Pct']}%", style={'padding':'10px 12px','color':'#e6edf3','borderBottom':'1px solid rgba(48,54,61,0.4)'}),
            html.Td(badge(r['Stockout_Risk']), style={'padding':'10px 12px','borderBottom':'1px solid rgba(48,54,61,0.4)'}),
            html.Td(r['Strategy'], style={'padding':'10px 12px','color':'#8b949e','fontSize':'12px','borderBottom':'1px solid rgba(48,54,61,0.4)'}),
        ]))
    return html.Table([
        html.Thead(html.Tr([
            html.Th(h, style={'padding':'10px 12px','fontSize':'11px','fontWeight':'600',
                              'textTransform':'uppercase','letterSpacing':'.05em','color':'#8b949e',
                              'borderBottom':'1px solid rgba(48,54,61,0.8)'})
            for h in ['Class','SKUs','Revenue %','Avg Turnover','Holding Cost','Stockout Risk','Strategy']
        ])),
        html.Tbody(rows),
    ], style={'width':'100%','borderCollapse':'collapse','fontSize':'13px'})


def page_risk():
    kpi_keys = ['resilience','esg','active_suppliers','forecast_acc']
    # Risk Matrix
    matrix_cells = [
        # row: High likelihood
        [('Medium',  'Forecast accuracy gap'),
         ('High',    'ESG compliance\nCurrency volatility'),
         ('Critical','Single-source dependency\nRed Sea disruption')],
        # row: Medium likelihood
        [('Low',   'ERP data quality'),
         ('Medium','Tier-2/3 visibility gap'),
         ('High',  'Semiconductor shortage')],
        # row: Low likelihood
        [('Low', 'Domestic disruption'),
         ('Low', 'Port congestion'),
         ('Medium','Warehouse capacity')],
    ]
    likelihood_labels = ['High likelihood','Medium likelihood','Low likelihood']
    impact_labels = ['Low impact','Medium impact','High impact']
    level_bg = {'Low':'rgba(29,158,117,.12)','Medium':'rgba(186,117,23,.12)',
                'High':'rgba(226,75,74,.15)','Critical':'rgba(226,75,74,.35)'}
    level_color = {'Low':'#4dcfa8','Medium':'#f0b042','High':'#f07575','Critical':'#f07575'}

    matrix_rows = []
    header_row = [html.Th('', style={'width':'120px','padding':'8px'})]
    for lbl in impact_labels:
        header_row.append(html.Th(lbl, style={'padding':'8px 12px','fontSize':'11px',
            'fontWeight':'600','color':'#8b949e','textAlign':'center','width':'33%'}))
    matrix_rows.append(html.Tr(header_row))

    for i, (row_data, lh) in enumerate(zip(matrix_cells, likelihood_labels)):
        cells = [html.Td(lh, style={'fontSize':'11px','fontWeight':'600','color':'#8b949e',
                                    'padding':'8px','verticalAlign':'middle'})]
        for level, text in row_data:
            cells.append(html.Td(
                [html.Div(t, style={'fontSize':'11px','lineHeight':'1.5'}) for t in text.split('\n')],
                style={'background':level_bg[level],'color':level_color[level],'padding':'10px 12px',
                       'borderRadius':'6px','textAlign':'center','fontWeight':'500','margin':'2px',
                       'fontSize':'11px','verticalAlign':'middle'}
            ))
        matrix_rows.append(html.Tr(cells, style={'gap':'4px'}))

    # Risk register rows
    risk_rows = []
    level_border = {'Critical':'#E24B4A','High':'#BA7517','Medium':'#185FA5','Low':'#1D9E75'}
    for _, r in D.df_risks.iterrows():
        risk_rows.append(html.Div([
            html.Div([
                html.Div(r['ID'], style={'fontSize':'11px','fontWeight':'700','color':'#484f58','fontFamily':'monospace'}),
                html.Div(badge(r['Level']), style={'marginTop':'6px'}),
            ], style={'minWidth':'70px'}),
            html.Div([
                html.Div(r['Description'], style={'fontSize':'13px','fontWeight':'600','color':'#e6edf3','marginBottom':'4px'}),
                html.Div(f"Category: {r['Category']} · Likelihood: {r['Likelihood']} · Impact: {r['Impact']}",
                         style={'fontSize':'12px','color':'#8b949e','marginBottom':'6px'}),
                html.Div([html.Strong('Mitigation: ', style={'color':'#1D9E75'}), r['Mitigation']],
                         style={'fontSize':'11px','color':'#484f58'}),
            ]),
        ], style={
            'display':'flex','gap':'14px','alignItems':'flex-start',
            'background':'#1c2128','borderRadius':'10px','padding':'14px 16px',
            'marginBottom':'10px','borderLeft':f"3px solid {level_border.get(r['Level'],'#485f58')}",
        }))

    return html.Div([
        html.Div([kpi_card(k) for k in kpi_keys],
            style={'display':'grid','gridTemplateColumns':'repeat(auto-fill, minmax(160px, 1fr))','gap':'14px','marginBottom':'24px'}),
        # Matrix
        html.Div([
            html.Div('Risk likelihood × impact matrix', style={'fontSize':'14px','fontWeight':'600','color':'#e6edf3','marginBottom':'4px'}),
            html.Div('Classified by probability and business impact level', style={'fontSize':'12px','color':'#8b949e','marginBottom':'16px'}),
            html.Table(matrix_rows, style={'width':'100%','borderCollapse':'separate','borderSpacing':'4px'}),
        ], style={'background':'#161b22','borderRadius':'14px','border':'1px solid rgba(48,54,61,0.8)','padding':'20px','marginBottom':'24px'}),
        # Geo + Resilience
        html.Div([
            chart_card('Supplier geographic concentration','By spend % — Asia-Pacific concentration risk',
                       dcc_graph(CH.chart_geo, 'graph-geo')),
            chart_card('Resilience score — quarterly trend','Composite index (0–100): recovery + redundancy + readiness',
                       dcc_graph(CH.chart_resilience, 'graph-resilience')),
        ], style={'display':'grid','gridTemplateColumns':'1fr 1fr','gap':'16px','marginBottom':'24px'}),
        # Risk Register
        html.Div([
            html.Div('Risk register', style={'fontSize':'14px','fontWeight':'600','color':'#e6edf3','marginBottom':'4px'}),
            html.Div('9 identified risks with likelihood, impact, and mitigation strategies', style={'fontSize':'12px','color':'#8b949e','marginBottom':'16px'}),
            html.Div(risk_rows),
        ], style={'background':'#161b22','borderRadius':'14px','border':'1px solid rgba(48,54,61,0.8)','padding':'20px'}),
    ])


def page_recommendations():
    impact_color = {'High':'#1D9E75','Medium':'#185FA5','Low':'#8b949e'}
    cards = []
    for _, r in D.df_recs.iterrows():
        cards.append(html.Div([
            html.Div([
                html.Div(str(r['Priority']), style={
                    'width':'28px','height':'28px','borderRadius':'50%',
                    'background':'rgba(29,158,117,.15)','color':'#1D9E75',
                    'fontSize':'13px','fontWeight':'700','display':'flex',
                    'alignItems':'center','justifyContent':'center','flexShrink':'0',
                }),
                html.Div([
                    html.Div(r['Title'], style={'fontSize':'14px','fontWeight':'600','color':'#e6edf3'}),
                    html.Div([badge(r['Status']), badge(f"Impact: {r['Impact']}")],
                             style={'display':'flex','gap':'6px','marginTop':'6px','flexWrap':'wrap'}),
                ]),
            ], style={'display':'flex','gap':'12px','alignItems':'flex-start','marginBottom':'12px'}),
            html.Div(r['Description'], style={'fontSize':'12px','color':'#8b949e','lineHeight':'1.6','marginBottom':'10px'}),
            html.Div([
                html.Span('💡 ' + r['Saving'], style={'fontSize':'11px','fontWeight':'600','color':'#1D9E75'}),
                html.Span(f"Effort: {r['Effort']}", style={'fontSize':'11px','color':'#484f58','marginLeft':'auto'}),
            ], style={'display':'flex','alignItems':'center'}),
        ], style={
            'background':'#161b22','borderRadius':'14px',
            'border':'1px solid rgba(48,54,61,0.8)','padding':'18px',
            'display':'flex','flexDirection':'column','gap':'0',
        }))

    # Stats strip
    stats = html.Div([
        html.Div([html.Div('$7.3M', style={'fontSize':'22px','fontWeight':'700','color':'#1D9E75'}),
                  html.Div('Total identified savings', style={'fontSize':'11px','color':'#8b949e','marginTop':'2px'})]),
        html.Div([html.Div('6',  style={'fontSize':'22px','fontWeight':'700','color':'#e6edf3'}),
                  html.Div('Recommendations', style={'fontSize':'11px','color':'#8b949e','marginTop':'2px'})]),
        html.Div([html.Div('1',  style={'fontSize':'22px','fontWeight':'700','color':'#1D9E75'}),
                  html.Div('Completed', style={'fontSize':'11px','color':'#8b949e','marginTop':'2px'})]),
        html.Div([html.Div('3',  style={'fontSize':'22px','fontWeight':'700','color':'#6bb3f5'}),
                  html.Div('In Progress', style={'fontSize':'11px','color':'#8b949e','marginTop':'2px'})]),
        html.Div([html.Div('2',  style={'fontSize':'22px','fontWeight':'700','color':'#f0b042'}),
                  html.Div('Planned', style={'fontSize':'11px','color':'#8b949e','marginTop':'2px'})]),
    ], style={'display':'flex','gap':'28px','flexWrap':'wrap',
              'padding':'16px 20px','background':'#1c2128','borderRadius':'10px',
              'border':'1px solid rgba(48,54,61,0.8)','marginBottom':'24px'})

    # Roadmap table
    roadmap_data = [
        ('AI demand sensing',          '80%','100%','–','–',     'Data Science'),
        ('Dual-sourcing programme',    '20%','60%', '90%','100%','Procurement Lead'),
        ('Real-time control tower',    '50%','100%','–','–',     'Logistics Director'),
        ('ESG audit programme',        '60%','80%', '90%','100%','Sustainability'),
        ('Freight lane optimisation',  '–',  '40%', '80%','100%','Logistics Manager'),
    ]
    def pbar(pct_str):
        if pct_str == '–':
            return html.Span('–', style={'color':'#484f58'})
        pct = int(pct_str.replace('%',''))
        color = '#1D9E75' if pct >= 80 else '#185FA5' if pct >= 40 else '#BA7517'
        return html.Div([
            html.Div(style={'height':'4px','background':color,'borderRadius':'2px',
                            'width':pct_str,'transition':'width .5s'}),
        ], style={'height':'4px','background':'rgba(255,255,255,.08)','borderRadius':'2px','width':'100%','minWidth':'60px'})

    roadmap_rows = []
    for row in roadmap_data:
        roadmap_rows.append(html.Tr([
            html.Td(html.Strong(row[0]), style=td_s),
            html.Td(pbar(row[1]), style=td_s),
            html.Td(pbar(row[2]), style=td_s),
            html.Td(pbar(row[3]), style=td_s),
            html.Td(pbar(row[4]), style=td_s),
            html.Td(row[5], style={**td_s,'color':'#8b949e'}),
        ]))

    roadmap = html.Div([
        html.Div('Implementation roadmap — 2025', style={'fontSize':'14px','fontWeight':'600','color':'#e6edf3','marginBottom':'4px'}),
        html.Div('Quarterly execution timeline', style={'fontSize':'12px','color':'#8b949e','marginBottom':'16px'}),
        html.Table([
            html.Thead(html.Tr([
                html.Th(h, style={'padding':'10px 12px','fontSize':'11px','fontWeight':'600',
                                  'textTransform':'uppercase','letterSpacing':'.05em','color':'#8b949e',
                                  'borderBottom':'1px solid rgba(48,54,61,0.8)'})
                for h in ['Initiative','Q1 2025','Q2 2025','Q3 2025','Q4 2025','Owner']
            ])),
            html.Tbody(roadmap_rows),
        ], style={'width':'100%','borderCollapse':'collapse','fontSize':'13px'}),
    ], style={'background':'#161b22','borderRadius':'14px','border':'1px solid rgba(48,54,61,0.8)','padding':'20px','marginTop':'24px'})

    return html.Div([stats, html.Div(cards, style={
        'display':'grid','gridTemplateColumns':'repeat(auto-fill, minmax(280px, 1fr))',
        'gap':'14px','marginBottom':'0',
    }), roadmap])


td_s = {'padding':'10px 12px','borderBottom':'1px solid rgba(48,54,61,0.4)','color':'#e6edf3','verticalAlign':'middle'}


def page_methodology():
    def block(icon, title, content):
        return html.Div([
            html.Div([html.Span(icon, style={'fontSize':'18px','marginRight':'8px'}),
                      html.Span(title, style={'fontSize':'14px','fontWeight':'600','color':'#e6edf3'})],
                     style={'display':'flex','alignItems':'center','marginBottom':'12px'}),
            content,
        ], style={'background':'#161b22','borderRadius':'14px','border':'1px solid rgba(48,54,61,0.8)','padding':'20px','marginBottom':'16px'})

    def bullet_list(items):
        return html.Ul([
            html.Li(item, style={'fontSize':'13px','color':'#8b949e','marginBottom':'6px','paddingLeft':'8px'})
            for item in items
        ], style={'listStyle':'none','paddingLeft':'0'})

    def tag(t):
        return html.Span(t, style={'fontSize':'11px','padding':'4px 10px','border':'1px solid rgba(48,54,61,0.8)',
                                   'borderRadius':'20px','color':'#8b949e','margin':'3px','display':'inline-block'})

    layers = [
        ('#1D9E75', 'Layer 1 — Descriptive', 'KPI dashboards, trend reporting, 24-month historical benchmarking across 14 dimensions'),
        ('#185FA5', 'Layer 2 — Diagnostic',  'Root-cause analysis of stockouts, delivery failures, and cost overruns'),
        ('#BA7517', 'Layer 3 — Predictive',  'Demand forecasting via ARIMA + XGBoost ensemble; lead time and risk probability scoring'),
        ('#7F77DD', 'Layer 4 — Prescriptive','Optimisation recommendations for inventory positioning, supplier allocation, freight routing'),
    ]

    ds_cards = []
    for d in D.METHODOLOGY_SOURCES:
        ds_cards.append(html.Div([
            html.Div(d['name'], style={'fontSize':'13px','fontWeight':'500','color':'#e6edf3','marginBottom':'4px'}),
            html.Div([
                html.Span(d['type'], style={'fontSize':'10px','fontWeight':'600','textTransform':'uppercase',
                                            'color':'#1D9E75' if d['type']=='Primary' else '#185FA5'}),
                html.Span(f" · {d['records']} · {d['period']}", style={'fontSize':'11px','color':'#8b949e'}),
            ]),
        ], style={'background':'#1c2128','borderRadius':'6px','padding':'12px 14px'}))

    scoring_items = [
        ('30%','#1D9E75','On-time delivery'),
        ('25%','#185FA5','Quality (defect rate)'),
        ('20%','#BA7517','Responsiveness'),
        ('15%','#7F77DD','Cost competitiveness'),
        ('10%','#1D9E75','ESG compliance'),
    ]

    findings = [
        'AI demand sensing reduced forecast error by 12% and freed $3.2M in working capital',
        'Supplier segmentation improved average lead time by 2.1 days across preferred tier',
        'Dynamic safety stock model reduced stockout events by 38% and carrying costs by 1.4pp',
        'Red Sea route disruption added $2.3M freight cost — rerouting reduced exposure by 68%',
        '23 single-source components identified as top supply chain vulnerability by revenue impact',
        'Year-on-year OTD improvement of +3.1pp is statistically significant (paired t-test, p < 0.01)',
    ]

    return html.Div([
        block('🎯','Research objectives', bullet_list([
            'Quantify and benchmark supply chain performance against industry standards',
            'Identify root causes of delivery failures, stockouts, and elevated costs',
            'Develop a predictive model for demand forecasting and inventory positioning',
            'Score and segment suppliers by composite performance index',
            'Produce actionable recommendations to reduce cost, risk, and lead time',
        ])),
        block('📐','Analytical framework — four-layer pyramid', html.Div([
            html.Div([
                html.Div([
                    html.Div(lbl, style={'fontSize':'12px','fontWeight':'600','color':color,'marginBottom':'4px'}),
                    html.Div(desc, style={'fontSize':'12px','color':'#8b949e','lineHeight':'1.5'}),
                ], style={'background':'#1c2128','borderRadius':'6px','padding':'14px','borderLeft':f'3px solid {color}'})
            for color, lbl, desc in layers], style={'display':'grid','gridTemplateColumns':'repeat(auto-fill, minmax(200px, 1fr))','gap':'10px'}),
        ])),
        block('🗄️','Data sources', html.Div(ds_cards, style={
            'display':'grid','gridTemplateColumns':'repeat(auto-fill, minmax(220px, 1fr))','gap':'10px'})),
        block('⚖️','Supplier composite scoring model', html.Div([
            html.Div([
                html.Div(pct, style={'fontSize':'22px','fontWeight':'700','color':color}),
                html.Div(lbl, style={'fontSize':'11px','color':'#8b949e','marginTop':'2px'}),
            ], style={'background':'#1c2128','borderRadius':'6px','padding':'12px','textAlign':'center'})
        for pct, color, lbl in scoring_items], style={
            'display':'grid','gridTemplateColumns':'repeat(auto-fill, minmax(130px, 1fr))','gap':'10px'})),
        block('🛠️','Technology & tools', html.Div([tag(t) for t in [
            'Python 3.11','pandas','scikit-learn','statsmodels','Plotly','Dash',
            'SQL Server','Power BI','FourKites API','Jupyter Notebooks','Excel',
        ]])),
        block('📈','Statistical & ML methods', html.Div([tag(t) for t in [
            'ARIMA time-series forecasting','XGBoost demand sensing ensemble',
            'K-means supplier segmentation','Pearson correlation analysis',
            'Paired t-test (p<0.05)','ABC-XYZ inventory classification','Monte Carlo risk simulation',
        ]])),
        block('🔑','Key findings', bullet_list(findings)),
    ])


# ── Inject methodology sources into data module ──────────────────
D.METHODOLOGY_SOURCES = [
    {'name':'NetSuite ERP',         'type':'Primary',   'records':'2.4M transactions','period':'24 months'},
    {'name':'FourKites TMS',        'type':'Primary',   'records':'1.1M shipments',   'period':'24 months'},
    {'name':'Supplier Portal',      'type':'Primary',   'records':'847 suppliers',    'period':'Ongoing'},
    {'name':'Deloitte SC Report',   'type':'Secondary', 'records':'Benchmark data',   'period':'2024'},
    {'name':'McKinsey Manufacturing','type':'Secondary','records':'Industry KPIs',    'period':'2024'},
    {'name':'Gartner Top-25 SC',    'type':'Secondary', 'records':'Peer benchmarks',  'period':'2024'},
    {'name':'Shopify Logistics',    'type':'Secondary', 'records':'eCommerce metrics','period':'2024'},
    {'name':'CE Interim KPI Study', 'type':'Secondary', 'records':'KPI frameworks',   'period':'2025'},
]

# ─────────────────────────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────────────────────────

NAV_ITEMS = [
    ('overview',     '📊', 'Overview Dashboard'),
    ('suppliers',    '🏭', 'Supplier Performance'),
    ('inventory',    '📦', 'Inventory & Costs'),
    ('risk',         '⚠️', 'Risk Analysis'),
    ('recommendations','💡','Recommendations'),
    ('methodology',  '🔬', 'Methodology'),
]

def sidebar():
    nav_links = []
    for page_id, icon, label in NAV_ITEMS:
        nav_links.append(
            html.Button(
                [html.Span(icon, style={'fontSize':'16px','marginRight':'10px'}), label],
                id=f'nav-{page_id}',
                n_clicks=0,
                style={
                    'display':'flex','alignItems':'center','width':'100%','textAlign':'left',
                    'padding':'9px 12px','borderRadius':'6px','border':'none',
                    'background':'none','color':'#8b949e','fontSize':'13px','cursor':'pointer',
                    'marginBottom':'2px','fontFamily':'Inter, sans-serif',
                },
                className=f'nav-btn nav-btn-{page_id}',
            )
        )
    return html.Div([
        # Logo
        html.Div([
            html.Div('📦', style={'fontSize':'26px','marginBottom':'8px'}),
            html.Div('Supply Chain Analytics', style={'fontSize':'12px','fontWeight':'600','color':'#e6edf3','lineHeight':'1.3'}),
            html.Div('Supplier Performance Analysis', style={'fontSize':'10px','color':'#8b949e','marginTop':'2px'}),
        ], style={'padding':'18px 20px 16px','borderBottom':'1px solid rgba(48,54,61,0.8)'}),
        # Nav
        html.Div([
            html.Div('ANALYTICS', style={'fontSize':'10px','fontWeight':'600','letterSpacing':'.08em','color':'#484f58','padding':'12px 10px 6px'}),
            *nav_links[:4],
            html.Div('REPORTS', style={'fontSize':'10px','fontWeight':'600','letterSpacing':'.08em','color':'#484f58','padding':'14px 10px 6px'}),
            *nav_links[4:],
        ], style={'padding':'0 10px','flex':'1','overflowY':'auto'}),
        # Footer
        html.Div([
            html.Div('Period: Jan 2023 – Dec 2024', style={'marginBottom':'2px'}),
            html.Div('Suppliers: 847 analysed'),
            html.Div('KPI Dimensions: 14'),
        ], style={'padding':'14px 20px','borderTop':'1px solid rgba(48,54,61,0.8)',
                  'fontSize':'11px','color':'#484f58'}),
    ], style={
        'width':'240px','background':'#161b22','borderRight':'1px solid rgba(48,54,61,0.8)',
        'height':'100vh','position':'fixed','top':'0','left':'0',
        'display':'flex','flexDirection':'column','zIndex':'100','overflowY':'auto',
    })


app.layout = html.Div([
    dcc.Store(id='current-page', data='overview'),
    sidebar(),
    # Main
    html.Div([
        # Topbar
        html.Div([
            html.Div([
                html.Span('Supply Chain Analytics', style={'color':'#8b949e','fontSize':'13px'}),
                html.Span(' / ', style={'color':'#484f58','margin':'0 6px','fontSize':'13px'}),
                html.Span(id='topbar-page', children='Overview Dashboard',
                          style={'color':'#e6edf3','fontWeight':'500','fontSize':'13px'}),
            ]),
            html.Div(style={'flex':'1'}),
            html.Span('🟢  847 Suppliers Active', style={
                'fontSize':'11px','padding':'3px 10px','borderRadius':'20px',
                'background':'rgba(29,158,117,.12)','color':'#1D9E75',
                'border':'1px solid rgba(29,158,117,.3)','marginRight':'10px',
            }),
            html.Span('📅 Jan 2023 – Dec 2024', style={
                'fontSize':'12px','padding':'4px 12px',
                'border':'1px solid rgba(48,54,61,0.8)',
                'borderRadius':'6px','color':'#8b949e',
            }),
        ], style={
            'height':'60px','background':'#161b22','borderBottom':'1px solid rgba(48,54,61,0.8)',
            'display':'flex','alignItems':'center','padding':'0 24px','gap':'10px',
            'position':'sticky','top':'0','zIndex':'50',
        }),
        # Page content
        html.Div(id='page-content', style={'padding':'24px','minHeight':'calc(100vh - 60px)'}),
    ], style={'marginLeft':'240px','flex':'1'}),
    # Toast
    html.Div(id='toast', style={
        'position':'fixed','bottom':'20px','right':'20px',
        'background':'#21262d','border':'1px solid rgba(48,54,61,0.8)',
        'color':'#e6edf3','fontSize':'13px','padding':'10px 16px',
        'borderRadius':'6px','display':'none','zIndex':'999',
    }),
], style={
    'background':'#0d1117','minHeight':'100vh',
    'fontFamily':'Inter, Segoe UI, sans-serif','color':'#e6edf3',
    'display':'flex',
})

# ─────────────────────────────────────────────────────────────────
# CALLBACKS
# ─────────────────────────────────────────────────────────────────

PAGE_LABELS = {p: l for p, _, l in NAV_ITEMS}
PAGE_BUILDERS = {
    'overview':        page_overview,
    'suppliers':       page_suppliers,
    'inventory':       page_inventory,
    'risk':            page_risk,
    'recommendations': page_recommendations,
    'methodology':     page_methodology,
}

# Page navigation
@app.callback(
    Output('current-page', 'data'),
    [Input(f'nav-{p}', 'n_clicks') for p, _, _ in NAV_ITEMS],
    prevent_initial_call=True,
)
def update_page(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return 'overview'
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return btn_id.replace('nav-', '')

@app.callback(
    Output('page-content', 'children'),
    Output('topbar-page', 'children'),
    Input('current-page', 'data'),
)
def render_page(page):
    builder = PAGE_BUILDERS.get(page, page_overview)
    return builder(), PAGE_LABELS.get(page, 'Overview Dashboard')

# Supplier table with filter/search
@app.callback(
    Output('supplier-table-container', 'children'),
    Output('supplier-count', 'children'),
    Input('filter-search', 'value'),
    Input('filter-rating', 'value'),
    Input('filter-risk', 'value'),
)
def update_supplier_table(search, rating, risk):
    df = D.df_suppliers.copy()
    if search:
        mask = (df['Supplier'].str.contains(search, case=False, na=False) |
                df['Region'].str.contains(search, case=False, na=False))
        df = df[mask]
    if rating:
        df = df[df['Rating'] == rating]
    if risk:
        df = df[df['Risk'] == risk]

    count_text = f"{len(df)} suppliers shown"

    rows = []
    for _, r in df.iterrows():
        score_color = '#1D9E75' if r['Score'] >= 90 else '#185FA5' if r['Score'] >= 80 else '#BA7517'
        rows.append(html.Tr([
            html.Td(html.Strong(r['Supplier']), style=td_s),
            html.Td(r['Region'], style={**td_s,'color':'#8b949e'}),
            html.Td(f"{r['OTD']}%", style=td_s),
            html.Td(f"{r['Quality']}%", style=td_s),
            html.Td(f"{r['Lead_Days']}d", style=td_s),
            html.Td([
                html.Div([
                    html.Div(style={
                        'width':'70px','height':'5px','background':'rgba(255,255,255,.08)',
                        'borderRadius':'3px','overflow':'hidden','display':'inline-block','verticalAlign':'middle','marginRight':'8px',
                    }, children=[
                        html.Div(style={'width':f"{r['Score']}%",'height':'100%','background':score_color,'borderRadius':'3px'})
                    ]),
                    html.Span(str(r['Score']), style={'fontSize':'12px','fontWeight':'600','color':score_color}),
                ], style={'display':'flex','alignItems':'center'}),
            ], style=td_s),
            html.Td(badge(r['Rating']), style=td_s),
            html.Td(badge(r['Risk']), style=td_s),
        ]))

    table = html.Table([
        html.Thead(html.Tr([
            html.Th(h, style={'padding':'10px 12px','fontSize':'11px','fontWeight':'600',
                              'textTransform':'uppercase','letterSpacing':'.05em','color':'#8b949e',
                              'borderBottom':'1px solid rgba(48,54,61,0.8)','whiteSpace':'nowrap'})
            for h in ['Supplier','Region','OTD %','Quality %','Lead Time','Score','Rating','Risk']
        ])),
        html.Tbody(rows),
    ], style={'width':'100%','borderCollapse':'collapse','fontSize':'13px'})

    return html.Div(table, style={'overflowX':'auto'}), count_text

# CSV Export
@app.callback(
    Output('download-csv', 'data'),
    Input('btn-export-csv', 'n_clicks'),
    prevent_initial_call=True,
)
def export_csv(n):
    return dcc.send_data_frame(D.df_suppliers.to_csv, 'supplier_performance.csv', index=False)


# ─────────────────────────────────────────────────────────────────
# CUSTOM CSS (injected)
# ─────────────────────────────────────────────────────────────────
app.index_string = '''<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
<style>
  * { box-sizing: border-box; }
  body { margin: 0; background: #0d1117; }
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: #161b22; }
  ::-webkit-scrollbar-thumb { background: #21262d; border-radius: 3px; }
  .nav-btn:hover { background: #1c2128 !important; color: #e6edf3 !important; }
  .Select-control { background: #1c2128 !important; border: 1px solid rgba(48,54,61,0.8) !important; color: #e6edf3 !important; border-radius: 6px !important; }
  .Select-menu-outer { background: #1c2128 !important; border: 1px solid rgba(48,54,61,0.8) !important; }
  .Select-option { background: #1c2128 !important; color: #8b949e !important; }
  .Select-option:hover, .Select-option.is-focused { background: #21262d !important; color: #e6edf3 !important; }
  .Select-value-label { color: #e6edf3 !important; }
  .Select-placeholder { color: #484f58 !important; }
  .Select-arrow { border-top-color: #8b949e !important; }
  tr:hover td { background: rgba(255,255,255,0.02) !important; }
  .js-plotly-plot .plotly .modebar { display: none !important; }
</style>
</head>
<body>
{%app_entry%}
<footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>'''


# ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print()
    print('╔══════════════════════════════════════════════════════════╗')
    print('║   SUPPLY CHAIN ANALYTICS DASHBOARD                      ║')
    print('║   Data-Driven Optimization of Supply Chain Operations    ║')
    print('╠══════════════════════════════════════════════════════════╣')
    print('║   Open your browser and go to:                          ║')
    print('║   http://localhost:8050                                  ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print()
    app.run(debug=False, host='localhost', port=8050)
