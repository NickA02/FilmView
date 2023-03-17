from Controller import Controller
import numpy as np
import cv2 as cv
from MetaDataHandler import parsed_metadata
import os

video_name_base = "work/users/n/a/nalmy/split_clips/"

class VideoThread():
    video: cv.VideoWriter = None

    def __init__(self, path: str):
        """Initialize Controller for film model"""
        self.controller = Controller(path)
        self._run_flag = True
        #Pull height and width for clip creation
        self.height, self.width, layers = self.controller.fetch_current_frame().shape
        #Initialize Metadata
        self.metadata = self.controller.fetch_metadata()
        self.new_clip()

    def run(self):
        """Main method that begins video parsing"""
        self._stop_flag = False
        self._run_flag = True
        while self._run_flag:
            #Update and pull next frame from model
            self.controller.update_frame()

            #Check to see if it is still current play/view
            if self.controller.check_metadata_change():
                #If view has changed, fetch metadata and create a new clip
                self.metadata = self.controller.fetch_metadata()
                self.new_clip()
                print(self.metadata.play_number)

            #Add current frame to clip
            self.add_frame(self.controller.fetch_current_frame())
            

    def add_frame(self, frame: np.array):
        """Function that adds a given frame to the clip"""
        try:
            self.video.write(frame)
        except:
            print("Video not open. Done recording clips?")
    
    def new_clip(self):
        """Function that ends current clip and begins a new one"""
        if self.video != None:
            self.video.release()

        if self.metadata.play_number >= self.controller.get_num_plays():
            self._run_flag == False
            return
        
        if self.metadata.current_view == "SB":
            #We do not want to capture the Score Board View -- Skip if it is SB
            self.controller.nextView()
            self.metadata = self.controller.fetch_metadata()
        
        elif self.metadata.current_view == "EZ":
            #SL and EZ are padded with two frames of SB -- Remove from beginning of EZ clips
            self.controller.update_frame()
            self.controller.update_frame()
        
        #Create new clip for next view
        self.video = cv.VideoWriter(
            f"{video_name_base}_{self.metadata.play_number}_{self.metadata.current_view}.mp4",
            cv.VideoWriter_fourcc(*'mp4v'),
            60, 
            (self.width, self.height)
            )

vt = VideoThread("split_clips/Arizona Special Teams")
vt.run()