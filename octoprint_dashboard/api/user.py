from flask_restful import Resource, marshal_with, fields

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import User


class UserApi(Resource):
    """
    Api class for users in database
    """

    @login_required
    @marshal_with({
        'username': fields.String
    })
    def get(self):
        """Gets all users in database"""
        users = User.query.all()

        return users, 200
