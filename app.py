from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

NEWS_API_KEY = os.getenv("API_KEY")
NEWS_URL = "https://newsapi.org/v2/top-headlines"

def is_valid_image(url):
    """Check if the image URL is valid using an HTTP HEAD request."""
    try:
        response = requests.head(url, timeout=3)  # Faster than GET
        return response.status_code == 200 and response.headers.get('content-type', '').startswith('image')
    except requests.RequestException:
        return False  # Fail-safe

@app.route('/', methods=['GET'])
def get_news():
    category = request.args.get('category', 'business')  
    country = request.args.get('country', 'us')

    response = requests.get(NEWS_URL, params={"category": category, "country": country, "apiKey": NEWS_API_KEY})

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch news"}), response.status_code

    data = response.json()
    
    # Filter articles with valid images
    articles = [
        article for article in data.get("articles", [])[:50]  # Limit to 50 articles
        if article.get("urlToImage") and is_valid_image(article["urlToImage"])
    ]

    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
