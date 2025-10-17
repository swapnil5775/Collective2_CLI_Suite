# Collective2 Trading Scripts

A comprehensive suite of Python scripts to manage your Collective2 strategy **"ProfitSetup Swinger"** (ID: 153075915) via command-line interface.

---

## 🚀 **Unified Interface (Recommended)**

### **All-in-One Trading Suite** (`c2_trading.py`)

The easiest way to use all features! One command gives you access to everything:

```bash
python3 scripts/c2_trading.py
```

**Interactive Menu:**
```
1. 📊 View Open Positions     - See all positions with real-time prices
2. 🔄 Monitor Positions (Live) - Auto-refresh every 30 seconds
3. 💼 Submit New Trade Signal  - Place new trades with guided prompts
4. 🗂️  Manage Working Orders   - View and cancel pending orders
5. ℹ️  Help & Documentation    - Quick reference
6. 🚪 Exit                     - Clean exit
```

**Features:**
- ✅ Single command for all functions
- ✅ Clean, intuitive menu interface
- ✅ Runs each tool in its own workflow
- ✅ Returns to menu after each operation
- ✅ Easy navigation and help

---

## 📋 Individual Scripts (Advanced Users)

### 1. **View Open Positions** (`c2_open_positions.py`)
Display all your current open positions with real-time prices and P/L calculations.

**Usage:**
```bash
python3 scripts/c2_open_positions.py --mode strategy --strategy-id 153075915
```

**Features:**
- ✅ Real-time stock prices from Yahoo Finance
- ✅ Real-time option prices (when available)
- ✅ Per-position P/L calculations
- ✅ Portfolio summary (cash, buying power, total P/L)
- ✅ Clean output with no warning messages
- ✅ Supports stocks, options (calls/puts), futures, forex

**Output Example:**
```
========================================================
Open Positions
========================================================
Date            Symbol          Description                         Side     Quant    Basis      Price      Unrealized P/L
--------------------------------------------------------
10/16/25 15:06  NBIS2524J150    NBIS 150 call exp Oct25             Long     14       1.58       0.05       ($2,145)
10/13/25 13:55  HUT             HUT 8 MINING CORP. COMMON SHARES    Long     20       45.61      48.77      $63
10/06/25 13:31  TSLA            TESLA                               Long     11       439.19     428.58     ($117)
--------------------------------------------------------
TOTALS                                                                                                      ($12,705)
```

---

### 2. **Monitor Positions (Auto-Refresh)** (`c2_monitor.py`)
Continuously monitor your positions with automatic refresh every 30 seconds.

**Usage:**
```bash
python3 scripts/c2_monitor.py
```

**Features:**
- ✅ Auto-refreshes every 30 seconds
- ✅ Clears screen for fresh display
- ✅ Shows last update timestamp
- ✅ Press Ctrl+C to stop

---

### 3. **Submit Trading Signals (Interactive)** (`c2_signal_interactive.py`)
Submit new trading signals through an easy-to-use interactive prompt.

**Usage:**
```bash
python3 scripts/c2_signal_interactive.py
```

**Interactive Flow:**
1. **Instrument Type**: Stock or Option
2. **Symbol**: Enter ticker (e.g., AAPL, NBIS, TSLA)
3. **Option Type** (if option): Call or Put
4. **Strike Price** (if option): Enter strike
5. **Expiry Date** (if option): Choose from quick options or enter manually
6. **Action**: Buy or Sell
7. **Order Type**: Market, Limit, or Stop
8. **Quantity**: Number of contracts/shares
9. **Time in Force**: Day or GTC
10. **Confirmation**: Review and confirm before submitting

**Features:**
- ✅ Easy-to-use guided prompts
- ✅ Smart defaults (Option, Call, This Friday, Buy, Limit, Day)
- ✅ Quick date selection (Today, Tomorrow, This/Next Friday)
- ✅ Full order preview before submission
- ✅ Confirmation required before sending
- ✅ Shows Signal ID after successful submission

---

### 4. **Submit Trading Signals (Command Line)** (`c2_submit_signal.py`)
Submit signals directly via command-line arguments for scripting/automation.

**Usage Examples:**

**Buy Option:**
```bash
python3 scripts/c2_submit_signal.py \
  --symbol NBIS \
  --action buy \
  --quantity 5 \
  --option-type call \
  --strike 150 \
  --expiry 10/24/25 \
  --limit 2.00
```

**Buy Stock:**
```bash
python3 scripts/c2_submit_signal.py \
  --symbol AAPL \
  --action buy \
  --quantity 10 \
  --order-type market
```

**Bracket Order (with Stop Loss & Profit Target):**
```bash
python3 scripts/c2_submit_signal.py \
  --symbol TSLA \
  --action buy \
  --quantity 5 \
  --limit 250.00 \
  --stop-loss 245.00 \
  --profit-target 260.00
```

**Cancel & Replace Existing Signal:**
```bash
python3 scripts/c2_submit_signal.py \
  --cancel-replace 153180409 \
  --symbol NBIS \
  --action sell \
  --quantity 1 \
  --limit 9.00
```

**Available Options:**
- `--symbol`: Ticker symbol (required)
- `--action`: buy or sell (required)
- `--quantity`: Number of contracts/shares (required)
- `--order-type`: market, limit, or stop (default: limit)
- `--limit`: Limit price
- `--stop`: Stop price
- `--tif`: day, gtc (default: day)
- `--option-type`: call or put
- `--strike`: Option strike price
- `--expiry`: Option expiry date (MM/DD/YY)
- `--stop-loss`: Stop loss price for bracket order
- `--profit-target`: Profit target price for bracket order
- `--cancel-replace`: Signal ID to cancel and replace
- `--parent-signal`: Parent signal ID for conditional orders

---

### 5. **Manage Working Orders** (`c2_manage_orders.py`)
View and cancel your working (pending/open) orders interactively.

**Usage:**
```bash
python3 scripts/c2_manage_orders.py
```

**Features:**
- ✅ Lists all working orders with details
- ✅ Shows Symbol, Action, Quantity, Price, Status, Date
- ✅ Interactive selection to cancel orders
- ✅ Confirmation before canceling
- ✅ Refresh option to update the list
- ✅ Clean, easy-to-read display

**Interactive Options:**
- Enter order number (1-N) to cancel that order
- Enter 'r' to refresh the order list
- Enter 'q' to quit

**Example Display:**
```
WORKING ORDERS (4 total)
  #   Signal ID  |           Symbol  |  Action    Qty    Price/Type
  1. Signal ID:  153180409  |  NBIS2524J150  |  SELL     1 @ $8.00 Limit
  2. Signal ID:  153180396  |  NBIS2524J150  |  SELL     3 @ $4.00 Limit
  3. Signal ID:  153169222  |   LLY2517J840  |  SELL     1 @ $7.00 Limit
```

---

## 🔧 Setup

### Prerequisites
```bash
# Install required packages
pip3 install requests yfinance
```

### Configuration
All scripts are pre-configured with:
- **API Key**: `A884F5FD-B61A-4EF1-9FEB-697F13E4E32C`
- **Strategy ID**: `153075915`
- **Strategy Name**: ProfitSetup Swinger

To change these, edit the variables at the top of each script:
```python
API_KEY = "YOUR_API_KEY"
STRATEGY_ID = YOUR_STRATEGY_ID
```

---

## 📊 Quick Reference

### **Recommended: Unified Interface**
```bash
python3 scripts/c2_trading.py
```
One command for everything! Interactive menu with all features.

### **Individual Scripts** (Advanced)

| Task | Script | Command |
|------|--------|---------|
| **All-in-One Menu** | `c2_trading.py` | `python3 scripts/c2_trading.py` |
| View positions | `c2_open_positions.py` | `python3 scripts/c2_open_positions.py --mode strategy --strategy-id 153075915` |
| Monitor live | `c2_monitor.py` | `python3 scripts/c2_monitor.py` |
| Submit order (interactive) | `c2_signal_interactive.py` | `python3 scripts/c2_signal_interactive.py` |
| Submit order (CLI) | `c2_submit_signal.py` | `python3 scripts/c2_submit_signal.py --help` |
| Manage orders | `c2_manage_orders.py` | `python3 scripts/c2_manage_orders.py` |

---

## 🎯 Common Workflows

### **Easiest Way: Use the Unified Interface**
```bash
# One command for everything!
python3 scripts/c2_trading.py

# Then select from the menu:
# 1 - View positions
# 2 - Monitor live
# 3 - Submit trade
# 4 - Manage orders
# 5 - Help
# 6 - Exit
```

### Morning Routine (Using Unified Interface)
```bash
python3 scripts/c2_trading.py
# Select: 1 (View Positions)
# Then: 4 (Manage Orders)
```

### Morning Routine (Using Individual Scripts)
```bash
# 1. Check your positions
python3 scripts/c2_open_positions.py --mode strategy --strategy-id 153075915

# 2. Check working orders
python3 scripts/c2_manage_orders.py
```

### Place a New Trade
```bash
# Unified interface (easiest)
python3 scripts/c2_trading.py  # Select option 3

# Or interactive standalone
python3 scripts/c2_signal_interactive.py

# Or command-line mode
python3 scripts/c2_submit_signal.py --symbol AAPL --action buy --quantity 10 --limit 250.00
```

### Real-Time Monitoring
```bash
# Via unified interface
python3 scripts/c2_trading.py  # Select option 2

# Or direct
python3 scripts/c2_monitor.py
```

### Clean Up Orders
```bash
# Via unified interface
python3 scripts/c2_trading.py  # Select option 4

# Or direct
python3 scripts/c2_manage_orders.py
```

---

## 📝 Notes

- All prices are real-time from Yahoo Finance (when available)
- Options prices are fetched when available; falls back to intrinsic value calculation
- All timestamps are displayed in your local timezone
- Scripts include error handling and confirmation prompts for safety
- Press Ctrl+C to safely exit any script at any time

---

## 🔗 Resources

- [Collective2 API Documentation](https://api-docs.collective2.com/)
- [Strategy Page](https://collective2.com/strategy/153075915)
- [How to Submit Signals](https://api-docs.collective2.com/guides/how-to-submit-signals)

---

## ⚠️ Important

- **Always review** orders before confirming submission
- **Test with small quantities** when trying new features
- **Keep your API key secure** - don't share it publicly
- Scripts are configured for **paper trading** by default

---

**Last Updated**: October 17, 2025  
**Version**: 2.0
