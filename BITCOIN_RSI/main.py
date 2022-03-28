from contextlib import closing
from datetime import datetime, timedelta
import alpaca_helper as helper
from alpaca_trade_api import TimeFrame
import pandas_ta as pd

# SELL_POINT - The upper RSI value to sell at
SELL_POINT = 90
# BUY_POINT - The lower RSI value to buy at
BUY_POINT = 10
# BUY_SELL_QUANTITY - The USD value to buy or sell BTC
BUY_SELL_QUANTITY = 100
# ORDER_ID - The Order ID to distinguish this trade
ORDER_ID = 'BITCOIN_RSI'

def run():
    """
    Run the RSI check after clearing all existing trades
    """
    clearExistingTrades()
    k_value, d_value = calculateStochRSI('BTCUSD', TimeFrame.Minute)
    print("Current K Value: ", k_value, "Current D Value: ", d_value)
    if k_value < BUY_POINT and d_value < BUY_POINT:
        helper.submit_order('buy', 'BTCUSD', BUY_SELL_QUANTITY, ORDER_ID)
    elif k_value > SELL_POINT and d_value > SELL_POINT:
        helper.submit_order('sell', 'BTCUSD', BUY_SELL_QUANTITY, ORDER_ID)

# MARK - Helper Methods

def calculateStochRSI(symbol, timeframe):
    """
    calculate the Stochastic RSI given the symbol and timeframe
    :param symbol: The Ticker to get the crypto data from
    :param timeframe: The frequency to grab crypto datapoints from. Can be
    a Minute, Hour, or Day
    :return: (double, double)
    """
    closing_data = helper.get_crypto_data(symbol, timeframe).df
    rsi_data = pd.stochrsi(closing_data['close'])
    rsi_data.columns = ['k', 'd']
    return rsi_data['k'].iloc[-1], rsi_data['d'].iloc[-1]

def clearExistingTrades():
    """
    clear all holdings that are still held for 10 minutes
    """
    trades = helper.get_previous_trades('BTCUSD', 11)
    for trade in trades:
        should_sell = datetime.timestamp(datetime.utcnow() - timedelta(minutes=10)) > datetime.timestamp(trade.created_at)
        if trade.side == 'buy' and trade.client_order_id == ORDER_ID and should_sell:
            helper.submit_order('sell', 'BTCUSD', BUY_SELL_QUANTITY, ORDER_ID)
    

if __name__ == "__main__":
    #configure
    helper.test_REST_connectivity()

    #run rsi
    run()