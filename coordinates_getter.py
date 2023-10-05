def get_coordinates_by_name(df, name):
    coordinates = None
    name = name.lower().strip()  # Normalize the search name

    for row in df.iterrows():

        index, data = row
        for col in range(len(data)):
            cell_content = str(data[col]).lower().strip()
            if cell_content == name:
                coordinates = (index, col)
                break
        if coordinates:
            return coordinates[1]
    return 0