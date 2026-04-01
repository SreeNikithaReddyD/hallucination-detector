# server that runs all the checks

from flask import Flask, request, jsonify
from flask_cors import CORS
from self_consistency import SelfConsistencyChecker
from uncertainty_detection import UncertaintyDetector
from wikipedia_verification import WikipediaVerifier

app = Flask(__name__)
CORS(app)

# load everything
print("loading...")
consistency = SelfConsistencyChecker()
uncertainty = UncertaintyDetector()
wiki = WikipediaVerifier()
print("ready\n")

@app.route('/')
def home():
    return jsonify({
        'message': 'hallucination detector running',
        'status': 'ok'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/detect', methods=['POST'])
def detect():
    try:
        d = request.json
        q = d.get('query')
        resp = d.get('response')
        
        if not q or not resp:
            return jsonify({'error': 'need query and response'}), 400
        
        print(f"\nchecking: {q[:50]}...")
        
        # run checks
        c_result = consistency.check(q)
        c_score = c_result['consistency_score']
        
        u_result = uncertainty.detect(resp)
        u_score = u_result['uncertainty_score']
        
        w_result = wiki.verify(resp)
        w_score = w_result['verification_score']
        
        # combine scores
        # weights: 40% consistency, 35% uncertainty, 25% wiki
        risk = (
            0.40 * (1 - c_score) +
            0.35 * u_score +
            0.25 * (1 - w_score)
        )
        
        final = risk * 100
        
        print(f"risk: {final:.1f}/100")
        
        # interpret
        if final < 30:
            msg = "low risk"
        elif final < 60:
            msg = "medium risk"
        else:
            msg = "high risk"
        
        return jsonify({
            'risk_score': round(final, 2),
            'message': msg,
            'consistency': round(c_score, 2),
            'uncertainty': round(u_score, 2),
            'wikipedia': round(w_score, 2),
            'uncertain_words': u_result['hedging_words_found']
        })
        
    except Exception as e:
        print(f"error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\nstarting server on http://localhost:5000\n")
    app.run(debug=True, port=5000)