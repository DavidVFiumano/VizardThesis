from typing import Dict, Any

import viz

from AlexaEngine import EventHandler

from Events import NetworkEvent, FrameUpdateEvent, KeyPressEvent, KeyReleaseEvent
from Globals import globalGameState, playerSprintState
from PlayerMovement import moveMainViewFromKeys
from Inputs import keyStates
from Objects import Collectible
from Bots.Bot import Bot

frameUpdateHandler = EventHandler([globalGameState, playerSprintState, Collectible.getCallback(), Bot.getCallback(), moveMainViewFromKeys])

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