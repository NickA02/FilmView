"""VideoHandler Module"""
import cv2 as cv
import numpy as np
import os


class VideoHandler:
    video_player: cv.VideoCapture
    currentFrame: np.ndarray
    frame_number: int = 0
    isPlaying: bool = True


    def __init__(self, videoPath: str = "film/Arizona Offense"):
        if not os.path.exists(f"{videoPath}.mp4"):
            raise Exception(f"Video path {videoPath}.mp4 not found")
        self.video_player = cv.VideoCapture(f"{videoPath}.mp4")
        if not self.video_player.isOpened():
            raise Exception("Error: Could not open video file")
        self.feed()

    
    def startFeed(self):
        self.isPlaying = True

    def pauseFeed(self):
        self.isPlaying = False
    
    def feed(self) -> int:
        if self.isPlaying:
            # Capture frame-by-frame
            ret, frame = self.video_player.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                return
            self.frame_number += 1
            self.currentFrame = frame
        return self.frame_number

            
    def skip_to_frame(self, frame_number: int):
        if frame_number < 0 or frame_number > self.video_player.get(cv.CAP_PROP_FRAME_COUNT):
            print(frame_number)
            print(self.video_player.get(cv.CAP_PROP_FRAME_COUNT))
            raise Exception("Error: Frame Index Out of Bounds")
        self.video_player.set(cv.CAP_PROP_POS_FRAMES, frame_number)
        self.frame_number = frame_number
        if not self.isPlaying:
            self.isPlaying = True
            self.feed()
            self.isPlaying = False
            return
        self.feed()
    
    def set_video(self, path: str):
        if self.video_player.isOpened():
            self.video_player.release()
        if not path.endswith(".mp4"):
            raise Exception("Error: Invalid Data Type for video")
        self.video_player = cv.VideoCapture(path)
        if not self.video_player.isOpened():
            raise Exception("Error: Could not open video file")
        self.skip_to_frame(0)
        self.feed()
    
    def getCurrentFrame(self) -> np.ndarray:
        """Retrieves current frame"""
        cf = self.currentFrame
        cf = cv.cvtColor(cf, cv.COLOR_BGR2GRAY)
        cf = cv.GaussianBlur(cf, (3, 3), 0, 0, cv.BORDER_DEFAULT)
        cf = cv.Sobel(cf, -1, 1, 1)
        return cf










    
        