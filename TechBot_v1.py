from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow frontend to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversation per session (simplified)
conversation_history = []

@app.post("/start")
def start_interview(data: dict):
    skill = data.get("skill", "Python")
    conversation_history.clear()
    conversation_history.append({
        "role": "system",
        # "content": f"You are an HR interviewer. The candidate knows {skill}. Ask one question at a time. Do NOT give answers or feedback. Wait for the candidate response before asking the next question."
        "content": f"""
You are an HR interviewer conducting a technical interview.
Follow these strict rules:
1. Ask ONLY ONE question at a time.
2. Do NOT explain the answer, give feedback, or make comments like 'Thank you', 'Correct', 'Good', or 'That's right'.
3. Start with BASIC level questions in the current topic.
4. If the candidate answers correctly, increase difficulty gradually to INTERMEDIATE, then ADVANCED.
5. Ask a MINIMUM of 3 and a MAXIMUM of 5 questions on the current topic.
6. After completing 3-5 questions, switch to a NEW topic (e.g., Projects → Python → Operating System → Computer Networks).
7. Do NOT ask multiple questions in one response.
8. After the candidate answers, immediately ask the next question with no comments or explanations.
9. Keep your questions short and clear.
10. Continue switching topics in this order until the interview ends.
"""
    })

    # First question
    conversation_history.append({
        "role": "assistant",
        "content": f"Welcome! Let's start your {skill} interview. Can you introduce yourself?"
    })
    return {"reply": conversation_history[-1]["content"]}

@app.post("/chat")
def chat(user_input: dict):
    answer = user_input.get("answer", "")
    conversation_history.append({"role": "user", "content": answer})

    # Call LLaMA API for next question based on previous answer
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama2:latest",
            "messages": conversation_history,
            "stream": False
        }
    )

    try:
        data = response.json()
        next_question = data['message']['content']
    except:
        next_question = "Sorry, I couldn't generate the next question."

    conversation_history.append({"role": "assistant", "content": next_question})
    return {"reply": next_question}
