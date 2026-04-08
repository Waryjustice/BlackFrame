# Arthur AI - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Step 1: Navigate to Backend
```bash
cd ai-business-analyst/Backend
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key (Optional for basic testing)
```bash
# Copy the example .env file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 4: Run Tests
```bash
# Test all agents
python tests/test_all_agents.py

# Test API structure
python tests/test_api.py
```

### Step 5: Start the Server
```bash
uvicorn main:app --reload --port 8000
```

The server will start at: **http://localhost:8000**

### Step 6: Test the API

#### View API Documentation
Open in browser: http://localhost:8000/docs

#### Test Home Endpoint
```bash
curl http://localhost:8000/
```

#### Upload a Financial PDF
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@your_financial_document.pdf"
```

#### Retrieve Session Results
```bash
curl http://localhost:8000/session/{session_id}
```

---

## ☁️ Deploy on Vercel (Free Hobby)

This project is preconfigured for Vercel with:
- `api/index.py` (FastAPI entrypoint)
- `vercel.json` (routing all paths to FastAPI)
- root `requirements.txt` (Cloud/serverless install target)

### Vercel setup steps
1. Import your GitHub repo in Vercel.
2. If your repo root is `BlackFrame`, set **Root Directory** to `ai-business-analyst`.
3. Add environment variables:
   - `GOOGLE_API_KEY`
   - `CORS_ORIGINS` (example: `https://your-frontend.vercel.app`)
4. Deploy.

### Notes for serverless
- `POST /upload` is the primary endpoint and returns full analysis.
- `/session/{session_id}` uses in-memory storage and is not durable across serverless cold starts.

---

## ☁️ Deploy on Google Cloud Run

This project is now Cloud Run-ready with:
- `Dockerfile` at `ai-business-analyst/`
- `.dockerignore` to reduce build context
- FastAPI runtime command targeting `Backend.main:app`

### One-time setup
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

### Build image
```bash
cd ai-business-analyst
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/blackframe-api
```

### Deploy service
```bash
gcloud run deploy blackframe-api \
  --image gcr.io/YOUR_PROJECT_ID/blackframe-api \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=YOUR_GEMINI_KEY,CORS_ORIGINS=https://arthur-insight-ai.lovable.app
```

### Verify
```bash
curl https://YOUR_CLOUD_RUN_URL/
curl https://YOUR_CLOUD_RUN_URL/docs
```

> Hackathon tip: render `/upload` response directly in frontend; avoid relying on `/session/{id}` in autoscaled/serverless demos.

---

## 📊 What the System Does

Arthur AI analyzes financial documents through a 5-agent pipeline:

1. **Intake Agent** → Validates required data fields
2. **Finance Agent** → Calculates EBITDA, margins, ratios
3. **Valuation Agent** → Computes DCF, market multiples, liquidation value
4. **Risk Agent** → Evaluates Altman Z-Score and financial health
5. **Strategy Agent** → Generates AI-powered business recommendations

---

## 🧪 Test Without PDF (Manual Mode)

If you don't have a financial PDF, you can test the agents directly:

```python
from AGENTS.intake_agent import intake_agent
from AGENTS.finance_agent import analyze_financials
from AGENTS.Valution import valuation_agent
from AGENTS.risk_agent import risk_agent
from AGENTS.strategy_agent import generate_strategy

# Sample financial data
data = {
    "revenue": 5000000,
    "expenses": 3500000,
    "assets": 10000000,
    "liabilities": 3000000,
    "equity": 7000000,
    "debt": 2000000,
    "interest_expense": 150000,
    "depreciation": 200000
}

# Run pipeline
intake_result = intake_agent(data)
finance_result = analyze_financials(data)
valuation_result = valuation_agent(data, finance_result)
risk_result = risk_agent(data, finance_result)
strategy_result = generate_strategy({
    "raw_data": data,
    "finance": finance_result,
    "valuation": valuation_result,
    "risk": risk_result
})

# View results
print(f"Z-Score: {risk_result['z_score']}")
print(f"Health: {risk_result['health_status']}")
print(f"Valuation: ${valuation_result['intrinsic_value']['dcf_valuation']:,.0f}")
```

---

## 📈 Expected Output

```json
{
  "session_id": "abc-123-def",
  "status": "Analysis Complete",
  "extracted_data": {
    "revenue": 5000000,
    "expenses": 3500000,
    ...
  },
  "analysis_results": {
    "financial_metrics": {
      "ebitda": 1500000,
      "net_profit_margin": 0.30,
      "debt_to_equity": 0.29,
      "current_ratio": 3.33
    },
    "valuation_projections": {
      "intrinsic_value": {
        "dcf_valuation": 15947863.02
      },
      "market_multiples": {
        "Conservative": 6000000,
        "Market_Avg": 9000000,
        "Aggressive": 12000000
      }
    },
    "risk_assessment": {
      "z_score": 2.74,
      "health_status": "Grey Zone",
      "risk_level": "Medium"
    },
    "strategy_report": "# BUSINESS STRATEGY REPORT\n\n..."
  },
  "pipeline_status": {
    "intake": "✓ Complete",
    "finance": "✓ Complete",
    "valuation": "✓ Complete",
    "risk": "✓ Complete",
    "strategy": "✓ Complete"
  }
}
```

---

## 🔧 Troubleshooting

### Issue: "Module not found" error
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Server won't start
**Solution:** Check if port 8000 is available
```bash
# Windows
netstat -ano | findstr :8000

# Kill process if needed
Stop-Process -Id <PID>
```

### Issue: "Gemini API error"
**Solution:** The system works in fallback mode without Gemini. To use AI features:
1. Get API key from https://makersuite.google.com
2. Add to .env file
3. Restart server

### Issue: Tests failing
**Solution:** Ensure you're in the Backend directory
```bash
cd ai-business-analyst/Backend
python tests/test_all_agents.py
```

---

## 📚 Additional Resources

- **Full Documentation:** See README.md
- **Test Report:** See TEST_REPORT.md
- **API Docs:** http://localhost:8000/docs (when server is running)
- **Code Examples:** See tests/ folder

---

## 🎯 Next Steps

1. **Customize Agents:** Modify AGENTS/*.py files for your use case
2. **Add Frontend:** Build UI to interact with the API
3. **Deploy:** Use Docker or cloud platforms (AWS, Azure, GCP)
4. **Enhance:** Add more agents (competitor analysis, market research)

---

## 💡 Pro Tips

- Use `/docs` endpoint for interactive API testing
- Strategy agent uses fallback mode by default (no API key needed)
- All calculations are done locally - your data stays private
- Session storage is in-memory - use a database for production

---

**Need Help?** Check the test files in `tests/` for working examples!
