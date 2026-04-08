def intake_agent(data):
    required_fields = [
        "revenue",
        "expenses",
        "assets",
        "liabilities",
        "debt",
        "equity"
    ]

    # This line must have exactly 4 spaces of indentation
    missing = [field for field in required_fields if not data.get(field)]

    if missing:
        return {
            "status": "missing_data",
            "missing_fields": missing
        }

    return {
        "status": "complete",
        "data": data
    }