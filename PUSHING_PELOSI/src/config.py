import os

#QQ_ENDPOINT - QuiverQuant endpoint to draw data from
QQ_ENDPOINT = 'https://api.quiverquant.com/beta/live/congresstrading'

#CSRFTOKEN - Secure random token
CSRFTOKEN = os.environ.get('CSRFTOKEN')

#QQ_API_TOKEN - QuiverQuant service API token
QQ_API_TOKEN = os.environ.get('QQ_API_TOKEN')

#MINIMUM_AMNT - Minimum notional amount to buy a stock at
MINIMUM_AMNT = 1.00
