# checking if stuff is actually on wikipedia

import wikipediaapi
import spacy

class WikipediaVerifier:
    def __init__(self):
        # setup
        self.wiki = wikipediaapi.Wikipedia(user_agent='HallucinationDetector/1.0',language='en')
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("loaded wiki verifier")
        except:
            print("need spacy model")
            raise
    
    def find_stuff(self, text):
        # find names, places etc
        doc = self.nlp(text)
        stuff = []
        
        for e in doc.ents:
            # only care about certain types
            if e.label_ in ['PERSON', 'GPE', 'LOC', 'ORG', 'DATE']:
                stuff.append(e.text)
        
        return stuff
    
    def check_wiki(self, thing):
        # look it up
        page = self.wiki.page(thing)
        return page.exists()
    
    def verify(self, text):
        # main function
        print(f"\nchecking wikipedia...")
        
        # find entities
        things = self.find_stuff(text)
        print(f"found: {things}")
        
        if not things:
            return {
                'verification_score': 0.5,
                'entities_checked': 0,
                'verified': 0
            }
        
        # check each one
        verified = 0
        checked = min(len(things), 3)
        
        for thing in things[:3]:
            if self.check_wiki(thing):
                verified += 1
                print(f"  found {thing}")
            else:
                print(f"  not found {thing}")
        
        # score
        score = verified / checked if checked > 0 else 0.5
        
        return {
            'verification_score': score,
            'entities_checked': checked,
            'verified': verified
        }


# test
if __name__ == "__main__":
    print("testing wiki verifier")
    print("="*50)
    
    v = WikipediaVerifier()
    
    tests = [
        "Vatican City has 800 people.",
        "The Eiffel Tower is in Paris.",
        "Han Kang won the Nobel Prize."
    ]
    
    for t in tests:
        print(f"\ntext: {t}")
        r = v.verify(t)
        print(f"score: {r['verification_score']:.2f}")
        print(f"verified: {r['verified']}/{r['entities_checked']}")