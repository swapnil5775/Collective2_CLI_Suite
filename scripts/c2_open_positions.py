#!/usr/bin/env python3
"""
Collective2 Open Positions Viewer
Works for both Strategy Managers and Autotraders

Usage:
  # For strategy managers (view your own strategy positions):
  python3 c2_open_positions.py --mode strategy --strategy-id YOUR_STRATEGY_ID

  # For autotraders (view positions in your brokerage account):
  python3 c2_open_positions.py --mode autotrade --account YOUR_ACCOUNT

  # Discovery mode (find your strategies and accounts):
  python3 c2_open_positions.py --discover
"""

import warnings
# Suppress all warnings before any imports (urllib3, yfinance, etc.)
warnings.filterwarnings("ignore")

import argparse
import json
import os
import sys
from typing import Optional, List
import requests


# Your Collective2 API Key
API_KEY = "A884F5FD-B61A-4EF1-9FEB-697F13E4E32C"
PERSON_ID = 153075914
BASE_URL = "https://api4-general.collective2.com"


def get_headers():
    """Return headers for API requests."""
    return {"Authorization": f"Bearer {API_KEY}"}


def get_profile():
    """Get user profile."""
    try:
        response = requests.get(f"{BASE_URL}/General/GetProfile", headers=get_headers())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching profile: {e}", file=sys.stderr)
        return {}


def get_managed_strategies():
    """Get strategies you manage/own."""
    try:
        response = requests.get(
            f"{BASE_URL}/General/GetManagerPlanSubscriptions",
            headers=get_headers(),
            params={"PersonId": PERSON_ID}
        )
        response.raise_for_status()
        data = response.json()
        return data.get('Results', [])
    except Exception as e:
        print(f"Error fetching managed strategies: {e}", file=sys.stderr)
        return []


def get_autotraded_strategies():
    """Get your autotrade accounts."""
    try:
        response = requests.get(
            f"{BASE_URL}/Autotrade/GetAutotradedStrategies",
            headers=get_headers(),
            params={"PersonId": PERSON_ID}
        )
        response.raise_for_status()
        data = response.json()
        return data.get('Results', [])
    except Exception as e:
        print(f"Error fetching autotrade strategies: {e}", file=sys.stderr)
        return []


def get_strategy_details(strategy_id: int):
    """
    Get detailed strategy information including equity, cash, buying power.
    
    Args:
        strategy_id: Strategy ID
    """
    try:
        response = requests.get(
            f"{BASE_URL}/Strategies/GetStrategyDetails",
            headers=get_headers(),
            params={"StrategyId": strategy_id}
        )
        response.raise_for_status()
        data = response.json()
        results = data.get('Results', [])
        return results[0] if results else {}
    except Exception as e:
        print(f"Warning: Could not fetch strategy details: {e}", file=sys.stderr)
        return {}


def get_strategy_positions(strategy_ids: List[int], security_type: Optional[str] = None):
    """
    Get open positions for strategies you manage.
    
    Args:
        strategy_ids: List of strategy IDs
        security_type: Optional filter (CS=Stocks, FUT=Futures, OPT=Options, FOR=Forex)
    """
    url = f"{BASE_URL}/Strategies/GetStrategyOpenPositions"
    query_parts = [f"StrategyIds={sid}" for sid in strategy_ids]
    if security_type:
        query_parts.append(f"SecurityType={security_type}")
    full_url = f"{url}?{'&'.join(query_parts)}"
    
    try:
        response = requests.get(full_url, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print("\n❌ Error 403: You are not authorized to view these positions.", file=sys.stderr)
            print("Make sure you are the owner of the strategy.", file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching strategy positions: {e}", file=sys.stderr)
        sys.exit(1)


def get_autotrade_positions(account: str, strategy_id: Optional[int] = None):
    """
    Get open positions from autotrade account.
    
    Args:
        account: Brokerage account identifier
        strategy_id: Optional strategy ID filter
    """
    params = {"Account": account}
    if strategy_id:
        params["StrategyId"] = strategy_id
    
    try:
        response = requests.get(
            f"{BASE_URL}/Autotrade/GetAutoTradeOpenPositions",
            headers=get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print("\n❌ Error 403: Access forbidden to this account.", file=sys.stderr)
            print("Make sure you're using the correct account identifier.", file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching autotrade positions: {e}", file=sys.stderr)
        sys.exit(1)


def get_current_price(symbol: str, symbol_type: str = 'stock', underlying: str = None, strike: float = None, put_or_call: str = None, expiry: str = None) -> Optional[float]:
    """
    Get current price from Yahoo Finance for both stocks and options.
    """
    try:
        import yfinance as yf
        
        if symbol_type == 'stock':
            ticker = yf.Ticker(symbol)
            # Get the most recent data
            data = ticker.history(period='1d', interval='1m')
            if not data.empty:
                return float(data['Close'].iloc[-1])
            else:
                # Fallback to daily data
                data = ticker.history(period='5d')
                if not data.empty:
                    return float(data['Close'].iloc[-1])
        
        elif symbol_type == 'option' and underlying:
            # For options, try to get actual option price first, then fall back to underlying
            try:
                # Try to get actual option price using the description
                # This will be handled in the main function where we have access to description
                return None  # Will be handled in main function
            except Exception as e:
                print(f"Warning: Could not fetch option price for {symbol}: {e}", file=sys.stderr)
                return None
    
    except Exception as e:
        print(f"Warning: Could not fetch price for {symbol}: {e}", file=sys.stderr)
    
    return None


def convert_c2_expiry_to_yahoo(expiry: str) -> Optional[str]:
    """
    Convert C2 expiry format (e.g., "Oct25") to Yahoo Finance format (e.g., "2025-10-17").
    """
    try:
        from datetime import datetime, timedelta
        import calendar
        
        # Parse C2 format like "Oct25", "Nov25", etc.
        month_abbr = expiry[:3]
        year = int("20" + expiry[3:])
        
        # Convert month abbreviation to number
        month_num = list(calendar.month_abbr).index(month_abbr)
        
        # Find the third Friday of the month (standard options expiry)
        first_day = datetime(year, month_num, 1)
        first_friday = first_day + timedelta(days=(4 - first_day.weekday()) % 7)
        third_friday = first_friday + timedelta(days=14)
        
        return third_friday.strftime("%Y-%m-%d")
        
    except Exception as e:
        print(f"Warning: Could not convert expiry {expiry}: {e}", file=sys.stderr)
        return None


def parse_option_description(description: str) -> dict:
    """
    Parse option description to extract underlying, strike, type, and expiry.
    Examples:
    - "NBIS 150 call exp Oct25" -> {underlying: "NBIS", strike: 150, type: "call", expiry: "Oct25"}
    - "ARM 190 call exp 10/24/25" -> {underlying: "ARM", strike: 190, type: "call", expiry: "Oct25"}
    """
    try:
        import re
        
        # Pattern to match: "SYMBOL STRIKE call/put exp EXPIRY"
        pattern = r'(\w+)\s+(\d+(?:\.\d+)?)\s+(call|put)\s+exp\s+(\w+)'
        match = re.search(pattern, description, re.IGNORECASE)
        
        if match:
            underlying = match.group(1)
            strike = float(match.group(2))
            option_type = match.group(3).lower()
            expiry = match.group(4)
            
            return {
                'underlying': underlying,
                'strike': strike,
                'type': option_type,
                'expiry': expiry
            }
    except:
        pass
    
    return None


def convert_expiry_to_yahoo_format(expiry: str) -> str:
    """
    Convert various expiry formats to YYMMDD format for Yahoo Finance.
    Examples: "Oct25" -> "251017", "10/24/25" -> "251024"
    Note: This just provides an initial guess - get_yahoo_option_ticker will try multiple dates
    """
    try:
        from datetime import datetime
        import calendar
        
        # Handle "Oct25" format - provide initial guess for 3rd Friday
        if len(expiry) == 5 and expiry[:3].isalpha():
            month_abbr = expiry[:3]
            year = int("20" + expiry[3:])
            month_num = list(calendar.month_abbr).index(month_abbr)
            
            # Start with 3rd Friday (typically day 15-21)
            # The actual date will be tested in get_yahoo_option_ticker
            return f"{year-2000:02d}{month_num:02d}17"
        
        # Handle "10/24/25" format
        elif '/' in expiry:
            parts = expiry.split('/')
            if len(parts) == 3:
                month = int(parts[0])
                day = int(parts[1])
                year = int("20" + parts[2])
                return f"{year-2000:02d}{month:02d}{day:02d}"
    
    except:
        pass
    
    return None


def get_yahoo_option_ticker(underlying: str, strike: float, option_type: str, expiry: str) -> str:
    """
    Create Yahoo Finance option ticker symbol and test if it exists.
    Format: <Underlying><YY><MM><DD><C or P><StrikePrice (8 digits)>
    """
    try:
        # Convert expiry to YYMMDD format
        expiry_yy_mm_dd = convert_expiry_to_yahoo_format(expiry)
        if not expiry_yy_mm_dd:
            return None
        
        # Format option type
        option_letter = 'C' if option_type == 'call' else 'P'
        
        # Format strike price (multiply by 1000, pad to 8 digits)
        strike_formatted = f"{int(strike * 1000):08d}"
        
        # Create ticker
        ticker = f"{underlying}{expiry_yy_mm_dd}{option_letter}{strike_formatted}"
        
        # Test if this ticker exists by trying to get data
        try:
            import yfinance as yf
            import warnings
            from contextlib import redirect_stderr
            import io
            
            with warnings.catch_warnings(), redirect_stderr(io.StringIO()):
                warnings.simplefilter("ignore")
                test_ticker = yf.Ticker(ticker)
                # Try different periods - some options only show up with longer periods
                for period in ['1d', '5d']:
                    data = test_ticker.history(period=period)
                    if not data.empty:
                        return ticker
        except:
            pass
        
        # If the first attempt failed, try alternative dates
        if len(expiry) == 5 and expiry[:3].isalpha():
            import calendar
            month_abbr = expiry[:3]
            year = int("20" + expiry[3:])
            month_num = list(calendar.month_abbr).index(month_abbr)
            
            # Try different days - options can expire on various Fridays (weekly options)
            # Prioritize 3rd Friday (typically 15-21), but also check other common expiry dates
            alternative_days = [17, 18, 19, 20, 21, 15, 16, 22, 14, 23, 24, 25, 8, 9, 10, 11, 12, 13]
            for day in alternative_days:
                try:
                    alt_date = f"{year-2000:02d}{month_num:02d}{day:02d}"
                    alt_ticker = f"{underlying}{alt_date}{option_letter}{strike_formatted}"
                    
                    with warnings.catch_warnings(), redirect_stderr(io.StringIO()):
                        warnings.simplefilter("ignore")
                        test_ticker = yf.Ticker(alt_ticker)
                        # Try different periods
                        for period in ['1d', '5d']:
                            data = test_ticker.history(period=period)
                            if not data.empty:
                                return alt_ticker
                except:
                    continue
        
        return None
        
    except:
        return None


def get_option_price_from_yahoo(option_ticker: str) -> Optional[float]:
    """
    Get option price from Yahoo Finance using the proper ticker format.
    """
    try:
        import yfinance as yf
        import warnings
        from contextlib import redirect_stderr
        import io
        
        # Suppress yfinance warnings and errors
        with warnings.catch_warnings(), redirect_stderr(io.StringIO()):
            warnings.simplefilter("ignore")
            ticker = yf.Ticker(option_ticker)
            data = ticker.history(period='1d', interval='1m')
            if not data.empty:
                return float(data['Close'].iloc[-1])
            else:
                # Fallback to daily data
                data = ticker.history(period='5d')
                if not data.empty:
                    return float(data['Close'].iloc[-1])
    except:
        pass
    
    return None


def get_option_intrinsic_value(underlying_price: float, strike: float, put_or_call: str, quantity: int) -> float:
    """
    Calculate intrinsic value for options.
    """
    try:
        if put_or_call == 'call':
            intrinsic = max(0, underlying_price - strike)
        else:  # put
            intrinsic = max(0, strike - underlying_price)
        
        return intrinsic * quantity * 100  # Options are 100 shares per contract
    except:
        return 0.0


def format_date(date_str: str) -> str:
    """Format date string to match GUI format (e.g., '10/6/25 9:30')."""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%m/%d/%y %H:%M')
    except:
        return date_str


def get_option_description(c2_symbol: dict) -> str:
    """Generate option description like 'ARM 190 call exp 10/24/25'."""
    if not isinstance(c2_symbol, dict):
        return str(c2_symbol)
    
    underlying = c2_symbol.get('Underlying', '')
    strike = c2_symbol.get('StrikePrice', '')
    put_or_call = c2_symbol.get('PutOrCall', '')
    expiry = c2_symbol.get('Expiry', '')
    
    if underlying and strike and put_or_call and expiry:
        option_type = 'call' if put_or_call == 'call' else 'put'
        return f"{underlying} {strike} {option_type} exp {expiry}"
    
    return c2_symbol.get('FullSymbol', '')


def get_stock_description(symbol: str) -> str:
    """Get stock company name for description."""
    stock_names = {
        'AAPL': 'APPLE',
        'TSLA': 'TESLA',
        'HUT': 'HUT 8 MINING CORP. COMMON SHARES',
        'LLY': 'ELI LILLY',
        'CRWV': 'CROWDSTRIKE',
        'ARM': 'ARM HOLDINGS',
        'COIN': 'COINBASE',
        'GS': 'GOLDMAN SACHS',
        'LRCX': 'LAM RESEARCH',
        'NBIS': 'NVIDIA'
    }
    return stock_names.get(symbol, symbol)


def format_strategy_positions(data: dict, strategy_id: Optional[int] = None):
    """Format and display strategy positions exactly like the Collective2 GUI."""
    positions = data.get('Results', data.get('results', []))
    
    if not positions:
        print("\n✓ No open positions found.")
        return
    
    # Get strategy details for portfolio summary
    strategy_details = {}
    if strategy_id:
        strategy_details = get_strategy_details(strategy_id)
    
    print("\n" + "="*120)
    print("Open Positions")
    print("="*120)
    
    # Sort positions by date (newest first)
    positions.sort(key=lambda x: x.get('OpenedDate', ''), reverse=True)
    
    # Table header matching GUI
    print(f"{'Date':<15} {'Symbol':<15} {'Description':<35} {'Side':<8} {'Quant':<8} {'Basis':<10} {'Price':<10} {'Unrealized P/L':<15} {'Realized P/L':<15}")
    print("-"*120)
    
    total_unrealized_pnl = 0.0
    total_realized_pnl = 0.0
    total_entry_value = 0.0
    total_current_value = 0.0
    
    for pos in positions:
        c2_symbol = pos.get('C2Symbol', pos.get('c2Symbol', {}))
        
        # Extract symbol info
        if isinstance(c2_symbol, dict):
            full_symbol = c2_symbol.get('FullSymbol', c2_symbol.get('symbol', 'N/A'))
            symbol_type = c2_symbol.get('SymbolType', 'stock')
            underlying = c2_symbol.get('Underlying', full_symbol)
        else:
            full_symbol = str(c2_symbol)
            symbol_type = 'stock'
            underlying = full_symbol
        
        # Format date
        opened_date = pos.get('OpenedDate', pos.get('openedDate', ''))
        formatted_date = format_date(opened_date)
        
        # Get description
        if symbol_type == 'option':
            description = get_option_description(c2_symbol)
        else:
            description = get_stock_description(underlying)
        
        # Position details
        quantity = pos.get('Quantity', pos.get('quantity', 0))
        avg_px = pos.get('AvgPx', pos.get('avgPx', 0))
        side = "Long" if quantity > 0 else "Short"
        
        # Calculate values
        multiplier = 100 if symbol_type == 'option' else 1
        entry_value = abs(quantity) * avg_px * multiplier
        total_entry_value += entry_value
        
        # Get current price for both stocks and options
        current_price = None
        underlying_price = None
        
        if symbol_type == 'stock':
            current_price = get_current_price(underlying, symbol_type)
        elif symbol_type == 'option':
            # For options, try to get actual option price first
            option_details = parse_option_description(description)
            option_price = None
            
            if option_details:
                # Create Yahoo Finance option ticker
                option_ticker = get_yahoo_option_ticker(
                    option_details['underlying'],
                    option_details['strike'],
                    option_details['type'],
                    option_details['expiry']
                )
                
                if option_ticker:
                    # Try to get actual option price
                    option_price = get_option_price_from_yahoo(option_ticker)
            
            if option_price:
                # We got actual option price
                current_price = option_price
                underlying_price = None
            else:
                # Fall back to underlying price for intrinsic calculation
                current_price = get_current_price(underlying, 'stock')
                underlying_price = current_price
        
        # Calculate P/L
        unrealized_pnl = 0.0
        realized_pnl = 0.0  # This would need to come from C2 API - for now showing 0
        
        if current_price:
            if symbol_type == 'stock':
                # For stocks, calculate normal P/L
                current_value = abs(quantity) * current_price * multiplier
                total_current_value += current_value
                
                # Calculate unrealized P/L
                if quantity > 0:  # Long position
                    unrealized_pnl = current_value - entry_value
                else:  # Short position
                    unrealized_pnl = entry_value - current_value
                
                total_unrealized_pnl += unrealized_pnl
                price_str = f"{current_price:.2f}"
                
            elif symbol_type == 'option':
                if option_price:
                    # We have actual option price
                    current_value = abs(quantity) * current_price * multiplier
                    total_current_value += current_value
                    
                    # Calculate unrealized P/L based on actual option price
                    if quantity > 0:  # Long position
                        unrealized_pnl = current_value - entry_value
                    else:  # Short position
                        unrealized_pnl = entry_value - current_value
                    
                    total_unrealized_pnl += unrealized_pnl
                    price_str = f"{current_price:.2f}"  # Actual option price
                else:
                    # Fall back to intrinsic value calculation
                    strike = c2_symbol.get('StrikePrice', 0) if isinstance(c2_symbol, dict) else 0
                    put_or_call = c2_symbol.get('PutOrCall', 'call') if isinstance(c2_symbol, dict) else 'call'
                    
                    intrinsic_value = get_option_intrinsic_value(underlying_price, strike, put_or_call, abs(quantity))
                    total_current_value += intrinsic_value
                    
                    # Calculate unrealized P/L based on intrinsic value
                    if quantity > 0:  # Long position
                        unrealized_pnl = intrinsic_value - entry_value
                    else:  # Short position
                        unrealized_pnl = entry_value - intrinsic_value
                    
                    total_unrealized_pnl += unrealized_pnl
                    price_str = f"{underlying_price:.2f}*"  # * indicates underlying price
        else:
            price_str = "--"
        
        # Format P/L with colors (using text indicators since we can't use actual colors)
        if unrealized_pnl >= 0:
            unrealized_str = f"${unrealized_pnl:,.0f}"
        else:
            unrealized_str = f"(${abs(unrealized_pnl):,.0f})"
        
        if realized_pnl >= 0:
            realized_str = f"${realized_pnl:,.0f}"
        else:
            realized_str = f"(${abs(realized_pnl):,.0f})"
        
        # Print row
        print(f"{formatted_date:<15} {full_symbol:<15} {description:<35} {side:<8} {abs(quantity):<8.0f} {avg_px:<10.2f} {price_str:<10} {unrealized_str:<15} {realized_str:<15}")
    
    # Summary row
    print("-"*120)
    
    # Format totals with color indicators
    if total_unrealized_pnl >= 0:
        total_unrealized_str = f"${total_unrealized_pnl:,.0f}"
    else:
        total_unrealized_str = f"(${abs(total_unrealized_pnl):,.0f})"
    
    if total_realized_pnl >= 0:
        total_realized_str = f"${total_realized_pnl:,.0f}"
    else:
        total_realized_str = f"(${abs(total_realized_pnl):,.0f})"
    
    print(f"{'TOTALS':<15} {'':<15} {'':<35} {'':<8} {'':<8} {'':<10} {'':<10} {total_unrealized_str:<15} {total_realized_str:<15}")
    
    print("\n" + "="*120)
    
    # Portfolio summary
    if strategy_details:
        print("\n📈 PORTFOLIO SUMMARY")
        print("="*120)
        
        equity = strategy_details.get('Equity', 0)
        cash = strategy_details.get('Cash', 0)
        buying_power = strategy_details.get('BuyingPower', 0)
        model_value = strategy_details.get('ModelAccountValue', 0)
        starting_cash = strategy_details.get('StartingCash', 0)
        margin_used = strategy_details.get('MarginUsed', 0)
        
        # Calculate total P/L
        total_account_pnl = model_value - starting_cash
        total_account_pnl_pct = (total_account_pnl / starting_cash * 100) if starting_cash > 0 else 0
        
        print(f"\n  Starting Capital:          ${starting_cash:>15,.2f}")
        print(f"  Current Account Value:     ${model_value:>15,.2f}")
        print(f"  Available Cash:            ${cash:>15,.2f}")
        print(f"  Open Positions Value:      ${equity:>15,.2f}")
        print(f"  Buying Power:              ${buying_power:>15,.2f}")
        print(f"  Margin Used:               ${margin_used:>15,.2f}")
        print(f"\n  {'─'*50}")
        
        # Color code the P/L
        pnl_symbol = "🔴" if total_account_pnl < 0 else "🟢"
        print(f"  {pnl_symbol} Total Open P/L:           ${total_account_pnl:>15,.2f}  ({total_account_pnl_pct:>6.2f}%)")
        print(f"  {'─'*50}")
        
        # Additional stats
        num_trades = strategy_details.get('NumTrades', 0)
        num_winners = strategy_details.get('NumWinners', 0)
        num_losers = strategy_details.get('NumLosers', 0)
        win_pct = strategy_details.get('PercentWinTrades', 0)
        
        print(f"\n  Total Trades:              {num_trades:>15}")
        print(f"  Winners / Losers:          {num_winners:>7} / {num_losers:<7}  ({win_pct:.1f}% win rate)")
        
    print("\n" + "="*120)
    print("ℹ️  Note: * = Underlying stock price (when option price unavailable)")
    print("   All prices are real-time from Yahoo Finance. Options show actual market prices when available.")
    print("   Portfolio totals from C2 model account. Run the script again to refresh prices.\n")


def format_autotrade_positions(data: dict):
    """Format and display autotrade positions."""
    positions = data.get('positions', data.get('results', []))
    
    if not positions:
        print("\n✓ No open positions found.")
        return
    
    print("\n" + "="*100)
    print("COLLECTIVE2 AUTOTRADE OPEN POSITIONS")
    print("="*100)
    
    print(f"\n{'Symbol':<12} {'Side':<8} {'Quantity':<12} {'Entry Price':<12} {'P/L':<12}")
    print("-"*100)
    
    total_pnl = 0.0
    
    for pos in positions:
        symbol = pos.get('symbol', 'N/A')
        side = pos.get('side', pos.get('direction', 'N/A'))
        quantity = pos.get('quantity', pos.get('qty', 0))
        entry_price = pos.get('openPrice', pos.get('entryPrice', 0))
        
        # Calculate P/L if available
        pnl = pos.get('pnl', pos.get('PnL', 0))
        total_pnl += pnl
        
        print(f"{symbol:<12} {str(side):<8} {str(quantity):<12} ${float(entry_price):<11.2f} ${pnl:>10.2f}")
    
    print("-"*100)
    print(f"{'TOTAL P/L:':<56} ${total_pnl:>10.2f}")
    print("="*100 + "\n")


def discover_mode():
    """Discovery mode - show profile and available resources."""
    print("\n" + "="*100)
    print("🔍 COLLECTIVE2 ACCOUNT DISCOVERY")
    print("="*100)
    
    # Profile
    print("\n📋 YOUR PROFILE:")
    print("-"*100)
    profile = get_profile()
    if profile.get('Results'):
        prof = profile['Results'][0]
        print(f"  Person ID:    {prof.get('Id')}")
        print(f"  Alias:        {prof.get('Alias')}")
        print(f"  Email:        {prof.get('Email')}")
        print(f"  Is Manager:   {prof.get('IsManager')}")
        print(f"  Is Investor:  {prof.get('IsInvestor')}")
    
    # Managed strategies
    print("\n📊 STRATEGIES YOU MANAGE:")
    print("-"*100)
    managed = get_managed_strategies()
    if managed:
        for strat in managed:
            print(f"  • {strat.get('StrategyName')} (ID: {strat.get('StrategyId')})")
            print(f"    Monthly Cost: ${strat.get('MonthlyCost')}, Alive: {strat.get('IsAlive')}")
    else:
        print("  ⚠ No strategies found.")
        print("  → To create a strategy, visit: https://collective2.com/strategy/create")
    
    # Autotrade accounts
    print("\n🤖 AUTOTRADE ACCOUNTS:")
    print("-"*100)
    autotraded = get_autotraded_strategies()
    if autotraded:
        for account in autotraded:
            print(f"  • Account: {account.get('Account')}")
            print(f"    Strategy: {account.get('StrategyName')} (ID: {account.get('StrategyId')})")
    else:
        print("  ⚠ No autotrade accounts found.")
        print("  → To set up autotrading, visit: https://collective2.com/autotrading")
    
    print("\n" + "="*100)
    print("\n💡 NEXT STEPS:")
    print("-"*100)
    if not managed and not autotraded:
        print("  1. Create a strategy at: https://collective2.com/strategy/create")
        print("  2. Or set up autotrading at: https://collective2.com/autotrading")
        print("  3. Then run this script again to view positions!")
    elif managed:
        print("  To view strategy positions, run:")
        for strat in managed:
            print(f"    python3 {sys.argv[0]} --mode strategy --strategy-id {strat.get('StrategyId')}")
    elif autotraded:
        print("  To view autotrade positions, run:")
        for account in autotraded:
            print(f"    python3 {sys.argv[0]} --mode autotrade --account {account.get('Account')}")
    print("="*100 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="View Collective2 open positions (for strategy managers and autotraders)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--mode",
        choices=['strategy', 'autotrade'],
        help="Mode: 'strategy' for strategy managers, 'autotrade' for autotraders"
    )
    
    parser.add_argument(
        "--strategy-id",
        type=int,
        action='append',
        dest='strategy_ids',
        help="Strategy ID(s) - for strategy mode (can specify multiple times)"
    )
    
    parser.add_argument(
        "--account",
        help="Brokerage account identifier - for autotrade mode"
    )
    
    parser.add_argument(
        "--security-type",
        choices=['CS', 'FUT', 'OPT', 'FOR'],
        help="Filter by security type (strategy mode only): CS=Stocks, FUT=Futures, OPT=Options, FOR=Forex"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response"
    )
    
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Discovery mode: find your strategies and accounts"
    )
    
    args = parser.parse_args()
    
    # Discovery mode
    if args.discover:
        discover_mode()
        return
    
    # Require mode
    if not args.mode:
        print("Error: Please specify --mode (strategy or autotrade), or use --discover", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # Strategy mode
    if args.mode == 'strategy':
        if not args.strategy_ids:
            print("Error: --strategy-id required for strategy mode", file=sys.stderr)
            sys.exit(1)
        
        data = get_strategy_positions(args.strategy_ids, args.security_type)
        
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            format_strategy_positions(data, args.strategy_ids[0] if args.strategy_ids else None)
    
    # Autotrade mode
    elif args.mode == 'autotrade':
        if not args.account:
            print("Error: --account required for autotrade mode", file=sys.stderr)
            sys.exit(1)
        
        strategy_id = args.strategy_ids[0] if args.strategy_ids else None
        data = get_autotrade_positions(args.account, strategy_id)
        
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            format_autotrade_positions(data)


if __name__ == "__main__":
    main()
