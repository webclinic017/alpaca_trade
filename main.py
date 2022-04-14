from sqlalchemy import true
import helpers.alpaca_helper as ah
import PUSHING_PELOSI.src.stream as str

"""
Kent Waxman 2022

Executes the current scripts
"""

def run_scripts():
    # PUSHING_PELOSI
    if ah.is_market_open() == true:
        str.grab_trades_to_make()
        str.rebalance()

if __name__ == "__main__":
    #check if current credentials can access alpaca REST API
    ah.test_REST_connectivity()
    run_scripts()