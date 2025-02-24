import cv2
import easyocr




def progress(max, now):
    print(f"\rProgress: {round(100 * now / max)}%", end="", flush=True)

def video_to_frames(video_path, frame_rate=1):

    frames = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_rate <= 0 or frame_rate > fps: frame_rate = 1
    interval = int(fps / frame_rate)

    print(f"Extracting frames.")

    index = 0

    while True:
        ret, frame = cap.read()
        progress(frame_count, index)
        if not ret:
            break
        if index % interval == 0: frames.append(frame)
        index += 1

    cap.release()

    progress(1,1)
    print()
    print("Extraction done.")

    return frames




def ocr(frames_array, position, reader):

    text_array = []

    end = (position.x + position.width), (position.y + position.height)

    print("Running ocr on " + position.name)

    for index, frame in enumerate(frames_array):
        text_array.append(reader.readtext(frame[position.y:end[1], position.x:end[0]]))
        progress(len(frames_array), index)

    progress(1,1)
    print()
    print("Ocr on " + position.name + " done.")

    return text_array



def process_video(video_path, frame_rate, positions_array, languages):

    reader = easyocr.Reader(languages)
    frames_array = video_to_frames(video_path, frame_rate)

    data = []

    for position in positions_array:

        detections = ocr(frames_array, position, reader)

        text_array = []

        for index, detection in enumerate(detections):
            text = ""
            for det in detection:
                text += det[1]
            text_array.append(text)


        data.append((position.name, text_array))



    return data
