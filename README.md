# The Apex 20/50 Quantitative System: An Algorithmic Momentum Engine

## Abstract
The Apex 20/50 Quantitative System is a fully mechanical, state-dependent trading algorithm designed to capture medium-term market momentum while strictly managing downside risk. Built to eliminate subjective visual bias, this project bridges theoretical applied mathematics and programmatic logic architectures. 

## Architecture & Methodology
The system evaluates market data daily at 3:55 PM (End-of-Day proxy) to eliminate overnight gap exposure, executing decisions across five distinct phases.

### Phase 1: Macro & Trend Alignment
The engine requires strict mathematical proof of an established uptrend. 
* **Market Regime:** Benchmark Index Close > 200-day SMA.
* **Trend Stacking:** 20-day EMA > 50-day EMA > 200-day SMA.
* **Trend Velocity:** 14-period ADX ≥ 25.

### Phase 2: Multi-Branch Execution Logic
If Phase 1 is validated, the engine evaluates three distinct structural setups. All branches require the `Close > 20-day EMA` to anchor the setup to short-term momentum.
* **Branch A (Relaxed Bounce):** Requires a tested low below the 20 EMA, a close in the upper 50% of the daily range, and volume exceeding the 20-day SMA.
* **Branch B (Volatility Contraction):** Mathematically defines an "inside day" on low volume, indicating a pause in selling pressure.
* **Branch C (High-Momentum Breakout):** Captures breakouts into new 10-day highs supported by a 50% volume spike above the 20-day average.

### Phase 3: Volatility-Adjusted Risk Parity
* **Hard Stop-Loss:** Calculated as `Entry Price - (1.5 * 14-period ATR)`.
* **Risk Parity Sizing:** Position size is dynamically generated to ensure every trade risks exactly 1% of total account capital, normalizing risk across assets of varying volatility.

### Phase 4 & Phase 5: The Dual-Stage Trailing Exit
A mechanical scale-out engine manages live trades:
1. **Intraday Risk Boundary:** 100% market exit if the ATR Hard Stop is breached.
2. **Momentum Lock (3:55 PM):** Sells 50% of the position if the daily close drops below the fast 20-day EMA, securing short-term profits.
3. **Core Trend Break (3:55 PM):** Sells the remaining position if the daily close drops below the 50-day EMA, indicating a structural trend failure.

## Tech Stack
* **Language:** Python 3.10+
* **Core Libraries:** `pandas` (time-series data structures), `numpy` (numerical operations)

## Author's Note
System architecture, logic translation, and quantitative constraints were developed collaboratively as an exploratory project into algorithmic engineering and mechanical logic systems.