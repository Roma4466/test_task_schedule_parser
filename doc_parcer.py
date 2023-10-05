from docx import Document
import pandas as pd

from xlxs_parcer import analyze

# Load the document
doc_path = 'data/3.docx'
document = Document(doc_path)

table = document.tables[0]
data = []

# Iterate through each row in table
for row in table.rows:
    row_data = []
    for cell in row.cells:
        row_data.append(cell.text.strip())
    data.append(row_data)

# Convert list of lists into DataFrame
df = pd.DataFrame(data)

# Optionally, set the column headers if they are in the first row
df.columns = df.iloc[0]
df = df.drop(df.index[0])

# print(df['День'].iloc[0])

analyze(df, "", "", 1, 1)
# print(df)
