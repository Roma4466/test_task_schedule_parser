def get_day_coordinates(df, names):
    for row in df.iterrows():
        index, data = row
        for col in range(len(data)):
            if str(data[col]) in names:
                return index, col