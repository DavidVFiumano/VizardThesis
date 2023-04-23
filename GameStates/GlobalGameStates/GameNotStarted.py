from typing import Dict, Any, Union, List
import time

import viz

from StateManagement import State
from Events import FrameUpdateEvent

class GameNotStarted(State):

    def __init__(self, startKey='f', countdownDuration=5):
        super().__init__()
        self.startKey = startKey
        self.countdownDuration = countdownDuration
        self.startGame = False
        self.countdownStartTime = None
        self.countdownText = None

    def displayMessageText(self):
        # Display the message text
        self.messageText = viz.addText(f"When you're ready to start, press the '{self.startKey.upper()}' key", parent=viz.SCREEN)
        self.messageText.setScale(0.25, 0.25, mode=viz.REL_PARENT)
        self.centerTextOnScreen(self.messageText)
        
    def transitionIn(self, previousState: Union[None, str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        # Set up the environment when transitioning in
        viz.mouse.setTrap(viz.ON)
        viz.mouse.setVisible(viz.OFF)

        viz.callback(viz.KEYDOWN_EVENT, self.onKeydown)
        self.displayMessageText()

    def centerTextOnScreen(self, textObject):
        # Get the text object's width and height
        box = textObject.getBoundingBox(viz.REL_PARENT)
        width = box.width
        height = box.height

        # Calculate the centered position
        xPos = (1 - width) / 2
        yPos = (1 - height) / 2

        # Set the text object's position
        textObject.setPosition(xPos, yPos)

    def onKeydown(self, key):
        # Handle keydown event
        if key == self.startKey:
            if self.startGame:
                self.startGame = False
                self.countdownStartTime = None
                if self.countdownText:
                    self.countdownText.remove()
                    self.countdownText = None
                    self.displayMessageText()
            else:
                self.startGame = True
                self.messageText.remove()
                self.messageText = None
                self.countdownStartTime = time.time()
                self.countdownText = viz.addText("", parent=viz.SCREEN)
                self.countdownText.setScale(0.25, 0.25, mode=viz.REL_PARENT)

    def handle(self, event: FrameUpdateEvent, otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        # Handle frame update event
        if isinstance(event, FrameUpdateEvent):
            if self.startGame and self.countdownStartTime:
                elapsedTime = time.time() - self.countdownStartTime
                remainingTime = round(self.countdownDuration - elapsedTime)
                timerMessage = f"Starting in {remainingTime}..." if remainingTime > 0 else "Starting the game..."
                if self.countdownText is not None and timerMessage != self.countdownText.message:
                    self.countdownText.message(timerMessage)
                    self.centerTextOnScreen(self.countdownText)

    def getNextState(self, availableStates: List[str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> Union[str, None]:
        # Determine the next state
        if self.startGame and time.time() - self.countdownStartTime >= self.countdownDuration:
            return "PlayingGame"
        return None

    def transitionOut(self, nextState: str, otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        # Clean up when transitioning out of this state
        viz.callback(viz.KEYDOWN_EVENT, None)
        if self.messageText is not None:
            # honestly, this should never happen. But maybe you want to set the timer to zero and it does?
            self.messageText.remove()
        if self.countdownText:
            self.countdownText.remove()

