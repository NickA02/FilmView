"""Controller for App"""

from Model import Model

import xml.etree.ElementTree as ET
import numpy as np
from MetaDataHandler import parsed_metadata

class Controller:
    model: Model

    def __init__(self, path: str):
        self.model = Model(path)

    
    
    def pauseVideo(self):
        """Pause Current Video"""
        self.model.pauseVideo()
    
    def playVideo(self):
        """Play Current Video"""
        self.model.playVideo()
    
    def changeVideo(self, path: str):
        """Change Current Video"""
        self.model.changeVideo(path)
    
    def nextView(self):
        """Skip to next view in video"""
        self.model.nextView()
    
    def nextPlay(self):
        """Skip to next play in video"""
        self.model.nextPlay()
    
    def prevView(self):
        """Go back to previous view in video"""
        self.model.prevView()
    
    def prevPlay(self):
        """Go back to previous play in video"""
        self.model.prevPlay()
    
    def fetch_metadata(self) -> parsed_metadata:
        """Fetches current play metadata"""
        return self.model.fetch_metadata()
    
    def fetch_current_frame(self) -> np.ndarray:
        """Fetches current frame of video"""
        return self.model.fetch_current_frame()
    
    def update_frame(self):
        """Updates frame"""
        self.model.update_frame()
    
    def check_metadata_change(self) -> bool:
        """Check if the metadata of the current frame is different than when previously checked"""
        return self.model.check_metadata_change()
    
    def get_num_plays(self) -> int:
        """Return the number of plays included in the metadata"""
        return self.model.get_num_plays()



    
    
    