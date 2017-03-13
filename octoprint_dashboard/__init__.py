from datetime import datetime, timedelta
from flask import Flask, send_from_directory, request, session
from octoprint_dashboard.login import Neco, login_required
import requests
import jwt
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = "something"


@app.route('/')
def frontend():
    # return "Hello"
    # return render_template('index.html')
    return send_from_directory('dist', 'index.html')


@app.route('/<text>.js')
def neco(text):
    return send_from_directory('dist', text + ".js")


def create_token(data):
    payload = {
        'sub': data["username"],
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=data["exp"])
    }
    # print(payload['iat']-payload['exp'])
    print(payload)
    token = jwt.encode(payload, "secret", algorithm="HS256")
    # token = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
    print(token)
    return token


@app.route('/auth', methods=['POST'])
def auth():
    access_route = "https://auth.fit.cvut.cz/oauth/oauth/token"
    check_route = "https://auth.fit.cvut.cz/oauth/oauth/check_token"
    client_id = "fd19e88d-740e-4c82-822c-fff99ef0c4cb"
    client_secret = "Fb1VBJBaK9HYPSdY9YwOjEOwRU2B12IO"
    redirect_uri = "http://localhost:3000"
    authorization = "Basic "+base64.b64encode("{0}:{1}".format(client_id, client_secret).encode('ascii')).decode('utf-8')

    p = requests.post(access_route, headers={
        "Authorization": authorization
    }, data={
        "grant_type": "authorization_code",
        "code": request.json['code'],
        "scope": "something",
        "redirect_uri": redirect_uri
    })

    check = requests.post(check_route, data={
        "token": p.json().get("access_token")
    })

    session["oauth"] = p.json().get("access_token")
    print(p.text)
    print(check.text)
    token=create_token({
        "username": check.json().get("user_name"),
        "exp": p.json().get("expires_in")
    })
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
    print(session)
    return Neco.parek()
