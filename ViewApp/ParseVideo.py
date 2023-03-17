from Controller import Controller
import numpy as np
import cv2 as cv
from MetaDataHandler import parsed_metadata
import os

video_name_base = "split_clips/ARI_OFF_vs_ATL_DEF"

class VideoThread():
    def __init__(self):
        self.controller = Controller("film/Arizona Offense")
        self._run_flag = True
        self._stop_flag = False
        self.height, self.width, layers = self.controller.fetch_current_frame().shape
        self.metadata = self.controller.fetch_metadata()
        self.video = cv.VideoWriter(video_name_base+f"_{self.metadata.play_number}_{self.metadata.current_view}.mp4", cv.VideoWriter_fourcc(*'MP4V'), 60, (self.width, self.height))

    def run(self):
        # capture from web cam
        self._stop_flag = False
        self._run_flag = True
        while self._run_flag:
            self.controller.update_frame()
            if self.controller.check_metadata_change():
                self.metadata = self.controller.fetch_metadata()
                self.new_clip()
            self.add_frame(self.controller.fetch_current_frame())
            
        self._stop_flag = True

    def add_frame(self, frame: np.array):
        self.video.write(frame)
    
    def new_clip(self):
        self.video.release()
        if self.metadata.current_view == "SB":
            self.controller.nextView()
            self.metadata = self.controller.fetch_metadata()
        elif self.metadata.current_view == "EZ":
            self.controller.update_frame()
            self.controller.update_frame()
        self.video = cv.VideoWriter(
            f"{video_name_base}_{self.metadata.play_number}_{self.metadata.current_view}.mp4",
            cv.VideoWriter_fourcc(*'mp4v'),
            60, 
            (self.width, self.height)
            )

vt = VideoThread()
vt.run()