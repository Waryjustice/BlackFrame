def intake_agent(data):
    required_fields = [
        "revenue",
        "expenses",
        "assets",
        "liabilities",
        "debt",
        "equity"
    ]

    # Treat missing keys/None as missing, but allow numeric 0.
    missing = [field for field in required_fields if field not in data or data.get(field) is None]

    if missing:
        return {
            "status": "missing_data",
            "missing_fields": missing
        }

    return {
        "status": "complete",
        "data": data
    }
