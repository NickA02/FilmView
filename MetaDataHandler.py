"""Meta Data Handler Module"""

import xml.etree.ElementTree as ET

class MetadataHandler:
    full_game_tree: ET
    plays_tree: ET.Element
    current_play: int = 0
    current_view: int = 0
    plays_list: list[ET.Element]
    play_views: list[ET.Element]
    


    def __init__(self, path: str="film/Arizona Defense.xchange"):
        if not path.endswith(".xchange"):
            raise Exception("Error: Invalid Data Type for video")
        self.full_game_tree = ET.parse(path)
        self.plays_tree = self.full_game_tree.find("Plays")
        self.plays_list = self.plays_tree.findall("Play")
        self.play_views = self.plays_list[self.current_play].find("Views").findall("View")
    
    def nextPlay(self) -> int:
        self.current_play += 1
        if self.current_play >= len(self.plays_list):
            self.current_play = 0
        self.current_view = 0
        self.play_views = self.plays_list[self.current_play].find("Views").findall("View")
        return int(self.play_views[self.current_view].find("MarkIn").text)
    
    def nextView(self) -> int:
        self.current_view += 1
        if self.current_view >= len(self.play_views):
            return self.nextPlay()
        return int(self.play_views[self.current_view].find("MarkIn").text)

    def prevPlay(self) -> int:
        self.current_play -= 1
        if self.current_play < 0:
            self.current_play = 0
        self.current_view = 0
        self.play_views = self.plays_list[self.current_play].find("Views").findall("View")
        return int(self.play_views[self.current_view].find("MarkIn").text)

    def prevView(self) -> int:
        self.current_view -= 1
        if self.current_view < 0:
            self.prevPlay()
            self.current_view = len(self.play_views) - 1
        return int(self.play_views[self.current_view].find("MarkIn").text)
    
    def getMetadata(self) -> ET.Element:
        return self.plays_list[self.current_play]
    
    def checkCurrentPlay(self, frame_index: int):
        view = self.play_views[self.current_view]
        max_frame = int(view.find("MarkIn").text) + int(view.find("Duration").text)
        if frame_index > max_frame:
            self.nextView()