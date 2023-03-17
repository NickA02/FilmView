"""Meta Data Handler Module"""

import xml.etree.ElementTree as ET
import pandas as pd
import os

class parsed_metadata():
    play_number: int
    current_view: str
    pff_data: pd.DataFrame


    def __init__(self, play_number: int, current_view: str, pff_data: pd.DataFrame):
        self.play_number = play_number
        self.current_view = current_view
        self.pff_data = pff_data


class MetadataHandler:
    full_game_tree: ET
    plays_tree: ET.Element
    current_play: int = 0
    current_view: int = 0
    plays_list: list[ET.Element]
    play_views: list[ET.Element]
    pff_data: pd.DataFrame    
    changes: bool = True
    


    def __init__(self, path: str="film/Arizona Offense"):
        if not os.path.exists(f"{path}.xchange") or not os.path.exists(f"{path}.csv"):
            raise Exception("Metadata does not exist")
        self.full_game_tree = ET.parse(f"{path}.xchange")
        self.plays_tree = self.full_game_tree.find("Plays")
        self.plays_list = self.plays_tree.findall("Play")
        self.play_views = self.plays_list[self.current_play].find("Views").findall("View")
        self.pff_data = pd.read_csv(f"{path}.csv")
    
    def nextPlay(self) -> int:
        self.current_play += 1
        self.changes = True
        if self.current_play >= len(self.plays_list):
            self.current_play = 0
        self.current_view = 0
        self.play_views = self.plays_list[self.current_play].find("Views").findall("View")
        return int(self.play_views[self.current_view].find("MarkIn").text)
    
    def nextView(self) -> int:
        self.current_view += 1
        self.changes = True
        if self.current_view >= len(self.play_views):
            return self.nextPlay()
        return int(self.play_views[self.current_view].find("MarkIn").text)

    def prevPlay(self) -> int:
        if self.current_play == 0:
            self.current_view = 0
            return int(self.play_views[self.current_view].find("MarkIn").text)
        self.current_play -= 1
        self.changes = True
        self.current_view = 0
        self.play_views = self.plays_list[self.current_play].find("Views").findall("View")
        return int(self.play_views[self.current_view].find("MarkIn").text)

    def prevView(self) -> int:
        self.current_view -= 1
        self.changes = True
        if self.current_view < 0:
            self.prevPlay()
            self.current_view = len(self.play_views) - 1
        return int(self.play_views[self.current_view].find("MarkIn").text)
    
    def getMetadata(self) -> parsed_metadata:
        return parsed_metadata(
            play_number=self.current_play, 
            current_view=self.play_views[self.current_view].find("CameraView").text,
            pff_data=self.pff_data.iloc[self.current_play]
            )
    
    def checkCurrentPlay(self, frame_index: int):
        view = self.play_views[self.current_view]
        max_frame = int(view.find("MarkIn").text) + int(view.find("Duration").text)
        if frame_index > max_frame:
            self.nextView()
    
    def checkChanges(self) -> bool:
        if self.changes:
            self.changes = False
            return True
        return False

    def set_metadata(self, path: str):
        self.full_game_tree = ET.parse(path + ".xchange")
        self.current_play= 0
        self.current_view = 0
        self.plays_tree = self.full_game_tree.find("Plays")
        self.plays_list = self.plays_tree.findall("Play")
        self.play_views = self.plays_list[self.current_play].find("Views").findall("View")
        self.pff_data = pd.read_csv(path + ".csv")
        self.changes = True

MetadataHandler()