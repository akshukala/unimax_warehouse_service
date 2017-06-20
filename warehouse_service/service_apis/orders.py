from flask import current_app as app
from flask.globals import request

from warehouse_service.utils.resource import Resource
from warehouse_service.service_api_handlers import get_fulfillable_orders_handler


class Orders(Resource):

    def get(self):
        return get_fulfillable_orders_handler.handle_request()
