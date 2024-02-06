import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the data from the Excel file
df = pd.read_excel('your_file.xlsx')

# Drop the Position column as it is not needed for the plot
df = df.drop(['Position'], axis=1)

# Calculate the cumulative sum across the weeks for each player
cumulative_scores = df.iloc[:, 2:].cumsum(axis=1)
cumulative_scores['Name'] = df['Name']  # Add names back to the cumulative_scores DataFrame
cumulative_scores = cumulative_scores.set_index('Name')

# Calculate the standard deviation for each player and add it as a new column to the original df
df['Std Dev'] = df.iloc[:, 2:].std(axis=1)

# Plotting
plt.figure(figsize=(10, 6))
for player in cumulative_scores.index:
    plt.plot(cumulative_scores.columns, cumulative_scores.loc[player], label=player, marker='o')

plt.title('Cumulative Scores Over Time')
plt.xlabel('Week')
plt.ylabel('Cumulative Score')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Display the data frame with the standard deviation column
print(df)