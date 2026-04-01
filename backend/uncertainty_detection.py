# finding words that show AI is unsure
# like "maybe" or "possibly"

import spacy

class UncertaintyDetector:
    def __init__(self):
        # load spacy
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("loaded uncertainty detector")
        except:
            print("need to install spacy model")
            print("run: python -m spacy download en_core_web_sm")
            raise
        
        # words that show uncertainty
        self.words = [
            'maybe', 'possibly', 'perhaps', 'might', 'could',
            'approximately', 'roughly', 'about', 'around',
            'i think', 'i believe', 'probably', 'likely',
            'seems', 'appears', 'may'
        ]
    
    def detect(self, text):
        # find uncertain words
        if not text:
            return {
                'uncertainty_score': 0.0,
                'hedging_words_found': [],
                'hedging_count': 0
            }
        
        lower = text.lower()
        
        # check each word
        found = []
        for w in self.words:
            if w in lower:
                found.append(w)
        
        # count sentences
        doc = self.nlp(text)
        sents = list(doc.sents)
        num = len(sents)
        
        # calculate score
        if num == 0:
            s = 0.0
        else:
            s = min(len(found) / (num * 2), 1.0)
        
        return {
            'uncertainty_score': s,
            'hedging_words_found': found,
            'hedging_count': len(found),
            'num_sentences': num
        }


# test
if __name__ == "__main__":
    print("testing uncertainty detector")
    print("="*50)
    
    d = UncertaintyDetector()
    
    tests = [
        "The Eiffel Tower is 330 meters tall.",
        "Vatican City possibly has around 800 people, I think.",
        "It might be approximately 1200 or maybe 800."
    ]
    
    for i, t in enumerate(tests, 1):
        print(f"\ntest {i}: {t}")
        r = d.detect(t)
        print(f"score: {r['uncertainty_score']:.2f}")
        print(f"found: {r['hedging_words_found']}")