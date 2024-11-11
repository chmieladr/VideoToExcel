from extract import extract_frames, extract_data, Position
from custom import measures


def process_video(video_path: str, processor: callable, pos: Position = None,
                  start_timestamp: int = 0, end_timestamp: int = None):
    extract_frames(video_path, pos)
    extract_data(video_path.split('.')[0] + '_frames', processor=processor,
                 start_timestamp=start_timestamp, end_timestamp=end_timestamp)


# Example usage, edit the params first
if __name__ == "__main__":
    path = "video.mp4"
    process_video(path, measures, pos=Position(1280, 720))
