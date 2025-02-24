import pandas as pd

from main import process_video
from position import Position



def create_df_from_tuples(data):

    column_names = [col_name for col_name, _ in data]
    values = [vals for _, vals in data]
    df = pd.DataFrame(values).T
    df.columns = column_names

    return df



p1 = Position("kohm", 353, 630, 319, 48)
p2 = Position("N", 853, 435, 79, 36)


data = process_video("test.mp4", 1, [p1, p2], ['en'])



df = create_df_from_tuples(data)
csv_filename = "output.csv"
df.to_csv(csv_filename, index=False)
print(f"CSV file '{csv_filename}' has been created!")
