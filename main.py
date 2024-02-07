import pandas as pd
import tia.bbg.datamgr as dm

mgr = dm.BbgDataManager()

# Assuming 'events' is your list of event codes
events = ['JNCICLEI Index', 'SZUE Index', ...]  # truncated for brevity

df = pd.DataFrame(index=events)

# Function to fetch country data for a list of tickers
def get_countries(tickers):
    # Assuming that 'mgr' can handle a list of tickers and return their countries
    # This is a placeholder; you'll need to replace it with actual logic
    # that fetches country data for the given tickers.
    countries_info = mgr[tickers].get_field('COUNTRY')
    return countries_info

# Batch processing
batch_size = 100
for i in range(0, len(events), batch_size):
    tickers_batch = events[i:i+batch_size]
    countries = get_countries(tickers_batch)
    
    # Update the DataFrame with the country information
    for ticker in tickers_batch:
        if ticker in countries:
            df.at[ticker, 'country'] = countries[ticker]

print(df)