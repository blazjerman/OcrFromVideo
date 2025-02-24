import cv2
from PIL import Image


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



video_path = "test.mp4"
frames_array = video_to_frames(video_path, 30)


# Function to open image with system's default viewer
def open_image(image):
    # Convert numpy array to Image using Pillow
    pil_image = Image.fromarray(image)
    pil_image.show()

for frame in frames_array:
    open_image(frame)

