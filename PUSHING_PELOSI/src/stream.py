import helpers.alpaca_helper as ah
import PUSHING_PELOSI.src.config as cf
import requests
"""
Kent Waxman 2022

Builds a rebalancing Congress trading portfolio
"""

# MARK - HELPER FUNCTIONS
def grab_trades_to_make():
    global orders
    global sum
    orders = {}
    sum = 0.0
    try:
        #accesses QuiverQuant API
        headers = { 'accept': 'application/json',
        'X-CSRFToken': cf.CSRFTOKEN,
        'Authorization': 'Token ' + cf.QQ_API_TOKEN
        }
        req = requests.get(cf.QQ_ENDPOINT, headers=headers)
        req.raise_for_status()

        json_trades = req.json()
        
        for index in range(len(json_trades)):
            if json_trades[index]["Transaction"] == 'Purchase':
                orders[json_trades[index]["Ticker"]] = orders.get(json_trades[index]["Ticker"], 0) + float(json_trades[index]["Amount"])
                sum += float(json_trades[index]["Amount"])
            else:
                orders[json_trades[index]["Ticker"]] = orders.get(json_trades[index]["Ticker"], 0) - float(json_trades[index]["Amount"])
    except Exception as err:
        print(f'Error occurred: {err}')

def rebalance():
    # put in sell orders to sell first
    equity = float(ah.get_account_attributes('equity'))
    print("EQUITY1:", equity)
    
    #sort the orders from smallest to largest
    sorted(orders, key=orders.get)
    for key in orders:
        amnt = abs((orders[key] * equity)/sum)
        if orders[key] < 0:
            print("SELLING: ", key, " AMOUNT: $", amnt)
            ah.submit_order('sell', key, amnt)
        elif orders[key] > 0:
            print("BUYING: ", key, " AMOUNT: $", amnt)
            ah.submit_order('buy', key, amnt)
#     for key in sells:
#         amnt = abs((sells[key] * equity)/sum)
#         orders[key] = amnt
# #         print("SELLING: ", key, " AMOUNT: $", amnt)

# #     # equate for portfolio value change and now put in buy orders
#     equity = float(ah.get_account_attributes('equity')) 
#     print("EQUITY1: ", equity)
#     for key in purchases:
#         amnt = abs((purchases[key] * equity)/sum)
#         print("PUCHASE: (", abs(purchases[key])," * ", equity, ")/", abs(sum), " = ", amnt)
#         print("BUYING: ", key, " AMOUNT: $", amnt)
#         ah.submit_order('buy', key, amnt)    
