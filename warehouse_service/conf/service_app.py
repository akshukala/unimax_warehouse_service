from uni_db.settings.pool import init_pool
from os.path import dirname, abspath

import django
from django.db import close_old_connections
from flask import Flask
from flask.ext import restful

from warehouse_service.conf.config_logger_setup import setup_config_logger
from warehouse_service.session.interfaces import DBInterface
from flask.ext.cors import CORS
from warehouse_service.service_apis.ping import Ping
from warehouse_service.service_apis.products import AllProducts
from warehouse_service.service_apis.orders import Orders
from warehouse_service.service_apis.invoice import Invoice

close_old_connections()
init_pool()

django.setup()
app = Flask(__name__)
CORS(app)
app.auth_header_name = 'X-Authorization-Token'
app.session_interface = DBInterface()
app.root_dir = dirname(dirname(abspath(__file__)))

api = restful.Api(app)

setup_config_logger(app)

app.logger.info("Setting up Resources")
api.add_resource(Ping, '/warehouseservice/ping/')
api.add_resource(AllProducts, '/warehouseservice/products/')
api.add_resource(Orders, '/warehouseservice/orders/')
api.add_resource(Invoice, '/warehouseservice/invoice/')

app.logger.info("Resource setup done")

if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=7289,threaded=True)
