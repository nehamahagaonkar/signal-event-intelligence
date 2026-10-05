from datetime import datetime


SIGNAL_WEIGHTS = {
    "funding": 1.0,
    "expansion": 0.9,
    "hiring": 0.7,
    "product_launch": 0.6,
    "partnership": 0.5,
}


def calculate_signal_score(
    signal_type: str,
    confidence: float,
) -> float:
    weight = SIGNAL_WEIGHTS.get(
        signal_type.lower(),
        0.3,
    )

    return round(weight * confidence, 3)


def calculate_recency_weight(
    created_at: datetime,
) -> float:
    """
    Give more importance to recent signals.

    < 7 days   -> 1.00
    < 30 days  -> 0.90
    < 90 days  -> 0.75
    < 180 days -> 0.60
    180+ days  -> 0.40
    """

    age_days = (
        datetime.utcnow() - created_at
    ).days

    if age_days < 7:
        return 1.0

    if age_days < 30:
        return 0.9

    if age_days < 90:
        return 0.75

    if age_days < 180:
        return 0.6

    return 0.4


def calculate_diversity_bonus(signals) -> float:
    """
    Reward companies showing different types of signals.

    1 signal type  -> 0.00
    2 signal types -> 0.05
    3 signal types -> 0.10
    4 signal types -> 0.15
    5+ types       -> 0.20
    """

    if not signals:
        return 0.0

    unique_types = {
        signal.signal_type.lower()
        for signal in signals
    }

    diversity_bonus = min(
        len(unique_types) * 0.05 - 0.05,
        0.20,
    )

    return round(
        max(diversity_bonus, 0.0),
        3,
    )


def calculate_company_score(signals) -> float:
    if not signals:
        return 0.0

    weighted_scores = []

    for signal in signals:
        base_score = calculate_signal_score(
            signal.signal_type,
            signal.confidence,
        )

        recency = calculate_recency_weight(
            signal.created_at
        )

        weighted_score = (
            base_score * recency
        )

        weighted_scores.append(
            weighted_score
        )

    base_company_score = (
        sum(weighted_scores)
        / len(weighted_scores)
    )

    diversity_bonus = calculate_diversity_bonus(
        signals
    )

    final_score = (
        base_company_score
        + diversity_bonus
    )

    return round(
        min(final_score, 1.0),
        3,
    )