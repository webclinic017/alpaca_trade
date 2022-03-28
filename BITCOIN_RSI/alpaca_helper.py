import datetime
from time import sleep
from datetime import datetime, timedelta
from sqlalchemy import false, true
import alpaca_trade_api as alpacaTrade
import os

# MARK - API HELPER METHODS

def test_REST_connectivity():
    """
    Tests to make sure a connection can be made to Alpaca REST API
    """
    global api
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    base_url = 'https://paper-api.alpaca.markets'
    try:
        api = alpacaTrade.REST(api_key, api_secret, base_url)
        account = api.get_account()

    except:
        print("Login failed.")

def get_account_attributes(attribute):
    """
    Gets attribute from account
    Valid Attributes: account_number, accrued_fees, buying_power, cash, created_at, crypto_status, currency, daytrade_count, daytrading_buying_power,
    equity, id, initial_margin, last_equity, last_maintenance_margin, long_market_value, maintenance_margin, multiplier, non_marginable_buying_power, pattern_day_trader,
    pending_transfer_in, portfolio_value, regt_buying_power, short_market_value, shorting_enabled, sma, status, trade_suspended_by_user, trading_blocked, transfers_blocked
    """
    return getattr(api.get_account(), attribute)

def get_previous_trades(ticker, timespan=None):
    """
    Gets the current account's previous trades on ticker
    :param ticker: the ticker to check
    :param timespan: the most recent time interval to look for trades in
    """
    if timespan is not None:
        return api.list_orders('all', after= datetime.utcnow() - timedelta(minutes=timespan), symbols= [ticker])
    else:
        return api.list_orders('all', symbols= [ticker])

# MARK - MARKET HELPER METHODS

def submit_order(direction, ticker, qty, order_id, order_type = 'market', time_in_force = 'day'):
    """
    Submit an order
    :param direction: either 'buy' or 'sell'
    :param ticker: the ticker to either buy or sell of
    :param qty: the USD quantity to buy of ticker
    :param order_type: the type of order to put in. Can be a market, limit, stop, stop_limit or trailing_stop
    :param time_in_force: the type of order to put in. Can be day, gtc, opg, cls, ioc, or fok  
    """
    try:
        api.submit_order(
            symbol= ticker,
            side= direction,
            notional= qty,
            client_order_id= order_id,
            type= order_type,
            time_in_force= time_in_force
        )
        print("Market order of | $" + str(qty) + " " + ticker + " " + direction + " | completed.")
        return true
    except Exception as e:
        print(f"Order not placed. {e}")
        return false

def get_crypto_data(ticker, interval):
    """
    Getting the crypto data of ticker
    :param ticker: the ticker to grab the data from
    :param interval: the most recent time interval to look for trades in
    """
    return api.get_crypto_bars(ticker, interval, exchanges= 'CBSE')