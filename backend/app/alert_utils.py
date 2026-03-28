def build_alert_message(probability: float, status: str) -> str:
    if status == "Critical":
        return f"Critical alert: predicted failure probability is {probability:.2%}."
    if status == "Warning":
        return f"Warning: equipment needs inspection. Failure probability is {probability:.2%}."
    return f"System normal. Failure probability is {probability:.2%}."
