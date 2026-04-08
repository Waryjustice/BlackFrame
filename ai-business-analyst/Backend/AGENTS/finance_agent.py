from typing import Dict

def analyze_financials(data: Dict):
    # main.py sends flattened data, so we grab keys directly
    revenue = data.get("revenue", 0)
    expenses = data.get("expenses", 0)
    assets = data.get("assets", 0)
    liabilities = data.get("liabilities", 0)
    equity = data.get("equity", 0)
    debt = data.get("debt", 0)

    # Key Metrics
    ebitda = revenue - expenses
    net_profit_margin = (ebitda / revenue) if revenue != 0 else 0
    debt_to_equity = (debt / equity) if equity != 0 else 0
    current_ratio = (assets / liabilities) if liabilities != 0 else 0

    return {
        "ebitda": ebitda,
        "net_profit_margin": round(net_profit_margin, 2),
        "debt_to_equity": round(debt_to_equity, 2),
        "current_ratio": round(current_ratio, 2)
    }