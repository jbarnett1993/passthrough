# ... (imports and initial setup remain the same) ...

with PdfPages('bollinger_bands.pdf') as export_pdf:
    for sid in sids:
        # ... (data fetching and Bollinger Bands calculation remain the same) ...

        # Initialize Position, Trade_Value, and PnL
        df['Position'] = None
        df['Trade_Value'] = df['PX_LAST'] * unit_size
        df['PnL'] = 0

        current_position = None
        position_open_price = None
        trade_counter = 0

        for i in range(len(df)):
            row = df.iloc[i]
            if current_position is None:
                if row['Order'] == 'Buy':
                    current_position = 'Buy'
                    position_open_price = row['Trade_Value']
                elif row['Order'] == 'Sell':
                    current_position = 'Sell'
                    position_open_price = row['Trade_Value']
            else:
                if (current_position == 'Buy' and row['Order'] == 'Sell') or \
                   (current_position == 'Sell' and row['Order'] == 'Buy') or \
                   (row['Order'] == 'Hold' and row['PX_LAST'] > df['Lower_Band'][i] and row['PX_LAST'] < df['Upper_Band'][i]):
                    # Close the position
                    df.at[i, 'PnL'] = row['Trade_Value'] - position_open_price if current_position == 'Buy' else position_open_price - row['Trade_Value']
                    trade_counter += 1
                    current_position = None
                    position_open_price = None
                elif (current_position == 'Buy' and row['Order'] == 'Buy') or \
                     (current_position == 'Sell' and row['Order'] == 'Sell'):
                    # Continue holding the position
                    continue

            df.at[i, 'Position'] = current_position

        # ... (summary DataFrame and plotting code remain the same) ...


