from typing import Dict, Any

import viz

from AlexaEngine import EventHandler

from Events import FrameUpdateEvent, KeyPressEvent, KeyReleaseEvent, logFrameEvent
from Globals import globalGameState
from PlayerMovement import moveMainViewFromKeys
from Inputs import keyStates
from Objects import Collectible
from Bots import PathFollowingBot

frameUpdateHandler = EventHandler([logFrameEvent, globalGameState, Collectible.getCallback(), PathFollowingBot.getCallback(), moveMainViewFromKeys])

keyDownHandler = EventHandler(keyStates)
keyUpHandler = EventHandler(keyStates)

@frameUpdateHandler.callback
def frameDrawCallback() -> FrameUpdateEvent:
    return FrameUpdateEvent(viz.MainView.getPosition()) # TODO get general game state data and return it as an "event"
    
@keyDownHandler.callback
def sprintKeyDownHandler(key):
    return KeyPressEvent(key)
    
@keyUpHandler.callback
def sprintKeyUpHandler(key):
    return KeyReleaseEvent(key)