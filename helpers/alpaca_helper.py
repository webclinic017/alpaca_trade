import alpaca_trade_api as alpacaTrade
from . import config as cf
from datetime import datetime, timedelta
from sqlalchemy import false, true

# MARK - API HELPER METHODS

def test_REST_connectivity():
    """
    Tests to make sure a connection can be made to Alpaca REST API
    """
    global api
    try:
        api = alpacaTrade.REST(cf.API_KEY, cf.API_SECRET, cf.ALPACA_ENDPOINT)
    except:
        print("Login failed.")

def get_account_attributes(attribute: str):
    """
    Gets attribute from account
    Valid Attributes: account_number, accrued_fees, buying_power, cash, created_at, crypto_status, currency, daytrade_count, daytrading_buying_power,
    equity, id, initial_margin, last_equity, last_maintenance_margin, long_market_value, maintenance_margin, multiplier, non_marginable_buying_power, pattern_day_trader,
    pending_transfer_in, portfolio_value, regt_buying_power, short_market_value, shorting_enabled, sma, status, trade_suspended_by_user, trading_blocked, transfers_blocked
    """
    return getattr(api.get_account(), attribute)

def get_previous_trades(ticker: str, timespan: int = None):
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

def submit_order(direction: str, ticker: str, qty: float, order_type: str = 'market', time_in_force: str = 'day'):
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
            type= order_type,
            time_in_force= time_in_force
        )
        print("Market order of | $" + str(qty) + " " + ticker + " " + direction + " | completed.")
        return true
    except Exception as e:
        print(f"Order not placed. {e}")
        return false

def is_market_open():
    """
    Checks if the market is open
    """
    if api.get_clock().__getattr__('is_open'):
        return true
    else:
        return false

def is_an_active_asset(symbol: str):
    try:
        api.get_asset(symbol)
        print("test")
    except:
        return false
