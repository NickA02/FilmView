"""Controller Module"""
import xml.etree.ElementTree as ET
import numpy as np

from VideoHandler import VideoHandler
from MetaDataHandler import MetadataHandler, parsed_metadata

class Model:
    videoModel: VideoHandler
    metadataModel: MetadataHandler
    observers: list = []

    def __init__(self):
        self.videoModel = VideoHandler()
        self.metadataModel = MetadataHandler()
    
    def pauseVideo(self):
        """Pause Current Video"""
        self.videoModel.pauseFeed()
    
    def playVideo(self):
        """Play Current Video"""
        self.videoModel.startFeed()
    
    def changeVideo(self, path: str):
        """Change Current Video"""
        self.videoModel.set_video(path)
        self.metadataModel.set_metadata(path.removesuffix(".mp4"))
    
    def nextView(self):
        """Skip to next view in video"""
        frame_number = self.metadataModel.nextView()
        self.videoModel.skip_to_frame(frame_number)
    
    def nextPlay(self):
        """Skip to next play in video"""
        frame_number = self.metadataModel.nextPlay()
        self.videoModel.skip_to_frame(frame_number)
    
    def prevView(self):
        """Go back to previous view in video"""
        frame_number = self.metadataModel.prevView()
        self.videoModel.skip_to_frame(frame_number)
    
    def prevPlay(self):
        """Go back to previous play in video"""
        frame_number = self.metadataModel.prevPlay()
        self.videoModel.skip_to_frame(frame_number)
    
    def fetch_metadata(self) -> parsed_metadata:
        """Fetches current play metadata"""
        return self.metadataModel.getMetadata()
    
    def fetch_current_frame(self) -> np.ndarray:
        """Fetches current frame of video"""
        return self.videoModel.getCurrentFrame()
    
    def update_frame(self):
        """Updates frame"""
        frame_number = self.videoModel.feed()
        self.metadataModel.checkCurrentPlay(frame_number)
    
    def notifyObservers(self):
        """Notify the observers of this model that a change has been made"""
        for o in self.observers:
            o.update(self)
    
    def check_metadata_change(self) -> bool:
        return self.metadataModel.checkChanges()
    



    
    