import os
import uuid
import json
import re
from io import BytesIO
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from pypdf import PdfReader

# --- AGENT IMPORTS ---
# These pull the logic from the files in your AGENTS folder
from AGENTS.intake_agent import intake_agent
from AGENTS.finance_agent import analyze_financials
from AGENTS.Valution import valuation_agent
from AGENTS.risk_agent import risk_agent
from AGENTS.strategy_agent import generate_strategy

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI(title="AI Business Analyst - Multi-Agent System")

# Simple In-Memory Session Storage for Hackathon
sessions: Dict[str, dict] = {}

REQUIRED_FINANCIAL_FIELDS = (
    "revenue",
    "expenses",
    "assets",
    "liabilities",
    "equity",
    "debt",
    "interest_expense",
    "depreciation",
)


def _to_float(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return 0.0

    cleaned = str(value).strip().replace(",", "").replace("$", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = f"-{cleaned[1:-1]}"
    return float(cleaned)


def _normalize_financial_payload(payload: Dict[str, Any]) -> Dict[str, float]:
    normalized: Dict[str, float] = {}
    for field in REQUIRED_FINANCIAL_FIELDS:
        raw_value = payload.get(field, 0)
        try:
            normalized[field] = _to_float(raw_value)
        except (TypeError, ValueError):
            normalized[field] = 0.0
    return normalized


def _extract_financials_locally(content: bytes) -> Dict[str, float]:
    reader = PdfReader(BytesIO(content))
    raw_text = "\n".join(page.extract_text() or "" for page in reader.pages).lower()

    patterns = {
        "revenue": r"revenue[^0-9\-]*([-]?\d[\d,]*(?:\.\d+)?)",
        "expenses": r"expenses?[^0-9\-]*([-]?\d[\d,]*(?:\.\d+)?)",
        "assets": r"assets?[^0-9\-]*([-]?\d[\d,]*(?:\.\d+)?)",
        "liabilities": r"liabilities?[^0-9\-]*([-]?\d[\d,]*(?:\.\d+)?)",
        "equity": r"equity[^0-9\-]*([-]?\d[\d,]*(?:\.\d+)?)",
        "debt": r"debt[^0-9\-]*([-]?\d[\d,]*(?:\.\d+)?)",
        "interest_expense": r"interest(?:\s+expense)?[^0-9\-]*([-]?\d[\d,]*(?:\.\d+)?)",
        "depreciation": r"depreciation[^0-9\-]*([-]?\d[\d,]*(?:\.\d+)?)",
    }

    local_payload: Dict[str, float] = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, raw_text, flags=re.IGNORECASE)
        if match:
            local_payload[field] = _to_float(match.group(1))
        else:
            local_payload[field] = 0.0

    if all(local_payload[field] == 0 for field in REQUIRED_FINANCIAL_FIELDS):
        raise ValueError("Local PDF parser could not extract financial values.")

    return local_payload

@app.get("/")
def home():
    return {"message": "Multi-Agent Business Analyst Online"}

# Agent 1: PDF Extraction Logic (Gemini 1.5 Flash)
async def extract_financials_from_pdf(file: UploadFile):
    # Read PDF bytes
    content = await file.read()

    prompt = """
    Analyze this financial document. Extract the following values into a valid JSON format:
    revenue, expenses, assets, liabilities, equity, debt, interest_expense, depreciation.
    If a value is missing, set it to 0. 
    Return ONLY the JSON object.
    """

    gemini_error: Exception | None = None
    api_key = os.getenv("GOOGLE_API_KEY")

    if api_key:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                [
                    prompt,
                    {"mime_type": "application/pdf", "data": content},
                ]
            )
            text = response.text.replace("```json", "").replace("```", "").strip()
            gemini_payload = json.loads(text)
            normalized = _normalize_financial_payload(gemini_payload)
            normalized["extraction_mode"] = "gemini"
            return normalized
        except Exception as error:
            gemini_error = error
    else:
        gemini_error = RuntimeError("GOOGLE_API_KEY is not configured.")

    # Explicit fallback for local development and testability.
    local_payload = _extract_financials_locally(content)
    local_payload["extraction_mode"] = "local_fallback"
    if gemini_error:
        local_payload["extraction_warning"] = str(gemini_error)
    return local_payload

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    try:
        # 1. BRAIN: Gemini Extraction (Raw Data)
        extracted_data = await extract_financials_from_pdf(file)
        
        # 2. AGENT 1: Intake (Validation)
        # Checks if we have the required fields to move forward
        intake_res = intake_agent(extracted_data)
        if intake_res["status"] == "missing_data":
            return {
                "session_id": session_id,
                "status": "Incomplete Data",
                "missing_fields": intake_res["missing_fields"]
            }

        # 3. AGENT 2: Finance (Calculations)
        # Calculates EBITDA, Profit Margin, Debt-to-Equity, etc.
        finance_results = analyze_financials(extracted_data)
        
        # 4. AGENT 3: Valuation (The "Crazy" High-Detail Math)
        # Uses the raw data and the EBITDA from Agent 2
        val_results = valuation_agent(extracted_data, finance_results)
        
        # 5. AGENT 4: Risk Assessment (Altman Z-Score)
        # Evaluates bankruptcy risk and financial health
        risk_results = risk_agent(extracted_data, finance_results)
        
        # 6. AGENT 5: Strategy Generation (AI-Powered Recommendations)
        # Combines all analysis to generate actionable strategy
        all_results = {
            "raw_data": extracted_data,
            "finance": finance_results,
            "valuation": val_results,
            "risk": risk_results
        }
        strategy_results = generate_strategy(all_results)
        
        # 7. STORE EVERYTHING IN SESSION
        sessions[session_id] = {
            "raw_data": extracted_data,
            "finance": finance_results,
            "valuation": val_results,
            "risk": risk_results,
            "strategy": strategy_results
        }
        
        # 8. RETURN COMPREHENSIVE FINAL REPORT TO FRONTEND
        return {
            "session_id": session_id,
            "status": "Analysis Complete",
            "extracted_data": extracted_data,
            "analysis_results": {
                "financial_metrics": finance_results,
                "valuation_projections": val_results,
                "risk_assessment": risk_results,
                "strategy_report": strategy_results.get("strategy_report", "")
            },
            "message": "All 5 agents successfully processed the document.",
            "pipeline_status": {
                "intake": "✓ Complete",
                "finance": "✓ Complete",
                "valuation": "✓ Complete",
                "risk": "✓ Complete",
                "strategy": "✓ Complete"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System Error: {str(e)}")

# Add a specific endpoint to check a session later
@app.get("/session/{session_id}")
def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]
