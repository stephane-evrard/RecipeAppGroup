from PIL import Image, ImageFont, ImageDraw
from django.shortcuts import render     
from recipeapp.models.models import LNmpesaOnline
from recipeapp.serializers.mpesaserializer import LNMOnlineSerializer
from rest_framework.generics import CreateAPIView
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from django.contrib.auth.models import User
from recipeapp.views.mpesa_credentials import LipanaMpesaPpassword, MpesaAccessToken
from django.views.decorators.csrf import csrf_exempt

def getAccessToken(request):
    consumer_key = '9Ct0gNXcCKbcNBbX4IlMqO5lIChMsXiO'
    consumer_secret = '9lthLw1bOfNAjt6I'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)
@csrf_exempt
def lipa_na_mpesa_online(request):
    phone=request.POST.get('phone')
    phone=str(phone)
    print(phone)
    phone=phone[1:]
    phone=str(phone)
    pre='254'
    phone=(pre+phone)
    
   
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": phone,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phone,  # replace with your phone number to get stk push
        "CallBackURL": "https://addd-154-123-35-225.ngrok.io/lnm",
        "AccountReference": "Mwashe",
        "TransactionDesc": "Testing stk push"
    }
    
    response = requests.post(api_url, json=request, headers=headers)
    print(response.json)
    return HttpResponse(response)

from rest_framework.permissions import AllowAny
class LnmOnlinecallbackurlView(CreateAPIView):
    queryset = LNmpesaOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self,request):
        print(request.data,'htis is request.data')
        if (request.data["Body"]["stkCallback"]["ResultCode"])==1:
                
            merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
            print(merchant_request_id, "this should be MerchantRequestID")
            checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
            result_code = request.data["Body"]["stkCallback"]["ResultCode"]
            result_description = request.data["Body"]["stkCallback"]["ResultDesc"]


            our_model = LNmpesaOnline.objects.create(
            CheckoutRequestID=checkout_request_id,
            MerchantRequestID=merchant_request_id,
            ResultDesc= request.data["Body"]["stkCallback"]["ResultDesc"]
            
            
             )

            our_model.save()

            from rest_framework.response import Response

            return Response({"OurResultDesc": "0 response!"})
        else:
            merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
            print(merchant_request_id, "this should be MerchantRequestID")
            checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
            result_code = request.data["Body"]["stkCallback"]["ResultCode"]
            result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
            amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
            print(amount, "this should be an amount")

            mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
            print(mpesa_receipt_number, "this should be an mpesa_receipt_number")

            balance = ""
            transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][2]["Value"]
            print(transaction_date, "this should be an transaction_date")

            phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
            print(phone_number, "this should be an phone_number")


           
         


            from datetime import datetime

            str_transaction_date = str(transaction_date)
            print(str_transaction_date, "this should be an str_transaction_date")

            transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")
            print(transaction_datetime, "this should be an transaction_datetime")

            import pytz
            aware_transaction_datetime = pytz.utc.localize(transaction_datetime)
            print(aware_transaction_datetime, "this should be an aware_transaction_datetime")


       

            our_model = LNmpesaOnline.objects.create(
            CheckoutRequestID=checkout_request_id,
            MerchantRequestID=merchant_request_id,
            Amount=amount,
            ResultCode=result_code,
            ResultDesc=result_description,
            MpesaReceiptNumber=mpesa_receipt_number,
            Balance=balance,
            TransactionDate=aware_transaction_datetime,
            PhoneNumber=phone_number,
          
          
            )

            our_model.save()

            from rest_framework.response import Response

            return Response({"OurResultDesc": "YEEY!!! It worked!"})

    """
    {
        'Body': 
    {
        'stkCallback': 
    {
        'MerchantRequestID': '24996-28895321-1',
        'CheckoutRequestID': 'ws_CO_201020211139418897',
        'ResultCode': 1, 
        'ResultDesc':
        'The balance is insufficient for the transaction'
    }
        }
            }
    """
    
    """
    {'Body': {'stkCallback': {'MerchantRequestID': '4823-4875128-1', 
    'CheckoutRequestID': 'ws_CO_211020211156436315', 
    'ResultCode': 0, 
    'ResultDesc': 'The service request is processed successfully.',
     'CallbackMetadata': {'Item': [
    {'Name': 'Amount', 'Value': 1.0}, 
     {'Name': 'MpesaReceiptNumber', 'Value': 'PJL3J4JYWF'}, 
    {'Name': 'TransactionDate', 'Value': 20211021115656}, 

    {'Name': 'PhoneNumber', 'Value': 254745441222}]
    }}}}
    """
        

