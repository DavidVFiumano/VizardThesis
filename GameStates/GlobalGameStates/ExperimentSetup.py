from typing import Dict, Any, Union, List
from os.path import abspath, join, isdir
from os import makedirs, listdir
from shutil import rmtree
from threading import Lock
import logging

import vizinput
import viz

from AlexaEngine import State

from Events import NetworkEvent, FrameUpdateEvent
import Configuration

# this experiment stage exists to make sure we get good configuraiton settings
class ExperimentSetup(State):
    
    # called before the first time this state is transitioned to for the first time
    def initialize(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        self.setupComplete = False

        
    # transition in
    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        globalValues["GameState"] = dict()
        globalValues["GameState"]["PlayerPosition"] = {
            "Position" : viz.MainView.getPosition(),
            "Attitude" : viz.MainView.getQuat()
        }

    # calls the handler
    # takes in global state, has access to the state configuration.
    # has read-only access to other state configurations through the state machine
    def handle(self, event : Any, otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        if isinstance(event, FrameUpdateEvent):
            if not self.setupComplete:
                saveDirectory = vizinput.directory(prompt="Select a game save location", directory="C:")
                if len(saveDirectory.strip()) == 0: # if the user clicks cancel.
                    viz.quit()
                    return
                    
                saveDirectory = abspath(saveDirectory)

                if isdir(saveDirectory) and len(listdir(saveDirectory)) > 0:
                    vizinput.message("Selected directory exists and isn't empty, select another directory.")
                    return # don't allow anything to progress if we don't have a save directory.
                
                Configuration.SAVE_DIRECTORY = saveDirectory
                
                makedirs(saveDirectory, exist_ok=True)
                self.setupComplete = True
            
    
    # called after the getNextState if the state has changed.
    # if this state has been transitioned to before, the localState will be the same as the previous time transitionOut was called.
    def transitionOut(self, nextState : str, otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        pass
                
    # decides whether or not to change the current state
    # returns a State object to change to that State
    # returns None to stay in the current state.
    def getNextState(self, availableStates : List[str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> Union[str, None]:
        return "GameNotStarted" if self.setupComplete else None