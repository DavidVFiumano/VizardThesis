from typing import Dict, Any

import viz

from AlexaEngine import EventHandler

from Events import NetworkEvent, FrameUpdateEvent
from Globals import globalGameState

networkHandler = EventHandler([globalGameState])
frameUpdateHandler = EventHandler([globalGameState])

@networkHandler.callback
def networkCallback(event : viz.NetworkEvent) -> NetworkEvent:
    return NetworkEvent(event)

@frameUpdateHandler.callback
def frameDrawCallback() -> FrameUpdateEvent:
    return FrameUpdateEvent() # TODO get general game state data and return it as an "event"