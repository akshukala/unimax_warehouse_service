from flask import current_app as app
from flask.globals import request

from warehouse_service.utils.resource import Resource
from uni_db.client_erp.models import Product


class AllProducts(Resource):

    def get(self):
        '''Get all product list'''
        return [{
                 'product_id': p.id,
                 'productName': p.product_name,
                 'mrp': p.mrp,
                 'selling_price': p.selling_price
                 }for p in Product.objects.filter(active=True)]