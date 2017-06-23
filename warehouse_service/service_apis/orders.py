from flask.globals import request

from warehouse_service.utils.resource import Resource
from warehouse_service.service_api_handlers import get_orders_handler
from warehouse_service.service_api_handlers import put_orders_handler


class Orders(Resource):

    def get(self):
        data = request.args.to_dict()
        return get_orders_handler.handle_request(data)

    def put(self):
        request_data = request.get_json(force=True)
        return put_orders_handler.handle_request(request_data)