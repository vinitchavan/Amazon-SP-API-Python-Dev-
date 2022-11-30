
#for refrence : https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference 

#First we need to install python amazon sp api package 


!pip install python-amazon-sp-api

from sp_api.api import Orders

from sp_api.base import SellingApiException


#from datetime import datetime, timedelta
from sp_api.base import SellingApiException, Marketplaces
#from datetime import date
from oauth2client.service_account import ServiceAccountCredentials

import sp_api
import pandas as pd
import csv
import io
import requests
import os

"""
To store the credentials  you can use diffrent types of methods such as 
1. .env file 
2. key ring method
3. save it in dict

Here I am using dict to save it one can save their credentials in .env file that would be a great choice.
"""
marketpalce_id = 'A1PA6795UKMFR9'

#app_id = 'amzn1.application-oa2-client.eee360076bac453ba5a4b2c1d7bf66ba'
refresh_token_from_app = 'Atzr|*************'

clientid_from_app = 'amzn1.application*********'
clientsecret_from_app = '*****************'

aws_access_key = '******************'
aws_secret_key = '******************'
role_arn = 'arn:aws:iam::***********'

credentials=dict(
refresh_token=refresh_token_from_app,
lwa_app_id=clientid_from_app,
lwa_client_secret=clientsecret_from_app,
aws_secret_key=aws_secret_key,
aws_access_key=aws_access_key,
role_arn=role_arn )# from application

marketplaces = ['A1PA6795UKMFR9'] # you can create a list of your all marketplace IDS

"""
Fuction to get date wise order from Order API
This Function will take date argument before and after then until next token ends it will run and fetch all the records from all the pags. 
Shippening add and Order total are need to be normalized at the end.    

"""
def start_orders(CreatedAfter,CreatedBefore):
  try:
    orders_obj = Orders(marketplace=Marketplaces.DE,credentials=credentials).get_orders(CreatedAfter=CreatedAfter,CreatedBefore = CreatedBefore,MarketplaceIds=','.join(marketplaces))
    orders = orders_obj.payload

    data = orders['Orders']
    Data = pd.DataFrame(data)

    NextToken = orders['NextToken']
    while(1):
      orders_new_obj = Orders(marketplace=Marketplaces.DE,credentials=credentials). get_orders(NextToken = NextToken)
      orders_new = orders_new_obj.payload

      i_data = orders_new['Orders']
      i_Data = pd.DataFrame(i_data)
      Data = pd.concat([Data,i_Data], ignore_index = True)
      NextToken = orders_new['NextToken']
      #time = Data['PurchaseDate'].tail(1).to_string(index = False)

  except:
    Data = pd.concat([Data.drop(['OrderTotal'], axis=1),pd.json_normalize(Data['OrderTotal'])],axis=1)
    Data = pd.concat([Data.drop(['ShippingAddress'], axis=1),pd.json_normalize(Data['ShippingAddress'])],axis=1)
    pass

