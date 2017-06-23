from flask.globals import request
from num2words import num2words

from warehouse_service.utils.resource import Resource
from uni_db.order_management.models import Order, OrderItem
from uni_db.inventory.models import Delivery, Stock, OrderItemDetails, Barcode
from uni_db.client_erp.models import Product, ClientMobile


class Invoice(Resource):

    def post(self):
        request_data = request.get_json(force=True)
        order_id = request_data.get("order_id")
        barcode_list = request_data.get("barcodes")
#         quantity_list = request_data.get("quantity")
        order = Order.objects.get(sales_order_id=int(order_id))
        delivery_type = request_data.get("delivery_type")
        order_item_count = OrderItem.objects.filter(order=order)
        product_ids = []
        for item in order_item_count:
            product_ids.append(int(str(item.item_name).split("-")[0]))
        j = 0
        try:
            for itr in range(0, len(barcode_list)):
                barcode = Barcode.objects.get(barcode_no=str(barcode_list[itr]))
                if barcode_list[itr] != "" and order_id:
                    if barcode.product_id != int(product_ids[j]):
                        return {"responseCode": 400,
                                "Message": "Product and Barcodes are mismatched"}
                    else:
                        j = j+1
        except:
                return {"responseCode": 400,
                        "Message": "Wrong Barcode inserted."}

        '''#updating delivery barcode'''
        for itr in range(0, len(barcode_list)):
            barcode = Barcode.objects.get(barcode_no=str(barcode_list[itr]))
            delivery = Delivery.objects.get(order=order)
            OrderItemDetails.objects.create(barcode=barcode,
                                            delivery=delivery,
                                            weight=0)
        '''Getting Item details'''
        item_response = []
        tax = []
        tax_percent = []
        for item in order_item_count:
            item_dict = {}
            itemnamesplit = str(item.item_name).split('-')
            item_dict['itemname'] = str(itemnamesplit[1])
            item_dict['quantity'] = str(item.quantity)
            item_dict['selling_price'] = str(item.selling_price)
            item_dict['total_product_price'] = str(int(item.selling_price
                                                       ) * int(item.quantity))
            stock = Stock.objects.get(product=int(itemnamesplit[0]))
            previousStock = stock.quantity
            fullfilled_stock = stock.fulfilled_qty
            stock.quantity = (previousStock - item.quantity)
            stock.fulfilled_qty = (fullfilled_stock - item.quantity)
            stock.save()
            item_tax = Product.objects.get(id=int(itemnamesplit[0])).gst
            temp = float(item.selling_price) * float(item.quantity)
            taxable_amt = round((float(item_tax) / 100) * temp, 2)
            tax.append(taxable_amt)
            tax_percent.append(item_tax)
            item_response.append(item_dict)
        phone = ', '.join(str(mob.mobile) for mob
                          in ClientMobile.objects.filter(client=order.owner))

        total_amount = int(order.cod_amount)
        total_amount_str = str(total_amount)
        advance_payment = str(order.advance_payment)
        amt_temp = num2words(total_amount)
        amt_in_words = amt_temp.title()
#         if ((int(order.cod_amount)+int(order.advance_payment))-100) < 800:
#             delivery_charges=100
#         else:
#             delivery_charges=0
        order_info = {}

        order_info['client_name'] = str(order.owner.client_name)
        order_info['order_id'] = str(order_id)
        order_info['address_line1'] = str(order.shipping_address.address_line1)
        order_info['area'] = str(order.shipping_address.area)
        order_info['city'] = str(order.shipping_address.city)
        order_info['pincode'] = str(order.shipping_address.pin_code)
        order_info['state'] = str(order.shipping_address.state)
        order_info['phone'] = str(phone)

#         order_info['indiaPostBarcodeNo'] = str(indiaPostBarcodeNo)
#         order_info['indiaPostBarcodeNo_id'] = str(indiaPostBarcodeNo_id)
#         order_info['delivery_type']=int(delivery_type)
#         # order_info['itemName'] = str(itemName)
#         order_info['product_wt'] = str(product_weight)
        order_info['discount'] = str(order.order_discount)
        order_info['tax'] = tax
        order_info['tax_percent'] = tax_percent
#         order_info['total_item_amount'] = float(total_item_amount)
#         order_info['total_tax'] = str(total_tax)
        order_info['created_on'] = (order.created_on).strftime("%d-%b-%Y")
        order_info['total_amount_str'] = str(total_amount_str)
        order_info['advance_payment'] = str(advance_payment)
        order_info['amt_in_words'] = str(amt_in_words)
#         #order_info['seller_address'] = str(seller_address)
#         #order_info['seller_pan'] = str(seller_pan)
#         #order_info['seller_vat'] = str(seller_vat)
        order_info['itemresponse'] = item_response
        order.status = 'READY TO DISPATCH'
        order.save()
#         Delivery.objects.filter(order=order).update(delivery_by=str(delivery_type))
#         order_info['delivery_charge'] = delivery_charges
        return order_info
