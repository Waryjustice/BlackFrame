import os
import uuid
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from dotenv import load_dotenv
import google.generativeai as genai

# --- AGENT IMPORTS ---
# These pull the logic from the files in your /agents folder
from agents.intake_agent import intake_agent
from agents.finance_agent import analyze_financials
from agents.valuation_agent import valuation_agent

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI(title="AI Business Analyst - Multi-Agent System")

# Simple In-Memory Session Storage for Hackathon
sessions: Dict[str, dict] = {}

@app.get("/")
def home():
    return {"message": "Multi-Agent Business Analyst Online"}

# Agent 1: PDF Extraction Logic (Gemini 1.5 Flash)
async def extract_financials_from_pdf(file: UploadFile):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Read PDF bytes
    content = await file.read()
    
    prompt = """
    Analyze this financial document. Extract the following values into a valid JSON format:
    revenue, expenses, assets, liabilities, equity, debt, interest_expense, depreciation.
    If a value is missing, set it to 0. 
    Return ONLY the JSON object.
    """
    
    # Gemini 1.5 Flash handles PDF bytes directly
    response = model.generate_content([
        prompt,
        {"mime_type": "application/pdf", "data": content}
    ])
    
    # Basic cleaning of the string to ensure it's JSON
    text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

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
        
        # 5. STORE EVERYTHING IN SESSION
        sessions[session_id] = {
            "raw_data": extracted_data,
            "finance": finance_results,
            "valuation": val_results
        }
        
        # 6. RETURN FINAL REPORT TO FRONTEND
        return {
            "session_id": session_id,
            "status": "Analysis Complete",
            "extracted_data": extracted_data,
            "analysis_results": {
                "financial_metrics": finance_results,
                "valuation_projections": val_results
            },
            "message": "All agents successfully processed the document."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System Error: {str(e)}")

# Add a specific endpoint to check a session later
@app.get("/session/{session_id}")
def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]