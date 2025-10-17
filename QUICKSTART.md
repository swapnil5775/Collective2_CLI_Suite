# ⚡ Quick Start Guide

Get trading in 5 minutes!

## 1️⃣ Install (1 minute)

```bash
git clone https://github.com/swapnil5775/Collective2_CLI_Suite.git
cd Collective2_CLI_Suite
pip3 install requests yfinance
```

## 2️⃣ Configure (2 minutes)

```bash
# Copy example config
cp scripts/config_example.py scripts/config.py

# Edit with your credentials
nano scripts/config.py
```

**What to add:**
- **API Key**: Get from [Collective2 API Docs](https://api-docs.collective2.com/)
- **Strategy ID**: From your strategy URL (the number at the end)

```python
API_KEY = "YOUR-API-KEY-HERE"
STRATEGY_ID = 123456789  # Your actual strategy ID
PERSON_ID = 123456788    # Usually Strategy ID - 1
```

## 3️⃣ Run (30 seconds)

```bash
python3 scripts/c2_trading.py
```

**Select from menu:**
- `1` - View positions
- `2` - Monitor live
- `3` - Submit trade
- `4` - Manage orders
- `5` - Help
- `6` - Exit

## 🎯 Multiple Strategies?

Create config for each:
```bash
cp scripts/config_example.py scripts/config_strategy1.py
cp scripts/config_example.py scripts/config_strategy2.py

# Edit each with different strategy IDs
nano scripts/config_strategy1.py
nano scripts/config_strategy2.py
```

Switch between them:
```bash
# Use Strategy 1
cp scripts/config_strategy1.py scripts/config.py
python3 scripts/c2_trading.py

# Use Strategy 2
cp scripts/config_strategy2.py scripts/config.py
python3 scripts/c2_trading.py
```

**Or create aliases:**
```bash
# Add to ~/.zshrc or ~/.bashrc
alias c2-strategy1='cd ~/Collective2_CLI_Suite && cp scripts/config_strategy1.py scripts/config.py && python3 scripts/c2_trading.py'
alias c2-strategy2='cd ~/Collective2_CLI_Suite && cp scripts/config_strategy2.py scripts/config.py && python3 scripts/c2_trading.py'

# Then just type:
c2-strategy1  # Opens Strategy 1
c2-strategy2  # Opens Strategy 2
```

## 📚 More Help

- **Detailed Setup**: See [README.md](README.md)
- **Multi-Strategy**: See [MULTI_STRATEGY.md](scripts/MULTI_STRATEGY.md)
- **Getting Started**: See [GETTING_STARTED.md](scripts/GETTING_STARTED.md)

## ⚠️ Security

✅ Your `config.py` is gitignored (safe from git)  
✅ All `config_strategy*.py` files are gitignored  
✅ API keys never committed to GitHub  

## 🚀 You're Ready!

Start trading:
```bash
python3 scripts/c2_trading.py
```

**Happy Trading!** 🎉

