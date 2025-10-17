# 📊 Managing Multiple Strategies

This guide explains how to manage multiple Collective2 strategies with the CLI Suite.

---

## 🎯 Overview

If you manage multiple trading strategies on Collective2, you can easily switch between them using the CLI Suite. The system is designed to work with **one strategy at a time per session**, which keeps things simple and prevents accidental cross-strategy trading.

---

## 🔧 Setup for Multiple Strategies

### Step 1: Create Config Files

Create a separate config file for each strategy:

```bash
cd ~/Collective2_CLI_Suite

# Copy the example for each strategy
cp scripts/config_example.py scripts/config_strategy1.py
cp scripts/config_example.py scripts/config_strategy2.py
cp scripts/config_example.py scripts/config_strategy3.py
```

### Step 2: Edit Each Config File

Edit each file with the respective strategy's information:

**Strategy 1 (e.g., "ProfitSetup Swinger"):**
```bash
nano scripts/config_strategy1.py
```
```python
"""Strategy 1: ProfitSetup Swinger"""
API_KEY = "YOUR_API_KEY"  # Same for all strategies
STRATEGY_ID = 153075915
PERSON_ID = 153075914
```

**Strategy 2 (e.g., "Tech Momentum Trader"):**
```bash
nano scripts/config_strategy2.py
```
```python
"""Strategy 2: Tech Momentum Trader"""
API_KEY = "YOUR_API_KEY"  # Same API key
STRATEGY_ID = 123456789   # Different strategy ID
PERSON_ID = 123456788
```

**Strategy 3 (e.g., "Value Investor"):**
```bash
nano scripts/config_strategy3.py
```
```python
"""Strategy 3: Value Investor"""
API_KEY = "YOUR_API_KEY"  # Same API key
STRATEGY_ID = 987654321   # Different strategy ID
PERSON_ID = 987654320
```

### Step 3: Add Comments to Identify Strategies

It's helpful to add the strategy name as a comment:

```python
"""
Strategy: ProfitSetup Swinger
Type: Options Trading
Risk Level: Medium
"""
API_KEY = "YOUR_API_KEY"
STRATEGY_ID = 153075915
PERSON_ID = 153075914
```

---

## 🚀 Usage Methods

### Method 1: Manual Switching

Switch strategies by copying the config you want:

```bash
# Use Strategy 1
cp scripts/config_strategy1.py scripts/config.py
python3 scripts/c2_trading.py

# When done, switch to Strategy 2
cp scripts/config_strategy2.py scripts/config.py
python3 scripts/c2_trading.py
```

### Method 2: Shell Aliases (Recommended)

Create convenient aliases in your `~/.zshrc` or `~/.bashrc`:

```bash
# Edit your shell config
nano ~/.zshrc  # or ~/.bashrc for bash

# Add these aliases
alias c2-swinger='cd ~/Collective2_CLI_Suite && cp scripts/config_strategy1.py scripts/config.py && python3 scripts/c2_trading.py'
alias c2-momentum='cd ~/Collective2_CLI_Suite && cp scripts/config_strategy2.py scripts/config.py && python3 scripts/c2_trading.py'
alias c2-value='cd ~/Collective2_CLI_Suite && cp scripts/config_strategy3.py scripts/config.py && python3 scripts/c2_trading.py'

# Reload your shell config
source ~/.zshrc  # or source ~/.bashrc
```

**Then just type:**
```bash
c2-swinger    # Opens ProfitSetup Swinger strategy
c2-momentum   # Opens Tech Momentum Trader strategy
c2-value      # Opens Value Investor strategy
```

### Method 3: Shell Scripts

Create launcher scripts for each strategy:

**launch_strategy1.sh:**
```bash
#!/bin/bash
cd ~/Collective2_CLI_Suite
cp scripts/config_strategy1.py scripts/config.py
echo "🚀 Loading: ProfitSetup Swinger"
python3 scripts/c2_trading.py
```

**launch_strategy2.sh:**
```bash
#!/bin/bash
cd ~/Collective2_CLI_Suite
cp scripts/config_strategy2.py scripts/config.py
echo "🚀 Loading: Tech Momentum Trader"
python3 scripts/c2_trading.py
```

Make them executable:
```bash
chmod +x launch_strategy1.sh launch_strategy2.sh
```

Run them:
```bash
./launch_strategy1.sh
./launch_strategy2.sh
```

### Method 4: Command Line Override

Use command-line arguments for individual scripts:

```bash
# View positions for Strategy 1
python3 scripts/c2_open_positions.py --mode strategy --strategy-id 153075915

# View positions for Strategy 2  
python3 scripts/c2_open_positions.py --mode strategy --strategy-id 123456789

# Submit trade to Strategy 3
python3 scripts/c2_submit_signal.py --strategy-id 987654321 --symbol AAPL --action buy --quantity 10 --limit 150.00
```

---

## 📋 Best Practices

### 1. **Name Your Config Files Clearly**
```
config_strategy1.py  → config_swinger.py
config_strategy2.py  → config_momentum.py
config_strategy3.py  → config_value.py
```

### 2. **Add Strategy Names in Comments**
Always include the strategy name in the config file:
```python
"""
Strategy: ProfitSetup Swinger
Created: 2024-10-15
"""
```

### 3. **Check Active Strategy**
Before placing trades, always verify you're in the correct strategy:
- Look at the menu header which shows Strategy ID
- Check positions to confirm they match expected strategy

### 4. **One Strategy at a Time**
Never run multiple instances of the suite simultaneously - work with one strategy per session to avoid confusion.

### 5. **Keep Track of Open Orders**
Before switching strategies, review and close any working orders in the current strategy.

---

## 🔒 Security Note

All `config_strategy*.py` files are automatically gitignored, so your API keys remain safe even if you create multiple config files.

Files that are protected:
- `scripts/config.py`
- `scripts/config_strategy1.py`
- `scripts/config_strategy2.py`
- `scripts/config_strategy*.py` (all variations)

---

## 🎯 Example Workflow

Here's a typical multi-strategy workflow:

```bash
# Morning: Check all strategies
c2-swinger    # Check positions, press 1, then 6 to exit
c2-momentum   # Check positions, press 1, then 6 to exit
c2-value      # Check positions, press 1, then 6 to exit

# Trade on Strategy 1
c2-swinger
# Select 3 (Submit Trade)
# Place your trade
# Select 6 (Exit)

# Later: Check Strategy 2
c2-momentum
# Select 1 (View Positions)
# Select 4 (Manage Orders) to cancel if needed
# Select 6 (Exit)
```

---

## 💡 Tips

1. **Use descriptive aliases** - Name them after your strategy names for easy recall
2. **Document your strategies** - Keep notes about what each strategy trades
3. **Regular checks** - Review all strategies daily, not just the active one
4. **Separate terminals** - Open different terminal windows when monitoring multiple strategies
5. **Risk management** - Be extra careful about which strategy you're trading in

---

## 🆘 Troubleshooting

**Problem: Wrong strategy loaded**
- Solution: Check the Strategy ID in the menu header
- Run: `cat scripts/config.py` to see which config is active

**Problem: API calls failing**
- Solution: Ensure your API key has access to all your strategies
- Check: Each STRATEGY_ID is correct in its config file

**Problem: Positions from wrong strategy showing**
- Solution: You may have the wrong config loaded
- Fix: Copy the correct `config_strategy*.py` to `config.py`

---

## 🚀 Future Enhancement

A future version may include an interactive strategy selector that lets you choose from all your strategies at startup, eliminating the need for multiple config files!

---

---

**Questions?** Check the main [README.md](../README.md) or [open an issue](https://github.com/swapnil5775/Collective2_CLI_Suite/issues).

**Other Guides:**
- [Quick Start](../QUICKSTART.md)
- [Getting Started](GETTING_STARTED.md)
- [Features & Commands](FEATURES.md)

