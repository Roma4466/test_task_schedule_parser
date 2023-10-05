import pandas as pd

from xlxs_parcer import analyze

file_path = 'data/3.xlsx'
df = pd.read_excel(file_path, header=None)

faculty = df.iloc[5, 0]
specialty = df.iloc[6, 0].split("\"")[1]
year_of_study = int(df.iloc[6, 0].split(", ")[1][0])
started_year = int(df.iloc[7, 0].split("-")[0][-4:])

analyze(df, faculty, specialty, year_of_study, started_year)
print(type(df))
