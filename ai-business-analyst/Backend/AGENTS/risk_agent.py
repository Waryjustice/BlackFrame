from typing import Dict

def risk_agent(data: Dict, finance_results: Dict):
    """
    Calculates Altman Z-Score and provides risk assessment.
    Z-Score formula for private companies:
    Z = 0.717*X1 + 0.847*X2 + 3.107*X3 + 0.420*X4 + 0.998*X5
    
    Where:
    X1 = Working Capital / Total Assets
    X2 = Retained Earnings / Total Assets
    X3 = EBIT / Total Assets
    X4 = Book Value of Equity / Total Liabilities
    X5 = Sales / Total Assets
    """
    
    # Extract data
    revenue = data.get("revenue", 0)
    assets = data.get("assets", 0)
    liabilities = data.get("liabilities", 0)
    equity = data.get("equity", 0)
    debt = data.get("debt", 0)
    ebitda = finance_results.get("ebitda", 0)
    
    # Prevent division by zero
    if assets == 0:
        return {
            "z_score": 0,
            "health_status": "Insufficient Data",
            "risk_level": "Unknown",
            "liquidity_risks": ["No asset data available"],
            "solvency_risks": ["Cannot calculate ratios"]
        }
    
    # Calculate Altman Z-Score components
    # X1: Working Capital / Total Assets (liquidity)
    working_capital = assets - liabilities
    x1 = working_capital / assets if assets != 0 else 0
    
    # X2: Retained Earnings / Total Assets (we'll estimate as equity/2)
    retained_earnings = equity * 0.5  # Estimation
    x2 = retained_earnings / assets if assets != 0 else 0
    
    # X3: EBIT / Total Assets (profitability)
    x3 = ebitda / assets if assets != 0 else 0
    
    # X4: Book Value of Equity / Total Liabilities (leverage)
    x4 = equity / liabilities if liabilities != 0 else 0
    
    # X5: Sales / Total Assets (asset turnover)
    x5 = revenue / assets if assets != 0 else 0
    
    # Altman Z-Score for private companies
    z_score = (0.717 * x1) + (0.847 * x2) + (3.107 * x3) + (0.420 * x4) + (0.998 * x5)
    
    # Determine health status
    if z_score > 2.9:
        health_status = "Safe"
        risk_level = "Low"
    elif z_score >= 1.23:
        health_status = "Grey"
        risk_level = "Medium"
    else:
        health_status = "Distress"
        risk_level = "High"
    
    # Assess specific risks
    liquidity_risks = []
    solvency_risks = []
    
    # Liquidity Analysis
    current_ratio = finance_results.get("current_ratio", 0)
    if current_ratio < 1.0:
        liquidity_risks.append("Current ratio below 1.0 - potential short-term liquidity issues")
    if working_capital < 0:
        liquidity_risks.append("Negative working capital - immediate liquidity concern")
    if current_ratio >= 1.5 and working_capital > 0:
        liquidity_risks.append("Liquidity position is healthy")
    
    # Solvency Analysis
    debt_to_equity = finance_results.get("debt_to_equity", 0)
    if debt_to_equity > 2.0:
        solvency_risks.append("High debt-to-equity ratio - overleveraged position")
    if debt_to_equity > 1.5:
        solvency_risks.append("Moderate debt burden - monitor debt servicing capacity")
    if liabilities > assets:
        solvency_risks.append("Liabilities exceed assets - severe solvency risk")
    if debt_to_equity <= 1.0 and liabilities < assets:
        solvency_risks.append("Solvency position is stable")
    
    # Profitability risks
    net_profit_margin = finance_results.get("net_profit_margin", 0)
    if net_profit_margin < 0:
        liquidity_risks.append("Negative profit margins - cash flow concerns")
    
    return {
        "z_score": round(z_score, 2),
        "health_status": health_status,
        "risk_level": risk_level,
        "score_breakdown": {
            "working_capital_ratio": round(x1, 3),
            "retained_earnings_ratio": round(x2, 3),
            "profitability_ratio": round(x3, 3),
            "leverage_ratio": round(x4, 3),
            "asset_turnover": round(x5, 3)
        },
        "liquidity_risks": liquidity_risks if liquidity_risks else ["No significant liquidity concerns identified"],
        "solvency_risks": solvency_risks if solvency_risks else ["No significant solvency concerns identified"],
        "interpretation": {
            "Safe (Z > 2.9)": "Low bankruptcy risk",
            "Grey (1.23 - 2.9)": "Moderate risk, requires monitoring",
            "Distress (Z < 1.23)": "High bankruptcy risk within 2 years"
        }
    }
