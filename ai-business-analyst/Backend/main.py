from fastapi import FastAPI
from pydantic import BaseModel

# 👇 ADD IT HERE (with other imports)
from agents.intake_agent import intake_agent


app = FastAPI()
@app.post("/finance_analysis")
def finance_analysis(business_data: dict):
    # Step 1: Intake check
    intake_result = intake_agent(business_data)
    if intake_result.get("status") != "complete":
        return intake_result

    # Step 2: Finance Analysis
    finance_result = analyze_financials(business_data)
    return {"status": "finance_complete", "finance_data": finance_result}

class AnalyzeRequest(BaseModel):
    business_name: str
    context: str
    balance_sheet: dict | None = None
    profit_loss: dict | None = None
    cash_flow: dict | None = None


@app.get("/")
def home():
    return {"message": "Backend is working"}


@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    combined_data = {}

    if data.balance_sheet:
        combined_data.update(data.balance_sheet)

    if data.profit_loss:
        combined_data.update(data.profit_loss)

    if data.cash_flow:
        combined_data.update(data.cash_flow)

    result = intake_agent(combined_data)

    return result