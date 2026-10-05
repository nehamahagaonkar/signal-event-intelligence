SIGNAL_RULES = {
    "funding": {
        "keywords": [
            "funding",
            "raised",
            "raises",
            "series a",
            "series b",
            "series c",
            "investment",
            "invested",
            "capital",
        ],
        "confidence": 0.90,
    },
    "hiring": {
        "keywords": [
            "hiring",
            "hired",
            "recruiting",
            "recruitment",
            "jobs",
            "employees",
            "talent",
            "workforce",
        ],
        "confidence": 0.85,
    },
    "expansion": {
        "keywords": [
            "expansion",
            "expanding",
            "new office",
            "new market",
            "entered",
            "launches in",
            "expanding operations",
        ],
        "confidence": 0.88,
    },
    "product_launch": {
        "keywords": [
            "launch",
            "launched",
            "new product",
            "new service",
            "released",
            "release",
            "unveiled",
        ],
        "confidence": 0.80,
    },
    "partnership": {
        "keywords": [
            "partnership",
            "partnered",
            "collaboration",
            "strategic partnership",
            "agreement",
        ],
        "confidence": 0.75,
    },
}


def extract_signals(
    title: str,
    description: str | None = None,
):
    text = f"{title} {description or ''}".lower()

    signals = []

    for signal_type, rule in SIGNAL_RULES.items():
        matched_keywords = [
            keyword
            for keyword in rule["keywords"]
            if keyword in text
        ]

        if matched_keywords:
            signals.append(
                {
                    "signal_type": signal_type,
                    "signal_value": (
                        f"Detected keywords: "
                        f"{', '.join(matched_keywords)}"
                    ),
                    "confidence": rule["confidence"],
                }
            )

    return signals