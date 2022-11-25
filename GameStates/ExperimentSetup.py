from typing import Dict, Any, Union, List
from os.path import abspath, join, isdir
from os import makedirs, listdir
from shutil import rmtree
import logging

import vizinput
import viz

from AlexaEngine import State

from Events import NetworkEvent, FrameUpdateEvent
from GlobalGameLog import globalGameState, globalGameStateHistory
from Events import NetworkEvent, FrameUpdateEvent

class ExperimentSetup(State):
    
    # called before the first time this state is transitioned to for the first time
    def initialize(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
                
        localState = {
            "UserType" : None,
            "OtherComputer" : None
        }
        self.setLocalState(localState)
        self.setupComplete = False
        self.networkMachineSpecified = False
        self.targetMachine = None
        self.targetMailbox = None
        
    # transition in
    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        pass

    def _setNetworkTargets(self, targetMachine : str, globalValues : Dict[str, Any]) -> bool:
        #Add a mailbox from which to send messages. This is your outbox.
        targetMailbox = viz.addNetwork(targetMachine)
        if not targetMailbox.valid:
            return False
        
        self.targetMachine = targetMachine
        self.targetMailbox = targetMailbox
        self.networkMachineSpecified = True
        globalValues["TargetMailbox"] = targetMailbox
        return True

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
                roles = ["Seeker", "Hider"]
                role = roles[vizinput.choose("What type of player is this user?", roles)]
                saveDirectory = join(saveDirectory, role)
                
                if isdir(saveDirectory) and len(listdir(saveDirectory)) > 0:
                    vizinput.message("Selected directory exists and isn't empty, select another directory.")
                    return # don't allow anything to progress if we don't have a save directory.
                
                globalGameState["Role"] = role
                globalValues["SaveDirectory"] = saveDirectory
                
                makedirs(saveDirectory, exist_ok=True)
                self.setupComplete = True
            
            if not self.networkMachineSpecified:
                targetMachine = vizinput.input('Enter the address of the other machine')
                if self._setNetworkTargets(targetMachine, globalValues):
                    self.networkMachineSpecified = True
                
    # decides whether or not to change the current state
    # returns a State object to change to that State
    # returns None to stay in the current state.
    def getNextState(self, availableStates : List[str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> Union[str, None]:
        return "GameNotStarted" if self.setupComplete and self.networkMachineSpecified else None