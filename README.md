# Hallucination Detection System for LLMs

A Chrome extension for detecting hallucinations in ChatGPT and Claude responses using ensemble detection methods.

## Author
Sree Nikitha Reddy Doddareddy (002414150)

## Project Overview

This project detects when AI models like ChatGPT or Claude generate false information that sounds believable. It uses three detection methods:

1. **Self-Consistency Checking** - Asks the same question multiple times and checks if answers match
2. **Uncertainty Detection** - Looks for hedging words like "maybe", "possibly"  
3. **Wikipedia Verification** - Cross-checks facts against Wikipedia (coming soon)

## Progress So Far

- ✅ Self-consistency checking module implemented (adapted from SelfCheckGPT)
- ✅ Uncertainty detection using spaCy
- ✅ Basic Flask server setup
- ⏳ Wikipedia verification (in progress)
- ⏳ Ensemble scoring system (next step)
- ⏳ Chrome extension frontend (planned)

## Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

## Setup

1. Get OpenAI API key from https://platform.openai.com/api-keys
2. Create a `.env` file:
```
   OPENAI_API_KEY=your-api-key-here
```

## Usage
```bash
# Run Flask server
python backend/server.py

# Test self-consistency checker
python backend/self_consistency.py

# Test uncertainty detector
python backend/uncertainty_detection.py
```

## Technical Stack

- **Backend:** Python, Flask
- **LLM API:** OpenAI GPT-3.5-turbo
- **Sentence Similarity:** Sentence-Transformers (all-MiniLM-L6-v2)
- **NLP:** spaCy (en_core_web_sm)
- **Wikipedia API:** wikipediaapi (planned)

## Based On

- **SelfCheckGPT** (EMNLP 2023): https://github.com/potsawee/selfcheckgpt
  - Used for self-consistency implementation approach
- **LLM-Check** (NeurIPS 2024): Methodology for uncertainty detection
  - Paper: https://openreview.net/forum?id=LYx4w3CAgy

## Project Timeline

- Week 1-2: ✅ Self-consistency implementation
- Week 3-4: 🔄 Uncertainty + Wikipedia modules (current)
- Week 5-6: Ensemble scoring system
- Week 7-8: Chrome extension development
- Week 9-10: Testing and evaluation

## License

MIT License