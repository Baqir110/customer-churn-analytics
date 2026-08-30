import hashlib
from typing import Tuple


def assign_ab_variant(customer_id: str) -> str:
    """Assigns customer deterministically to Variant A or B via MD5 hash."""
    hash_val = int(hashlib.md5(customer_id.encode()).hexdigest(), 16)
    return (
        "Variant_A_20_Percent_Discount"
        if (hash_val % 2 == 0)
        else "Variant_B_Free_Month_Extension"
    )


def get_retention_strategy(
    probability: float, customer_id: str | None = None
) -> Tuple[str, str, str]:
    """Returns risk tier, strategy description, and A/B campaign variant."""
    if probability >= 0.70:
        variant = (
            assign_ab_variant(customer_id) if customer_id else "Standard_Retention_Call"
        )
        return (
            "CRITICAL",
            f"Trigger priority outbound retention call and offer 20% renewal discount. Strategy: {variant}",
            variant,
        )
    elif probability >= 0.40:
        return (
            "MODERATE",
            "Send proactive service check-in survey and targeted onboarding tutorial.",
            "Control_Survey",
        )

    return (
        "LOW",
        "Maintain standard automated customer engagement lifecycle.",
        "None",
    )
