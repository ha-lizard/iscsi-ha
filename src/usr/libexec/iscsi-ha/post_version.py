#!/usr/bin/env python3
"""
Script to gather usage statistics by sending a version number to a server.
This script is intended to be called once during installation.

Usage:
    python script_name.py <version_number>

Dependencies:
    Requires the 'requests' library. Install it via pip if not already installed:
    pip install requests
"""

import sys
import requests


def main():
    # Validate command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <version_number>", file=sys.stderr)
        sys.exit(1)

    # Extract the version number from the command-line arguments
    version = sys.argv[1]

    # Define the URL for reporting usage statistics
    url = f"http://halizard.pulse-lists.com/count.php?VERSION={version}"

    try:
        # Send a GET request to the server
        # 10-second timeout for safety
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"Usage statistics sent successfully for version {version}.")
    except requests.exceptions.RequestException as e:
        # Handle any errors during the HTTP request
        print(f"Failed to send usage statistics: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
