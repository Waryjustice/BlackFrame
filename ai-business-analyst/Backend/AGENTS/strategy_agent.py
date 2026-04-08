import os
from typing import Dict
import google.generativeai as genai

def generate_strategy(all_results: Dict):
    """
    Uses Gemini 1.5 Flash to generate strategic recommendations 
    based on financial, valuation, and risk analysis.
    """
    
    # Extract key metrics for context
    finance = all_results.get("finance", {})
    valuation = all_results.get("valuation", {})
    risk = all_results.get("risk", {})
    raw_data = all_results.get("raw_data", {})
    
    # Build context for Gemini
    context = f"""
    You are a strategic business consultant. Analyze the following financial assessment and provide actionable recommendations.
    
    FINANCIAL METRICS:
    - Revenue: ${raw_data.get('revenue', 0):,.2f}
    - EBITDA: ${finance.get('ebitda', 0):,.2f}
    - Net Profit Margin: {finance.get('net_profit_margin', 0)*100:.1f}%
    - Debt-to-Equity: {finance.get('debt_to_equity', 0):.2f}
    - Current Ratio: {finance.get('current_ratio', 0):.2f}
    
    VALUATION:
    - DCF Valuation: ${valuation.get('intrinsic_value', {}).get('dcf_valuation', 0):,.2f}
    - Market Multiple (Conservative): ${valuation.get('market_multiples', {}).get('Conservative', 0):,.2f}
    - Market Multiple (Market Avg): ${valuation.get('market_multiples', {}).get('Market_Avg', 0):,.2f}
    - Liquidation Value: ${valuation.get('liquidation_value', 0):,.2f}
    
    RISK ASSESSMENT:
    - Altman Z-Score: {risk.get('z_score', 0):.2f}
    - Health Status: {risk.get('health_status', 'Unknown')}
    - Risk Level: {risk.get('risk_level', 'Unknown')}
    - Liquidity Risks: {', '.join(risk.get('liquidity_risks', []))}
    - Solvency Risks: {', '.join(risk.get('solvency_risks', []))}
    
    Based on this analysis, provide:
    1. EXECUTIVE SUMMARY (2-3 sentences on overall company health)
    2. TOP 5 STRATEGIC PRIORITIES (specific, actionable recommendations)
    3. RISK MITIGATION STEPS (address identified weaknesses)
    4. GROWTH OPPORTUNITIES (based on valuation potential)
    5. NEXT 90 DAYS ACTION PLAN (immediate tactical steps)
    
    Format your response professionally with clear sections and bullet points.
    Be specific, actionable, and data-driven.
    """
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate strategy
        response = model.generate_content(context)
        strategy_text = response.text.strip()
        
        return {
            "strategy_report": strategy_text,
            "generation_status": "success",
            "model_used": "gemini-1.5-flash"
        }
    
    except Exception as e:
        # Fallback to rule-based strategy if Gemini fails
        return {
            "strategy_report": generate_fallback_strategy(all_results),
            "generation_status": "fallback",
            "error": str(e)
        }


def generate_fallback_strategy(all_results: Dict):
    """
    Generates a basic strategy when AI model is unavailable.
    """
    finance = all_results.get("finance", {})
    risk = all_results.get("risk", {})
    
    strategy = "# BUSINESS STRATEGY REPORT\n\n"
    
    strategy += "## EXECUTIVE SUMMARY\n"
    health = risk.get('health_status', 'Unknown')
    z_score = risk.get('z_score', 0)
    strategy += f"The company is currently in **{health}** financial health with an Altman Z-Score of {z_score:.2f}. "
    
    if z_score > 2.9:
        strategy += "Strong fundamentals indicate low bankruptcy risk and solid growth potential.\n\n"
    elif z_score >= 1.23:
        strategy += "Moderate risk profile requires strategic improvements to strengthen financial position.\n\n"
    else:
        strategy += "High risk profile demands immediate corrective actions to avoid financial distress.\n\n"
    
    strategy += "## TOP 5 STRATEGIC PRIORITIES\n\n"
    
    # Priority 1: Profitability
    profit_margin = finance.get('net_profit_margin', 0)
    if profit_margin < 0.1:
        strategy += "1. **Improve Profit Margins**: Current margin at {:.1f}% - implement cost reduction initiatives and pricing optimization\n".format(profit_margin * 100)
    else:
        strategy += "1. **Maintain Profitability**: Strong margins - focus on scaling operations while preserving efficiency\n"
    
    # Priority 2: Leverage
    dte = finance.get('debt_to_equity', 0)
    if dte > 2.0:
        strategy += "2. **Reduce Debt Burden**: High D/E ratio - prioritize debt paydown and explore refinancing options\n"
    elif dte > 1.0:
        strategy += "2. **Optimize Capital Structure**: Moderate leverage - balance growth investments with debt management\n"
    else:
        strategy += "2. **Strategic Leverage**: Low debt levels - consider strategic borrowing for growth initiatives\n"
    
    # Priority 3: Liquidity
    liquidity_risks = risk.get('liquidity_risks', [])
    if any("concern" in r.lower() or "issue" in r.lower() for r in liquidity_risks):
        strategy += "3. **Strengthen Liquidity**: Address working capital gaps and improve cash flow management\n"
    else:
        strategy += "3. **Cash Deployment**: Healthy liquidity - allocate excess cash to growth or shareholder returns\n"
    
    # Priority 4: Growth
    strategy += "4. **Revenue Growth**: Expand market share through product innovation and customer acquisition\n"
    
    # Priority 5: Risk Management
    strategy += "5. **Risk Mitigation**: Implement financial controls and diversify revenue streams\n\n"
    
    strategy += "## NEXT 90 DAYS ACTION PLAN\n\n"
    strategy += "- Month 1: Conduct detailed cost analysis and identify quick wins for margin improvement\n"
    strategy += "- Month 2: Develop cash flow forecast and implement working capital optimization\n"
    strategy += "- Month 3: Execute priority initiatives and establish KPI tracking dashboard\n"
    
    return strategy
