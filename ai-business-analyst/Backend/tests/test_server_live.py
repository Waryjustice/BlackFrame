"""
Live Server Test - Tests the running FastAPI server
"""

import os
import requests
from reportlab.pdfgen import canvas

SERVER_URL = "http://localhost:8000"

def test_home_endpoint():
    """Test the home endpoint"""
    print("\n[TEST 1] Home Endpoint (GET /)")
    print("-" * 60)
    
    response = requests.get(f"{SERVER_URL}/")
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    assert response.status_code == 200, "Home endpoint failed"
    assert "message" in response.json(), "Missing message field"
    print("   ✓ PASSED")
    return True

def test_session_endpoint_not_found():
    """Test session endpoint with invalid ID"""
    print("\n[TEST 2] Session Endpoint - Invalid ID (GET /session/invalid)")
    print("-" * 60)
    
    response = requests.get(f"{SERVER_URL}/session/invalid-session-id")
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    assert response.status_code == 404, "Should return 404 for invalid session"
    print("   ✓ PASSED - Correctly returns 404")
    return True

def test_upload_without_file():
    """Test upload endpoint without file"""
    print("\n[TEST 3] Upload Endpoint - No File (POST /upload)")
    print("-" * 60)
    
    response = requests.post(f"{SERVER_URL}/upload")
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    assert response.status_code == 422, "Should return 422 for missing file"
    print("   ✓ PASSED - Correctly validates missing file")
    return True


def _create_sample_pdf(path: str):
    c = canvas.Canvas(path)
    lines = [
        "Financial Statement FY2025",
        "Revenue: 5000000",
        "Expenses: 3200000",
        "Assets: 12000000",
        "Liabilities: 4500000",
        "Equity: 7500000",
        "Debt: 3000000",
        "Interest Expense: 180000",
        "Depreciation: 250000",
    ]
    y = 780
    for line in lines:
        c.drawString(72, y, line)
        y -= 22
    c.save()


def test_upload_with_pdf_and_session():
    """Test successful upload pipeline and session retrieval."""
    print("\n[TEST 4] Upload Endpoint - Real PDF Pipeline (POST /upload)")
    print("-" * 60)

    pdf_path = "live_test_financials.pdf"
    _create_sample_pdf(pdf_path)

    try:
        with open(pdf_path, "rb") as f:
            response = requests.post(
                f"{SERVER_URL}/upload",
                files={"file": ("live_test_financials.pdf", f, "application/pdf")},
            )

        print(f"   Status Code: {response.status_code}")
        payload = response.json()
        print(f"   Status: {payload.get('status')}")
        print(
            "   Extraction Mode: "
            f"{payload.get('extracted_data', {}).get('extraction_mode', 'unknown')}"
        )

        assert response.status_code == 200, "Upload should succeed with sample PDF"
        assert payload.get("status") == "Analysis Complete", "Unexpected analysis status"
        assert "analysis_results" in payload, "Missing analysis_results"
        assert "risk_assessment" in payload["analysis_results"], "Missing risk assessment"
        assert "strategy_report" in payload["analysis_results"], "Missing strategy report"

        session_id = payload.get("session_id")
        assert session_id, "Missing session_id in upload response"

        session_response = requests.get(f"{SERVER_URL}/session/{session_id}")
        print(f"   Session Status Code: {session_response.status_code}")
        assert session_response.status_code == 200, "Session retrieval should succeed"
        print("   ✓ PASSED - Full upload/session pipeline works")
        return True
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

def run_all_server_tests():
    """Run all live server tests"""
    print("\n" + "▓"*80)
    print("  ARTHUR AI - LIVE SERVER TEST SUITE")
    print("  Testing: http://localhost:8000")
    print("▓"*80)
    
    # Check if server is running
    print("\n[PRE-CHECK] Verifying server is online...")
    try:
        response = requests.get(f"{SERVER_URL}/", timeout=2)
        print("   ✓ Server is responding")
    except requests.exceptions.ConnectionError:
        print("   ✗ Server is not running!")
        print("\n   Please start the server first:")
        print("     cd Backend && uvicorn main:app --reload --port 8000")
        return False
    
    try:
        # Run tests
        test_home_endpoint()
        test_session_endpoint_not_found()
        test_upload_without_file()
        test_upload_with_pdf_and_session()
        
        print("\n" + "▓"*80)
        print("  🎉 ALL LIVE SERVER TESTS PASSED!")
        print("▓"*80)
        
        print("\n  📊 TEST SUMMARY:")
        print("     ✓ Home endpoint working")
        print("     ✓ Session endpoint working")
        print("     ✓ Upload endpoint validates inputs")
        print("     ✓ Full PDF upload pipeline working")
        print()
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("Installing requests library...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    
    success = run_all_server_tests()
    sys.exit(0 if success else 1)
