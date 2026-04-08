def intake_agent(data):
    required_fields = [
        "revenue",
        "expenses",
        "assets",
        "liabilities",
        "debt",
        "equity"
    ]

    missing = [field for field in required_fields if field not in data]

    if missing:
        return {
            "status": "missing_data",
            "missing_fields": missing
        }

    return {
        "status": "complete",
        "data": data
    }