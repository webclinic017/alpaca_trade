import helpers.alpaca_helper as ah
import PUSHING_PELOSI.src.config as cf
import requests
"""
Kent Waxman 2022

Builds a rebalancing Congress trading portfolio
"""

# MARK - HELPER FUNCTIONS
def grab_trades_to_make():
    global purchases
    global sells
    global sum
    purchases = {}
    sells = {}
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
            sum += float(json_trades[index]["Amount"])
            if json_trades[index]["Transaction"] == 'Purchase':
                purchases[json_trades[index]["Ticker"]] = purchases.get(json_trades[index]["Ticker"], 0) + float(json_trades[index]["Amount"])
            else:
                sells[json_trades[index]["Ticker"]] = sells.get(json_trades[index]["Ticker"], 0) - float(json_trades[index]["Amount"])
    except Exception as err:
        print(f'Error occurred: {err}')

def rebalance():
    # put in sell orders to sell first
    portfolio_value = float(ah.get_account_attributes('portfolio_value'))
    print("PORTFOLIO VALUE 1:", portfolio_value)
    for key in sells:
        amnt = abs((sells[key] * portfolio_value)/sum)
        print("SELLING: ", key, " AMOUNT: $", amnt)
        ah.submit_order('sell', key, amnt)

    # equate for portfolio value change and now put in buy orders
    cash = float(ah.get_account_attributes('cash'))
    print("CASH: ", cash)
    for key in purchases:
        amnt = abs((purchases[key] * cash)/sum)
        print("BUYING: ", key, " AMOUNT: $", amnt)
        ah.submit_order('buy', key, amnt)    
