from typing import Dict, Any

import viz

from AlexaEngine import EventHandler

from Events import NetworkEvent, FrameUpdateEvent, KeyPressEvent, KeyReleaseEvent
from Globals import globalGameState, playerSprintState
from Inputs import keyStates
from Objects import Collectible

networkHandler = EventHandler([globalGameState, Collectible.getCallback()])
frameUpdateHandler = EventHandler([globalGameState, playerSprintState, Collectible.getCallback()])

keyDownHandler = EventHandler(keyStates)
keyUpHandler = EventHandler(keyStates)

@networkHandler.callback
def networkCallback(event : viz.NetworkEvent) -> NetworkEvent:
    return NetworkEvent(event)

@frameUpdateHandler.callback
def frameDrawCallback() -> FrameUpdateEvent:
    return FrameUpdateEvent() # TODO get general game state data and return it as an "event"
    
@keyDownHandler.callback
def sprintKeyDownHandler(key):
    return KeyPressEvent(key)
    
@keyUpHandler.callback
def sprintKeyUpHandler(key):
    return KeyReleaseEvent(key)