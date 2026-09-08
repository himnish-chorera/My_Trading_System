import pandas as pd
from src.rules_engine import evaluate_entry_and_risk
from src.backtest_engine import simulate_trade_lifecycle

def main():
    ACCOUNT_VALUE = 100000.0
    RISK_PCT = 0.01  
    
    # Mocking macro environment for isolated backtest
    SPY_CURRENT_CLOSE = 500
    SPY_SMA_200 = 450 
    
    try:
        df = pd.read_csv('data/historical_stock_data.csv', index_col='Date', parse_dates=True)
    except FileNotFoundError:
        print("Error: Add a formatted 'historical_stock_data.csv' to the data/ folder.")
        return

    current_capital = ACCOUNT_VALUE
    print("Initializing Apex Quantitative Engine...\n")

    for i in range(200, len(df)):
        signal = evaluate_entry_and_risk(
            df, i, SPY_CURRENT_CLOSE, SPY_SMA_200, current_capital, RISK_PCT
        )
        
        if signal["Status"] == "EXECUTE BUY":
            entry_date = df.index[i].strftime('%Y-%m-%d')
            print(f"[{entry_date}] BUY SIGNAL: {signal['Trigger']} at ${signal['Entry_Price']:.2f}")
            
            live_df = df.iloc[i + 1:]
            pnl, log = simulate_trade_lifecycle(
                live_df, signal["Entry_Price"], signal["Shares"], signal["Hard_Stop"]
            )
            
            current_capital += pnl
            print(f"   -> Trade Closed. PnL: ${pnl:.2f}. New Balance: ${current_capital:.2f}\n")

    print(f"Simulation Complete. Final Account Value: ${current_capital:.2f}")

if __name__ == "__main__":
    main()