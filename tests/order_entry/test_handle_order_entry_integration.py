from unittest.mock import Mock
from oec.order_entry import handle_order_entry
from oec.main import TradingContext
from alpaca.trading.enums import OrderSide

def test_handle_order_entry_buy():
    mock_client = Mock()
    ctx = TradingContext(client=mock_client, risk_pct=0.02, is_paper=True, account_value=10000, risk_reward=3)

    handle_order_entry(ctx, side="buy", entry_price=100, stop_loss_price=98, symbol="AAPL")

    assert mock_client.submit_order.called
    order = mock_client.submit_order.call_args[0][0]
    assert order.symbol == "AAPL"
    assert order.side == OrderSide.BUY
    assert order.qty == 100  # risk_amount=200, delta=2, qty=100

def test_handle_order_entry_sell():
    mock_client = Mock()
    ctx = TradingContext(client=mock_client, risk_pct=0.01, is_paper=True, account_value=50000, risk_reward=5)

    handle_order_entry(ctx, side="sell", entry_price=200, stop_loss_price=205, symbol="TSLA")

    assert mock_client.submit_order.called
    order = mock_client.submit_order.call_args[0][0]
    assert order.symbol == "TSLA"
    assert order.side == OrderSide.SELL
