from flask_restful import Resource, reqparse
from octoprint_dashboard.login import superadmin_required
from octoprint_dashboard.model import User


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Username can\'t be converted')


class SuperAdminApi(Resource):
    @superadmin_required
    def post(self):
        args = parser.parse_args()
        User.upsert_superadmin(args["username"])

        return None, 201
