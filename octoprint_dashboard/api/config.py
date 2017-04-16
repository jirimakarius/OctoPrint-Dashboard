from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.app import db, scheduler
from octoprint_dashboard.login import login_required, superadmin_required

from octoprint_dashboard.model import Config


class ClientConfigApi(Resource):
    @marshal_with({
        "refresh": fields.Integer(attribute="client_refresh"),
        "auth": fields.String
    })
    def get(self):
        config = Config.query.first()

        return config, 200


configParser = reqparse.RequestParser()
configParser.add_argument('server_refresh', type=int, required=True, help='Server refresh can\'t be converted')
configParser.add_argument('client_refresh', type=int, required=True, help='Client refresh can\'t be converted')
configParser.add_argument('auth', type=str, help='Auth can\'t be converted')
configParser.add_argument('oauth_redirect_uri', type=str)
configParser.add_argument('oauth_client_id', type=str)
configParser.add_argument('oauth_client_secret', type=str)


class ConfigApi(Resource):
    @superadmin_required
    @marshal_with({
        "server_refresh": fields.Integer,
        "client_refresh": fields.Integer,
        "auth": fields.String
    })
    def get(self):
        config = Config.query.first()

        return config, 200

    @superadmin_required
    def post(self):
        args = configParser.parse_args()
        config = Config.query.first()

        if config.server_refresh != args["server_refresh"]:
            scheduler.reschedule(args["server_refresh"])
        config.server_refresh = args["server_refresh"]
        config.client_refresh = args["client_refresh"]
        if args["auth"]:
            config.auth = args["auth"]
        if args["oauth_redirect_uri"]:
            config.oauth_redirect_uri = args["oauth_redirect_uri"]
        if args["oauth_client_id"]:
            config.oauth_client_id = args["oauth_client_id"]
        if args["oauth_client_secret"]:
            config.oauth_client_secret = args["oauth_client_secret"]
        db.session.commit()
        return None, 200
