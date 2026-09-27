from __future__ import annotations

# Independent language-form stress cases for the transparent local estimator.
# These are deliberately more varied than the simulator's training-like templates.
PREFERENCE_STRESS_CASES = [
    ("I prefer working in the morning.", "preference.work_time", "morning"),
    ("Evening works better for me when I focus.", "preference.work_time", "evening"),
    ("I usually work better at night.", "preference.work_time", "night"),
    ("Maybe I prefer working in the evening.", "preference.work_time", "evening"),
    ("I used to prefer mornings, but now evenings work better for me.", "preference.work_time", "evening"),
    ("Mornings no longer work for me; I prefer evenings now.", "preference.work_time", "evening"),
    ("I preferred evenings before, but morning is better now.", "preference.work_time", "morning"),
    ("For work, night is what works best for me now.", "preference.work_time", "night"),
    ("Keep answers concise.", "preference.response_detail", "concise"),
    ("I prefer short answers.", "preference.response_detail", "concise"),
    ("I want detailed answers.", "preference.response_detail", "detailed"),
    ("For technical topics, I prefer detailed explanations.", "preference.response_detail.technical", "detailed"),
    ("Technical questions should be detailed, but otherwise keep it concise.", "preference.response_detail.technical", "detailed"),
    ("I like window seats.", "preference.general.window_seats", "window seats"),
    ("I don't like red-eye flights.", "preference.dislike.red_eye_flights", "red-eye flights"),
]

REVERSAL_SEQUENCES = [
    (["I prefer working in the morning.", "Actually, evenings work better for me now."], "preference.work_time", "evening"),
    (["I usually work better at night.", "That changed; I prefer mornings now."], "preference.work_time", "morning"),
    (["I prefer short answers.", "For technical topics, give me detailed answers."], "preference.response_detail.technical", "detailed"),
]
