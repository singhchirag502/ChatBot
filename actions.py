# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"


#
import numpy as np
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import smtplib
#
class DisplayFoodMenu(Action):

    def name(self) -> Text:

        return "display_food_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Inside actions")
        conn = sqlite3.connect('food.db')
        user_message = str((tracker.latest_message)['text'])

        print("User message : ", user_message)
        if "7 Plates" in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format('7 plates')
        elif 'Anugraha Veg' in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format('Anugraha Veg')
        elif 'Leon Grill' in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format('Leon Grill')
        elif 'Brahmins Thatte Idli' in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format('Brahmins Thatte Idli')
        elif 'Delhi Xpress' in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format(
                'Delhi Xpress')
        elif 'KFC' in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format('KFC')

        content = conn.execute(exe_str)
        content_text = ''
        for index, value in enumerate(content):
            content_text += str(index + 1) + ") " + str(value[0]) + "  ----  " + str(value[1]) + "/-\n"

        content_text += "Enter item numbers (eg : 1,2,4)"
        dispatcher.utter_message(text=content_text)

        return []


class OrderReceivedFromUser(Action):

    def name(self) -> Text:

        return "order_received_from_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = sqlite3.connect('food.db')
        user_message = str((tracker.latest_message)['text'])

        messages = []

        for event in (list(tracker.events))[:15]:
            if event.get("event") == "user":
                messages.append(event.get("text"))

        user_message = messages[-1]
        print("messages : ",messages)
        print("user_message : ",user_message)
        restaurant_name = ''
        if "7 Plates" in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format('7 plates')
            restaurant_name = "7 Plates"

        elif 'Anugraha Veg' in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format('Anugraha Veg')
            restaurant_name = "Anugraha Veg"

        elif 'Leon Grill' in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format('Leon Grill')
            restaurant_name = "Leon Grill"

        elif 'Brahmins Thatte Idli' in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format('Brahmins Thatte Idli')
            restaurant_name = "Brahmins Thatte Idli"

        elif 'Delhi Xpress' in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format(
                'Delhi Xpress')
            restaurant_name = "Delhi Xpress"

        elif 'KFC' in user_message:
            exe_str = "Select food, price from food_items where restaurant_name is '{0}'".format('KFC')
            restaurant_name = "KFC"

        try:
            content = conn.execute(exe_str)

            user_input = str((tracker.latest_message)['text'])
            user_input = user_input.replace(" ", "")
            # user_input = user_input.split(',')
            user_input = [int(n) for n in user_input.split(',')]
            print("user_input : ", user_input)

            total = 0
            content_text = ''
            food_items = ''
            for index, value in enumerate(content):
                if index + 1 in user_input:
                    total += value[1]
                    food_items += value[0] + '\n'

            bill_no = np.random.randint(1,1000,1)[0]


            fromaddr = '@gmail.com'
            toaddrs = '@gmail.com'
            msg = "Hello " + restaurant_name + ",\n\nThe following food items are the new order for the bill no " \
                  + str(bill_no) + "\n\n" + food_items + "\nThanks,\nYour own food ordering app!"
            username = '@gmail.com'
            obj = open('pass.txt')
            password = obj.read()
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
            content = "The order has been taken and the respective restaurent will be notified"

            content_text = "Your order has been received and your total order is " + str(total) + \
                           " and your bill number is " + str(bill_no)
            dispatcher.utter_message(text=content_text)
            dispatcher.utter_message(text=content)

        except:
            content_text = "Sorry system run into trouble.. Can you please check again?"
            dispatcher.utter_message(text=content_text)

        return []