from typing import Dict, Any, Union, List
import viz

from AlexaEngine import State

from Events import FrameUpdateEvent
from PlayerMovement import disableMovement

class GameEnded(State):
    
    def __init__(self, displayText: str):
        super().__init__()
        self.displayText = displayText
        self.textObject = None

    def centerTextOnScreen(self, textObject: viz.VizNode) -> None:
        boundingBox = textObject.getBoundingBox(viz.REL_PARENT)
        width = boundingBox.width
        height = boundingBox.height

        xPosition = (1 - width) / 2
        yPosition = (1 - height) / 2

        textObject.setPosition(xPosition, yPosition, viz.REL_PARENT, viz.REL_PARENT)

    def displayCenteredText(self) -> None:
        self.textObject = viz.addText(self.displayText, parent=viz.SCREEN)
        self.textObject.setScale(0.5, 0.5, mode=viz.REL_PARENT)
        self.centerTextOnScreen(self.textObject)

    def transitionIn(self, previousState: Union[None, str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        disableMovement()
        self.displayCenteredText() 


    def handle(self, event: FrameUpdateEvent, otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        pass

    def getNextState(self, availableStates: List[str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> Union[str, None]:
        return None

    def transitionOut(self, nextState: str, otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        if self.textObject:
            self.textObject.remove()

class GameEndedByRobot(GameEnded):
    def __init__(self):
        super().__init__("A robot caught you! You lose!")


class GameEndedByTimer(GameEnded):
    def __init__(self):
        super().__init__("You're out of time!")

class GameEndedInVictory(GameEnded):
    def __init__(self):
        super().__init__("Winner, Winner, Chicken Dinner!")