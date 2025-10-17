#!/usr/bin/env python3
"""
Collective2 Trading Suite - Unified Interface
All-in-one interactive tool for managing your C2 strategy

Usage:
  python3 c2_trading.py
"""

import warnings
warnings.filterwarnings("ignore")

import os
import sys
import time
import subprocess

# Your Collective2 API Configuration
STRATEGY_ID = 153075915
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print the main header"""
    print("\n" + "="*100)
    print("  🚀 COLLECTIVE2 TRADING SUITE")
    print("="*100)
    print(f"  Strategy: ProfitSetup Swinger (ID: {STRATEGY_ID})")
    print("="*100)


def print_menu():
    """Print the main menu"""
    print("\n" + "-"*100)
    print("  📋 MAIN MENU")
    print("-"*100)
    print()
    print("  1. 📊 View Open Positions")
    print("       ├─ See all current positions")
    print("       ├─ Real-time prices and P/L")
    print("       └─ Portfolio summary")
    print()
    print("  2. 🔄 Monitor Positions (Live)")
    print("       ├─ Auto-refresh every 30 seconds")
    print("       └─ Press Ctrl+C to stop")
    print()
    print("  3. 💼 Submit New Trade Signal")
    print("       ├─ Interactive guided prompts")
    print("       ├─ Stocks and Options supported")
    print("       └─ Confirmation before sending")
    print()
    print("  4. 🗂️  Manage Working Orders")
    print("       ├─ View all pending orders")
    print("       ├─ Cancel orders interactively")
    print("       └─ Refresh capability")
    print()
    print("  5. ℹ️  Help & Documentation")
    print("       └─ View README and command examples")
    print()
    print("  6. 🚪 Exit")
    print()
    print("-"*100)


def view_positions():
    """Run the view positions script"""
    clear_screen()
    print_header()
    print("\n📊 VIEWING OPEN POSITIONS...\n")
    print("="*100)
    
    script_path = os.path.join(SCRIPT_DIR, "c2_open_positions.py")
    cmd = ["python3", script_path, "--mode", "strategy", "--strategy-id", str(STRATEGY_ID)]
    
    try:
        subprocess.run(cmd)
        print("\n" + "="*100)
        input("\n✅ Press Enter to return to main menu...")
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
        input("\nPress Enter to return to main menu...")


def monitor_positions():
    """Run the monitor script"""
    clear_screen()
    print_header()
    print("\n🔄 STARTING LIVE MONITOR...")
    print("="*100)
    print("\n⚠️  Auto-refresh every 30 seconds")
    print("⚠️  Press Ctrl+C to stop and return to main menu\n")
    print("="*100)
    
    input("\nPress Enter to start monitoring...")
    
    script_path = os.path.join(SCRIPT_DIR, "c2_monitor.py")
    cmd = ["python3", script_path]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n⏸️  Monitoring stopped")
    
    input("\nPress Enter to return to main menu...")


def submit_trade():
    """Run the interactive signal submission script"""
    clear_screen()
    print_header()
    print("\n💼 SUBMIT NEW TRADE SIGNAL\n")
    print("="*100)
    
    script_path = os.path.join(SCRIPT_DIR, "c2_signal_interactive.py")
    cmd = ["python3", script_path]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n❌ Trade submission canceled")
    
    input("\nPress Enter to return to main menu...")


def manage_orders():
    """Run the order management script"""
    clear_screen()
    print_header()
    print("\n🗂️  MANAGE WORKING ORDERS\n")
    print("="*100)
    
    script_path = os.path.join(SCRIPT_DIR, "c2_manage_orders.py")
    cmd = ["python3", script_path]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n⏸️  Order management interrupted")
    
    input("\nPress Enter to return to main menu...")


def show_help():
    """Show help and documentation"""
    clear_screen()
    print_header()
    print("\n" + "="*100)
    print("  ℹ️  HELP & DOCUMENTATION")
    print("="*100)
    
    print("""
📖 QUICK REFERENCE:

1. VIEW OPEN POSITIONS (Option 1)
   • See all your current positions with real-time prices
   • Calculate per-position and total P/L
   • View portfolio summary (cash, buying power, margin)
   • Real-time stock prices from Yahoo Finance
   • Real-time option prices when available

2. MONITOR POSITIONS (Option 2)
   • Live monitoring with auto-refresh every 30 seconds
   • Continuously track your positions and P/L
   • Press Ctrl+C to stop monitoring

3. SUBMIT NEW TRADE (Option 3)
   Interactive prompts guide you through:
   • Stock or Option selection
   • Symbol entry (e.g., AAPL, NBIS, TSLA)
   • For Options: Call/Put, Strike, Expiry
   • Buy or Sell action
   • Market, Limit, or Stop order
   • Quantity entry
   • Full preview and confirmation

4. MANAGE WORKING ORDERS (Option 4)
   • View all pending/working orders
   • See details: Symbol, Action, Quantity, Price, Status
   • Cancel orders with confirmation
   • Refresh to update the list

═══════════════════════════════════════════════════════════════════════════

📝 COMMAND-LINE ALTERNATIVES:

If you prefer command-line over interactive menus:

# View positions (single command)
python3 scripts/c2_open_positions.py --mode strategy --strategy-id 153075915

# Submit trade via CLI
python3 scripts/c2_submit_signal.py --symbol NBIS --action buy --quantity 5 \\
  --option-type call --strike 150 --expiry 10/24/25 --limit 2.00

# Get CLI help
python3 scripts/c2_submit_signal.py --help

═══════════════════════════════════════════════════════════════════════════

📚 FULL DOCUMENTATION:

For complete documentation, examples, and troubleshooting:
    cat scripts/README.md

Or open in your browser:
    open scripts/README.md

═══════════════════════════════════════════════════════════════════════════

🔗 USEFUL LINKS:

• Collective2 API Docs: https://api-docs.collective2.com/
• Your Strategy Page: https://collective2.com/strategy/153075915
• Signal Submission Guide: https://api-docs.collective2.com/guides/how-to-submit-signals

═══════════════════════════════════════════════════════════════════════════
""")
    
    input("\nPress Enter to return to main menu...")


def main():
    """Main interactive loop"""
    
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("Enter your choice [1-6]: ").strip()
        
        if choice == '1':
            view_positions()
        
        elif choice == '2':
            monitor_positions()
        
        elif choice == '3':
            submit_trade()
        
        elif choice == '4':
            manage_orders()
        
        elif choice == '5':
            show_help()
        
        elif choice == '6':
            clear_screen()
            print("\n" + "="*100)
            print("  👋 Thank you for using Collective2 Trading Suite!")
            print("  🚀 Happy Trading!")
            print("="*100 + "\n")
            sys.exit(0)
        
        else:
            print("\n⚠️  Invalid choice. Please enter a number between 1 and 6.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        # Check if we're in the right directory
        if not os.path.exists(os.path.join(SCRIPT_DIR, "c2_open_positions.py")):
            print("❌ Error: Cannot find required scripts.", file=sys.stderr)
            print("Make sure you're running this from the scripts directory.", file=sys.stderr)
            sys.exit(1)
        
        main()
    
    except KeyboardInterrupt:
        clear_screen()
        print("\n" + "="*100)
        print("  👋 Goodbye! (Ctrl+C)")
        print("="*100 + "\n")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

