from flask_restful import Resource, marshal_with, fields

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
