from flask import Flask, request, jsonify, make_response
from nyanTranslate import parse_and_convert

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Welcome to CatDominatesWorld_backend!"


@app.route('/translate', methods=['POST'])
def translateHTML():
    content = request.json['content']
    level = request.json('level')
    response = make_response(parse_and_convert(content,level), 200)
    response.mimetype = "text/plain"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
