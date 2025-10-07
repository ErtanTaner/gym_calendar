from flask import g
from ollama import ChatResponse, chat

class GymBot():
    def __init__(self, model="deepseek-r1:14b"):
        self.model = model

    def chat_with_bot(self, msg):
        pre_prompt = f"""
You are a JSON-only fitness program generator. You MUST return ONLY a valid JSON array of event objects with no additional text, explanations, or formatting.

USER INPUT:
- Weight: [number]kg
- Height: [number]m  
- Date range: [start date] - [end date]
- Conditions: [any mentioned conditions]

OUTPUT: ONLY JSON array following EXACTLY this structure:
[
  {{
    "id": "workout-1",
    "groupId": "fitness-program",
    "title": "Workout Name<br/>-- Exercise 1: sets x reps<br/>-- Exercise 2: sets x reps<br/>Notes",
    "start": "YYYY-MM-DDTHH:MM:SS",
    "end": "YYYY-MM-DDTHH:MM:SS",
    "allDay": false,
    "backgroundColor": "#color",
    "borderColor": "#color",
    "textColor": "#FFFFFF",
    "editable": true
  }}
]

RULES:
- NO EXPLANATIONS
- NO EXTRA TEXT
- ONLY JSON ARRAY
- Adapt exercises for any mentioned conditions
- Use <br/> for line breaks
- Colors: Strength=#4CAF50, Cardio=#2196F3, HIIT=#FF9800, Recovery=#9C27B0, Rest=#757575
- 5-6 workouts per week, 45-90 minutes each

IF YOU RETURN ANYTHING OTHER THAN PURE JSON, THE APPLICATION WILL FAIL.

BEGIN OUTPUT:

{msg}
"""
        return chat(model=self.model, messages=[{"role": "user", "content":msg}])
