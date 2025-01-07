from flask import Flask, request, jsonify, redirect, render_template
import random
import string

app = Flask(__name__, template_folder='urlShortener')

url_mapping = {}

base_url = "http://127.0.0.1:5000"

def generate_short_url():
    characters = string.ascii_letters + string.digits
    shortString = ''.join(random.choices(characters, k = 6))
    return shortString


@app.route('/')
def index():
    """Serve the frontend page."""
    return render_template('frontend.html')


@app.route('/shorten', methods = ['POST'])
def shortern_url():
    """Endpoint to shortern a URL."""
    data = request.get_json()


    if 'original_url' not in data or not data['original_url']:
        return jsonify({'Error': 'original url is required'}), 400
    
    original_url = data['original_url']


    short_url = generate_short_url()
    while short_url in url_mapping:
        short_url = generate_short_url()


    url_mapping[short_url] = original_url

    shortened_url = f"{base_url}/{short_url}"
    return jsonify({'short_url': shortened_url}), 200


@app.route('/<short_code>', methods = ['GET'])
def redirect_to_url(short_code):
    original_url = url_mapping.get(short_code)

    if not original_url:
        return jsonify({'error': 'Short URL not found'}), 404
    
    print(f"Redirecting {short_code} to {original_url}")

    return redirect(original_url)


if __name__ == '__main__':
    app.run(debug = True)