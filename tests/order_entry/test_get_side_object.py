from oec.order_entry import get_side_object
from alpaca.trading.enums import OrderSide

def test_get_side_buy():
    assert get_side_object("buy") == OrderSide.BUY

def test_get_side_sell():
    assert get_side_object("sell") == OrderSide.SELL
