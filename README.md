# Collective2 CLI Trading Suite

A comprehensive command-line interface for managing your [Collective2](https://collective2.com) trading strategy. View positions, submit trades, manage orders, and monitor your portfolio in real-time—all from your terminal.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- 🚀 **Unified Interface** - One command for all functions
- 📊 **Real-time Pricing** - Live stock and option prices from Yahoo Finance
- 💰 **P/L Tracking** - Accurate profit/loss calculations
- 📈 **Live Monitoring** - Auto-refresh positions every 30 seconds
- 💼 **Trade Submission** - Interactive prompts for placing trades
- 🗂️ **Order Management** - View and cancel working orders
- 🔒 **Secure** - API keys never committed to git
- 📚 **Well Documented** - Complete guides and examples

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/swapnil5775/Collective2_CLI_Suite.git
cd Collective2_CLI_Suite
```

### 2. Install Dependencies

```bash
pip3 install requests yfinance
```

### 3. Configure Your API Credentials

**⚠️ IMPORTANT: Never commit your actual API key to version control!**

```bash
# Copy the example config file
cp scripts/config_example.py scripts/config.py

# Edit with your credentials
nano scripts/config.py  # or use your favorite editor
```

Add your Collective2 credentials:
```python
API_KEY = "YOUR_ACTUAL_API_KEY"
STRATEGY_ID = 123456789  # Your strategy ID
```

Get your API key from: https://collective2.com/api-docs/latest

### 4. Run the Suite

```bash
python3 scripts/c2_trading.py
```

**That's it!** You'll see an interactive menu with 6 options.

---

## 📋 Main Menu

```
╔════════════════════════════════════════════════╗
║  🚀 COLLECTIVE2 TRADING SUITE                  ║
╚════════════════════════════════════════════════╝

  1. 📊 View Open Positions
  2. 🔄 Monitor Positions (Live)
  3. 💼 Submit New Trade Signal
  4. 🗂️  Manage Working Orders
  5. ℹ️  Help & Documentation
  6. 🚪 Exit
```

---

## 📖 Documentation

- **[Getting Started Guide](scripts/GETTING_STARTED.md)** - Quick 2-minute tutorial
- **[Full Documentation](scripts/README.md)** - Complete feature reference
- **[API Documentation](https://api-docs.collective2.com/)** - Collective2 API reference

---

## 🛠️ Available Scripts

### Unified Interface (Recommended)
- **`c2_trading.py`** - All-in-one menu interface

### Individual Scripts
- **`c2_open_positions.py`** - View positions with real-time prices and P/L
- **`c2_monitor.py`** - Live monitoring with auto-refresh
- **`c2_signal_interactive.py`** - Submit trades with guided prompts
- **`c2_submit_signal.py`** - CLI trade submission for automation
- **`c2_manage_orders.py`** - View and cancel working orders

---

## 🔒 Security Best Practices

### API Key Protection

1. **Never commit `config.py`** to version control (it's gitignored)
2. **Use environment variables** as an alternative:
   ```bash
   export C2_API_KEY="your_api_key"
   export C2_STRATEGY_ID="your_strategy_id"
   ```
3. **Rotate your API key** periodically
4. **Use read-only keys** when possible

### What's Gitignored

The following files are automatically excluded from git:
- `scripts/config.py` - Your actual credentials
- `*.key` - Any key files
- `.env` - Environment files
- See [.gitignore](.gitignore) for complete list

### What's Safe to Commit

- `scripts/config_example.py` - Template with placeholders
- All script files (no hardcoded keys)
- Documentation files

---

## 📊 Example Usage

### View Your Positions
```bash
python3 scripts/c2_trading.py
# Select option 1
```

### Submit a Trade
```bash
python3 scripts/c2_trading.py
# Select option 3
# Follow the interactive prompts
```

### Monitor Live
```bash
python3 scripts/c2_trading.py
# Select option 2
# Auto-refreshes every 30 seconds
```

### CLI Trade Submission (Advanced)
```bash
# Buy AAPL call option
python3 scripts/c2_submit_signal.py \
  --symbol AAPL \
  --action buy \
  --quantity 5 \
  --option-type call \
  --strike 200 \
  --expiry 12/20/24 \
  --limit 5.00
```

---

## 🎯 Use Cases

- **Strategy Managers** - Manage your published strategies
- **Automated Trading** - Integrate with your trading bots
- **Portfolio Monitoring** - Real-time tracking of positions and P/L
- **Quick Trading** - Place trades faster than the GUI
- **Research** - Analyze positions and orders programmatically

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Note:** Never commit actual API keys or credentials!

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This software is for educational and informational purposes only. Trading stocks and options involves risk. Always test with paper trading first. The authors are not responsible for any trading losses incurred while using this software.

---

## 🙏 Acknowledgments

- [Collective2](https://collective2.com) for providing the API
- [Yahoo Finance](https://finance.yahoo.com) for real-time market data
- The Python community for excellent libraries

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/swapnil5775/Collective2_CLI_Suite/issues)
- **Documentation**: [Full Docs](scripts/README.md)
- **Collective2 API**: [API Docs](https://api-docs.collective2.com/)

---

## 🌟 Star This Repo!

If you find this project useful, please give it a star ⭐ on GitHub!

---

**Made with ❤️ for traders who love the command line**

