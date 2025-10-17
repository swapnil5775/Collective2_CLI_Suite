# 📁 Repository Structure

Clean and organized structure for easy navigation.

```
Collective2_CLI_Suite/
│
├── 📄 README.md              # Main project documentation
├── ⚡ QUICKSTART.md          # 5-minute quick start guide
├── 📋 STRUCTURE.md           # This file - repository structure
├── 📜 LICENSE                # MIT License
│
├── 📚 docs/                  # Documentation
│   ├── GETTING_STARTED.md   # Detailed tutorial
│   ├── MULTI_STRATEGY.md    # Multi-strategy management
│   └── FEATURES.md          # Complete feature reference
│
└── 🔧 scripts/              # All executable scripts
    ├── c2_trading.py        # ⭐ Main unified interface
    ├── c2_open_positions.py # View positions
    ├── c2_monitor.py        # Live monitoring
    ├── c2_signal_interactive.py # Interactive trading
    ├── c2_submit_signal.py  # CLI trading
    ├── c2_manage_orders.py  # Order management
    ├── config_example.py    # Configuration template
    └── load_config.py       # Config loader utility
```

---

## 📖 Where to Start

**New Users:**
1. Read [README.md](README.md) - Overview and setup
2. Follow [QUICKSTART.md](QUICKSTART.md) - Get running in 5 minutes
3. Check [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) - Detailed walkthrough

**Documentation:**
- **[QUICKSTART.md](QUICKSTART.md)** - Fastest way to get started
- **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)** - Step-by-step guide
- **[docs/MULTI_STRATEGY.md](docs/MULTI_STRATEGY.md)** - Managing multiple strategies
- **[docs/FEATURES.md](docs/FEATURES.md)** - All features and commands

**Scripts:**
All Python scripts are in `scripts/` directory:
- Run the unified interface: `python3 scripts/c2_trading.py`
- Or use individual scripts as needed

---

## 🎯 Key Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation, features, setup |
| `QUICKSTART.md` | Ultra-fast 5-minute setup |
| `LICENSE` | MIT License |
| `docs/` | All documentation files |
| `scripts/` | All executable Python scripts |
| `scripts/config_example.py` | Template for your configuration |

---

## 🔒 Private Files (Not in Git)

These files are gitignored and stay local:
- `scripts/config.py` - Your actual credentials
- `scripts/config_strategy*.py` - Multi-strategy configs
- `scripts/__pycache__/` - Python cache files

---

## 🚀 Quick Navigation

```bash
# View main documentation
cat README.md

# Quick start
cat QUICKSTART.md

# Detailed guides
ls docs/

# Run the suite
python3 scripts/c2_trading.py

# View all scripts
ls scripts/
```

---

**Clean. Organized. Easy to navigate.** 📁✨
