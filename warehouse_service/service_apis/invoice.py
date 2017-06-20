from flask import current_app as app
from flask.globals import request

from warehouse_service.utils.resource import Resource


class Invoice(Resource):

    def post(self):
        request_data = request.get_json(force=True)
        print request_data
        return "Success"
