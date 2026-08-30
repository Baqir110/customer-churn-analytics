def get_retention_strategy(probability: float):
    if probability >= 0.70:
        return (
            "CRITICAL",
            "Trigger priority outbound retention call and offer 20% renewal discount.",
        )
    elif probability >= 0.40:
        return (
            "MODERATE",
            "Send proactive service check-in survey and targeted onboarding tutorial.",
        )
    return ("LOW", "Maintain standard automated customer engagement lifecycle.")
