"""
Configuration loader for Collective2 CLI Suite
Attempts to load from config.py, falls back to environment variables or prompts
"""

import os
import sys

def load_config():
    """
    Load API configuration from config.py or environment variables
    Returns: (api_key, strategy_id, person_id)
    """
    # Try to import from config.py
    try:
        from config import API_KEY, STRATEGY_ID, PERSON_ID
        
        # Validate that values have been changed from defaults
        if API_KEY == "YOUR_API_KEY_HERE" or STRATEGY_ID == 0:
            raise ValueError("Please update config.py with your actual credentials")
        
        return API_KEY, STRATEGY_ID, PERSON_ID
    
    except ImportError:
        # config.py doesn't exist, try environment variables
        api_key = os.environ.get("C2_API_KEY")
        strategy_id = os.environ.get("C2_STRATEGY_ID")
        person_id = os.environ.get("C2_PERSON_ID")
        
        if api_key and strategy_id:
            return api_key, int(strategy_id), int(person_id) if person_id else 0
        
        # Neither config.py nor env vars found
        print("\n" + "="*80, file=sys.stderr)
        print("  ⚠️  CONFIGURATION ERROR", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print("\nNo configuration found. Please do ONE of the following:\n", file=sys.stderr)
        print("OPTION 1: Create config.py file (RECOMMENDED)", file=sys.stderr)
        print("  1. Copy the example: cp scripts/config_example.py scripts/config.py", file=sys.stderr)
        print("  2. Edit scripts/config.py with your API key and strategy ID", file=sys.stderr)
        print("\nOPTION 2: Set environment variables", file=sys.stderr)
        print("  export C2_API_KEY='your_api_key'", file=sys.stderr)
        print("  export C2_STRATEGY_ID='your_strategy_id'", file=sys.stderr)
        print("\nGet your API key from: https://collective2.com/api-docs/latest", file=sys.stderr)
        print("="*80 + "\n", file=sys.stderr)
        sys.exit(1)
    
    except ValueError as e:
        print("\n" + "="*80, file=sys.stderr)
        print("  ⚠️  CONFIGURATION ERROR", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print(f"\n{e}\n", file=sys.stderr)
        print("Please edit scripts/config.py and replace placeholder values with your actual:", file=sys.stderr)
        print("  • API_KEY from https://collective2.com/api-docs/latest", file=sys.stderr)
        print("  • STRATEGY_ID from your strategy page", file=sys.stderr)
        print("="*80 + "\n", file=sys.stderr)
        sys.exit(1)


# For backwards compatibility, expose values at module level
try:
    API_KEY, STRATEGY_ID, PERSON_ID = load_config()
except SystemExit:
    # Let the exit happen
    raise

