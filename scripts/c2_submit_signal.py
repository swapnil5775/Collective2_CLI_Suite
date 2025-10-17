#!/usr/bin/env python3
"""
Collective2 Signal Submission Tool
Submit trading signals to your C2 strategy via CLI

Usage Examples:
  # Buy NBIS 150 call Oct 24, 2025 at limit $2.00, qty 5
  python3 c2_submit_signal.py --symbol NBIS --action buy --quantity 5 --option-type call --strike 150 --expiry 10/24/25 --limit 2.00

  # Buy stock at market
  python3 c2_submit_signal.py --symbol AAPL --action buy --quantity 10 --order-type market

  # Sell short with bracket (stop loss and profit target)
  python3 c2_submit_signal.py --symbol TSLA --action sell --quantity 5 --limit 250.00 --stop-loss 255.00 --profit-target 240.00

  # Cancel and replace existing signal
  python3 c2_submit_signal.py --cancel-replace 144260505 --symbol TSLA --action sell --quantity 5 --limit 248.00
"""

import warnings
warnings.filterwarnings("ignore")

import argparse
import json
import sys
import requests
from datetime import datetime
from typing import Optional, Dict

# Your Collective2 API Configuration
API_KEY = "A884F5FD-B61A-4EF1-9FEB-697F13E4E32C"
STRATEGY_ID = 153075915
BASE_URL = "https://api4-general.collective2.com"


def parse_expiry_date(expiry_str: str) -> str:
    """
    Parse expiry date from various formats to YYYYMMDD
    Examples: "10/24/25" -> "20251024", "Oct 24 2025" -> "20251024"
    """
    try:
        # Try MM/DD/YY format
        if '/' in expiry_str:
            parts = expiry_str.split('/')
            if len(parts) == 3:
                month, day, year = parts
                if len(year) == 2:
                    year = "20" + year
                return f"{year}{int(month):02d}{int(day):02d}"
        
        # Try parsing as date string
        for fmt in ["%m/%d/%Y", "%b %d %Y", "%B %d %Y", "%Y-%m-%d"]:
            try:
                dt = datetime.strptime(expiry_str, fmt)
                return dt.strftime("%Y%m%d")
            except:
                continue
    except:
        pass
    
    print(f"Error: Could not parse expiry date '{expiry_str}'", file=sys.stderr)
    print("Expected formats: MM/DD/YY (e.g., 10/24/25) or 'Oct 24 2025'", file=sys.stderr)
    sys.exit(1)


def create_option_symbol(symbol: str, strike: float, option_type: str, expiry: str) -> Dict:
    """
    Create ExchangeSymbol JSON for options
    """
    expiry_formatted = parse_expiry_date(expiry)
    
    put_or_call = 1 if option_type.lower() == 'call' else 0
    
    return {
        "Symbol": symbol.upper(),
        "Currency": "USD",
        "SecurityExchange": "DEFAULT",
        "SecurityType": "OPT",
        "MaturityMonthYear": expiry_formatted,
        "PutOrCall": put_or_call,
        "StrikePrice": float(strike)
    }


def create_stock_symbol(symbol: str) -> Dict:
    """
    Create ExchangeSymbol JSON for stocks
    """
    return {
        "Symbol": symbol.upper(),
        "Currency": "USD",
        "SecurityType": "CS"
    }


def submit_signal(
    symbol: str,
    action: str,
    quantity: int,
    order_type: str = "market",
    limit: Optional[float] = None,
    stop: Optional[float] = None,
    tif: str = "day",
    option_type: Optional[str] = None,
    strike: Optional[float] = None,
    expiry: Optional[str] = None,
    stop_loss: Optional[float] = None,
    profit_target: Optional[float] = None,
    cancel_replace_signal_id: Optional[int] = None,
    parent_signal_id: Optional[int] = None,
    strategy_id: Optional[int] = None,
    api_key: Optional[str] = None
) -> Dict:
    """
    Submit a trading signal to Collective2
    """
    
    # Use defaults if not provided
    strategy_id = strategy_id or STRATEGY_ID
    api_key = api_key or API_KEY
    
    # Map order type to C2 codes
    order_type_map = {
        "market": "1",
        "limit": "2",
        "stop": "3"
    }
    
    # Map side to C2 codes
    side_map = {
        "buy": "1",
        "sell": "2"
    }
    
    # Map TIF to C2 codes
    tif_map = {
        "day": "0",
        "gtc": "1",
        "good_till_cancel": "1"
    }
    
    # Build the order object
    order = {
        "StrategyId": strategy_id,
        "OrderType": order_type_map[order_type.lower()],
        "Side": side_map[action.lower()],
        "OrderQuantity": quantity,
        "TIF": tif_map[tif.lower()]
    }
    
    # Add limit price if specified
    if limit is not None:
        order["Limit"] = str(limit)
    
    # Add stop price if specified
    if stop is not None:
        order["Stop"] = str(stop)
    
    # Add stop loss and profit target for bracket orders
    if stop_loss is not None:
        order["StopLoss"] = stop_loss
    
    if profit_target is not None:
        order["ProfitTarget"] = profit_target
    
    # Add cancel-replace signal ID if specified
    if cancel_replace_signal_id is not None:
        order["CancelReplaceSignalId"] = cancel_replace_signal_id
    
    # Add parent signal ID for conditional orders
    if parent_signal_id is not None:
        order["ParentSignalId"] = parent_signal_id
    
    # Create the appropriate symbol format
    if option_type and strike is not None and expiry:
        # Option order
        order["ExchangeSymbol"] = create_option_symbol(symbol, strike, option_type, expiry)
    else:
        # Stock order
        order["ExchangeSymbol"] = create_stock_symbol(symbol)
    
    # Build the full request
    request_body = {"Order": order}
    
    # Print the request for debugging
    print("\n" + "="*80)
    print("📤 SUBMITTING SIGNAL TO COLLECTIVE2")
    print("="*80)
    print(json.dumps(request_body, indent=2))
    print("="*80 + "\n")
    
    # Submit to C2
    url = f"{BASE_URL}/Strategies/NewStrategyOrder"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=request_body, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        # Print the response
        print("="*80)
        print("✅ SIGNAL SUBMITTED SUCCESSFULLY")
        print("="*80)
        print(json.dumps(result, indent=2))
        print("="*80 + "\n")
        
        # Extract and display key information
        if "Results" in result and len(result["Results"]) > 0:
            signal_info = result["Results"][0]
            print("📋 SIGNAL DETAILS:")
            print(f"   Signal ID: {signal_info.get('SignalId', 'N/A')}")
            
            if "ProfitTargetSignalId" in signal_info:
                print(f"   Profit Target Signal ID: {signal_info['ProfitTargetSignalId']}")
            
            if "StopLossSignalId" in signal_info:
                print(f"   Stop Loss Signal ID: {signal_info['StopLossSignalId']}")
            
            if "ExitSignalsOCAGroupId" in signal_info:
                print(f"   OCA Group ID: {signal_info['ExitSignalsOCAGroupId']}")
            
            print()
        
        return result
        
    except requests.exceptions.HTTPError as e:
        print("="*80)
        print("❌ ERROR SUBMITTING SIGNAL")
        print("="*80)
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
        print("="*80 + "\n")
        sys.exit(1)
    except Exception as e:
        print("="*80)
        print("❌ ERROR")
        print("="*80)
        print(f"Error: {e}")
        print("="*80 + "\n")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Submit trading signals to Collective2 strategy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Buy NBIS 150 call Oct 24, 2025 at limit $2.00, qty 5
  %(prog)s --symbol NBIS --action buy --quantity 5 --option-type call --strike 150 --expiry 10/24/25 --limit 2.00

  # Buy AAPL stock at market, qty 10, GTC
  %(prog)s --symbol AAPL --action buy --quantity 10 --order-type market --tif gtc

  # Sell TSLA with bracket order (stop loss and profit target)
  %(prog)s --symbol TSLA --action sell --quantity 5 --limit 250.00 --stop-loss 255.00 --profit-target 240.00

  # Buy LLY put option
  %(prog)s --symbol LLY --action buy --quantity 3 --option-type put --strike 775 --expiry 10/17/25 --limit 2.50

  # Cancel and replace existing signal (change limit price)
  %(prog)s --cancel-replace 144260505 --symbol TSLA --action sell --quantity 5 --limit 248.00
        """
    )
    
    # Required arguments
    parser.add_argument("--symbol", required=True, help="Stock symbol (e.g., AAPL, TSLA, NBIS)")
    parser.add_argument("--action", required=True, choices=["buy", "sell"], help="Buy or Sell")
    parser.add_argument("--quantity", type=int, required=True, help="Order quantity")
    
    # Order type arguments
    parser.add_argument("--order-type", default="limit", choices=["market", "limit", "stop"], 
                       help="Order type (default: limit)")
    parser.add_argument("--limit", type=float, help="Limit price")
    parser.add_argument("--stop", type=float, help="Stop price")
    parser.add_argument("--tif", default="day", choices=["day", "gtc", "good_till_cancel"],
                       help="Time in force (default: day)")
    
    # Option-specific arguments
    parser.add_argument("--option-type", choices=["call", "put"], help="Option type (call or put)")
    parser.add_argument("--strike", type=float, help="Option strike price")
    parser.add_argument("--expiry", help="Option expiry date (e.g., 10/24/25 or 'Oct 24 2025')")
    
    # Bracket order arguments
    parser.add_argument("--stop-loss", type=float, help="Stop loss price for bracket order")
    parser.add_argument("--profit-target", type=float, help="Profit target price for bracket order")
    
    # Advanced arguments
    parser.add_argument("--cancel-replace", type=int, help="Cancel and replace signal ID")
    parser.add_argument("--parent-signal", type=int, help="Parent signal ID for conditional orders")
    
    # Override defaults
    parser.add_argument("--strategy-id", type=int, help=f"Strategy ID (default: {STRATEGY_ID})")
    parser.add_argument("--api-key", help="C2 API Key (default: from script)")
    
    args = parser.parse_args()
    
    # Validation
    if args.order_type == "limit" and args.limit is None:
        print("Error: --limit price is required for limit orders", file=sys.stderr)
        sys.exit(1)
    
    if args.order_type == "stop" and args.stop is None:
        print("Error: --stop price is required for stop orders", file=sys.stderr)
        sys.exit(1)
    
    # Check if option parameters are complete
    if args.option_type or args.strike is not None or args.expiry:
        if not (args.option_type and args.strike is not None and args.expiry):
            print("Error: For option orders, you must specify --option-type, --strike, and --expiry", file=sys.stderr)
            sys.exit(1)
    
    # Submit the signal
    submit_signal(
        symbol=args.symbol,
        action=args.action,
        quantity=args.quantity,
        order_type=args.order_type,
        limit=args.limit,
        stop=args.stop,
        tif=args.tif,
        option_type=args.option_type,
        strike=args.strike,
        expiry=args.expiry,
        stop_loss=args.stop_loss,
        profit_target=args.profit_target,
        cancel_replace_signal_id=args.cancel_replace,
        parent_signal_id=args.parent_signal,
        strategy_id=args.strategy_id,
        api_key=args.api_key
    )


if __name__ == "__main__":
    main()

