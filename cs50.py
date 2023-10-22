import sys
import requests

def get_bitcoin_price():
    """Returns the current price of Bitcoin in USD."""
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        return data["bpi"]["USD"]["rate_float"]
    
    except requests.RequestException:
        sys.exit("Error: Unable to fetch Bitcoin price from CoinDesk API.")

def main():
    # Ensure correct number of command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python bitcoin.py [number_of_bitcoins]")
    
    # Try to convert the argument to a float
    try:
        number_of_bitcoins = float(sys.argv[1])
    except ValueError:
        sys.exit("Error: Please provide a valid number of Bitcoins.")
    
    # Get the current price of Bitcoin
    bitcoin_price = get_bitcoin_price()
    
    # Calculate the cost for the specified number of Bitcoins
    total_cost = number_of_bitcoins * bitcoin_price
    
    # Print the cost formatted to 4 decimal places and with thousands separator
    print(f"The cost of {number_of_bitcoins} Bitcoins is: ${total_cost:,.4f}")

if __name__ == "__main__":
    main()