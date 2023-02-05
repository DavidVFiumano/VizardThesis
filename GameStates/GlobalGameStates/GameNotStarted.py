﻿from typing import Dict, Any, Union, List

import viz

from AlexaEngine import State

from Events import NetworkEvent, FrameUpdateEvent

class GameNotStarted(State):
    
    # called before the first time this state is transitioned to for the first time
    def initialize(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        
        localState = dict()
        self.setLocalState(localState)
    
    # called when transitioning in to this state
    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        viz.addText("When you're ready to start, press the 'F' key", parent=viz.SCREEN)


    # calls the handler
    # takes in global state, has access to the state configuration.
    # has read-only access to other state configurations through the state machine
    def handle(self, event : Any, otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        if isinstance(event, NetworkEvent):
            sender = event.sender
            address = event.address
            port = event.port
            data = event.data
            kwargs = event.kwargs
            
            # do error checking, make sure no one entered anything wrong before the game starts
        elif isinstance(event, FrameUpdateEvent):
            pass
            #globalValues["TargetMailbox"].send(otherState["ExperimentSetup"])

    # decides whether or not to change the current state
    # returns a State object to change to that State
    # returns None to stay in the current state.
    def getNextState(self, availableStates : List[str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> Union[str, None]:
        return None