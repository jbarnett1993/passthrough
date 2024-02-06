import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the data from the Excel file
df = pd.read_excel('your_file.xlsx')

# Drop the SUM and Position columns as they are not needed for the plot and calculations
df = df.drop(['SUM', 'Position'], axis=1)

# Calculate the standard deviation for each player and add it as a new column
df['Std Dev'] = df.iloc[:, 1:].std(axis=1)

# Prepare data for plotting ranks over time
ranking_df = df.set_index('Name').T.apply(lambda x: x.rank(ascending=False))

# Plotting
plt.figure(figsize=(10, 6))
for player in ranking_df.columns:
    plt.plot(ranking_df.index, ranking_df[player], label=player, marker='o')

plt.title('Ranking Over Time')
plt.xlabel('Week')
plt.ylabel('Rank')
plt.gca().invert_yaxis()  # Invert y-axis to show the best rank (1) at the top
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Display the data frame with the standard deviation column
print(df)


'''
Position	Name	Week 1 	Week 2	Week3	Week4	SUM
1	PETER WELSBY	222	171	207	118	718
2	NEAL CAPECCI	191	165	191	161	708
3	JOE ROTHWELL	207	129	149	143	628
4	DOMINIQUE LAPOINTE	187	140	150	141	618
5	JAMES BARNETT	200	225	126	53	604
6	PHILIP EHRMANN	157	140	148	148	593
7	AMAN JOHAR	158	202	114	117	591
8	DAVID DUGDALE	152	127	139	139	557
9	WESLEY ADEYEMI	129	149	138	95	511
10	ERICA CAMILLERI	127	131	147	93	498
11	DAVID RULE	159	156	129	52	496
12	GEORGE HAMBLING	119	86	101	87	393
13	LAUREN MARIANO	129	98	122	26	375
14	EDWARD RITCHIE	85	89	99	91	364



'''