# Self-Consistency Checker
# Based on the idea from SelfCheckGPT paper (EMNLP 2023)
# The main idea is simple - if the model really knows something,
# it should give the same answer even when you ask differently

from sentence_transformers import SentenceTransformer
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

class SelfConsistencyChecker:
    def __init__(self, api_key=None):
        # Set up OpenAI and sentence transformer
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Self-consistency checker ready")
    
    def generate_paraphrases(self, query, n=3):
        # Make different versions of the same question
        paraphrases = [query]
        
        # Simple prompts to rephrase the question
        templates = [
            f"Rephrase this question: {query}",
            f"Ask the same thing differently: {query}",
            f"Reword this: {query}"
        ]
        
        for i in range(min(n-1, len(templates))):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": templates[i]}],
                    temperature=0.7,
                    max_tokens=100
                )
                new_question = response.choices[0].message.content.strip()
                paraphrases.append(new_question)
            except Exception as e:
                print(f"Could not generate paraphrase {i}: {e}")
        
        return paraphrases
    
    def get_responses(self, paraphrases):
        # Ask all the paraphrased questions and collect answers
        responses = []
        
        for question in paraphrases:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": question}],
                    temperature=0.5
                )
                answer = response.choices[0].message.content.strip()
                responses.append(answer)
            except Exception as e:
                print(f"Error getting response: {e}")
                responses.append("")
        
        return responses
    
    def calculate_similarity(self, responses):
        # Compare how similar all the responses are using sentence embeddings
        # Remove any empty responses
        responses = [r for r in responses if r]
        
        if len(responses) < 2:
            return 0.0
        
        # Convert responses to embeddings
        embeddings = self.model.encode(responses)
        
        # Compare every pair of responses
        all_similarities = []
        for i in range(len(embeddings)):
            for j in range(i+1, len(embeddings)):
                # Cosine similarity formula
                similarity = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                )
                all_similarities.append(similarity)
        
        # Average similarity across all pairs
        avg_sim = np.mean(all_similarities) if all_similarities else 0.0
        return avg_sim
    
    def check(self, query, n_paraphrases=3):
        # Main function that does everything
        print(f"\nChecking query: '{query}'")
        print(f"Generating {n_paraphrases} different versions...")
        
        # Step 1: Make different versions of the question
        paraphrases = self.generate_paraphrases(query, n_paraphrases)
        print(f"Got {len(paraphrases)} versions")
        
        # Step 2: Get answers for each version
        print(f"Getting responses from GPT...")
        responses = self.get_responses(paraphrases)
        print(f"Got {len(responses)} responses")
        
        # Step 3: Check how similar the answers are
        print(f"Comparing similarity...")
        similarity = self.calculate_similarity(responses)
        
        result = {
            'query': query,
            'consistency_score': similarity,
            'is_consistent': similarity > 0.7,  # If > 0.7, answers are similar enough
            'responses': responses,
            'num_responses': len(responses)
        }
        
        print(f"Consistency Score: {similarity:.2f}")
        if similarity > 0.7:
            print("✓ Responses are consistent")
        else:
            print("⚠ Responses are inconsistent - possible hallucination")
        
        return result


# Quick test
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING SELF-CONSISTENCY CHECKER")
    print("=" * 60)
    
    checker = SelfConsistencyChecker()
    
    # Try a test question
    test_query = "What is the population of Vatican City?"
    result = checker.check(test_query, n_paraphrases=3)
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Question: {result['query']}")
    print(f"Consistency: {result['consistency_score']:.2f}")
    print(f"Seems consistent? {result['is_consistent']}")
    print(f"\nAll responses:")
    for i, resp in enumerate(result['responses'], 1):
        print(f"\n{i}. {resp[:150]}...")