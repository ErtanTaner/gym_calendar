import os
import json
from flask import g
from ollama import ChatResponse, chat
from openai import OpenAI

class GymBot():
    def __init__(self, model="deepseek-r1:14b", token=None):
        self.model = model
        self.local = True if os.environ.get("LOCAL") == "true" else False
        self.token = token

    def chat_with_bot(self, msg, history):
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
    "groupId": "fitness-program",
    "title": "Workout Name<br/>-- Exercise 1: sets x reps<br/>-- Exercise 2: sets x reps<br/>Notes",
    "start": "YYYY-MM-DDTHH:MM:SS",
    "end": "YYYY-MM-DDTHH:MM:SS",
    "allDay": false,
    "backgroundColor": "#color",
    "borderColor": "#color",
    "textColor": "#FFFFFF",
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

"""
        if self.local == False:
            base_message = [{"role": "system", "content": pre_prompt}]
            messages = history + [{"role": "user", "content": msg}] if len(history) else [{"role": "user", "content": msg}] 
            final = base_message + messages
            client = OpenAI(api_key=self.token, base_url="https://api.deepseek.com")
            res = client.chat.completions.create(
                model=self.model,
                messages=final,
                stream=False
            )
            print(f"\n*********res.usage {res.usage}*********\n")
            res_content = res.choices[0].message.content 
            messages.append({"role": "assistant", "content": res_content})
            return (res_content, messages)

        else:
            return chat(model=self.model, messages=[{"role": "user", "content":pre_prompt + msg}])["message"]["content"]
