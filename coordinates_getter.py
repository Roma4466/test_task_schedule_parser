def get_day_coordinates(df, name):
    coordinates = None

    for row in df.iterrows():
        index, data = row
        for col in range(len(data)):
            if data[col] == name:
                coordinates = (index, col)
                break
        if coordinates:
            return coordinates
