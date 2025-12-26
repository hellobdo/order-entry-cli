import csv
import os
from datetime import datetime
from typing import Tuple

from alpaca.data.historical import OptionHistoricalDataClient, StockHistoricalDataClient
from alpaca.trading.client import TradingClient
from alpaca.trading.stream import TradingStream
from dotenv import load_dotenv

from hermes.context import TradingContext


def _get_api_keys(is_paper) -> Tuple:
    load_dotenv()

    api_key = (
        os.environ["ALPACA_API_KEY_PAPER"]
        if is_paper
        else os.environ["ALPACA_API_KEY_LIVE"]
    )
    secret_key = (
        os.environ["ALPACA_SECRET_KEY_PAPER"]
        if is_paper
        else os.environ["ALPACA_SECRET_KEY_LIVE"]
    )

    return api_key, secret_key


def get_alpaca_clients(is_paper: bool, raw_data: bool = False) -> Tuple:
    api_key, secret_key = _get_api_keys(is_paper)
    client = TradingClient(api_key, secret_key, paper=is_paper, raw_data=raw_data)
    stock_data = StockHistoricalDataClient(api_key, secret_key)
    option_data = OptionHistoricalDataClient(api_key, secret_key)

    return client, stock_data, option_data


def get_account_value(client: TradingClient) -> Tuple:
    account = client.get_account()
    account_value = float(account.last_equity or 0)
    account_currency = account.currency

    print(
        f"Account value for risk calculations today is {account_currency} {account_value:,.2f}"
    )

    return account_value, account_currency


async def start_stream(ctx: TradingContext) -> None:
    api_key, secret_key = _get_api_keys(ctx.is_paper)

    trading_stream = TradingStream(api_key, secret_key, paper=ctx.is_paper)

    async def update_handler(data):
        order = data.order
        print(f"\n Order Update: {data.event.upper()}")
        print(
            f"   Symbol: {order.symbol} | Side: {order.side.value} | Type: {order.type.value}"
        )
        print(f"   Qty: {order.qty} | Status: {order.status.value}")
        if order.limit_price:
            print(f"   Limit Price: ${order.limit_price}")
        if order.stop_price:
            print(f"   Stop Price: ${order.stop_price}")

        if data.event == "fill":
            print("Order filled! Use 'modify order' to adjust quantity")
            with open("order_fills.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([datetime.now(), str(data.__dict__)])
            # ctx.duckdb.log_trades(data)

        if order.filled_avg_price:
            print(f"   Filled Price: ${order.filled_avg_price}")

        print()  # Add blank line after update

    trading_stream.subscribe_trade_updates(update_handler)
    await trading_stream._run_forever()
