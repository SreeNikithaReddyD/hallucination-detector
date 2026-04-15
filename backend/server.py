from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# add backend to path so imports work
sys.path.insert(0, os.path.dirname(__file__))

from self_consistency import SelfConsistencyChecker
from uncertainty_detection import UncertaintyDetector
from wikipedia_verification import WikipediaVerifier

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

print("loading modules...")
consistency = SelfConsistencyChecker()
uncertainty = UncertaintyDetector()
wiki = WikipediaVerifier()
print("ready")

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'running', 'message': 'hallucination detector api'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/detect', methods=['POST', 'OPTIONS'])
def detect():
    if request.method == 'OPTIONS':
        return '', 204
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'no data'}), 400
    
    query = data.get('query', '')
    response_text = data.get('response', '')
    
    if not query or not response_text:
        return jsonify({'error': 'need query and response'}), 400
    
    print(f"\nprocessing: {query[:50]}")
    
    # run all three checks
    c_res = consistency.check(query)
    u_res = uncertainty.detect(response_text)
    w_res = wiki.verify(response_text)
    
    # calculate risk
    risk = (
        0.40 * (1 - c_res['consistency_score']) +
        0.35 * u_res['uncertainty_score'] +
        0.25 * (1 - w_res['verification_score'])
    )
    
    final_score = risk * 100
    
    if final_score < 30:
        message = "low risk"
    elif final_score < 60:
        message = "medium risk"
    else:
        message = "high risk"
    
    result = {
        'risk_score': float(round(final_score, 1)),
        'message': message,
        'consistency': float(round(c_res['consistency_score'], 2)),
        'uncertainty': float(round(u_res['uncertainty_score'], 2)),
        'wikipedia': float(round(w_res['verification_score'], 2)),
        'uncertain_words': u_res['hedging_words_found']
    }
    
    print(f"result: {final_score:.1f}/100")
    
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)