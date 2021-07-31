from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pymysql

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet



def read(order):
    db = pymysql.connect(host='database-2.cjl0yu7gdnh3.eu-west-1.rds.amazonaws.com',
  user='admin',
  password='Mac31415926',
  port=3306,
  database='mysql')
    cursor = db.cursor()
    sql = "Select * from Chatbot.Person where Id = {}".format(order)
    try:
        return cursor.execute(sql)
    except:
        print("Error fetching data.")
        return results 


class GetOrderInformaition(Action):
    def name(self):
        return "get_order_information"
    def run(self,dispatcher,tracker,domain):
        user_order = tracker.get_slot('order number')
        order_information = read(user_order)
        response = "Your order information:\n{}".format(order_information)
        dispatcher.utter_message(response)
        return [Slotset("order number", user_order)]

    
    
    