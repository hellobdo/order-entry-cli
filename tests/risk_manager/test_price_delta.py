from trading_order_entries.trading.risk_manager import define_price_delta


def test_define_price_delta_long():
    assert define_price_delta(100.0, 95.0) == 5.0


def test_define_price_delta_short():
    assert define_price_delta(95.0, 100.0) == 5.0


def test_define_price_delta_zero():
    assert define_price_delta(100.0, 100.0) == 0.0
