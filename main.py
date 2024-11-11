from extract import extract_frames, extract_data, Position
from custom import measures


def process_video(video_path: str, processor: callable,
                  pos: Position = None,
                  start_timestamp: int = 0):
    extract_frames(video_path, pos)
    extract_data(video_path.split('.')[0] + '_frames', processor=processor, start_timestamp=start_timestamp)


if __name__ == "__main__":
    # path = "Pomiary 430i 2024-11-10 23-32-09.mp4"
    # process_video(video_path=path, processor=measures, pos=Position(width=535, height=600, x=655, y=160))

    path = "Pomiary X1 2024-11-10 20-56-45.mp4"
    process_video(video_path=path, processor=measures, pos=Position(width=535, height=600, x=655, y=160),
                  start_timestamp=83)
