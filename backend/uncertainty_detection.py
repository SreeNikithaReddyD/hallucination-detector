# Uncertainty Detector
# Looks for words that show the AI is not confident
# Like when people say "maybe" or "I think" when they're unsure

import spacy

class UncertaintyDetector:
    def __init__(self):
        # Load spacy for text analysis
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("Uncertainty detector ready")
        except:
            print("Error: spaCy model not found")
            print("Please run: python -m spacy download en_core_web_sm")
            raise
        
        # Words that show uncertainty
        self.uncertain_words = [
            'maybe', 'possibly', 'perhaps', 'might', 'could',
            'approximately', 'roughly', 'about', 'around',
            'i think', 'i believe', 'probably', 'likely',
            'seems', 'appears', 'suggests', 'may'
        ]
    
    def detect(self, text):
        # Find uncertainty words in the text
        if not text:
            return {
                'uncertainty_score': 0.0,
                'hedging_words_found': [],
                'hedging_count': 0
            }
        
        text_lower = text.lower()
        
        # Look for each uncertain word
        found_words = []
        for word in self.uncertain_words:
            if word in text_lower:
                found_words.append(word)
        
        count = len(found_words)
        
        # Figure out how many sentences are in the text
        doc = self.nlp(text)
        sentences = list(doc.sents)
        num_sentences = len(sentences)
        
        # Calculate uncertainty score
        # More uncertain words per sentence = higher score
        if num_sentences == 0:
            score = 0.0
        else:
            # Divide by 2 so we don't max out too easily
            score = min(count / (num_sentences * 2), 1.0)
        
        return {
            'uncertainty_score': score,
            'hedging_words_found': found_words,
            'hedging_count': count,
            'num_sentences': num_sentences
        }


# Test it out
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING UNCERTAINTY DETECTOR")
    print("=" * 60)
    
    detector = UncertaintyDetector()
    
    # Try different examples
    examples = [
        "The Eiffel Tower is 330 meters tall.",
        "Vatican City possibly has around 800 people, I think.",
        "The population might be approximately 1200 or maybe 800."
    ]
    
    for i, text in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(f"Text: {text}")
        result = detector.detect(text)
        print(f"Uncertainty score: {result['uncertainty_score']:.2f}")
        print(f"Found these uncertain words: {result['hedging_words_found']}")