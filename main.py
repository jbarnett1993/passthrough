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

'''
Happy Quiz Day!! Enjoy and good luck.

1	Lunar New Year 2024 is the year of what animal?
2	What year did the Scottish Independence Referendum take place?
3	In medicine, how is the 'Carpal' region of the body more commonly known?
4	"First Lord of the Treasury” is inscribed on the brass letterbox of which door in London?
5	Which now famous TV chef started cooking at the age of eight in his parents’ pub, ‘The Cricketers, in Clavering, Essex?
6	If the Earth were made into a black hole, what would be the diameter of its event horizon - (i) 20mm (ii) 20cm (iii) 20m?
7	In men’s football, who is the most capped player for (i) England (ii) Wales (iii) Scotland
8	Throughout the Harry Potter novels, Harry is mentioned by name 18,956 times. Which character is the second most mentioned coming in at a total of 6,464?
9	What is the name of the third-longest river in the world?
10	Which films do the following quotes come from?
(i) “I’m also just a girl, standing in front of a boy, asking him to love her.”
(ii) ""Just keep swimming.”
(iii) “Jack, I Want You To Draw Me Like One Of Your French Girls.”

'''