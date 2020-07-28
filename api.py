from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from nyanTranslate import parse_and_convert

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return "Welcome to CatDominatesWorld_backend!"


@app.route('/translate', methods=['POST'])
def translateHTML():
    content = request.json['content']
    level = request.json['level']
    url = request.json['url']
    response = make_response(parse_and_convert(content,level, url), 200)
    response.mimetype = "text/plain"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=443, ssl_context=('cert.pem', 'key.pem'))
