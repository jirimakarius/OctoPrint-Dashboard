from flask import Flask, send_from_directory, request
from octoprint_dashboard.login import Neco, login_required
import requests

app = Flask(__name__)


@app.route('/')
def frontend():
    # return "Hello"
    # return render_template('index.html')
    return send_from_directory('dist', 'index.html')


@app.route('/<text>.js')
def neco(text):
    return send_from_directory('dist', text + ".js")


@app.route('/auth', methods=['POST'])
def auth():
    access_route = "https://auth.fit.cvut.cz/oauth/oauth/token"
    client_id = "fd19e88d-740e-4c82-822c-fff99ef0c4cb"
    client_secret = "Fb1VBJBaK9HYPSdY9YwOjEOwRU2B12IO"
    redirect_uri = "http://localhost:3000"

    p = requests.post(access_route, data={
        "grant_type": "authorization_code",
        "code": request.json['code'],
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "something",
        "redirect_uri": redirect_uri
    })

    print(p.text)
    return 'parek', 200


@app.route('/api/upload', methods=['PUT'])
def upload():
    print(request.data)
    for i in request.files.keys():
        print(i)
    return 'parek', 201


@app.route('/test')
@login_required
def test():
    return Neco.parek()
