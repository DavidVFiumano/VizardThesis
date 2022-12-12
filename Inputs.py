import viz

from AlexaEngine import StateMachine

from GameStates.InputStates import KeyPressed, KeyReleased

def makeStateMachineForKeyPress(key : str) -> StateMachine:
	pressedState = KeyPressed(key)
	releasedState = KeyReleased(key)
	
	machine = StateMachine([
							(releasedState, [pressedState]),
							(pressedState, [releasedState])
							])
	
	return machine

# key states
sprintKeyState = makeStateMachineForKeyPress(viz.KEY_SHIFT_L)

keyStates = [sprintKeyState]