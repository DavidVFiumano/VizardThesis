from typing import Tuple, List

import viz

from .VizardEvent import VizardEvent

class FrameUpdateEvent(VizardEvent):
    PlayerPosition : List[float] = viz.MainView.getPosition()
    LastPosition : List[float] = viz.MainView.getPosition()
    PlayerVelocity : List[float] = [0.0, 0.0, 0.0]
    FrameNumber : int = 0
    
    def __init__(self, playerPosition : Tuple[float, float, float]):
        type(self).FrameNumber += 1
        type(self).LastPosition = type(self).PlayerPosition
        type(self).PlayerPosition = playerPosition
        type(self).PlayerVelocity = [last - current for last, current in zip(type(self).LastPosition, type(self).PlayerPosition)]