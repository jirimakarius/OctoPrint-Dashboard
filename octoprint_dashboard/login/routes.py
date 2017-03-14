from flask import session, request

from octoprint_dashboard import app
from octoprint_dashboard.login import LoginService
import requests


@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    print(data)
    if "code" not in data:
        return "", 400

    try:
        access_response = LoginService.get_access_code(data["code"])
        check_response = LoginService.check_token(access_response.get("access_token"))

    except requests.RequestException:
        return "", 400
    session["user"] = access_response.get("access_token")
    print(access_response)
    print(check_response)
    token = LoginService.create_token(check_response.get("user_name"))
    return token, 200
