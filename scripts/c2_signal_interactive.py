#!/usr/bin/env python3
"""
Collective2 Interactive Signal Submission Tool
Submit trading signals to your C2 strategy with guided prompts

Usage:
  python3 c2_signal_interactive.py
"""

import warnings
warnings.filterwarnings("ignore")

import json
import sys
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict

# Your Collective2 API Configuration
API_KEY = "A884F5FD-B61A-4EF1-9FEB-697F13E4E32C"
STRATEGY_ID = 153075915
BASE_URL = "https://api4-general.collective2.com"


def get_next_friday(start_date: datetime = None) -> datetime:
    """Get the next Friday from the given date (or today)"""
    if start_date is None:
        start_date = datetime.now()
    
    days_ahead = 4 - start_date.weekday()  # Friday is weekday 4
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    
    return start_date + timedelta(days=days_ahead)


def get_week_after_next_friday() -> datetime:
    """Get Friday of the week after next"""
    next_friday = get_next_friday()
    return get_next_friday(next_friday + timedelta(days=1))


def print_header(text: str):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)


def print_section(text: str):
    """Print a section divider"""
    print("\n" + "-"*80)
    print(f"  {text}")
    print("-"*80)


def get_input(prompt: str, default: str = None) -> str:
    """Get user input with optional default"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("  ⚠️  This field is required. Please enter a value.")


def get_choice(prompt: str, choices: list, default: int = 0) -> str:
    """Get user choice from a list"""
    print(f"\n{prompt}")
    for i, choice in enumerate(choices, 1):
        marker = "→" if i == default else " "
        print(f"  {marker} {i}. {choice}")
    
    while True:
        choice_input = input(f"\nEnter choice [1-{len(choices)}] (default: {default}): ").strip()
        
        if not choice_input:
            return choices[default - 1]
        
        try:
            choice_num = int(choice_input)
            if 1 <= choice_num <= len(choices):
                return choices[choice_num - 1]
            else:
                print(f"  ⚠️  Please enter a number between 1 and {len(choices)}")
        except ValueError:
            print("  ⚠️  Please enter a valid number")


def confirm(prompt: str = "Proceed?") -> bool:
    """Ask for confirmation"""
    while True:
        response = input(f"\n{prompt} [y/n]: ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("  ⚠️  Please enter 'y' or 'n'")


def submit_signal_to_c2(order_data: Dict) -> Dict:
    """Submit the signal to Collective2 API"""
    url = f"{BASE_URL}/Strategies/NewStrategyOrder"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=order_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": str(e), "response": e.response.text}
    except Exception as e:
        return {"error": str(e)}


def main():
    print_header("🚀 COLLECTIVE2 SIGNAL SUBMISSION")
    print(f"Strategy ID: {STRATEGY_ID}")
    print(f"Strategy: ProfitSetup Swinger")
    
    # Step 1: Stock or Option
    print_section("Step 1: Instrument Type")
    instrument_type = get_choice(
        "What type of instrument?",
        ["Stock", "Option"],
        default=2  # Default to Option
    )
    
    # Step 2: Symbol
    print_section("Step 2: Symbol")
    symbol = get_input("Enter ticker symbol (e.g., AAPL, TSLA, NBIS)").upper()
    
    # Option-specific fields
    option_type = None
    strike = None
    expiry = None
    expiry_formatted = None
    
    if instrument_type == "Option":
        # Step 3: Call or Put
        print_section("Step 3: Option Type")
        option_type = get_choice(
            "Call or Put?",
            ["Call", "Put"],
            default=1  # Default to Call
        ).lower()
        
        # Step 4: Strike Price
        print_section("Step 4: Strike Price")
        while True:
            strike_input = get_input("Enter strike price (e.g., 150 or 150.00)")
            try:
                strike = float(strike_input.replace('$', ''))
                break
            except ValueError:
                print("  ⚠️  Please enter a valid number")
        
        # Step 5: Expiry Date
        print_section("Step 5: Expiry Date")
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        this_friday = get_next_friday()
        next_friday = get_week_after_next_friday()
        
        expiry_choices = [
            f"Today ({today.strftime('%m/%d/%y')})",
            f"Tomorrow ({tomorrow.strftime('%m/%d/%y')})",
            f"This week's Friday ({this_friday.strftime('%m/%d/%y')})",
            f"Next week's Friday ({next_friday.strftime('%m/%d/%y')})",
            "Enter manually"
        ]
        
        expiry_choice = get_choice(
            "Select expiry date:",
            expiry_choices,
            default=3  # Default to this week's Friday
        )
        
        if "Today" in expiry_choice:
            expiry_formatted = today.strftime("%Y%m%d")
            expiry = today.strftime("%m/%d/%y")
        elif "Tomorrow" in expiry_choice:
            expiry_formatted = tomorrow.strftime("%Y%m%d")
            expiry = tomorrow.strftime("%m/%d/%y")
        elif "This week" in expiry_choice:
            expiry_formatted = this_friday.strftime("%Y%m%d")
            expiry = this_friday.strftime("%m/%d/%y")
        elif "Next week" in expiry_choice:
            expiry_formatted = next_friday.strftime("%Y%m%d")
            expiry = next_friday.strftime("%m/%d/%y")
        else:
            # Manual entry
            while True:
                expiry_input = get_input("Enter expiry date (MM/DD/YY, e.g., 10/24/25)")
                try:
                    # Parse and validate
                    parts = expiry_input.split('/')
                    if len(parts) == 3:
                        month, day, year = parts
                        if len(year) == 2:
                            year = "20" + year
                        expiry_date = datetime(int(year), int(month), int(day))
                        expiry_formatted = expiry_date.strftime("%Y%m%d")
                        expiry = expiry_date.strftime("%m/%d/%y")
                        break
                    else:
                        print("  ⚠️  Invalid format. Use MM/DD/YY (e.g., 10/24/25)")
                except:
                    print("  ⚠️  Invalid date. Please try again.")
    
    # Step 6: Action (Buy or Sell)
    print_section(f"Step {'6' if instrument_type == 'Option' else '3'}: Action")
    action = get_choice(
        "Buy or Sell?",
        ["Buy", "Sell"],
        default=1  # Default to Buy
    ).lower()
    
    # Step 7: Order Type
    print_section(f"Step {'7' if instrument_type == 'Option' else '4'}: Order Type")
    order_type = get_choice(
        "Order type:",
        ["Market", "Limit", "Stop"],
        default=2  # Default to Limit
    ).lower()
    
    # Get limit/stop price if needed
    limit_price = None
    stop_price = None
    
    if order_type == "limit":
        while True:
            limit_input = get_input("Enter limit price (e.g., 2.00)")
            try:
                limit_price = float(limit_input.replace('$', ''))
                break
            except ValueError:
                print("  ⚠️  Please enter a valid number")
    
    elif order_type == "stop":
        while True:
            stop_input = get_input("Enter stop price (e.g., 2.00)")
            try:
                stop_price = float(stop_input.replace('$', ''))
                break
            except ValueError:
                print("  ⚠️  Please enter a valid number")
    
    # Step 8: Quantity
    print_section(f"Step {'8' if instrument_type == 'Option' else '5'}: Quantity")
    while True:
        qty_input = get_input(
            f"Enter quantity ({'contracts' if instrument_type == 'Option' else 'shares'})"
        )
        try:
            quantity = int(qty_input)
            if quantity > 0:
                break
            else:
                print("  ⚠️  Quantity must be greater than 0")
        except ValueError:
            print("  ⚠️  Please enter a valid number")
    
    # Step 9: Time in Force
    print_section(f"Step {'9' if instrument_type == 'Option' else '6'}: Time in Force")
    tif = get_choice(
        "Time in force:",
        ["Day", "GTC (Good Till Canceled)"],
        default=1  # Default to Day
    )
    tif_code = "0" if tif == "Day" else "1"
    
    # Build the order
    order = {
        "StrategyId": STRATEGY_ID,
        "OrderType": "1" if order_type == "market" else ("2" if order_type == "limit" else "3"),
        "Side": "1" if action == "buy" else "2",
        "OrderQuantity": quantity,
        "TIF": tif_code
    }
    
    if limit_price is not None:
        order["Limit"] = str(limit_price)
    
    if stop_price is not None:
        order["Stop"] = str(stop_price)
    
    # Add symbol
    if instrument_type == "Option":
        order["ExchangeSymbol"] = {
            "Symbol": symbol,
            "Currency": "USD",
            "SecurityExchange": "DEFAULT",
            "SecurityType": "OPT",
            "MaturityMonthYear": expiry_formatted,
            "PutOrCall": 1 if option_type == "call" else 0,
            "StrikePrice": strike
        }
    else:
        order["ExchangeSymbol"] = {
            "Symbol": symbol,
            "Currency": "USD",
            "SecurityType": "CS"
        }
    
    request_body = {"Order": order}
    
    # Display order summary
    print_header("📋 ORDER SUMMARY")
    print(f"  Instrument:    {instrument_type}")
    print(f"  Symbol:        {symbol}")
    
    if instrument_type == "Option":
        print(f"  Option Type:   {option_type.upper()}")
        print(f"  Strike:        ${strike}")
        print(f"  Expiry:        {expiry}")
    
    print(f"  Action:        {action.upper()}")
    print(f"  Order Type:    {order_type.upper()}")
    
    if limit_price:
        print(f"  Limit Price:   ${limit_price:.2f}")
    if stop_price:
        print(f"  Stop Price:    ${stop_price:.2f}")
    
    print(f"  Quantity:      {quantity} {'contract(s)' if instrument_type == 'Option' else 'share(s)'}")
    print(f"  Time in Force: {tif}")
    print("="*80)
    
    # Show JSON request
    print("\n📤 API Request:")
    print(json.dumps(request_body, indent=2))
    
    # Confirm submission
    if not confirm("\n✅ Submit this order to Collective2?"):
        print("\n❌ Order canceled by user.")
        sys.exit(0)
    
    # Submit to C2
    print("\n⏳ Submitting order to Collective2...")
    result = submit_signal_to_c2(request_body)
    
    # Display result
    if "error" in result:
        print_header("❌ ERROR SUBMITTING SIGNAL")
        print(f"  Error: {result['error']}")
        if "response" in result:
            print(f"  Response: {result['response']}")
        sys.exit(1)
    else:
        print_header("✅ SIGNAL SUBMITTED SUCCESSFULLY!")
        print(json.dumps(result, indent=2))
        
        if "Results" in result and len(result["Results"]) > 0:
            signal_info = result["Results"][0]
            print("\n📋 Signal Details:")
            print(f"  Signal ID: {signal_info.get('SignalId', 'N/A')}")
            
            if "ProfitTargetSignalId" in signal_info:
                print(f"  Profit Target Signal ID: {signal_info['ProfitTargetSignalId']}")
            
            if "StopLossSignalId" in signal_info:
                print(f"  Stop Loss Signal ID: {signal_info['StopLossSignalId']}")
            
            if "ExitSignalsOCAGroupId" in signal_info:
                print(f"  OCA Group ID: {signal_info['ExitSignalsOCAGroupId']}")
        
        print("\n✨ Your order has been submitted to your Collective2 strategy!")
        print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Order canceled by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)

