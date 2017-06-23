'''
    @author = Akshay Kale
'''

from uni_db.order_management.models import (
    Order, OrderItem
)
from uni_db.inventory.models import Delivery
from django.core.exceptions import ObjectDoesNotExist


def handle_request(data):
    response = []
    for order in Order.objects.filter(status=str(data.get('status'))):
        orderDict = {}
        orderDict['order_id'] = str(order.sales_order_id)
        orderDict['client'] = str(order.owner.client_name.title())
        orderDict['grand_total'] = str(order.grand_total)
        orderDict['addressline1'] = str(order.shipping_address.address_line1)
        orderDict['area'] = str(order.shipping_address.area)
        orderDict['city'] = str(order.shipping_address.city)
        orderDict['pin_code'] = str(order.shipping_address.pin_code)
        orderDict['internal_note'] = order.internal_note
        orderDict['created_on'] = (order.created_on).strftime("%d/%m/%Y")
        orderItemList = []
        orderQuantityList = []
        for oi in OrderItem.objects.filter(order=order):
            itemname = oi.item_name.split('-')
            orderItemList.append(itemname[1])
            orderQuantityList.append(oi.quantity)
        orderDict['orderitems'] = orderItemList
        orderDict['orderitem_quantity'] = orderQuantityList
        try:
            orderDict['delivery_by'] = str(Delivery.objects.get(order=order
                                                                ).delivery_by)
        except ObjectDoesNotExist:
            orderDict['delivery_by'] = 'Delivery Object Not Created'
        response.append(orderDict)
    return response