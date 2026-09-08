import pandas as pd
import numpy as np

def evaluate_entry_and_risk(df, current_index, spy_close, spy_sma_200, account_value, risk_pct):
    """
    Evaluates Phases 1-3 of the Apex System. 
    Requires mathematical proof of trend stacking and volume participation.
    """
    if current_index < 20:
        return {"Status": "No Trade"}

    today = df.iloc[current_index]
    yesterday = df.iloc[current_index - 1]
    highest_high_10 = df['High'].iloc[current_index-9:current_index+1].max()

    # PHASE 1: Macro & Trend Filters
    macro_regime = spy_close > spy_sma_200
    trend_stacking = (today['EMA_20'] > today['EMA_50']) and (today['EMA_50'] > today['SMA_200'])
    trend_velocity = today['ADX_14'] >= 25
    
    if not (macro_regime and trend_stacking and trend_velocity):
        return {"Status": "No Trade"}

    # PHASE 2: Multi-Branch Entry Triggers (All anchored to 20-day EMA)
    close_above_20 = today['Close'] > today['EMA_20']
    
    branch_a = (today['Low'] <= today['EMA_20']) and close_above_20 and \
               ((today['Close'] - today['Low']) / (today['High'] - today['Low']) >= 0.50) and \
               (today['Volume'] >= today['Vol_SMA_20'])

    branch_b = close_above_20 and \
               (today['High'] < yesterday['High']) and \
               (today['Low'] > yesterday['Low']) and \
               (today['Close'] > yesterday['Close']) and \
               (today['Volume'] < today['Vol_SMA_20'])

    branch_c = (today['Low'] > today['EMA_20']) and \
               (today['Close'] > highest_high_10) and \
               (today['Volume'] >= (today['Vol_SMA_20'] * 1.50))

    if not (branch_a or branch_b or branch_c):
        return {"Status": "No Trade"}

    # PHASE 3: Risk Mathematics & Risk Parity Sizing
    entry_price = today['Close']
    hard_stop = entry_price - (1.5 * today['ATR_14'])
    risk_per_share = entry_price - hard_stop
    
    if risk_per_share <= 0:
        return {"Status": "No Trade"}
        
    shares_to_buy = np.floor((account_value * risk_pct) / risk_per_share)
    trigger = "Branch A" if branch_a else "Branch B" if branch_b else "Branch C"

    return {
        "Status": "EXECUTE BUY",
        "Trigger": trigger,
        "Entry_Price": entry_price,
        "Hard_Stop": hard_stop,
        "Shares": shares_to_buy
    }