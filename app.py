from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app) 
NEWS_API_KEY = os.getenv("API_KEY")
NEWS_URL = "https://newsapi.org/v2/top-headlines"

@app.route('/', methods=['GET'])
def get_news():
    category = request.args.get('category', 'business')  # Default to business news
    country = request.args.get('country', 'us')  # Default to US news

    response = requests.get(NEWS_URL, params={
        "category": category,
        "country": country,
        "apiKey": NEWS_API_KEY
    })
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch news"}), response.status_code

    data = response.json()
    return jsonify(data["articles"][:50])  # Return top 50 articles

if __name__ == '__main__':
    app.run(debug=True)
