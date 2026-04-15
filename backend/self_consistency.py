# checking if AI gives same answer when asked multiple times
# using hugging face official client

from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient
import numpy as np
import os
from dotenv import load_dotenv
import time

load_dotenv()

class SelfConsistencyChecker:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        token = os.getenv('HUGGINGFACE_API_KEY')
        self.client = InferenceClient(api_key=token)
        print("loaded consistency checker")
    
    def ask_question(self, q):
        # ask hugging face using chat format
        try:
            messages = [{"role": "user", "content": q}]
            response = self.client.chat_completion(
                messages=messages,
                model="Qwen/Qwen2.5-72B-Instruct",
                max_tokens=50
            )
            answer = response.choices[0].message.content
            return answer.strip()
        except Exception as e:
            print(f"  error: {e}")
            return ""
    
    def get_multiple_responses(self, question):
        # ask 3 times
        answers = []
        
        print(f"asking: {question}")
        for i in range(3):
            print(f"  try {i+1}...")
            ans = self.ask_question(question)
            if ans:
                answers.append(ans)
            time.sleep(2)
        
        return answers
    
    def check_similarity(self, answers):
        # compare similarity
        answers = [a for a in answers if a]
        
        if len(answers) < 2:
            return 0.0
        
        vecs = self.model.encode(answers)
        
        sims = []
        for i in range(len(vecs)):
            for j in range(i+1, len(vecs)):
                s = np.dot(vecs[i], vecs[j]) / (
                    np.linalg.norm(vecs[i]) * np.linalg.norm(vecs[j])
                )
                sims.append(s)
        
        return np.mean(sims) if sims else 0.0
    
    def check(self, query):
        print(f"\nchecking: {query}")
        
        answers = self.get_multiple_responses(query)
        
        if not answers:
            print("no responses")
            return {
                'query': query,
                'consistency_score': 0.5,
                'is_consistent': False,
                'responses': []
            }
        
        print(f"got {len(answers)} answers")
        
        score = self.check_similarity(answers)
        
        print(f"similarity: {score:.2f}")
        
        return {
            'query': query,
            'consistency_score': score,
            'is_consistent': score > 0.7,
            'responses': answers
        }


# test
if __name__ == "__main__":
    print("testing consistency checker")
    print("="*50)
    
    c = SelfConsistencyChecker()
    
    q = "What is the capital of France?"
    res = c.check(q)
    
    print("\nresults:")
    print(f"score: {res['consistency_score']:.2f}")
    print("\nresponses:")
    for i, r in enumerate(res['responses'], 1):
        print(f"{i}. {r}")