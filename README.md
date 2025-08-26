# AI Interview System



\# AI Interview System (Ollama + FastAPI + static frontend)



\## Prereqs

\- Python 3.10+

\- Ollama (installed \& running) — https://ollama.com/download. Ollama serves models at localhost:11434. :contentReference\[oaicite:9]{index=9}

\- Chrome browser (for mic)



\## Install \& run

1\. Start Ollama and run the model:

&nbsp;  ```bash

&nbsp;  ollama pull llama2

&nbsp;  ollama run llama2

Python env \& deps:



bash

Copy

Edit

python -m venv venv

\# Windows

venv\\Scripts\\activate

\# macOS/Linux

source venv/bin/activate

pip install -r requirements.txt

Start backend:



bash

Copy

Edit

uvicorn main:app --host 127.0.0.1 --port 8000 --reload

