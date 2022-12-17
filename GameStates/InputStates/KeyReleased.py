from typing import Dict, Any, Union, List

from AlexaEngine import State

from Events import KeyPressEvent, KeyReleaseEvent

class KeyReleased(State):
	
	def __init__(self, keys : Union[str, List[str]]):
		self.keys = [keys] if isinstance(keys, str) else keys
		self.transitionToKeyPressed = False
	
	# calls the handler
	# takes in global state, has access to the state configuration.
	# has read-only access to other state configurations through the state machine
	def handle(self, event : Any, otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
		if not isinstance(event, KeyReleaseEvent) and not isinstance(event, KeyPressEvent):
			self.transitionToKeyPressed = False
			return
			
		if event.key in self.keys and isinstance(event, KeyPressEvent):
			self.transitionToKeyPressed = True
		else:
			self.transitionToKeyPressed = False

	def getNextState(self, availableStates : List[str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> Union[str, None]:
		return availableStates[0] if self.transitionToKeyPressed else None