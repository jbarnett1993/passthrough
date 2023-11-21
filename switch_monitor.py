import pandas as pd
from openpyxl.utils import get_column_letter

writer = pd.ExcelWriter('eur_exposure.xlsx', engine='openpyxl')
for df in final_dfs_merged:
    name = df['NAME()'][0].split(" ")[0]
    df.to_excel(writer, sheet_name=name, index=False)

    worksheet = writer.sheets[name]

    for col in df.columns:
        # Find the maximum length of the data in each column
        max_length = max(df[col].astype(str).apply(len).max(), len(col))
        # Adjust the column width; add a small buffer to ensure fit
        column_letter = get_column_letter(df.columns.get_loc(col) + 1)
        worksheet.column_dimensions[column_letter].width = max_length + 2

writer.save()