from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/submit-bet', methods=['POST'])
def submit_bet():
    data = request.json
    # Here you would typically process the bet data
    # For now, we'll just echo it back
    return jsonify({
        "message": "Bet received",
        "data": data
    }), 200

if __name__ == '__main__':
    app.run(debug=True)