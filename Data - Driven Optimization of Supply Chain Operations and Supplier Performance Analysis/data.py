# ================================================================
# SUPPLY CHAIN ANALYTICS — Data Module
# Data-Driven Optimization of Supply Chain Operations
# ================================================================

import pandas as pd

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
QUARTERS = ['Q1 2023','Q2 2023','Q3 2023','Q4 2023','Q1 2024','Q2 2024','Q3 2024','Q4 2024']

# ── KPIs ─────────────────────────────────────────────────────────
KPIS = {
    'otd':               {'value': 94.2,  'unit': '%',  'label': 'On-Time Delivery',          'delta': '+3.1%',  'delta_dir': 'up',      'note': 'vs prior year'},
    'por':               {'value': 88.7,  'unit': '%',  'label': 'Perfect Order Rate',         'delta': '+2.4%',  'delta_dir': 'up',      'note': 'vs prior year'},
    'inv_turnover':      {'value': 8.3,   'unit': '×',  'label': 'Inventory Turnover',         'delta': '+1.2×',  'delta_dir': 'up',      'note': 'Industry avg 7.1×'},
    'c2c':               {'value': 34,    'unit': 'd',  'label': 'Cash-to-Cash Cycle',         'delta': '−6d',    'delta_dir': 'up',      'note': 'days saved'},
    'forecast_acc':      {'value': 82.5,  'unit': '%',  'label': 'Forecast Accuracy',          'delta': 'Target', 'delta_dir': 'neutral', 'note': '85% target'},
    'sc_cost':           {'value': 9.4,   'unit': '%',  'label': 'Supply Chain Cost',          'delta': '−1.8%',  'delta_dir': 'up',      'note': 'of revenue'},
    'active_suppliers':  {'value': 847,   'unit': '',   'label': 'Active Suppliers',           'delta': '34',     'delta_dir': 'neutral', 'note': 'countries'},
    'avg_lead':          {'value': 12.4,  'unit': 'd',  'label': 'Avg Lead Time',              'delta': '−2.1d',  'delta_dir': 'up',      'note': 'vs 2023'},
    'defect_rate':       {'value': 1.3,   'unit': '%',  'label': 'Defect Rate',                'delta': '−0.4%',  'delta_dir': 'up',      'note': 'vs 2023'},
    'stockout_rate':     {'value': 2.1,   'unit': '%',  'label': 'Stockout Rate',              'delta': '−1.3%',  'delta_dir': 'up',      'note': 'vs 2023'},
    'gmroi':             {'value': 3.42,  'unit': '$',  'label': 'GMROI',                      'delta': '+$0.38', 'delta_dir': 'up',      'note': 'vs 2023'},
    'dio':               {'value': 44,    'unit': 'd',  'label': 'Days Inventory Outstanding', 'delta': '−8d',    'delta_dir': 'up',      'note': 'vs 2023'},
    'resilience':        {'value': 74,    'unit': '',   'label': 'Resilience Score',           'delta': '+16',    'delta_dir': 'up',      'note': 'vs Q1 2023'},
    'esg':               {'value': 62,    'unit': '%',  'label': 'ESG Compliance (Tier-2)',    'delta': 'Target', 'delta_dir': 'neutral', 'note': '100% by 2026'},
}

# ── OTD / POR Monthly ────────────────────────────────────────────
OTD_2024  = [91.2,92.1,93.0,93.8,94.1,94.5,94.3,94.8,95.0,94.9,95.2,95.5]
OTD_2023  = [87.5,88.1,88.8,89.2,89.9,90.1,90.5,90.8,91.0,91.3,91.6,91.9]
POR_2024  = [86.1,87.0,87.8,88.3,88.7,89.1,88.9,89.4,89.7,89.8,90.1,90.3]
POR_2023  = [83.2,83.8,84.1,84.5,85.0,85.3,85.7,86.0,86.4,86.7,87.0,87.3]

# ── Forecast Accuracy ────────────────────────────────────────────
FORECAST_2024 = [78.2,79.1,80.0,80.8,81.5,82.0,82.2,82.5,82.9,83.1,83.5,84.0]
FORECAST_2023 = [72.1,73.5,74.2,75.0,75.8,76.3,76.9,77.4,77.9,78.3,78.7,79.0]

# ── Inventory ────────────────────────────────────────────────────
INV_CATEGORIES = ['Electronics','Apparel','Food','Industrial','Pharma','Consumer']
INV_ACTUAL     = [10.2, 6.8, 14.1, 5.3, 4.7, 9.1]
INV_BENCHMARK  = [9.1,  6.2, 13.5, 5.0, 4.4, 8.5]
INV_VALUE_2024 = [54,51,58,55,53,57,60,56,54,58,62,65]
SALES_VELOCITY = [72,68,81,78,83,88,85,91,87,84,92,95]
STOCKOUT_EVENTS= [2, 1, 5, 2, 1, 1, 2, 4, 1, 1, 2, 1]

# ── Cash-to-Cash ─────────────────────────────────────────────────
C2C_COMPONENTS = ['DIO (days)','DSO (days)','DPO (days)','C2C Net (days)']
C2C_2024 = [44, 22, 32, 34]
C2C_2023 = [52, 25, 27, 50]

# ── Freight ──────────────────────────────────────────────────────
FREIGHT_LANES = ['Asia-Pacific','Europe','Latin America','Middle East',
                 'Africa','North America','Domestic (air)','Domestic (ground)']
FREIGHT_COSTS = [4.80, 3.20, 3.60, 3.90, 4.10, 2.10, 1.80, 0.90]

# ── Cost Breakdown ───────────────────────────────────────────────
COST_LABELS  = ['Transportation','Warehousing','Procurement','Returns']
COST_VALUES  = [3.8, 2.5, 1.7, 1.4]
COST_COLORS  = ['#1D9E75','#185FA5','#BA7517','#E24B4A']

# ── Geo Concentration ────────────────────────────────────────────
GEO_LABELS = ['Asia-Pacific','Europe','N. America','Other']
GEO_VALUES = [44, 28, 19, 9]
GEO_COLORS = ['#185FA5','#1D9E75','#BA7517','#7F77DD']

# ── Resilience ───────────────────────────────────────────────────
RESILIENCE_SCORES = [58, 61, 63, 65, 67, 69, 72, 74]

# ── Rating Distribution ──────────────────────────────────────────
RATING_LABELS = ['A (≥90)','B (75–89)','C (60–74)','D (<60)']
RATING_COUNTS = [312, 284, 178, 73]
RATING_COLORS = ['#1D9E75','#185FA5','#BA7517','#E24B4A']

# ── Suppliers DataFrame ──────────────────────────────────────────
SUPPLIERS_RAW = [
    {'Supplier':'Apex Manufacturing',  'Region':'Germany',   'OTD':98.2,'Quality':99.1,'Lead_Days':7, 'Score':96,'Rating':'A','Spend_M':12.4,'Defect_Pct':0.4,'Risk':'Low'},
    {'Supplier':'Vantage Logistics',   'Region':'Japan',     'OTD':97.5,'Quality':98.4,'Lead_Days':9, 'Score':94,'Rating':'A','Spend_M':10.8,'Defect_Pct':0.6,'Risk':'Low'},
    {'Supplier':'Syncore Materials',   'Region':'USA',       'OTD':96.1,'Quality':97.8,'Lead_Days':5, 'Score':93,'Rating':'A','Spend_M':14.2,'Defect_Pct':0.8,'Risk':'Low'},
    {'Supplier':'NovaTech Parts',      'Region':'S. Korea',  'OTD':95.8,'Quality':98.1,'Lead_Days':11,'Score':91,'Rating':'A','Spend_M':9.1, 'Defect_Pct':1.1,'Risk':'Low'},
    {'Supplier':'SkyLink Parts',       'Region':'Canada',    'OTD':96.8,'Quality':97.2,'Lead_Days':6, 'Score':92,'Rating':'A','Spend_M':11.2,'Defect_Pct':0.7,'Risk':'Low'},
    {'Supplier':'DeltaForge Inc.',     'Region':'China',     'OTD':94.3,'Quality':96.5,'Lead_Days':14,'Score':87,'Rating':'B','Spend_M':8.3, 'Defect_Pct':1.8,'Risk':'Medium'},
    {'Supplier':'BluePath Supply',     'Region':'India',     'OTD':93.7,'Quality':95.9,'Lead_Days':12,'Score':85,'Rating':'B','Spend_M':7.5, 'Defect_Pct':1.4,'Risk':'Medium'},
    {'Supplier':'Meridian Components', 'Region':'Mexico',    'OTD':92.1,'Quality':95.2,'Lead_Days':8, 'Score':83,'Rating':'B','Spend_M':6.9, 'Defect_Pct':1.2,'Risk':'Medium'},
    {'Supplier':'Arco Precision',      'Region':'France',    'OTD':94.9,'Quality':96.8,'Lead_Days':10,'Score':89,'Rating':'B','Spend_M':8.8, 'Defect_Pct':1.0,'Risk':'Low'},
    {'Supplier':'Eastway Textiles',    'Region':'Vietnam',   'OTD':90.5,'Quality':94.0,'Lead_Days':16,'Score':78,'Rating':'B','Spend_M':5.8, 'Defect_Pct':2.2,'Risk':'Medium'},
    {'Supplier':'OmniSource Ltd.',     'Region':'Malaysia',  'OTD':91.4,'Quality':94.5,'Lead_Days':13,'Score':82,'Rating':'B','Spend_M':6.1, 'Defect_Pct':1.6,'Risk':'Medium'},
    {'Supplier':'RedLine Supplies',    'Region':'Poland',    'OTD':89.3,'Quality':93.8,'Lead_Days':9, 'Score':76,'Rating':'B','Spend_M':5.3, 'Defect_Pct':1.9,'Risk':'Medium'},
    {'Supplier':'Hallmark Metals',     'Region':'Brazil',    'OTD':88.9,'Quality':93.1,'Lead_Days':18,'Score':71,'Rating':'C','Spend_M':4.2, 'Defect_Pct':2.8,'Risk':'High'},
    {'Supplier':'GreenSource Co.',     'Region':'Australia', 'OTD':87.2,'Quality':92.5,'Lead_Days':10,'Score':69,'Rating':'C','Spend_M':3.8, 'Defect_Pct':0.9,'Risk':'Low'},
    {'Supplier':'IronPath Global',     'Region':'Turkey',    'OTD':85.0,'Quality':90.1,'Lead_Days':20,'Score':65,'Rating':'C','Spend_M':3.1, 'Defect_Pct':3.1,'Risk':'High'},
]
df_suppliers = pd.DataFrame(SUPPLIERS_RAW)

# ── Risk Register ────────────────────────────────────────────────
RISKS = [
    {'ID':'R01','Category':'Operational', 'Description':'Single-source dependency for 23 critical components',        'Likelihood':'High',  'Impact':'High',  'Level':'Critical','Mitigation':'Dual-sourcing programme for top 10 by revenue impact'},
    {'ID':'R02','Category':'Geopolitical','Description':'Red Sea/Suez disruption — Asia-Europe lane delays',          'Likelihood':'High',  'Impact':'High',  'Level':'Critical','Mitigation':'Pre-negotiated Cape of Good Hope rerouting contracts'},
    {'ID':'R03','Category':'Compliance', 'Description':'38% Tier-2 suppliers lack ESG audit (EU CSDDD by 2026)',      'Likelihood':'High',  'Impact':'Medium','Level':'High',    'Mitigation':'Mandatory audit programme launched Q1 2025'},
    {'ID':'R04','Category':'Financial',  'Description':'Currency volatility in Asia-Pacific (+/−12% swing)',          'Likelihood':'Medium','Impact':'High',  'Level':'High',    'Mitigation':'Forward contracts for top-5 currency pairs'},
    {'ID':'R05','Category':'Technology', 'Description':'Semiconductor shortage impacting 6 product categories',       'Likelihood':'Medium','Impact':'High',  'Level':'High',    'Mitigation':'12-month buffer stock strategy for critical ICs'},
    {'ID':'R06','Category':'Operational','Description':'Demand forecast accuracy below 85% target',                   'Likelihood':'Medium','Impact':'Medium','Level':'Medium',  'Mitigation':'ML ensemble model deployment in Q2 2025'},
    {'ID':'R07','Category':'Supplier',   'Description':'Tier-2/3 supplier visibility gap — only 42% mapped',          'Likelihood':'Medium','Impact':'Medium','Level':'Medium',  'Mitigation':'Supply chain mapping tool rollout underway'},
    {'ID':'R08','Category':'Logistics',  'Description':'Port congestion at 3 key gateway ports',                      'Likelihood':'Low',   'Impact':'Medium','Level':'Low',     'Mitigation':'Real-time port congestion monitoring via FourKites'},
    {'ID':'R09','Category':'Data',       'Description':'ERP data quality issues in legacy procurement modules',        'Likelihood':'Low',   'Impact':'Low',   'Level':'Low',     'Mitigation':'Data cleansing sprint completed Q3 2024'},
]
df_risks = pd.DataFrame(RISKS)

# ── Recommendations ──────────────────────────────────────────────
RECOMMENDATIONS = [
    {'Priority':1,'Title':'Deploy AI demand sensing',           'Impact':'High',  'Effort':'Medium','Saving':'$3.2M working capital','Status':'In Progress','Description':'ML ensemble (ARIMA + XGBoost) to reduce forecast error from 17.5% to under 10%. Pilot with top-20 SKUs.'},
    {'Priority':2,'Title':'Supplier dual-sourcing programme',   'Impact':'High',  'Effort':'High',  'Saving':'Risk mitigation',      'Status':'Planned',    'Description':'Qualify secondary sources for all 23 single-source critical components. Target: Q4 2025.'},
    {'Priority':3,'Title':'Real-time control tower',            'Impact':'High',  'Effort':'High',  'Saving':'$1.8M logistics costs','Status':'In Progress','Description':'Full FourKites deployment for end-to-end visibility. Expected OTD improvement +2.5%.'},
    {'Priority':4,'Title':'Dynamic safety stock model',         'Impact':'Medium','Effort':'Low',   'Saving':'$1.4M carrying costs', 'Status':'Completed',  'Description':'Demand-volatility-adjusted safety stock replaced static model. Stockout events down 38%.'},
    {'Priority':5,'Title':'ESG Tier-2 audit programme',         'Impact':'Medium','Effort':'Medium','Saving':'Compliance risk',      'Status':'In Progress','Description':'Mandatory audits for all 325 Tier-2 suppliers. 62% complete; targeting 100% before CSDDD.'},
    {'Priority':6,'Title':'Freight lane optimisation',          'Impact':'Medium','Effort':'Medium','Saving':'$0.9M freight costs',  'Status':'Planned',    'Description':'Renegotiate Asia-Pacific contracts; consolidate high-frequency lanes to reduce per-unit cost.'},
]
df_recs = pd.DataFrame(RECOMMENDATIONS)

# ── ABC-XYZ Classification ───────────────────────────────────────
ABC_XYZ = [
    {'Class':'A-X','SKUs':142,'Revenue_Pct':61.2,'Avg_Turnover':12.4,'Holding_Cost_Pct':14.2,'Stockout_Risk':'Low',     'Strategy':'Tight safety stock, frequent reorder'},
    {'Class':'A-Y','SKUs':89, 'Revenue_Pct':14.8,'Avg_Turnover':9.8, 'Holding_Cost_Pct':16.5,'Stockout_Risk':'Medium',  'Strategy':'Statistical safety stock + supplier collab'},
    {'Class':'A-Z','SKUs':31, 'Revenue_Pct':5.4, 'Avg_Turnover':6.2, 'Holding_Cost_Pct':22.1,'Stockout_Risk':'High',    'Strategy':'High safety stock; dual sourcing required'},
    {'Class':'B-X','SKUs':210,'Revenue_Pct':9.8, 'Avg_Turnover':8.3, 'Holding_Cost_Pct':17.4,'Stockout_Risk':'Low',     'Strategy':'Periodic review; EOQ model'},
    {'Class':'B-Y','SKUs':178,'Revenue_Pct':5.2, 'Avg_Turnover':6.7, 'Holding_Cost_Pct':19.0,'Stockout_Risk':'Medium',  'Strategy':'Min-max policy with demand sensing'},
    {'Class':'C-X/Y/Z','SKUs':496,'Revenue_Pct':3.6,'Avg_Turnover':3.9,'Holding_Cost_Pct':28.3,'Stockout_Risk':'Variable','Strategy':'Consignment or on-demand procurement'},
]
df_abc = pd.DataFrame(ABC_XYZ)
