from datetime import datetime, timedelta
from octoprint_dashboard import app
import jwt
import requests
import base64


class LoginService:
    access_route = "https://auth.fit.cvut.cz/oauth/oauth/token"
    check_route = "https://auth.fit.cvut.cz/oauth/oauth/check_token"
    client_id = "fd19e88d-740e-4c82-822c-fff99ef0c4cb"
    client_secret = "Fb1VBJBaK9HYPSdY9YwOjEOwRU2B12IO"
    redirect_uri = "http://localhost:3000"
    authorization = "Basic " + base64.b64encode("{0}:{1}".format(client_id, client_secret).encode('ascii')).decode(
        'utf-8')

    @staticmethod
    def create_token(username):
        payload = {
            'sub': username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=14)
        }
        token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
        return token.decode('unicode_escape')

    @staticmethod
    def get_access_code(code):
        # {"access_token":"39fe293d-0966-4160-994e-4e24fc0aad01","token_type":"bearer","refresh_token":"3594dd6c-5416-41db-8eca-e4683ec617c4","expires_in":1550,"scope":"urn:zuul:oauth"}
        response = requests.post(LoginService.access_route, headers={
            "Authorization": LoginService.authorization
        }, data={
            "grant_type": "authorization_code",
            "code": code,
            "scope": "urn:zuul:oauth",
            "redirect_uri": LoginService.redirect_uri
        })
        response.raise_for_status()
        return response.json()

    @staticmethod
    def check_token(access_token):
        response = requests.post(LoginService.check_route, data={
            "token": access_token
        })
        response.raise_for_status()
        return response.json()

    @staticmethod
    def refresh_token(refresh_token):
        response = requests.post(LoginService.access_route, headers={
            "Authorization": LoginService.authorization
        }, data={
            "grant_type": "refresh_token",
            "scope": "urn:zuul:oauth",
            "refresh_token": refresh_token
        })
        response.raise_for_status()
        return response.json()
