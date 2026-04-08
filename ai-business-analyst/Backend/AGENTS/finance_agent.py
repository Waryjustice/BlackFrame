# finance_agent.py
from typing import Dict

def analyze_financials(data: Dict):
    balance = data.get("balance_sheet", {})
    pl = data.get("profit_loss", {})
    cash = data.get("cash_flow", {})

    # Key metrics
    ebitda = pl.get("revenue", 0) - pl.get("expenses", 0)
    net_profit_margin = ebitda / pl.get("revenue", 1)
    debt_to_equity = balance.get("liabilities", 0) / cash.get("equity", 1)
    current_ratio = balance.get("assets", 0) / balance.get("liabilities", 1)

    # Return structured results
    return {
        "EBITDA": ebitda,
        "NetProfitMargin": round(net_profit_margin, 2),
        "DebtToEquity": round(debt_to_equity, 2),
        "CurrentRatio": round(current_ratio, 2)
    }