import helpers.alpaca_helper as ah
import PUSHING_PELOSI.src.config as cf
import requests
from sqlalchemy import true
"""
Kent Waxman 2022

Builds a rebalancing Congress trading portfolio
"""

def run():
    # if ah.is_market_open() == true:
    grab_trades_to_make()
    rebalance()

# MARK - HELPER FUNCTIONS
def grab_trades_to_make():
    """
    Grab the most recent Congress trades and check if they are
    eligible to be traded on the Alpaca platform
    """
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

        tradable_assets = ah.get_tradable_assets()
    
        for index in range(len(json_trades)):
            symbol = json_trades[index]["Ticker"]
            transaction = json_trades[index]["Transaction"]
            amount = float(json_trades[index]["Amount"])
            # filter to check if the stock is traded on Alpaca
            is_tradable = [a for a in tradable_assets if a.__getattr__('symbol') == symbol]
            if is_tradable and amount >= cf.MINIMUM_AMNT:
                if transaction == 'Purchase':
                    orders[symbol] = orders.get(symbol, 0) + amount
                    sum += amount
                elif transaction == 'Sale':
                    orders[symbol] = orders.get(symbol, 0) - amount
    except Exception as err:
        print(f'Error occurred: {err}')

def rebalance():
    """
    Rebalances the portfolio based off the new trades
    """
    # put in sell orders to sell first
    equity = float(ah.get_account_attributes('equity'))
    print("EQUITY:", equity)
    
    #sort the orders from smallest to largest + iterate
    for (key, value) in sorted(orders.items(), key= lambda x: x[1]):
        weight = abs(value/sum)
        amnt = weight * equity
        if value < 0:
            print("SELLING: ", key, " AMOUNT: $", amnt)
            ah.submit_order('sell', key, amnt)
        elif value > 0:
            print("BUYING: ", key, " AMOUNT: $", amnt)
            ah.submit_order('buy', key, amnt)