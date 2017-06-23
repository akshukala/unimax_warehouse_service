from flask.globals import request

from warehouse_service.utils.resource import Resource
from uni_db.inventory.models import Stock


class ProductBarcode(Resource):

    def put(self):
        request_data = request.get_json(force=True)
        stock_obj = Stock.objects.get(product_id=int(request_data.get('product_id')))
        qty = int(request_data.get('quantity')) + int(stock_obj.quantity)
        stock_obj.quantity = qty
        stock_obj.save()
        return "Stock successfully updated."