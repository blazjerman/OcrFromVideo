import cv2
from PIL import Image
import easyocr
import pandas as pd



reader = easyocr.Reader(['en'])


class Position:
    def __init__(self, name, x, y, width, height):
        super().__setattr__("_locked", False)
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.name = name
        super().__setattr__("_locked", True)

def video_to_frames(video_path, frame_rate=1):

    frames = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

    fps = cap.get(cv2.CAP_PROP_FPS)

    if frame_rate <= 0 or frame_rate > fps: frame_rate = 1
    interval = int(fps / frame_rate)

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_index % interval == 0: frames.append(frame)
        frame_index += 1

    cap.release()
    print(f"Extracted {len(frames)} frames.")
    return frames



def open_image(image):
    pil_image = Image.fromarray(image)
    pil_image.show()



def ocr(frames_array, position):

    text_array = []

    end = (position.x + position.width), (position.y + position.height)

    if len(frames_array) > 0:
        open_image(frames_array[0][position.y:end[1], position.x:end[0]])

    for frame in frames_array:
        text_array.append(reader.readtext(frame[position.y:end[1], position.x:end[0]]))

    return text_array



def main_shit(video_path, frame_rate, positions_array):

    frames_array = video_to_frames(video_path, frame_rate)

    data = []

    for position in positions_array:

        detections = ocr(frames_array, position)

        text_array = []

        for detection in detections:
            text = ""
            for det in detection:
                text += det[1]
            text_array.append(text)

        data.append((position.name, text_array))

    return data




p1 = Position("kohm", 353, 630, 319, 48)
p2 = Position("N", 853, 435, 79, 36)


data = main_shit("test.mp4", 1, [p1, p2])




def create_df_from_tuples(data):

    column_names = [col_name for col_name, _ in data]
    values = [vals for _, vals in data]
    df = pd.DataFrame(values).T
    df.columns = column_names

    return df


df = create_df_from_tuples(data)

csv_filename = "output.csv"
df.to_csv(csv_filename, index=False)

print(f"CSV file '{csv_filename}' has been created!")


