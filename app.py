import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SETUP API KEY
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    print("WARNING: GOOGLE_API_KEY not found in environment.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("API Key configured successfully.")

model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET'])
def home():
    return "PAPI Brain is Online. Status: Active."

@app.route('/chat', methods=['POST'])
def chat():
    if not GOOGLE_API_KEY:
        return jsonify({"error": "Server missing API Key"}), 500

    try:
        data = request.json
        user_text = data.get('text', '')
        
        if not user_text:
            return jsonify({"error": "No text provided"}), 400

        response = model.generate_content(user_text)
        
        return jsonify({
            "response": response.text, 
            "status": "success"
        })

    except Exception as e:
        print(f"Error generating content: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)