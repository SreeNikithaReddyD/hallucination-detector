# Hallucination Detector

Detects when ChatGPT or Claude makes up fake facts.

## Author
Sree Nikitha Reddy Doddareddy (002414150)

## What it does

Checks AI responses using three methods:
1. Self-consistency - asks same question multiple times, checks if answers match
2. Uncertainty - looks for words like "maybe" or "possibly" 
3. Wikipedia - checks if facts are on Wikipedia

## How to run

Install stuff:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Add your Hugging Face token to .env file:
```
HUGGINGFACE_API_KEY=your_token
```

Test each part:
```bash
python backend/uncertainty_detection.py
python backend/self_consistency.py
python backend/wikipedia_verification.py
```

Start server:
```bash
python backend/server.py
```

## Current status

Working:
- uncertainty detection (finds uncertain words)
- wikipedia verification (checks facts)
- self-consistency (uses hugging face API)
- flask server (combines everything)

Todo:
- chrome extension
- evaluation on datasets
- demo video

## Based on

SelfCheckGPT paper from EMNLP 2023
LLM-Check paper from NeurIPS 2024