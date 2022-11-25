from typing import Dict, Any

import viz

from AlexaEngine import State

from Events import NetworkEvent, FrameUpdateEvent

class GameNotStarted(State):
    
    # called before the first time this state is transitioned to for the first time
    def initialize(self, previousState : Union[None, str], otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        
        localState = {
            "DeterminedRole" : None
        }
        self.setLocalState(localState)
    
    # called when transitioning in to this state
    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        if previousState is None or previousState != "ExperimentSetup":
            raise RuntimeError("This is supposed to be the first game state! No state should have been reached before this state.")
        self.localState["DeterminedRole"] = vizinput.choose("What is this user's role?", ["Seeker", "Hider"])

    # calls the handler
    # takes in global state, has access to the state configuration.
    # has read-only access to other state configurations through the state machine
    def handle(self, event : Any, otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        #if isinstance(event, NetworkEvent):
        #    sender = event.sender
        #    address = event.address
        #    port = event.port
        #    data = event.data
        #    kwargs = event.kwargs
            
        #    self.localState["DeterminedRole"] = "Hider" if "Role" in kwargs.keys() and kwargs["Role"] == "Seeker" else "Seeker"
        pass

    # decides whether or not to change the current state
    # returns a State object to change to that State
    # returns None to stay in the current state.
    def getNextState(self, availableStates : List[str], otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> Union[str, None]:
        return None