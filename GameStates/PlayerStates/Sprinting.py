from typing import Dict, Any, Union, List
from time import time

import viz

from StateManagement import State

from PlayerMovement import setSprintingSpeed
from Inputs import sprintKeyState

class Sprinting(State):
    
    def __init__(self, sprintTimeSeconds : float, 
                        sprintBar : viz.VizProgressBar,
                        sprintTheme : viz.Theme,
                        exhaustionTheme : viz.Theme):
        self.sprintTimeSeconds = sprintTimeSeconds
        self.sprintBar = sprintBar
        self.lastFrameTime = None
        self.sprintPercentLossInASecond = 1.0 / float(sprintTimeSeconds)
        self.sprintTheme = sprintTheme
        self.exhaustionTheme = exhaustionTheme
    
    # called when transitioning in to this state
    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        setSprintingSpeed()
        self.lastFrameTime = time()

    # calls the handler
    # takes in global state, has access to the state configuration.
    # has read-only access to other state configurations through the state machine
    def handle(self, event : Any, otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        currentTime = time()
        sprintBarValue = self.sprintBar.get()
        nextSprintBarValue = sprintBarValue - ((currentTime - self.lastFrameTime)*self.sprintPercentLossInASecond)
        nextSprintBarValue = nextSprintBarValue if nextSprintBarValue > 0.0 else 0.0
        
        sprintColor = self.sprintTheme.highBackColor
        exhaustionColor = self.exhaustionTheme.highBackColor
        weightedAverageColor = [((1.0-nextSprintBarValue)*ec) + (nextSprintBarValue*sc) for sc, ec in zip(sprintColor[:-1], exhaustionColor[:-1])]
        weightedAverageColor.append(1) # add alpha
        newTheme = viz.Theme()
        newTheme.borderColor = self.sprintTheme.borderColor
        newTheme.backColor = self.sprintTheme.backColor
        newTheme.highBackColor = tuple(weightedAverageColor)
        self.sprintBar.setTheme(newTheme)
        
        self.sprintBar.set(nextSprintBarValue)
        self.lastFrameTime = currentTime
        

    # decides whether or not to change the current state
    # returns a State object to change to that State
    # returns None to stay in the current state.
    def getNextState(self, availableStates : List[str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> Union[str, None]:
        return availableStates[0] if sprintKeyState.getCurrentState() == "KeyReleased" or self.sprintBar.get() == 0 else None