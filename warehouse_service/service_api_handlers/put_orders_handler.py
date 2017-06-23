'''
    @author = Akshay Kale
'''

from uni_db.inventory.models import Delivery


def handle_request(data):
    delivery_obj = Delivery.objects.get(order_id=int(data.get('order_id')))
    delivery_obj.delivery_chalan = str(data.get('challan')).strip()
    delivery_obj.driver_name = str(data.get('driver')).strip()
    order_obj = delivery_obj.order
    order_obj.status = "DISPATCHED"
    order_obj.save()
    delivery_obj.save()
    return "Sucessfully Dispatched."
