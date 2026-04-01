from backend.self_consistency import SelfConsistencyChecker
from backend.uncertainty_detection import UncertaintyDetector
from backend.wikipedia_verification import WikipediaVerifier

print("testing all modules directly...")

# test query
query = "What is the capital of France?"
response = "Paris is possibly the capital, I think."

print(f"\nquery: {query}")
print(f"response: {response}\n")

# test each module
print("1. uncertainty...")
u = UncertaintyDetector()
u_result = u.detect(response)
print(f"   score: {u_result['uncertainty_score']}")
print(f"   words: {u_result['hedging_words_found']}")

print("\n2. wikipedia...")
w = WikipediaVerifier()
w_result = w.verify(response)
print(f"   score: {w_result['verification_score']}")

print("\n3. consistency...")
c = SelfConsistencyChecker()
c_result = c.check(query)
print(f"   score: {c_result['consistency_score']}")

# calculate final
risk = (
    0.40 * (1 - c_result['consistency_score']) +
    0.35 * u_result['uncertainty_score'] +
    0.25 * (1 - w_result['verification_score'])
)

print(f"\nfinal risk score: {risk * 100:.1f}/100")