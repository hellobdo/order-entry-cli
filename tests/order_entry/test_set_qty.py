from trading_order_entries.trading.risk_manager import set_qty


# Stock tests
def test_set_qty_stock_buy():
    entry_price, stop_loss_price, risk_amount = 100, 98, 1000
    qty = set_qty(entry_price, stop_loss_price, risk_amount, is_options=False)
    assert qty == 500  # 1000 / |100 - 98| = 1000 / 2 = 500
    assert qty * abs(entry_price - stop_loss_price) == risk_amount


def test_set_qty_stock_sell():
    entry_price, stop_loss_price, risk_amount = 100, 105, 500
    qty = set_qty(entry_price, stop_loss_price, risk_amount, is_options=False)
    assert qty == 100  # 500 / |100 - 105| = 500 / 5 = 100
    assert qty * abs(entry_price - stop_loss_price) == risk_amount


# Option tests
def test_set_qty_option():
    entry_price, stop_loss_price, risk_amount = 5.0, 4.5, 1000
    qty = set_qty(entry_price, stop_loss_price, risk_amount, is_options=True)
    assert qty == 20  # (1000 / |5.0 - 4.5|) / 100 = 2000 / 100 = 20 contracts
    assert qty * 100 * abs(entry_price - stop_loss_price) == risk_amount


def test_set_qty_option_sell():
    entry_price, stop_loss_price, risk_amount = 3.0, 4.0, 500
    qty = set_qty(entry_price, stop_loss_price, risk_amount, is_options=True)
    assert qty == 5  # (500 / |3.0 - 4.0|) / 100 = 500 / 100 = 5 contracts
    assert qty * 100 * abs(entry_price - stop_loss_price) == risk_amount
