# Supply Chain Analytics Dashboard (Python / Dash)
## Data-Driven Optimization of Supply Chain Operations

---

## ✅ STEP-BY-STEP SETUP (Windows)

### Step 1 — Install Python
1. Go to: https://www.python.org/downloads/
2. Click "Download Python 3.x.x" (latest)
3. Run the installer
4. ✅ CHECK "Add Python to PATH" before clicking Install

### Step 2 — Open PowerShell in the project folder
1. Open File Explorer
2. Navigate to the `supply-chain-analytics-python` folder
3. Click the address bar at the top, type `powershell`, press Enter

### Step 3 — Install dependencies
```powershell
py -m pip install -r requirements.txt
```

### Step 4 — Run the app
```powershell
py app.py
```

### Step 5 — Open in browser
Go to: **http://localhost:8050**

---

## 📁 Project Files

```
supply-chain-analytics-python/
│
├── app.py            ← Main Dash app (run this)
├── data.py           ← All supply chain data & KPIs
├── charts.py         ← Plotly chart functions
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| **Overview** | 6 KPI cards + OTD/POR trend + cost breakdown + inventory turnover + forecast |
| **Supplier Performance** | 15 suppliers, sortable/filterable table + rating chart + scatter |
| **Inventory & Costs** | Inventory trend, cash-to-cash, freight lanes, ABC-XYZ table |
| **Risk Analysis** | Risk matrix, geographic concentration, resilience trend, risk register |
| **Recommendations** | 6 prioritised actions + implementation roadmap |
| **Methodology** | Framework, data sources, scoring model, statistical methods |

---

## 🔧 Customise Data

To update the data, edit **`data.py`**:
- KPIs: update `KPIS` dictionary
- Suppliers: update `SUPPLIERS_RAW` list
- Chart data: update the list variables (e.g. `OTD_2024`, `MONTHS`, etc.)

To add a new chart, add a function to **`charts.py`** and call it from the relevant page in `app.py`.

---

## ❓ Troubleshooting

**"pip is not recognized"**
→ Python was not added to PATH. Reinstall Python and check "Add Python to PATH"

**"No module named dash"**
→ Run `pip install -r requirements.txt` again

**Port 8050 already in use**
→ Change port in last line of app.py: `app.run(port=8051)`

**Blank page in browser**
→ Wait 3–5 seconds and refresh; Dash takes a moment to load initially

---

*Period: Jan 2023 – Dec 2024 · 847 Suppliers · 14 KPI Dimensions*
*Stack: Python · Dash · Plotly · Pandas*
