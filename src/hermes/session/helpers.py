from typing import List, Tuple

import questionary
from alpaca.trading.requests import GetOptionContractsRequest

from hermes.context import TradingContext


def get_option_contract_request(symbol) -> GetOptionContractsRequest:
    return GetOptionContractsRequest(underlying_symbols=[f"{symbol}"])


def get_symbol_from_input(input) -> str:
    return input.split()[1]


def get_strike(option_symbol) -> float:
    return int(option_symbol[-8])


def get_option_type() -> str:
    return questionary.select("Expiration:", choices=["Call", "Put"]).ask()


def get_option_symbol(selected_option) -> str:
    return selected_option.split()[0]


def get_selected_date(dates: List) -> str:
    return questionary.select("Expiration:", choices=dates).ask()


def parsing_options(ctx: TradingContext, input: str) -> Tuple:
    symbol = get_symbol_from_input(input)
    request = get_option_contract_request(symbol)
    response = ctx.client.get_option_contracts(request)

    contracts = response.option_contracts
    if contracts:
        dates = sorted(set(str(c.expiration_date) for c in contracts))
        selected_date = get_selected_date(dates)

        matching_contract = [
            c for c in contracts if str(c.expiration_date) == selected_date
        ]
        option_symbol = [c.symbol for c in matching_contract]
        print(f"Ticker of the option chain is {symbol}")

    option_type = get_option_type()
    strike = get_strike(contracts)

    stop_price = float(input("Stop price: "))

    return strike, option_type, stop_price, option_symbol
