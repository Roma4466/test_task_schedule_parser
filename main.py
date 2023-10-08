import pandas as pd

from xlxs_parcer import analyze

print("Drag your file into data folder in root directory of this project")
name = str(input("Write file name without extension, for example: fen:\n"))

file_path = f'data/{name}.xlsx'
df = pd.read_excel(file_path, header=None)

analyze(df, name)

print("Analysis finished, seek json result file in output folder")
print("Note, that file may be in wrong encoding for your IDE")
print("If you are using PyCharm, just click on \"Reload in 'windows-1251'\"")