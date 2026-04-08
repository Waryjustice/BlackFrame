def valuation_agent(data, finance_results):
    ebitda = finance_results.get("ebitda", 0)
    revenue = data.get("revenue", 0)
    debt = data.get("debt", 0)
    equity = data.get("equity", 0)
    
    # --- 1. THE "DCF" ENGINE (5-Year Projection) ---
    # We simulate 5 years of growth and then a 'Terminal Value'
    growth_rate = 0.05  # 5% growth
    discount_rate = 0.10 # 10% WACC (Risk adjustment)
    
    projections = []
    current_ebitda = ebitda
    for i in range(1, 6):
        current_ebitda *= (1 + growth_rate)
        # Present Value = Future Value / (1 + r)^n
        pv = current_ebitda / ((1 + discount_rate) ** i)
        projections.append(pv)
    
    # Terminal Value (Value beyond year 5)
    terminal_value = (projections[-1] * 1.02) / (discount_rate - 0.02)
    pv_terminal = terminal_value / ((1 + discount_rate) ** 5)
    
    dcf_final = sum(projections) + pv_terminal

    # --- 2. THE MULTIPLES ENGINE (Industry specific) ---
    # Tech SMEs usually trade at higher multiples than manufacturing
    multiples = {
        "Conservative": ebitda * 4,
        "Market_Avg": ebitda * 6,
        "Aggressive": ebitda * 8
    }

    # --- 3. LIQUIDATION VALUE (Safety Net) ---
    # If the business closed today, what is left?
    liquidation = data.get("assets", 0) - data.get("liabilities", 0)

    return {
        "intrinsic_value": {
            "dcf_valuation": round(dcf_final, 2),
            "logic": "5-Year Free Cash Flow projection with 2% perpetual growth"
        },
        "market_multiples": multiples,
        "liquidation_value": liquidation,
        "valuation_confidence": "High" if revenue > 0 else "Low (No Revenue)"
    }