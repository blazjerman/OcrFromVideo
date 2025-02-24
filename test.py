import pandas as pd

from main import process_video
from position import Position

import os
import glob
import pandas as pd

def create_df_from_tuples(data):

    column_names = [col_name for col_name, _ in data]
    values = [vals for _, vals in data]
    df = pd.DataFrame(values).T
    df.columns = column_names

    return df



p1 = Position("kohm", 353, 630, 319, 48)
p2 = Position("N", 853, 435, 79, 36)


frame_rate = 30
video_folder = "videos"
mp4_files = glob.glob(os.path.join(video_folder, "*.mp4"))

for video_path in mp4_files:

    print(f"Proccesing file '{video_path}'.")

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    csv_filename = os.path.join(video_folder, f"{video_name}.csv")

    data = process_video(video_path, frame_rate, [p1, p2], ['en'])
    df = create_df_from_tuples(data)
    df.to_csv(csv_filename, index=False)

    print(f"CSV file '{csv_filename}' has been created!")

