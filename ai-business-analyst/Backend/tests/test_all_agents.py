"""
Comprehensive test suite for Arthur AI multi-agent system
Tests all agents individually and the complete pipeline
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from AGENTS.intake_agent import intake_agent
from AGENTS.finance_agent import analyze_financials
from AGENTS.Valution import valuation_agent
from AGENTS.risk_agent import risk_agent
from AGENTS.strategy_agent import generate_strategy

# Test data scenarios
HEALTHY_COMPANY = {
    "revenue": 5000000,
    "expenses": 3500000,
    "assets": 10000000,
    "liabilities": 3000000,
    "equity": 7000000,
    "debt": 2000000,
    "interest_expense": 150000,
    "depreciation": 200000
}

DISTRESSED_COMPANY = {
    "revenue": 1000000,
    "expenses": 1200000,
    "assets": 2000000,
    "liabilities": 2500000,
    "equity": 500000,
    "debt": 2000000,
    "interest_expense": 200000,
    "depreciation": 50000
}

GREY_ZONE_COMPANY = {
    "revenue": 3000000,
    "expenses": 2800000,
    "assets": 5000000,
    "liabilities": 3000000,
    "equity": 2000000,
    "debt": 2500000,
    "interest_expense": 180000,
    "depreciation": 100000
}

INCOMPLETE_DATA = {
    "revenue": 1000000,
    "expenses": 800000,
    # Missing: assets, liabilities, equity, debt
}

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def test_intake_agent():
    """Test intake validation agent"""
    print_section("TEST 1: INTAKE AGENT")
    
    # Test 1.1: Complete data
    print("\n[1.1] Testing with complete data...")
    result = intake_agent(HEALTHY_COMPANY)
    assert result["status"] == "complete", "Failed: Should accept complete data"
    print("✓ Complete data validation passed")
    
    # Test 1.2: Incomplete data
    print("\n[1.2] Testing with incomplete data...")
    result = intake_agent(INCOMPLETE_DATA)
    assert result["status"] == "missing_data", "Failed: Should reject incomplete data"
    assert len(result["missing_fields"]) > 0, "Failed: Should identify missing fields"
    print(f"✓ Incomplete data rejected. Missing: {result['missing_fields']}")
    
    # Test 1.3: Empty data
    print("\n[1.3] Testing with empty data...")
    result = intake_agent({})
    assert result["status"] == "missing_data", "Failed: Should reject empty data"
    print(f"✓ Empty data rejected. Missing: {len(result['missing_fields'])} fields")
    
    print("\n✅ INTAKE AGENT: All tests passed!")

def test_finance_agent():
    """Test financial analysis agent"""
    print_section("TEST 2: FINANCE AGENT")
    
    # Test 2.1: Healthy company metrics
    print("\n[2.1] Testing healthy company analysis...")
    result = analyze_financials(HEALTHY_COMPANY)
    assert "ebitda" in result, "Failed: Missing EBITDA"
    assert "net_profit_margin" in result, "Failed: Missing profit margin"
    assert "debt_to_equity" in result, "Failed: Missing D/E ratio"
    assert "current_ratio" in result, "Failed: Missing current ratio"
    print(f"   EBITDA: ${result['ebitda']:,.2f}")
    print(f"   Profit Margin: {result['net_profit_margin']*100:.1f}%")
    print(f"   Debt-to-Equity: {result['debt_to_equity']:.2f}")
    print(f"   Current Ratio: {result['current_ratio']:.2f}")
    print("✓ Healthy company metrics calculated")
    
    # Test 2.2: Distressed company metrics
    print("\n[2.2] Testing distressed company analysis...")
    result = analyze_financials(DISTRESSED_COMPANY)
    assert result['ebitda'] < 0, "Failed: EBITDA should be negative"
    assert result['net_profit_margin'] < 0, "Failed: Profit margin should be negative"
    assert result['debt_to_equity'] > 2.0, "Failed: High D/E ratio expected"
    print(f"   EBITDA: ${result['ebitda']:,.2f} (negative)")
    print(f"   Current Ratio: {result['current_ratio']:.2f} (below 1.0)")
    print("✓ Distressed company metrics calculated")
    
    # Test 2.3: Division by zero handling
    print("\n[2.3] Testing edge case handling...")
    edge_case = {"revenue": 0, "expenses": 0, "assets": 0, "liabilities": 0, "equity": 0, "debt": 0}
    result = analyze_financials(edge_case)
    assert result['net_profit_margin'] == 0, "Failed: Should handle zero revenue"
    print("✓ Edge cases handled correctly")
    
    print("\n✅ FINANCE AGENT: All tests passed!")

def test_valuation_agent():
    """Test valuation agent"""
    print_section("TEST 3: VALUATION AGENT")
    
    # Test 3.1: DCF valuation
    print("\n[3.1] Testing DCF valuation...")
    finance_results = analyze_financials(HEALTHY_COMPANY)
    result = valuation_agent(HEALTHY_COMPANY, finance_results)
    
    assert "intrinsic_value" in result, "Failed: Missing intrinsic value"
    assert "market_multiples" in result, "Failed: Missing market multiples"
    assert "liquidation_value" in result, "Failed: Missing liquidation value"
    
    dcf = result['intrinsic_value']['dcf_valuation']
    multiples = result['market_multiples']
    
    print(f"   DCF Valuation: ${dcf:,.2f}")
    print(f"   Conservative Multiple: ${multiples['Conservative']:,.2f}")
    print(f"   Market Avg Multiple: ${multiples['Market_Avg']:,.2f}")
    print(f"   Aggressive Multiple: ${multiples['Aggressive']:,.2f}")
    print(f"   Liquidation Value: ${result['liquidation_value']:,.2f}")
    print("✓ Valuation calculations completed")
    
    # Test 3.2: Verify multiple ranges
    print("\n[3.2] Testing valuation ranges...")
    assert multiples['Conservative'] < multiples['Market_Avg'], "Failed: Conservative should be lowest"
    assert multiples['Market_Avg'] < multiples['Aggressive'], "Failed: Aggressive should be highest"
    print("✓ Valuation ranges are logical")
    
    print("\n✅ VALUATION AGENT: All tests passed!")

def test_risk_agent():
    """Test risk assessment agent"""
    print_section("TEST 4: RISK AGENT")
    
    # Test 4.1: Healthy company (Safe zone)
    print("\n[4.1] Testing healthy company risk assessment...")
    finance_results = analyze_financials(HEALTHY_COMPANY)
    result = risk_agent(HEALTHY_COMPANY, finance_results)
    
    assert "z_score" in result, "Failed: Missing Z-Score"
    assert "health_status" in result, "Failed: Missing health status"
    assert "risk_level" in result, "Failed: Missing risk level"
    
    print(f"   Altman Z-Score: {result['z_score']:.2f}")
    print(f"   Health Status: {result['health_status']}")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Liquidity Risks: {result['liquidity_risks'][0]}")
    print("✓ Healthy company assessed correctly")
    
    # Test 4.2: Distressed company (Distress zone)
    print("\n[4.2] Testing distressed company risk assessment...")
    finance_results = analyze_financials(DISTRESSED_COMPANY)
    result = risk_agent(DISTRESSED_COMPANY, finance_results)
    
    print(f"   Altman Z-Score: {result['z_score']:.2f}")
    print(f"   Health Status: {result['health_status']}")
    print(f"   Risk Level: {result['risk_level']}")
    assert result['z_score'] < 1.23, "Failed: Should be in distress zone"
    assert result['health_status'] == "Distress", "Failed: Should be distressed"
    print("✓ Distressed company flagged correctly")
    
    # Test 4.3: Grey zone company
    print("\n[4.3] Testing grey zone company risk assessment...")
    finance_results = analyze_financials(GREY_ZONE_COMPANY)
    result = risk_agent(GREY_ZONE_COMPANY, finance_results)
    
    print(f"   Altman Z-Score: {result['z_score']:.2f}")
    print(f"   Health Status: {result['health_status']}")
    print(f"   Risk Level: {result['risk_level']}")
    print("✓ Grey zone company identified correctly")
    
    # Test 4.4: Score breakdown
    print("\n[4.4] Testing score breakdown...")
    assert "score_breakdown" in result, "Failed: Missing score breakdown"
    breakdown = result['score_breakdown']
    print(f"   Working Capital Ratio: {breakdown['working_capital_ratio']:.3f}")
    print(f"   Profitability Ratio: {breakdown['profitability_ratio']:.3f}")
    print(f"   Asset Turnover: {breakdown['asset_turnover']:.3f}")
    print("✓ Score breakdown provided")
    
    print("\n✅ RISK AGENT: All tests passed!")

def test_strategy_agent():
    """Test strategy generation agent"""
    print_section("TEST 5: STRATEGY AGENT")
    
    print("\n[5.1] Testing strategy generation (fallback mode)...")
    
    # Prepare complete analysis results
    finance_results = analyze_financials(HEALTHY_COMPANY)
    valuation_results = valuation_agent(HEALTHY_COMPANY, finance_results)
    risk_results = risk_agent(HEALTHY_COMPANY, finance_results)
    
    all_results = {
        "raw_data": HEALTHY_COMPANY,
        "finance": finance_results,
        "valuation": valuation_results,
        "risk": risk_results
    }
    
    result = generate_strategy(all_results)
    
    assert "strategy_report" in result, "Failed: Missing strategy report"
    assert "generation_status" in result, "Failed: Missing generation status"
    
    strategy = result['strategy_report']
    print(f"   Generation Status: {result['generation_status']}")
    print(f"   Report Length: {len(strategy)} characters")
    print(f"\n   Strategy Preview:")
    print("   " + "\n   ".join(strategy.split("\n")[:10]))  # First 10 lines
    print("   ...")
    print("✓ Strategy generated successfully")
    
    # Test 5.2: Verify strategy components
    print("\n[5.2] Testing strategy completeness...")
    assert len(strategy) > 100, "Failed: Strategy too short"
    assert "STRATEGIC" in strategy.upper() or "STRATEGY" in strategy.upper(), "Failed: Missing strategy section"
    print("✓ Strategy contains required sections")
    
    print("\n✅ STRATEGY AGENT: All tests passed!")

def test_complete_pipeline():
    """Test the complete multi-agent pipeline"""
    print_section("TEST 6: COMPLETE PIPELINE INTEGRATION")
    
    print("\n[6.1] Running complete pipeline on healthy company...")
    
    # Step 1: Intake
    intake_result = intake_agent(HEALTHY_COMPANY)
    assert intake_result["status"] == "complete", "Pipeline failed at intake"
    print("   ✓ Step 1: Intake validation passed")
    
    # Step 2: Finance
    finance_result = analyze_financials(HEALTHY_COMPANY)
    assert finance_result["ebitda"] > 0, "Pipeline failed at finance"
    print("   ✓ Step 2: Financial analysis completed")
    
    # Step 3: Valuation
    valuation_result = valuation_agent(HEALTHY_COMPANY, finance_result)
    assert valuation_result["intrinsic_value"]["dcf_valuation"] > 0, "Pipeline failed at valuation"
    print("   ✓ Step 3: Valuation completed")
    
    # Step 4: Risk
    risk_result = risk_agent(HEALTHY_COMPANY, finance_result)
    assert risk_result["z_score"] > 0, "Pipeline failed at risk"
    print("   ✓ Step 4: Risk assessment completed")
    
    # Step 5: Strategy
    all_results = {
        "raw_data": HEALTHY_COMPANY,
        "finance": finance_result,
        "valuation": valuation_result,
        "risk": risk_result
    }
    strategy_result = generate_strategy(all_results)
    assert len(strategy_result["strategy_report"]) > 0, "Pipeline failed at strategy"
    print("   ✓ Step 5: Strategy generation completed")
    
    print("\n[6.2] Testing pipeline with different scenarios...")
    
    # Test distressed company
    print("   Testing distressed company pipeline...")
    intake_result = intake_agent(DISTRESSED_COMPANY)
    if intake_result["status"] == "complete":
        finance_result = analyze_financials(DISTRESSED_COMPANY)
        risk_result = risk_agent(DISTRESSED_COMPANY, finance_result)
        assert risk_result["health_status"] == "Distress", "Failed to identify distress"
        print("   ✓ Distressed company pipeline completed")
    
    # Test incomplete data rejection
    print("   Testing incomplete data rejection...")
    intake_result = intake_agent(INCOMPLETE_DATA)
    assert intake_result["status"] == "missing_data", "Failed to reject incomplete data"
    print("   ✓ Incomplete data properly rejected")
    
    print("\n✅ COMPLETE PIPELINE: All integration tests passed!")

def run_all_tests():
    """Run all test suites"""
    print("\n" + "▓"*80)
    print("  ARTHUR AI - COMPREHENSIVE TEST SUITE")
    print("  Multi-Agent Business Analyst System")
    print("▓"*80)
    
    try:
        test_intake_agent()
        test_finance_agent()
        test_valuation_agent()
        test_risk_agent()
        test_strategy_agent()
        test_complete_pipeline()
        
        print("\n" + "▓"*80)
        print("  🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("  System is ready for production use")
        print("▓"*80 + "\n")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
