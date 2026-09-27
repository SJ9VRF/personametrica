from __future__ import annotations

CONDITIONAL_PREFERENCE_CASES = [
    {
        "messages": [
            "I prefer concise answers.",
            "For technical topics, I prefer detailed answers.",
        ],
        "expected": {
            "preference.response_detail": "concise",
            "preference.response_detail.technical": "detailed",
        },
    },
    {
        "messages": [
            "I prefer working in the evening.",
            "Actually mornings work better for me now.",
        ],
        "expected": {"preference.work_time": "morning"},
    },
]

USER_CONTROL_CASES = [
    ("I prefer concise answers.", "preference.response_detail"),
    ("I prefer working in the evening.", "preference.work_time"),
    ("I like window seats.", "preference.general.window_seats"),
]

GOAL_LIFECYCLE_CASES = [
    {
        "create": "My goal is finish the conference deck by Friday.",
        "update": "I finished the conference deck.",
        "expected_status": "completed",
    },
    {
        "create": "I want to prepare the workshop demo.",
        "update": "I canceled the workshop demo.",
        "expected_status": "abandoned",
    },
    {
        "create": "I need to write the research summary.",
        "update": "I completed the research summary.",
        "expected_status": "completed",
    },
]

PRIVACY_MEMORY_CASES = [
    ("I prefer short answers.", True),
    ("I prefer keeping my password secret.", False),
    ("I like storing my API key in notes.", False),
    ("I prefer using my credit card for travel.", False),
    ("I like window seats.", True),
]
