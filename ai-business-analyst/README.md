# Arthur AI

# Made by Dhrumil soni and shaurya singh

> **Your AI business strategist, always analyzing, always planning.**

Arthur AI is a **multi-agent AI system** designed for the tech sector that automatically analyzes businesses, evaluates financial health, identifies risks, benchmarks competitors, and generates actionable growth strategies.  

Arthur AI saves time, reduces errors, improves decision-making, and increases operational efficiency—reducing manual effort and hiring costs.

---

## 🏆 Tech Sector Innovation Hackathon 2026

**Competing for:**
- 🥇 Grand Prize – AI for Business Analytics & Strategy
- 🥇 Grand Prize – Automation & Decision Intelligence
- 🏅 Best Multi-Agent System
- 🏅 Best Financial Analytics Solution
- 🏅 Best AI-Driven Strategy Engine

---

## 📖 Overview

Arthur AI is a **multi-agent AI system** built for tech companies to streamline business analysis and strategy planning.  

**Key Features:**
- 📂 **Intake & Validation Agent:** Collects financials and converts them into structured data
- 📊 **Financial Processing Agent:** Extracts key metrics, calculates ratios, and structures financial data
- 💰 **Valuation Agent:** Computes DCF, asset-based, and comparable valuations
- ⚠️ **Risk Agent:** Evaluates liquidity, debt, and operational risks
- 📈 **Competitor Analysis Agent:** Benchmarks performance, growth, and market positioning
- 💣 **Decision & Growth Agent:** Generates actionable business strategies and expansion plans

**Agent Workflow:**  

┌───────────────────────────────────────────────┐
│                 DATA SOURCES                  │
│ (Financial statements, CRM, ERP, Market)     │
└─────────────────────────┬─────────────────────┘
                          │ Structured & Raw Data
                          ▼
┌───────────────────────────────────────────────┐
│          AGENT 1: INTAKE & VALIDATION         │
│ • Collects PDFs, Excel, Forms                 │
│ • Checks completeness & data quality         │
│ • Converts to structured JSON/CSV            │
└───────────────┬──────────────────────────────┘
                ▼
┌───────────────────────────────────────────────┐
│         AGENT 2: FINANCIAL PROCESSING         │
│ • Extracts key metrics (Revenue, Profit)     │
│ • Calculates ratios: EBITDA, Margins         │
│ • Structures financial database              │
└───────────────┬──────────────────────────────┘
                ▼
┌───────────────────────────┬──────────────────┐
│       AGENT 3: VALUATION  │    AGENT 4: RISK │
│ • DCF Valuation           │ • Liquidity Ratios│
│ • Asset-Based Valuation   │ • Debt-to-Equity │
│ • Comparable Analysis     │ • SWOT Analysis  │
└───────────────┬───────────┴──────────────┬───┘
                ▼                          ▼
         ┌─────────────┐              ┌─────────────┐
         │ AGENT 5:    │              │ Decision &  │
         │ Competitor  │              │ Growth Agent│
         │ Analysis    │              │             │
         │ Benchmarks  │              │ Combines all│
         │ Industry Avg│              │ outputs,    │
         └─────┬───────┘              │ generates   │
               ▼                      │ strategy    │
               └─────────► OUTPUT DASHBOARD ◄───────┘

**Architecture Highlights:**
- Agents communicate via **structured messaging protocols**
- Fully modular: new agents can be added without rewriting workflows
- Outputs include **KPIs, risk scores, competitor benchmarking, and growth plans**
- Backend built on **FastAPI + Uvicorn** for lightweight, scalable deployment
- **n8n** automation used for workflow orchestration and scheduling

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- FastAPI & Uvicorn
- Git
- Google Sheets or Excel for outputs
- Access to financial data (CSV, PDF, or API)

---

### Installation

```bash
# Clone repository
git clone https://github.com/liege/arthur-ai.git
cd arthur-ai

# Install Python dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

Demo Scenarios

Test Arthur AI with simulated business cases:\
# Scenario 1: Startup financial health check
python examples/demo_startup_analysis.py

# Scenario 2: Tech scale-up risk assessment
python examples/demo_scaleup_risk.py

# Scenario 3: Competitor benchmarking & growth plan
python examples/demo_competitor_growth.py


| KPI              | Value                           | Benchmark | Status |
| ---------------- | ------------------------------- | --------- | ------ |
| Revenue Growth   | 12%                             | 15%       | ⚠️     |
| EBITDA Margin    | 22%                             | 25%       | ⚠️     |
| Debt-to-Equity   | 1.2                             | <1        | ⚠️     |
| Competitor Rank  | 3/5                             | -         | ✅      |
| Suggested Action | Increase R&D spend, reduce OPEX | -         | ✅      |

Agents Breakdown
1️⃣ Intake & Validation Agent
Collects PDFs, Excel, API data
Validates completeness and correctness
Converts raw data to structured JSON/CSV
Logs missing or inconsistent data
Tech: Python, PyPDF2, Pandas

2️⃣ Financial Processing Agent
Extracts revenue, expenses, profit, EBITDA
Calculates margins, growth rates, cash flow metrics
Structures data for downstream agents
Tech: Pandas, NumPy

3️⃣ Valuation Agent
Computes DCF, asset-based, comparable valuations
Provides valuation range & sensitivity analysis
Supports investor & strategic decisions
Tech: NumPy, SciPy, financial modeling formulas

4️⃣ Risk Agent
Calculates liquidity, profitability, and solvency ratios
Generates risk scoring (high, medium, low)
Performs SWOT analysis
Tech: Pandas, AI scoring models

5️⃣ Competitor Analysis Agent
Compares company KPIs to industry benchmarks
Provides market positioning and growth comparison
Highlights gaps vs competitors
Tech: Web scraping, APIs, Pandas

6️⃣ Decision & Growth Agent
Combines financial, risk, and competitor outputs
Generates strategic recommendations
Suggests operational and expansion plans
Tech: Gemini powered reasoning on the data provided


Example Use Case

Startup Analysis:

1.Upload P&L, Balance Sheet, Cash Flow PDF
2.Intake agent validates & structures data
3.Finance agent extracts metrics
4.Risk agent scores company health
5.Competitor agent benchmarks growth
6.Decision agent generates growth plan:


- Increase R&D budget by 10%
- Reduce operational costs by 5%
- Target emerging market segments
- Raise Series A with improved valuation metrics

Impact:
Manual analysis: 6 hours → Arthur AI: 10 mins

🛠️ Technologies Used
Python 3.11
FastAPI + Uvicorn
Pandas, NumPy, SciPy
PDF/Excel parsers: PyPDF2, openpyxl
AI Gemoni for decision and strategy agent
GitHub for version control

💡 Key Design Decisions
Modular multi-agent architecture for scalability
Structured workflow communication for agent outputs
Integration with common business formats (CSV, PDF, Excel)
Automated decision-making to reduce human intervention
KPIs, risk scoring, competitor benchmarking integrated in a single dashboard


| Step | Agent      | Action           | Output                    |
| ---- | ---------- | ---------------- | ------------------------- |
| 1    | Intake     | Parse PDFs       | Structured JSON           |
| 2    | Finance    | Extract metrics  | Revenue, EBITDA, Margins  |
| 3    | Risk       | Calculate ratios | Risk Score: Medium        |
| 4    | Competitor | Benchmark        | Position: 3/5             |
| 5    | Decision   | Recommend growth | Increase R&D, reduce OPEX |

Scenario 2: Scale-Up Risk Assessment
Detect liquidity issues
Forecast cash runway
Evaluate debt impact on growth
Automated growth recommendations
Reduce manual risk assessment time from 2 days → 15 mins

Scenario 3: Competitor Benchmarking
Compare KPIs to 5 top competitors
Identify market gaps
Suggest expansion and investment opportunities
Generates visual dashboard with KPIs, ratios, and growth potential

# Run all tests
pytest

# Run individual scenarios
python examples/demo_startup_analysis.py
python examples/demo_scaleup_risk.py
python examples/demo_competitor_growth.py


👥 Team name - Blackframe 

