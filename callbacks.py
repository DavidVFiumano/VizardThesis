from typing import Dict, Any

import viz

from AlexaEngine import EventHandler

networkHandler = EventHandler([])
frameUpdateHandler = EventHandler([])

@networkHandler.callback
def networkCallback(event : viz.Event) -> Dict[str, Any]:
    return event[2]

@frameUpdateHandler.callback()
def frameDrawCallback() -> Dict[str, Any]:
    pass # TODO get general game state data and return it as an "event"