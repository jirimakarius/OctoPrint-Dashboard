from flask import request, g

from octoprint_dashboard import app
from octoprint_dashboard.login import login_required
from octoprint_dashboard.services import LoginService
from octoprint_dashboard.model import User
import requests


@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    if "code" not in data:
        return "", 400

    try:
        access_response = LoginService.get_access_code(data["code"])
        check_response = LoginService.check_token(access_response.get("access_token"))

    except requests.RequestException:
        return "", 400
    User.upsert(check_response.get("user_name"), access_response.get("access_token"), access_response.get("refresh_token"))

    token = LoginService.create_api_token(check_response.get("user_name"))
    print(token)
    return token, 200


@app.route('/auth/refresh', methods=['GET'])
@login_required
def auth_refresh():
    token = LoginService.create_api_token(g.user.username)

    return token, 200
