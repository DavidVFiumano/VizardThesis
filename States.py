import viz

from StateManagement import StateMachine

from GameStates.GlobalGameStates import GameNotStarted, ExperimentSetup, PlayingGame, GameEndedByRobot, GameEndedByTimer, GameEndedInVictory
from GameStates.InputStates import KeyPressed, KeyReleased

# global game state
gameNotStarted = GameNotStarted()
experimentSetup = ExperimentSetup()
playingGame = PlayingGame(4.5)
gameEndedByRobot = GameEndedByRobot()
gameEndedByTimer = GameEndedByTimer()
gameEndedInVictory = GameEndedInVictory()





						
