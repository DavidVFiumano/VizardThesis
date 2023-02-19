from typing import Tuple

import viz

from .VizardEvent import VizardEvent

class FrameUpdateEvent(VizardEvent):
    
    LastPosition = viz.MainView.getPosition()
    
    def __init__(self, playerPosition : Tuple[float, float, float]):
        self.playerVelocity = type(self).lastPosition - playerPosition
        type(self).LastPosition = self.playerPosition
        self.playerPosition = playerPosition