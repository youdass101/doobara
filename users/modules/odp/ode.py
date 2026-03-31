import csv
from pathlib import Path
from django.contrib.auth.models import User
from users.models import Delivery_Address_Details
import re
from ...models import *
from django.utils import timezone
from datetime import datetime

# print("starting")
# print("importing")
# with open(r'C:\Users\Hamze\Downloads\wp_postmeta.csv', 'r', newline='', encoding='utf-8') as file:
#     data = list(csv.DictReader(file))
# result = {}
# print("processing")
# for i in data:
#     id = i['post_id']
#     if   id not in result and i['meta_key'] in ['_billing_first_name', '_billing_last_name', '_billing_phone_number', '_billing_email', '_billing_address_1', '_billing_address_2', '_billing_city', '_billing_address_index', '_order_total', '_order_currency', '_customer_user']:
#         result[id] = {}
#     if id not in result:
#         pass
#     if i['meta_key'] == '_customer_user':
#         result[id]['user_id'] = i['meta_value']
#     # shipping details
#     if i['meta_key'] == '_billing_first_name':
#         result[id]['first_name'] = i['meta_value']
#     if i['meta_key'] == '_billing_last_name':
#         result[id]['last_name'] = i['meta_value']
#     if i['meta_key'] == '_billing_phone_number':
#         result[id]['phone_number'] = i['meta_value']
#     if i['meta_key'] == '_billing_email':
#         result[id]['email'] = i['meta_value']
#     if i['meta_key'] == '_billing_address_1':
#         result[id]['address_1'] = i['meta_value']
#     if i['meta_key'] == '_billing_address_2':
#         result[id]['address_2'] = i['meta_value']
#     if i['meta_key'] == '_billing_city':
#         result[id]['city'] = i['meta_value']
#     # if i['meta_key'] == '_billing_address_index':
#     #     result[id]['address_index'] = i['meta_value']

#     # order details
#     if i['meta_key'] == '_order_total':
#         result[id]['order_total'] = i['meta_value']
#     if i['meta_key'] == '_order_currency':
#         print("found currency")
#         print(i['meta_value'])
#         result[id]['order_currency'] = i['meta_value']
    
# print(result)

def shipping_data():
    with open(r'C:\Users\Hamze\Downloads\wp_postmeta.csv', 'r', newline='', encoding='utf-8') as file:
        data = list(csv.DictReader(file))
    result = {}
    for i in data:
        id = i['post_id']
        if id not in result and i['meta_key'] in ['_billing_first_name', '_billing_last_name', '_billing_phone_number', '_billing_email', '_billing_address_1', '_billing_address_2', '_billing_city', '_billing_address_index', '_order_total', '_order_currency', '_customer_user']:
            result[id] = {}
        if id not in result:
            pass

        if i['meta_key'] == '_customer_user':
            result[id]['user_id'] = i['meta_value']
        # shipping details
        if i['meta_key'] == '_billing_first_name':
            result[id]['first_name'] = i['meta_value']
        if i['meta_key'] == '_billing_last_name':
            result[id]['last_name'] = i['meta_value']
        if i['meta_key'] == '_billing_phone':
            result[id]['phone_number'] = i['meta_value']
        if i['meta_key'] == '_billing_email':
            result[id]['email'] = i['meta_value']
        if i['meta_key'] == '_billing_address_1':
            result[id]['address_1'] = i['meta_value']
        if i['meta_key'] == '_billing_address_2':
            result[id]['address_2'] = i['meta_value']
        if i['meta_key'] == '_billing_city':
            result[id]['city'] = i['meta_value']


        # order details
        if i['meta_key'] == '_order_total':
            result[id]['order_total'] = i['meta_value']
        if i['meta_key'] == '_order_currency':
            result[id]['order_currency'] = i['meta_value']
        

    for i in list(result.keys()):  # Iterate over a copy of the keys
        if result[i]['user_id'] == '0':
            del result[i]

    address = {}
    for i in result:
        if result[i]['user_id'] not in address:
            address[result[i]['user_id']] = {}
            address[result[i]['user_id']]['first_name'] = result[i]['first_name']
            address[result[i]['user_id']]['last_name'] = result[i]['last_name']
            address[result[i]['user_id']]['phone_number'] = re.sub(r'[^\d]', '', result[i]['phone_number'])
            address[result[i]['user_id']]['address_1'] = result[i]['address_1']
            if 'address_2' in result[i]:
                address[result[i]['user_id']]['address_2'] = result[i]['address_2']
            else:
                address[result[i]['user_id']]['address_2'] = ""
            address[result[i]['user_id']]['city'] = result[i]['city']
        else:
            pass
    return address


# for i in data:
#     Delivery_Address_Details.objects.create(name=data[i]['first_name'], 
#     last_name=data[i]['last_name'], city_town=data[i]['city'],     
#     street_name=data[i]['address_1'], building_appartment=data[i]['address_2'],
#     phone_number=data[i]['phone_number'], user=data[i], default=True)


def createshipping(data):
    for i in data:
        # Fetch the User instance using the user_id
        try:
            user = User.objects.get(id=i)  # Replace 'id' with the correct field if needed
        except User.DoesNotExist:
            continue  # Skip this iteration if the user does not exist

        raw_phone_number = data[i]['phone_number']
        phone_number = re.sub(r'[^\d]', '', raw_phone_number)  # Keep only digits
        print(f"Processed phone number: {phone_number}")

        # Create the Delivery_Address_Details object
        Delivery_Address_Details.objects.create(
            name=data[i]['first_name'],
            last_name=data[i]['last_name'],
            city_town=data[i]['city'],
            street_name=data[i]['address_1'],
            building_appartment=data[i]['address_2'],
            phone_number=phone_number,
            user=user,  # Pass the User instance here
            default=True
        )

def orders():
    with open(r'C:\Users\Hamze\Downloads\wp_postmeta.csv', 'r', newline='', encoding='utf-8') as file:
        data = list(csv.DictReader(file))
    with open(r'C:\Users\Hamze\Downloads\wp_orders.csv', 'r', newline='', encoding='utf-8') as file:
        orders = list(csv.DictReader(file))
    result = {}

    for i in orders:
        result[i['ID']] = {'order_date': i['post_date'], 'order_status': i['post_status']}
        for j in data:
            if j['post_id'] == i['ID']:
                if j['meta_key'] == '_customer_user':
                    result[i['ID']]['user_id'] = j['meta_value']
                if j['meta_key'] == '_order_total':
                    result[i['ID']]['order_total'] = j['meta_value']
                if j['meta_key'] == '_order_currency':
                    result[i['ID']]['order_currency'] = j['meta_value']

    return(result)

def createorders(data):
    for i in data:
        try:
            user = User.objects.get(id=data[i]['user_id'])
        except User.DoesNotExist:
            continue  # Skip this iteration if the user does not exist

        # Fetch a default delivery address for the user
        try:
            address = Delivery_Address_Details.objects.filter(user=user).first()
        except Delivery_Address_Details.DoesNotExist:
            address = None  # Handle case where no address exists
        
         # Remove the `wp_` prefix from the order status
        order_status = str(data[i]['order_status']).replace('wc-', '')
            # Parse the order_date and make it time zone aware
        try:
            naive_order_date = datetime.strptime(data[i]['order_date'], '%Y-%m-%d %H:%M:%S')  # Adjust format as needed
            order_date = timezone.make_aware(naive_order_date)  # Convert to aware datetime
        except ValueError:
            print(f"Invalid date format for order {i}")
            continue

        Orders.objects.create(
            id = i,
            user=user,
            address=address,
            status=order_status,
            total=data[i]['order_total'],
            date=order_date,
            currency=data[i]['order_currency'],
            note=""
        )

