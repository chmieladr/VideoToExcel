import os

from PIL import Image
import pandas as pd
import pytesseract
import cv2


class Position:
    def __init__(self, width: int, height: int, x: int = 0, y: int = 0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y


def extract_frames(video_path: str, pos: Position = None):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return

    output_folder = video_path.split('.')[0] + '_frames'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if pos is None:
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        pos = Position(width, height)

    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_count = 0  # current frame in the video
    extracted_count = 0  # number of frames extracted

    while True:
        ret, frame = video.read()  # reading frames until the end is reached
        if not ret:
            break

        if frame_count % fps == 0:  # saving one frame per each second
            height, width, _ = frame.shape
            assert pos.x + pos.width <= width and pos.y + pos.height <= height
            frame = frame[pos.y:pos.y + pos.height, pos.x:pos.x + pos.width]

            output_filename = os.path.join(output_folder, f"frame_{extracted_count}.jpg")
            cv2.imwrite(output_filename, frame)
            extracted_count += 1

        frame_count += 1

    video.release()
    print(f"{video_path} -> Frames extracted successfully!")


def extract_text(image_path: str) -> str:
    text = pytesseract.image_to_string(Image.open(image_path))
    return text


def extract_data(frames_folder_path: str, processor: callable, verbose: bool = False,
                 start_timestamp: int = 0, end_timestamp: int = None):
    df, columns = None, None
    if end_timestamp is not None:
        files_list = os.listdir(frames_folder_path)[start_timestamp:end_timestamp]
    else:
        files_list = os.listdir(frames_folder_path)[start_timestamp:]

    for filename in files_list:
        if filename.endswith(".jpg"):
            try:
                image_path = os.path.join(frames_folder_path, filename)
                processed_text = processor(extract_text(image_path))

                if df is None:  # create a new DataFrame if it doesn't exist
                    columns = processed_text.keys()
                    df = pd.DataFrame(columns=processed_text.keys())

                if columns != processed_text.keys():  # check if the column names match
                    if verbose:
                        print(f"Error for frame `{filename}`: Column mismatch")
                    continue

                df = pd.concat([df, pd.DataFrame([processed_text], columns=columns)], ignore_index=True)
            except Exception as e:
                if verbose:
                    print(f"Error for frame `{filename}`: {e}")
                continue

    excel_path = f"{frames_folder_path[:-7]}.xlsx"
    df.dropna(axis=0, how='any', inplace=True)  # remove columns with NaN vals
    df.to_excel(excel_path, index=False, engine='openpyxl')
    print(f"{excel_path} -> Data saved successfully!")
