import sys
import os
import logging
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from suedwestenergie.utils.logger import app_logger, log_info, log_warning, log_error

def simulate_logging():
    print("Starting logging simulation...")
    
    # 1. Info Log
    print("1. Logging INFO message...")
    log_info("Simulation started", context="simulate_logging")
    
    # 2. Warning Log
    print("2. Logging WARNING message...")
    log_warning("This is a simulated warning", context="simulate_logging")
    
    # 3. Error Log
    print("3. Logging ERROR message...")
    try:
        # Simulate an exception
        x = 1 / 0
    except Exception as e:
        log_error(e, context="simulate_logging")
        
    print("Simulation complete. Check logs/app.log")

if __name__ == "__main__":
    simulate_logging()
