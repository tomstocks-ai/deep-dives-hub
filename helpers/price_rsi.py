from openbb import obb
import pandas as pd


def get_price_and_rsi(ticker: str, hist_start: str = "2023-01-01", rsi_length: int = 14):
    """
    Fetch today's price and RSI for a given ticker.

    Parameters
    ----------
    ticker : str
        Stock symbol (e.g. "MSFT", "AAPL").
    hist_start : str, optional
        Start date for historical data used in RSI calculation (YYYY-MM-DD).
    rsi_length : int, optional
        RSI look-back period (default 14).

    Returns
    -------
    dict
        { "price": float, "rsi": float }
    """
    # Historical daily data for RSI calculation
    stock_df_hist = (
        obb.equity.price.historical(symbol=ticker, start_date=hist_start)
        .to_df()
        .reset_index()
        .drop_duplicates(subset="date")
    )

    # Today's latest 1-minute bar (current price)
    today_str = pd.Timestamp.now().strftime("%Y-%m-%d")
    stock_df_today = (
        obb.equity.price.historical(symbol=ticker, start_date=today_str, interval="1m")
        .to_df()
        .reset_index()
        .drop_duplicates(subset="date")
        .tail(1)
    )

    # Combine history + today's last tick
    stock_df = pd.concat([stock_df_hist, stock_df_today])

    # Calculate RSI
    rsi_df = obb.technical.rsi(
        data=stock_df, target="close", length=rsi_length, scalar=100.0, drift=1
    ).to_df()

    latest = rsi_df.iloc[-1]
    return {
        "price": round(float(latest["close"]), 2),
        "rsi": round(float(latest[f"close_RSI_{rsi_length}"]), 2),
    }


# Example usage
if __name__ == "__main__":
    result = get_price_and_rsi("MSFT")
    print(result)   # {'price': 450.12, 'rsi': 62.34}
