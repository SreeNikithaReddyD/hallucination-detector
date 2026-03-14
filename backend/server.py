# Simple Flask server for the hallucination detector
# This will eventually connect to the Chrome extension

from flask import Flask, request, jsonify
from flask_cors import CORS
from self_consistency import SelfConsistencyChecker
from uncertainty_detection import UncertaintyDetector

app = Flask(__name__)
CORS(app)  # So the Chrome extension can talk to this

# Start up the detection modules
print("Starting up...")
consistency_checker = SelfConsistencyChecker()
uncertainty_detector = UncertaintyDetector()
print("All systems ready!\n")

@app.route('/')
def home():
    # Just a basic home page
    return jsonify({
        'message': 'Hallucination Detector API is running',
        'available_endpoints': {
            '/detect': 'Send a POST request to check for hallucinations',
            '/health': 'Check if server is alive'
        }
    })

@app.route('/health')
def health():
    # Quick health check
    return jsonify({'status': 'ok'})

@app.route('/detect', methods=['POST'])
def detect():
    # Main endpoint that does the detection
    try:
        data = request.json
        query = data.get('query')
        response_text = data.get('response')
        
        # Make sure we got both pieces
        if not query or not response_text:
            return jsonify({'error': 'Need both query and response'}), 400
        
        print(f"\nGot new request:")
        print(f"Question: {query[:60]}...")
        
        # Run the two checks we have so far
        print("Running consistency check...")
        consistency_result = consistency_checker.check(query, n_paraphrases=3)
        consistency_score = consistency_result['consistency_score']
        
        print("Running uncertainty check...")
        uncertainty_result = uncertainty_detector.detect(response_text)
        uncertainty_score = uncertainty_result['uncertainty_score']
        
        # Wikipedia check not done yet, using placeholder
        wiki_score = 0.5
        
        # Combine scores with weights
        # 40% consistency, 35% uncertainty, 25% wikipedia
        # Higher risk score = more likely to be hallucination
        risk = (
            0.40 * (1 - consistency_score) +  
            0.35 * uncertainty_score +         
            0.25 * (1 - wiki_score)
        )
        
        final_score = risk * 100
        
        print(f"Final risk score: {final_score:.1f}/100\n")
        
        # Figure out what this score means
        if final_score < 30:
            interpretation = "Looks good, probably trustworthy"
        elif final_score < 60:
            interpretation = "Medium risk, double check if important"
        else:
            interpretation = "High risk, likely wrong"
        
        return jsonify({
            'risk_score': round(final_score, 2),
            'interpretation': interpretation,
            'details': {
                'consistency': round(consistency_score, 3),
                'uncertainty': round(uncertainty_score, 3),
                'uncertain_words_found': uncertainty_result['hedging_words_found'],
                'wiki_status': 'not implemented yet'
            }
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("HALLUCINATION DETECTION SERVER")
    print("Starting on http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)