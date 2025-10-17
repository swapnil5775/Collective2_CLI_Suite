#!/usr/bin/env python3
"""
Collective2 Order Management Tool
View and cancel open/working orders from your C2 strategy

Usage:
  python3 c2_manage_orders.py
"""

import warnings
warnings.filterwarnings("ignore")

import json
import sys
import requests
from datetime import datetime
from typing import Optional, List, Dict

# Your Collective2 API Configuration
API_KEY = "A884F5FD-B61A-4EF1-9FEB-697F13E4E32C"
STRATEGY_ID = 153075915
BASE_URL = "https://api4-general.collective2.com"


def print_header(text: str):
    """Print a formatted header"""
    print("\n" + "="*100)
    print(f"  {text}")
    print("="*100)


def print_section(text: str):
    """Print a section divider"""
    print("\n" + "-"*100)
    print(f"  {text}")
    print("-"*100)


def get_working_orders(strategy_id: int = None, api_key: str = None) -> List[Dict]:
    """
    Fetch working (open/pending) orders from C2 strategy
    """
    strategy_id = strategy_id or STRATEGY_ID
    api_key = api_key or API_KEY
    
    # Try the GetStrategyWorkingOrders endpoint
    url = f"{BASE_URL}/Strategies/GetStrategyWorkingOrders"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    params = {
        "StrategyId": strategy_id
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Check for results in both 'Results' and 'results' keys
        orders = data.get('Results', data.get('results', []))
        
        return orders if orders else []
        
    except requests.exceptions.HTTPError as e:
        # If that endpoint doesn't work, try GetStrategyHistoricalOrders without status filter
        try:
            url = f"{BASE_URL}/Strategies/GetStrategyHistoricalOrders"
            params = {
                "StrategyId": strategy_id,
                "Limit": 100,
                "AscendingOrder": False  # Get newest first
            }
            
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            orders = data.get('Results', data.get('results', []))
            
            # Filter for working orders (not filled, not canceled, not expired)
            working_orders = []
            for order in orders:
                status = order.get('orderStatus', order.get('OrderStatus', '')).lower()
                # Include orders that are working/pending (not filled, canceled, or expired)
                if status not in ['filled', '2', 'canceled', '4', 'expired', 'c']:
                    working_orders.append(order)
            
            return working_orders
            
        except Exception as inner_e:
            print(f"\n❌ Error fetching orders: {inner_e}", file=sys.stderr)
            if hasattr(inner_e, 'response'):
                print(f"Response: {inner_e.response.text}", file=sys.stderr)
            return []
    
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return []


def format_order_display(order: Dict, index: int) -> str:
    """Format an order for display"""
    # Extract order details with fallbacks for different key formats
    signal_id = order.get('signalId', order.get('SignalId', order.get('id', 'N/A')))
    order_id = order.get('orderId', order.get('OrderId', ''))
    
    # Symbol information
    symbol_info = order.get('c2Symbol', order.get('C2Symbol', {}))
    if isinstance(symbol_info, dict):
        symbol = symbol_info.get('fullSymbol', symbol_info.get('FullSymbol', 'N/A'))
    else:
        symbol = order.get('symbol', order.get('Symbol', 'N/A'))
    
    # Order type and side
    order_type_map = {'1': 'Market', '2': 'Limit', '3': 'Stop'}
    order_type = order.get('orderType', order.get('OrderType', ''))
    order_type_str = order_type_map.get(order_type, order_type)
    
    side_map = {'1': 'BUY', '2': 'SELL'}
    side = order.get('side', order.get('Side', ''))
    side_str = side_map.get(side, side)
    
    # Quantity and prices
    quantity = order.get('orderQuantity', order.get('OrderQuantity', 0))
    limit_price = order.get('limit', order.get('Limit', ''))
    stop_price = order.get('stop', order.get('Stop', ''))
    
    # Status
    status = order.get('orderStatus', order.get('OrderStatus', 'Working'))
    
    # Posted date
    posted_date = order.get('postedDate', order.get('PostedDate', ''))
    if posted_date:
        try:
            dt = datetime.fromisoformat(posted_date.replace('Z', '+00:00'))
            date_str = dt.strftime('%m/%d/%y %H:%M')
        except:
            date_str = posted_date
    else:
        date_str = 'N/A'
    
    # Build display string
    display = f"  {index:2d}. Signal ID: {signal_id:>10}  |  {symbol:>15}  |  {side_str:>4} {quantity:>5} @ "
    
    if limit_price:
        display += f"${float(limit_price):>7.2f} Limit"
    elif stop_price:
        display += f"${float(stop_price):>7.2f} Stop"
    else:
        display += "Market      "
    
    display += f"  |  Status: {status:>10}  |  {date_str}"
    
    return display


def cancel_signal(signal_id: int, strategy_id: int = None, api_key: str = None) -> Dict:
    """
    Cancel a specific signal/order
    """
    strategy_id = strategy_id or STRATEGY_ID
    api_key = api_key or API_KEY
    
    url = f"{BASE_URL}/Strategies/CancelSignal"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Build request body
    request_body = {
        "StrategyId": strategy_id,
        "SignalId": signal_id
    }
    
    try:
        response = requests.post(url, json=request_body, headers=headers)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        return {"error": str(e), "response": e.response.text}
    except Exception as e:
        return {"error": str(e)}


def main():
    """Main interactive loop"""
    
    while True:
        print_header("📋 COLLECTIVE2 ORDER MANAGEMENT")
        print(f"  Strategy ID: {STRATEGY_ID}")
        print(f"  Strategy: ProfitSetup Swinger")
        print("="*100)
        
        # Fetch working orders
        print("\n⏳ Fetching working orders...")
        orders = get_working_orders()
        
        if not orders:
            print("\n✅ No working orders found. All orders are filled or there are no open positions.")
            
            retry = input("\n🔄 Refresh and check again? [y/n]: ").strip().lower()
            if retry == 'y':
                continue
            else:
                print("\n👋 Goodbye!")
                break
        
        # Display orders
        print_section(f"WORKING ORDERS ({len(orders)} total)")
        print(f"\n  {'#':>3}  {'Signal ID':>10}  |  {'Symbol':>15}  |  {'Action':>4}  {'Qty':>5}    {'Price/Type':<15}  |  {'Status':>10}  |  Date")
        print("  " + "-"*96)
        
        for idx, order in enumerate(orders, start=1):
            print(format_order_display(order, idx))
        
        # Menu options
        print_section("OPTIONS")
        print("  • Enter order number (1-{}) to CANCEL that order".format(len(orders)))
        print("  • Enter 'r' to REFRESH the list")
        print("  • Enter 'q' to QUIT")
        print("-"*100)
        
        # Get user choice
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            print("\n👋 Goodbye!")
            break
        
        elif choice == 'r':
            continue
        
        else:
            # Try to parse as order number
            try:
                order_num = int(choice)
                
                if 1 <= order_num <= len(orders):
                    selected_order = orders[order_num - 1]
                    signal_id = selected_order.get('signalId', selected_order.get('SignalId', selected_order.get('id')))
                    
                    # Show order details
                    print("\n" + "="*100)
                    print("  📋 ORDER DETAILS TO CANCEL:")
                    print("="*100)
                    print(format_order_display(selected_order, order_num))
                    print("="*100)
                    
                    # Confirm cancellation
                    confirm = input("\n⚠️  Are you sure you want to CANCEL this order? [y/n]: ").strip().lower()
                    
                    if confirm == 'y':
                        print(f"\n⏳ Canceling signal {signal_id}...")
                        
                        result = cancel_signal(signal_id)
                        
                        if "error" in result:
                            print("\n" + "="*100)
                            print("  ❌ ERROR CANCELING ORDER")
                            print("="*100)
                            print(f"  Error: {result['error']}")
                            if "response" in result:
                                print(f"  Response: {result['response']}")
                            print("="*100)
                        else:
                            print("\n" + "="*100)
                            print("  ✅ ORDER CANCELED SUCCESSFULLY!")
                            print("="*100)
                            print(json.dumps(result, indent=2))
                            print("="*100)
                        
                        input("\nPress Enter to continue...")
                    else:
                        print("\n❌ Cancellation aborted.")
                        input("\nPress Enter to continue...")
                else:
                    print(f"\n⚠️  Invalid order number. Please enter a number between 1 and {len(orders)}")
                    input("\nPress Enter to continue...")
            
            except ValueError:
                print("\n⚠️  Invalid input. Please enter a number, 'r' to refresh, or 'q' to quit.")
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

