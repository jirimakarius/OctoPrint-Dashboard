import requests
from flask import request, Blueprint, current_app

from octoprint_dashboard.model import User, Config
from octoprint_dashboard.services import LoginService

login_bp = Blueprint("login", __name__)


@login_bp.route('/auth', methods=['POST'])
def auth():
    """
    Route for user login.
    Needs code in request body, given by OAuth2.0
    Checks code, gets access token, saves user in database and returns authorization token
    """
    if current_app.config["AUTH"] == Config.NONE:
        return "", 404

    data = request.json
    if "code" not in data:
        return "", 400

    try:
        access_response = LoginService.get_access_code(data["code"])
        check_response = LoginService.check_token(access_response.get("access_token"))

    except requests.RequestException:
        return "", 400

    user = User.upsert(check_response.get("user_name"), access_response.get("access_token"),
                       access_response.get("refresh_token"))

    if user.superadmin:
        role = "superadmin"
    elif user.get_editable_groups():
        role = "admin"
    else:
        role = "user"
    token = LoginService.create_api_token(check_response.get("user_name"), role)
    return token, 200
