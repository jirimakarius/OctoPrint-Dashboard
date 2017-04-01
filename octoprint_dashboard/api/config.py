from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard import db
from octoprint_dashboard.login import login_required, superadmin_required

from octoprint_dashboard.model import Config


class ClientConfigApi(Resource):
    @marshal_with({
        "refresh": fields.Integer(attribute="client_refresh"),
        "auth": fields.String
    })
    def get(self):
        config = Config.query.scalar()

        return config, 200


configParser = reqparse.RequestParser()
configParser.add_argument('serverRefresh', type=int, required=True, help='Server refresh can\'t be converted')
configParser.add_argument('clientRefresh', type=int, required=True, help='Client refresh can\'t be converted')
configParser.add_argument('auth', type=str, required=True, help='Auth can\'t be converted')


class ConfigApi(Resource):
    @superadmin_required
    @marshal_with({
        "server_refresh": fields.Integer,
        "client_refresh": fields.Integer,
        "auth": fields.String
    })
    def get(self):
        config = Config.get_config()

        return config, 200

    @superadmin_required
    def post(self):
        args = configParser.parse_args()
        config = Config.get_config()

        config.server_refresh = args["serverRefresh"]
        config.client_refresh = args["clientRefresh"]
        config.auth = args["auth"]
        db.session.commit()
        return None, 200
