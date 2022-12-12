import viz

from AlexaEngine import StateMachine

from GameStates.GlobalGameStates import GameNotStarted, ExperimentSetup
from GameStates.PlayerStates import Sprinting, Walking
from GameStates.InputStates import KeyPressed, KeyReleased

# global game state
gameNotStarted = GameNotStarted()
experimentSetup = ExperimentSetup()

# player states
playerSprinting = Sprinting()
playerWalking = Walking()