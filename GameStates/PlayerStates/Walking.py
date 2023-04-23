from typing import Dict, Any, Union, List
from time import time

import viz
import vizact

from StateManagement import State

from PlayerMovement import setWalkingSpeed
from Inputs import sprintKeyState

class Walking(State):
    
    def __init__(self, recoveryTimeSeconds : float, 
                       sprintBar : viz.VizProgressBar, 
                       exhaustionRecoveryPercent : float, 
                       sprintTheme : viz.Theme, 
                       exhaustionTheme : viz.Theme):
        self.recoveryTimeSeconds = recoveryTimeSeconds
        self.sprintBar = sprintBar
        self.lastFrameTime = None
        self.sprintPercentRecoveryInASecond = 1.0 / float(recoveryTimeSeconds)
        self.exhaustionRecoveryPercent = exhaustionRecoveryPercent
        self.exhausted = False
        self.exhaustionTheme = exhaustionTheme
        self.sprintTheme = sprintTheme
        
    def initialize(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        self.sprintBar.set(1)
        self.sprintBar.setTheme(self.sprintTheme)
    
    # called when transitioning in to this state
    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        setWalkingSpeed()
        sprintBarStart = self.sprintBar.get()
        if sprintBarStart == 0.0:
            self.exhausted = True
            self.sprintBar.setTheme(self.exhaustionTheme)
        self.lastFrameTime = time()

    # calls the handler
    # takes in global state, has access to the state configuration.
    # has read-only access to other state configurations through the state machine
    def handle(self, event : Any, otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        currentTime = time()
        timeElapsed = currentTime - self.lastFrameTime
        sprintBarValue = self.sprintBar.get()
        nextSprintBarValue = sprintBarValue + (timeElapsed*self.sprintPercentRecoveryInASecond)
        nextSprintBarValue = nextSprintBarValue if nextSprintBarValue < 1.0 else 1.0
                
        if self.exhausted:
            self.exhausted = False if self.sprintBar.get() > self.exhaustionRecoveryPercent else True
            if not self.exhausted:
                self.sprintBar.setTheme(self.sprintTheme)
        else:
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
        return availableStates[0] if sprintKeyState.getCurrentState() == "KeyPressed" and not self.exhausted else None # TODO place timelimit