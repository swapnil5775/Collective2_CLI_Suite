#!/usr/bin/env python3
"""
Real-time Collective2 Position Monitor
Refreshes positions every 30 seconds with live prices
"""

import time
import os
import sys
from subprocess import run

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    strategy_id = 153075915
    refresh_interval = 30  # seconds
    
    print("🚀 Collective2 Real-time Position Monitor")
    print(f"Strategy ID: {strategy_id}")
    print(f"Refresh interval: {refresh_interval} seconds")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            clear_screen()
            print(f"🔄 Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*80)
            
            # Run the main script
            result = run([
                'python3', 
                '/Users/swapnil5775/Collective2_CLI_Suite/scripts/c2_open_positions.py',
                '--mode', 'strategy',
                '--strategy-id', str(strategy_id)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"Error: {result.stderr}")
            
            print(f"\n⏰ Next refresh in {refresh_interval} seconds... (Ctrl+C to stop)")
            time.sleep(refresh_interval)
            
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
