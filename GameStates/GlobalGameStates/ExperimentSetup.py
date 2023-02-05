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
from Network import MAILBOX
import Configuration

# this experiment stage exists to make sure we get good configuraiton settings
class ExperimentSetup(State):
    
    # called before the first time this state is transitioned to for the first time
    def initialize(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:

        self.setupComplete = False
        self.networkMachineSpecified = False
        self.targetMachine = None
        self.targetMailbox = None
        self.networkSettingsLock = Lock()
        self.sentStateToSender = False
        self.connectedToOtherMachine = False
        
    # transition in
    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        globalValues["GameState"] = dict()
        globalValues["GameState"]["PlayerPosition"] = {
            "Position" : viz.MainView.getPosition(),
            "Attitude" : viz.MainView.getQuat()
        }

    def _setNetworkTargets(self, targetMachine : str) -> bool:
        with self.networkSettingsLock:
            #Add a mailbox from which to send messages. This is your outbox.
            targetMailbox = viz.addNetwork(targetMachine)
            #if not targetMailbox.valid:
            #    return False
            
            self.targetMachine = targetMachine
            self.targetMailbox = targetMailbox
            self.networkMachineSpecified = True
            return True

    def _sendToNetworkTarget(self, *args, **kwargs):
        with self.networkSettingsLock:
            self.targetMailbox.send(*args, **kwargs)
            
    def _messageIsConnectionACK(self, event : NetworkEvent) -> bool:
        return len(event.kwargs.keys()) == 0 and len(event.data) == 0
            
    def _otherConfigIsCompatible(self, otherConfig : State.LOCAL_STATE_TYPE) -> bool:
        print(otherConfig)
        otherRole = otherConfig["Role"]
        return otherRole == "Seeker" if Configuration.PLAYER_ROLE == "Hider" else otherRole == "Hider"

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
                
                Configuration.PLAYER_ROLE = role
                Configuration.SAVE_DIRECTORY = saveDirectory
                
                makedirs(saveDirectory, exist_ok=True)
                self.setupComplete = True
            
            if not self.networkMachineSpecified:
                targetMachine = vizinput.input('Enter the address of the other machine')
                if self._setNetworkTargets(targetMachine):
                    self.networkMachineSpecified = True
            
            if self.networkMachineSpecified:
                self._sendToNetworkTarget(Configuration.getConfiguration())
            
        elif isinstance(event, NetworkEvent) and self.setupComplete and self.networkMachineSpecified:
            targetMachine = self.targetMachine
            sender = event.sender
            ans = 0
            if targetMachine is None:
                ans = vizinput.ask(f"Machine {sender} is attempting to connect but isn't the sender you selected ({targetMachine}). Do you want to connect to this comptuer instead?")
            elif targetMachine != sender:
                ans = vizinput.ask(f"Machine {sender} is attempting to connect but isn't the sender you selected ({targetMachine}). Do you want to connect to this comptuer instead?")
                
            if ans:
                if self._setNetworkTargets(targetMachine):
                    return # in the case that this fails, return and try again next time they send a packet
            else:
                ans = vizinput.ask(f"Would you like to reselect the machine you're connecting to?")
                if ans:
                    self.networkMachineSpecified = False
                    return
            
            if not self._messageIsConnectionACK(event):
                otherConfig = event.kwargs
                if not self._otherConfigIsCompatible(otherConfig):
                    ans = vizinput.ask(f"The other player has an incompatible configuration, both players have the same roles. This computer's role is {Configuration.PLAYER_ROLE}, is that correct? If yes, reconfigure the other computer.")
                    if not ans:
                        self.setupComplete = False
                    else:
                        return
                else:
                    self._sendToNetworkTarget()
            else:
                self.connectedToOtherMachine = True
                self._sendToNetworkTarget()
            
            
    
    # called after the getNextState if the state has changed.
    # if this state has been transitioned to before, the localState will be the same as the previous time transitionOut was called.
    def transitionOut(self, nextState : str, otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        viz.mouse.setTrap(viz.ON)
        viz.mouse.setVisible(viz.OFF)
        MAILBOX = self.targetMailbox
            
                
    # decides whether or not to change the current state
    # returns a State object to change to that State
    # returns None to stay in the current state.
    def getNextState(self, availableStates : List[str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> Union[str, None]:
        return "GameNotStarted" if self.setupComplete and self.connectedToOtherMachine else None