from flask import Flask, request, jsonify
from googletrans import Translator
import re
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
translator = Translator()

# Regex to detect URLs
url_pattern = re.compile(
    r'^(https?:\/\/)?'           # protocol
    r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'  # domain
    r'(\/\S*)?$'                 # path
)

MAX_CHARS = 14000  # safe limit under 15k

# ----------------------------
# Chunk large text safely
# ----------------------------
def chunk_text(text, chunk_size=MAX_CHARS):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ----------------------------
# Translate a single string with chunk handling
# ----------------------------
def translate_string(text, target_lang):
    if url_pattern.match(text):
        return text  # Don't translate URLs

    # Split long text into chunks
    chunks = chunk_text(text)
    results = []

    # Translate in parallel
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(translator.translate, c, dest=target_lang) for c in chunks]
        for f in futures:
            try:
                results.append(f.result().text)
            except Exception:
                results.append(c)  # fallback
    return "".join(results)

# ----------------------------
# Recursive JSON translator
# ----------------------------
def translate_json_values(obj, target_lang):
    if isinstance(obj, dict):
        return {k: translate_json_values(v, target_lang) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [translate_json_values(v, target_lang) for v in obj]
    elif isinstance(obj, str):
        return translate_string(obj, target_lang)
    else:
        return obj

# ----------------------------
# API Endpoint
# ----------------------------
@app.route('/translate', methods=['POST'])
def translate_endpoint():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    body = request.json
    data = body.get('data')
    target_lang = body.get('target_lang', 'id')  # default Bahasa Indonesia

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        translated_data = translate_json_values(data, target_lang)
        return jsonify({'translated_data': translated_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
