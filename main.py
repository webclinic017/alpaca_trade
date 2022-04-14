import helpers.alpaca_helper as ah
import PUSHING_PELOSI.src.stream as str

"""
Kent Waxman 2022

Executes the current scripts
"""

def run_scripts():
    # PUSHING_PELOSI
    str.run()

if __name__ == "__main__":
    #check if current credentials can access alpaca REST API
    ah.test_REST_connectivity()
    run_scripts()