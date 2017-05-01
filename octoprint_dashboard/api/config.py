from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.app import db, scheduler
from octoprint_dashboard.login import superadmin_required
from octoprint_dashboard.model import Config


class ClientConfigApi(Resource):
    """
    Api class for client getting public configurations for client.
    This configurations are only for client and they do not require logged user
    """

    @marshal_with({
        "refresh": fields.Integer(attribute="client_refresh"),
        "oauth_redirect_uri": fields.String,
        "oauth_client_id": fields.String
    })
    def get(self):
        config = Config.query.first()

        return config, 200


configParser = reqparse.RequestParser()
configParser.add_argument('server_refresh', type=int, required=True, help='Server refresh can\'t be converted')
configParser.add_argument('client_refresh', type=int, required=True, help='Client refresh can\'t be converted')
configParser.add_argument('secret', type=str, help='Secret can\'t be converted')
configParser.add_argument('oauth_redirect_uri', type=str)
configParser.add_argument('oauth_client_id', type=str)
configParser.add_argument('oauth_client_secret', type=str)
"""Parser for POST request of server configuration API"""


class ConfigApi(Resource):
    """Api class for superadmin, login is required, specifically with superadmin permission
    """

    @superadmin_required
    @marshal_with({
        "server_refresh": fields.Integer,
        "client_refresh": fields.Integer
    })
    def get(self):
        config = Config.query.first()

        return config, 200

    @superadmin_required
    def post(self):
        """Updates application configuration and updates background tasks
        """
        args = configParser.parse_args()
        config = Config.query.first()

        if config.server_refresh != args["server_refresh"]:
            # updating background tasks on server refresh time change
            scheduler.reschedule(args["server_refresh"])

        config.server_refresh = args["server_refresh"]
        config.client_refresh = args["client_refresh"]
        if args["secret"]:
            config.auth = args["secret"]
        if args["oauth_redirect_uri"]:
            config.oauth_redirect_uri = args["oauth_redirect_uri"]
        if args["oauth_client_id"]:
            config.oauth_client_id = args["oauth_client_id"]
        if args["oauth_client_secret"]:
            config.oauth_client_secret = args["oauth_client_secret"]
        db.session.commit()
        return "", 200
