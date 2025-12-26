# This modules provides access to Motherduck and its persistent data (ohlcv and exchange tickers)
import os

import duckdb


class DuckDBConnector:
    def __init__(self, db_path: str = "md:stocksdb"):
        self.db_path = db_path
        self._setup_motherduck_token()
        self.conn = duckdb.connect(self.db_path)

    def _setup_motherduck_token(self) -> None:
        """Set up MotherDuck token if available."""
        token = os.getenv("MOTHERDUCK_TOKEN")
        if token:
            os.environ["motherduck_token"] = token

    def log_trades(self, data) -> None:
        """
        Log trades to the database.

        Args:
            Data
        """

        self.conn.execute("""
            INSERT INTO trades (id)

        """)
