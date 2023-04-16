from typing import Dict, Any, Union, List
import time

import viz

from AlexaEngine import State, StateMachine, EventHandler

from Events import FrameUpdateEvent
from GameStates.PlayerStates import Sprinting, Walking
from Bots import PathFollowingBot
from Objects import Collectible

class PlayingGame(State):

    def __init__(self, timerMinutes : int = 5):
        super().__init__()
        self.timerMinutes = timerMinutes
        self.timerSeconds = timerMinutes * 60
        self.timerStartTime = None
        self.timerText = None
            # player states
        sprintTheme = viz.Theme()
        sprintTheme.highBackColor = (0, 1, 0, 1)
        sprintTheme.borderColor = (0, 0, 0, 1)
        sprintTheme.backColor = (0.1, 0.1, 0.1, 0.5)

        exhaustedTheme = viz.Theme()
        exhaustedTheme.highBackColor = (1, 0, 0, 1)
        exhaustedTheme.borderColor = (1, 0, 0, 1)
        exhaustedTheme.backColor = (0.1, 0.1, 0.1, 0.5)

        sprintBar = viz.addProgressBar("")
        sprintBar.setPosition(0.5, 0.05)
        sprintBar.set(0.95)
        sprintBar.setTheme(sprintTheme)
        sprintBar.disable()

        sprintTimeSeconds = 1
        recoveryTimeSeconds = 10
        exhaustionRecoveryPercent = 0.5
        
        playerSprinting = Sprinting(sprintTimeSeconds, sprintBar, sprintTheme, exhaustedTheme)
        playerWalking = Walking(recoveryTimeSeconds, sprintBar, exhaustionRecoveryPercent,sprintTheme, exhaustedTheme)
        self.playerSprintState = StateMachine([(playerWalking, [playerSprinting]), (playerSprinting, [playerWalking])])
        self.frameUpdateEventHandler = EventHandler([self.playerSprintState])
        self.handle = self.frameUpdateEventHandler.callback(self.handle)
        # player movement state

    def positionTimerAtTopCenter(self, node: viz.VizNode) -> None:
        # Get the node's bounding box
        boundingBox = node.getBoundingBox(viz.REL_PARENT)
        width = boundingBox.width
        height = boundingBox.height

        # Calculate the centered position on the x-axis
        xPosition = (1 - width) / 2

        # Set the node's position
        node.setPosition(xPosition, 1 - height, viz.REL_PARENT, viz.REL_PARENT)

    def displayTimer(self):
        minutes = int(self.timerSeconds // 60)
        seconds = round(self.timerSeconds % 60)
        if seconds == 60:
            seconds = 0
            minutes += 1
        self.timerText = viz.addText(f"Time: {minutes}:{seconds:02d}", parent=viz.SCREEN)
        self.timerText.setScale(0.25, 0.25, mode=viz.REL_PARENT)
        self.positionTimerAtTopCenter(self.timerText)

    def updateTimer(self):
        elapsedTime = time.time() - self.timerStartTime
        remainingTime = self.timerSeconds - elapsedTime
        minutes = int(remainingTime // 60)
        seconds = round(remainingTime % 60)
        if seconds == 60:
            seconds = 0
            minutes += 1
        self.timerText.message(f"Time: {minutes}:{seconds:02d}")

    def initialize(self, previousState: Union[None, str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        self.displayTimer()

    def transitionIn(self, previousState: Union[None, str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        self.timerStartTime = time.time()
        PathFollowingBot.start_robots()

    def handle(self, event: FrameUpdateEvent, otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        self.updateTimer()

    def getNextState(self, availableStates: List[str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> Union[str, None]:
        if self.timerSeconds - (time.time() - self.timerStartTime) <= 0:
            return "GameEndedByTimer"
        elif PathFollowingBot.any_robots_caught_player(viz.MainView.getPosition()):
            return "GameEndedByRobot"
        elif Collectible.collectedAllCoins():
            return "GameEndedInVictory"
        else:
            return None

    def transitionOut(self, nextState: str, otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        self.timerText.remove()
        PathFollowingBot.stop_robots()
