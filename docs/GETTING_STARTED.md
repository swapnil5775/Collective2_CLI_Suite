# 🚀 Getting Started with Collective2 Trading Suite

Welcome! This guide will get you trading via CLI in 2 minutes.

## ⚡ Quick Start (Simplest Way)

Run this ONE command:

```bash
python3 scripts/c2_trading.py
```

You'll see a menu like this:

```
╔════════════════════════════════════════════════╗
║  🚀 COLLECTIVE2 TRADING SUITE                  ║
║  Strategy: ProfitSetup Swinger (ID: 153075915) ║
╚════════════════════════════════════════════════╝

📋 MAIN MENU

  1. 📊 View Open Positions
  2. 🔄 Monitor Positions (Live)
  3. 💼 Submit New Trade Signal
  4. 🗂️  Manage Working Orders
  5. ℹ️  Help & Documentation
  6. 🚪 Exit

Enter your choice [1-6]:
```

**That's it!** Just pick a number and hit Enter.

---

## 📖 What Each Option Does

### Option 1: View Open Positions
- See all your current positions
- Real-time prices from Yahoo Finance
- Profit/Loss calculations
- Portfolio summary

### Option 2: Monitor Positions (Live)
- Auto-refreshes every 30 seconds
- Watch your positions in real-time
- Press Ctrl+C to stop

### Option 3: Submit New Trade
Interactive prompts ask you:
1. Stock or Option?
2. Symbol? (e.g., AAPL, NBIS)
3. Call or Put? (if option)
4. Strike price? (if option)
5. Expiry date? (if option - quick selections available)
6. Buy or Sell?
7. Market, Limit, or Stop?
8. Quantity?
9. Confirm and submit!

### Option 4: Manage Working Orders
- View all pending orders
- Select order number to cancel it
- Confirm cancellation
- Refresh the list anytime

### Option 5: Help
- Quick reference guide
- Command examples
- Documentation links

### Option 6: Exit
- Clean exit from the program

---

## 🎯 Your First Trade (Step by Step)

1. **Start the program:**
   ```bash
   python3 scripts/c2_trading.py
   ```

2. **Press `3`** (Submit New Trade)

3. **Follow the prompts:**
   ```
   Stock or Option? → Press 2 (Option)
   Symbol? → Type: AAPL
   Call or Put? → Press 1 (Call)
   Strike? → Type: 200
   Expiry? → Press 3 (This Friday)
   Buy or Sell? → Press 1 (Buy)
   Order Type? → Press 2 (Limit)
   Limit Price? → Type: 5.00
   Quantity? → Type: 2
   Time in Force? → Press 1 (Day)
   ```

4. **Review and confirm:**
   - You'll see a summary of your order
   - Type `y` to submit or `n` to cancel

5. **Done!** Your order is now submitted to Collective2

---

## 💡 Pro Tips

### Tip 1: Check Positions First
Before trading, always check what you have:
```bash
python3 scripts/c2_trading.py
# Press 1 (View Positions)
```

### Tip 2: Monitor During Market Hours
Watch your positions live:
```bash
python3 scripts/c2_trading.py
# Press 2 (Monitor Live)
```

### Tip 3: Review Working Orders
See what's pending:
```bash
python3 scripts/c2_trading.py
# Press 4 (Manage Orders)
```

### Tip 4: Use Smart Defaults
The script has smart defaults:
- **Option** (not Stock) - most common
- **Call** (not Put) - most common
- **This Friday** expiry - most common
- **Buy** (not Sell) - most common
- **Limit** order (not Market) - safer
- **Day** order (not GTC) - most common

Just press Enter to accept defaults!

---

## 🆘 Troubleshooting

### "Command not found"
Make sure you're in the right directory:
```bash
cd /Users/swapnil5775
python3 scripts/c2_trading.py
```

### "No such file or directory"
Check if scripts exist:
```bash
ls scripts/
```

### "API Error"
Check your internet connection and API key in the scripts.

### Need to Cancel?
Press `Ctrl+C` at any time to safely exit.

---

## 📚 Learn More

- **Quick Start**: [QUICKSTART.md](../QUICKSTART.md)
- **Multi-Strategy**: [MULTI_STRATEGY.md](MULTI_STRATEGY.md)
- **Full Features**: [FEATURES.md](FEATURES.md)
- **Main README**: [README.md](../README.md)
- **API Docs**: https://api-docs.collective2.com/

---

## 🎉 You're Ready!

Start trading now:

```bash
python3 scripts/c2_trading.py
```

**Happy Trading! 🚀**
