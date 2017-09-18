from datetime import datetime, timedelta

import base64
import jwt
import requests


class LoginService:
    """
    This class is meant to be whole static to simulate singleton

    It is collection of functions for login handling
    """
    access_route = "https://auth.fit.cvut.cz/oauth/oauth/token"
    check_route = "https://auth.fit.cvut.cz/oauth/oauth/check_token"
    from octoprint_dashboard.model import Config
    config = Config.query.first()
    if config:
        secret = config.secret
        client_id = config.oauth_client_id
        client_secret = config.oauth_client_secret
        redirect_uri = config.oauth_redirect_uri
        authorization = "Basic " + base64.b64encode("{0}:{1}".format(client_id, client_secret).encode('ascii')).decode(
            'utf-8')

    @staticmethod
    def create_api_token(username, role):
        """
        Returns token for access to API
        """
        payload = {
            'username': username,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=14)
        }
        token = jwt.encode(payload, LoginService.secret, algorithm="HS256")
        return token.decode('unicode_escape')

    @staticmethod
    def parse_api_token(request):
        """
        Returns parsed and decoded token from authorization header
        """
        token = request.headers.get('Authorization').split()[1]
        return jwt.decode(token, LoginService.secret)

    @staticmethod
    def parse_api_token_direct(token):
        """
        Returns parsed and decoded token from authorization header
        """
        return jwt.decode(token, LoginService.secret)

    @staticmethod
    def get_access_code(code):
        """
        Makes request to OAuth to exchange code for access_token and returns response
        """
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
        """
        Makes request to OAuth check token route and returns response
        Returns information about token (user)
        """
        response = requests.post(LoginService.check_route, data={
            "token": access_token
        })
        response.raise_for_status()
        return response.json()

    @staticmethod
    def refresh_token(refresh_token):
        """
        Makes request to OAuth to refresh access token and returns response
        """
        response = requests.post(LoginService.access_route, headers={
            "Authorization": LoginService.authorization
        }, data={
            "grant_type": "refresh_token",
            "scope": "urn:zuul:oauth",
            "refresh_token": refresh_token
        })
        response.raise_for_status()
        return response.json()
