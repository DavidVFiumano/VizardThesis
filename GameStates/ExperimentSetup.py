from typing import Dict, Any
from os.path import abspath, join, isdir
from os import makedirs, remove
from glob import glob
import logging

import vizinput

from AlexaEngine import State

from Events import NetworkEvent, FrameUpdateEvent

class ExperimentSetup(State):
    
    # called before the first time this state is transitioned to for the first time
    def initialize(self, previousState : Union[None, str], otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
                
        localState = {
            "UserType" : None,
            "OtherComputer" : None
        }
        self.setLocalState(localState)
        
    # transition in
    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        if self.previousState is not None:
            raise RuntimeError("This is supposed to be the first game state! No state should have been reached before this state.")
        saveDirectory = abspath(vizinput.directory("Select a game save location"))
        self.localState["Role"] = vizinput.choose("What is this user's role?", ["Seeker", "Hider"])
        self.saveDirectory = join(saveDirectory, self.localState["Role"])
        if isdir(self.saveDirectory):
            logging.info(f"Previous Save exists in this directory, deleting {self.saveDirectory}")
            remove(glob(join(self.saveDirectory, "*")))
    
        makedirs()

    # calls the handler
    # takes in global state, has access to the state configuration.
    # has read-only access to other state configurations through the state machine
    def handle(self, event : Any, otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        pass

    # decides whether or not to change the current state
    # returns a State object to change to that State
    # returns None to stay in the current state.
    def getNextState(self, availableStates : List[str], otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> Union[str, None]:
        return None if self.localState["DeterminedRole"] == "Hider" else None # TODO fix