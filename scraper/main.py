from zillow import main as zillow_main
from log_handler import _logger

def main():
    """
    Main function to run the Zillow crawler.
    This function initializes the Zillow crawler and starts the data fetching process.
    """
    _logger.info("Starting Zillow Crawler...")
    zillow_main()   

if __name__ == "__main__":
    # for m in range(1,1000):
    main()