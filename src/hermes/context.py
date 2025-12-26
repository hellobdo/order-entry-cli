from dataclasses import dataclass

from alpaca.data.historical import OptionHistoricalDataClient, StockHistoricalDataClient
from alpaca.trading.client import TradingClient

from hermes.session.db import DuckDBConnector


@dataclass
class TradingContext:
    client: TradingClient
    stock_data: StockHistoricalDataClient
    option_data: OptionHistoricalDataClient
    duckdb: DuckDBConnector
    risk_pct: float
    is_paper: bool
    account_value: float
    account_currency: str
    risk_reward: float
    risk_amount: float
