import os

#QQ_ENDPOINT - QuiverQuant endpoint to draw data from
QQ_ENDPOINT = 'https://api.quiverquant.com/beta/live/congresstrading'

#CSRFTOKEN - Secure random token
CSRFTOKEN = os.environ['CSRFTOKEN']

#QQ_API_TOKEN - QuiverQuant service API token
QQ_API_TOKEN = os.environ['QQ_API_TOKEN']