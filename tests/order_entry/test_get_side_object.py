from alpaca.trading.enums import OrderSide

from trading_order_entries.trading.orders.utils import get_entry_side_object


def test_get_side_buy():
    assert get_entry_side_object("buy") == OrderSide.BUY


def test_get_side_sell():
    assert get_entry_side_object("sell") == OrderSide.SELL
