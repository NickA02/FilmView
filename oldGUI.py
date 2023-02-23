import numpy as np
import cv2 as cv
import cvui
from Controller import Controller
import xml.etree.ElementTree as ET

WINDOW_NAME = 'Film Viewer'
cvui.init(WINDOW_NAME)
frame = np.zeros((800, 1500, 3), np.uint8)

def main():
   controller = Controller()
   current_frame = controller.fetch_current_frame()
   while True:
      current_frame = controller.fetch_current_frame()
      frame[:] = (49, 52, 49)
      cvui.image(frame, 50, 40, current_frame)
      if cvui.button(frame, 1365, 40, 100, 20, "Play"):
         controller.playVideo()
      elif cvui.button(frame, 1365, 65, 100, 20, "Pause"):
         controller.pauseVideo()
      elif cvui.button(frame, 1365, 90, 100, 20, "Next View"):
         controller.nextView()
      elif cvui.button(frame, 1365, 115, 100, 20, "Next Play"):
         controller.nextPlay()
      elif cvui.button(frame, 1365, 140, 100, 20, "Previous View"):
         controller.prevView()
      elif cvui.button(frame, 1365, 165, 100, 20, "Previous Play"):
         controller.prevPlay()
      #data = controller.fetch_metadata()
      #cvui.text(frame, 1365, 190, ET.tostring(data, encoding='unicode'))

      cvui.imshow(WINDOW_NAME, frame)
      controller.update_frame()









if __name__ == "__main__":
   #running controller function
   main()