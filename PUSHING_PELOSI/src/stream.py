import helpers.alpaca_helper as ah
import PUSHING_PELOSI.src.config as cf
import requests
from sqlalchemy import true, false
"""
Kent Waxman 2022

Builds a rebalancing Congress trading portfolio
"""

def run():
    if ah.is_market_open() == false:
        grab_trades_to_make()
        rebalance()

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
        
        #check the trades for trading eligbility
        active_assets = ah.get_active_assets()
        for index in range(len(json_trades)):
            # check if the stock is traded on alpaca
            if json_trades[index]["Ticker"] in active_assets:
                if json_trades[index]["Transaction"] == 'Purchase':
                    orders[json_trades[index]["Ticker"]] = orders.get(json_trades[index]["Ticker"], 0) + float(json_trades[index]["Amount"])
                    sum += float(json_trades[index]["Amount"])
                elif json_trades[index]["Transaction"] == 'Sale':
                    orders[json_trades[index]["Ticker"]] = orders.get(json_trades[index]["Ticker"], 0) - float(json_trades[index]["Amount"])
    except Exception as err:
        print(f'Error occurred: {err}')

def rebalance():
    # put in sell orders to sell first
    equity = float(ah.get_account_attributes('equity'))
    print("EQUITY:", equity)
    
    #sort the orders from smallest to largest + iterate
    for (key, value) in sorted(orders.items(), key= lambda x: x[1]):
        weight = abs(value/sum)
        amnt = weight * equity
        if orders[key] < 0:
            print("SELLING: ", key, " AMOUNT: $", amnt)
            ah.submit_order('sell', key, amnt)
        elif orders[key] > 0:
            print("BUYING: ", key, " AMOUNT: $", amnt)
            ah.submit_order('buy', key, amnt)