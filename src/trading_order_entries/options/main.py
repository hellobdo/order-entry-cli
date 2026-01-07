from alpaca.trading.enums import ContractType

from trading_order_entries.context import TradingContext
from trading_order_entries.options.utils import (
    get_contract_type_enum,
    get_option_contract_request,
    get_option_type,
    get_selected_date,
    get_strike,
    get_symbol_from_input,
    get_underlying_price,
)


async def get_option_contracts(
    ctx: TradingContext,
    underlying_symbol: str,
    underlying_price: float,
    type_enum: ContractType,
):
    all_contracts = []
    request = get_option_contract_request(
        underlying_symbol, type_enum, underlying_price
    )

    response = ctx.client.get_option_contracts(request)
    all_contracts.extend(response.option_contracts)

    while response.next_page_token:
        request.page_token = response.next_page_token
        response = ctx.client.get_option_contracts(request)
        all_contracts.extend(response.option_contracts)

    return all_contracts


async def parsing_options(ctx: TradingContext, input: str) -> str | None:
    underlying_symbol = get_symbol_from_input(input)
    underlying_price = await get_underlying_price()
    option_type = await get_option_type()
    type_enum = get_contract_type_enum(option_type)
    contracts = await get_option_contracts(
        ctx, underlying_symbol, underlying_price, type_enum
    )

    if contracts:
        dates = sorted(set(str(c.expiration_date) for c in contracts))
        selected_date = await get_selected_date(dates)

        matching_contract = [
            c for c in contracts if str(c.expiration_date) == selected_date
        ]
        typed_contracts = [c for c in matching_contract if c.type == type_enum]

        strikes = sorted(set(c.strike_price for c in typed_contracts))
        selected_strike = await get_strike(strikes, underlying_price)

        final_contract = next(
            c for c in typed_contracts if c.strike_price == float(selected_strike)
        )

        option_symbol = final_contract.symbol

        print(f"Option Symbol is: {option_symbol}")

        return option_symbol

    else:
        print("No option contracts found for that ticker.")
