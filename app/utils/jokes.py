from flask import Blueprint, jsonify
import requests

# Crear el blueprint
jokes_bp = Blueprint('jokes', __name__)

def fetch_joke(category="Any", blacklist_flags=None, joke_type=None):
    base_url = "https://v2.jokeapi.dev/joke/"
    params = {}
    if blacklist_flags:
        params["blacklistFlags"] = blacklist_flags
    if joke_type:
        params["type"] = joke_type

    url = f"{base_url}{category}"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Ruta de ejemplo para el blueprint
@jokes_bp.route('/joke', methods=['GET'])
def get_joke():
    joke = fetch_joke()
    return jsonify(joke)
