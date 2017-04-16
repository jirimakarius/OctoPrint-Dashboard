from datetime import datetime, timedelta
from octoprint_dashboard.app import app
import jwt
import requests
import base64


class LoginService:
    access_route = "https://auth.fit.cvut.cz/oauth/oauth/token"
    check_route = "https://auth.fit.cvut.cz/oauth/oauth/check_token"
    from octoprint_dashboard.model import Config
    config = Config.query.first()
    if config:
        client_id = config.oauth_client_id
        client_secret = config.oauth_client_secret
        redirect_uri = config.oauth_redirect_uri
        authorization = "Basic " + base64.b64encode("{0}:{1}".format(client_id, client_secret).encode('ascii')).decode(
            'utf-8')

    @staticmethod
    def create_api_token(username, role):
        payload = {
            'username': username,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=14)
        }
        token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
        return token.decode('unicode_escape')

    @staticmethod
    def parse_api_token(request):
        token = request.headers.get('Authorization').split()[1]
        return jwt.decode(token, app.config['SECRET_KEY'])

    @staticmethod
    def get_access_code(code):
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
