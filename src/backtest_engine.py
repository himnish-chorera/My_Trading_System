import pandas as pd

def simulate_trade_lifecycle(live_df, entry_price, initial_shares, hard_stop):
    """
    Simulates the Phase 5 Dual-Stage Trailing Exit day-by-day.
    """
    position_pct = 1.0
    shares_remaining = initial_shares
    realized_pnl = 0.0
    exit_log = []

    for row in live_df.itertuples():
        
        # 1. Hard Risk Boundary (Intraday)
        if row.Low <= hard_stop:
            trade_pnl = (hard_stop - entry_price) * shares_remaining
            realized_pnl += trade_pnl
            exit_log.append({"Date": row.Index, "Exit": "Hard Stop", "PnL": trade_pnl})
            break

        # 2. Core Trend Break (100% Exit at Close)
        elif row.Close < row.EMA_50:
            trade_pnl = (row.Close - entry_price) * shares_remaining
            realized_pnl += trade_pnl
            exit_log.append({"Date": row.Index, "Exit": "Trend Break", "PnL": trade_pnl})
            break

        # 3. Momentum Lock (50% Scale-Out at Close)
        elif row.Close < row.EMA_20 and position_pct == 1.0:
            scale_out_shares = initial_shares * 0.5
            trade_pnl = (row.Close - entry_price) * scale_out_shares
            realized_pnl += trade_pnl
            exit_log.append({"Date": row.Index, "Exit": "50% Scale-Out", "PnL": trade_pnl})
            shares_remaining -= scale_out_shares
            position_pct = 0.5 

    return realized_pnl, exit_log