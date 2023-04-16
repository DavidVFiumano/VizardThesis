import viz

from AlexaEngine import StateMachine

from States import gameNotStarted, experimentSetup, playingGame, gameEndedByRobot, gameEndedByTimer, gameEndedInVictory

# global game state
globalGameState = StateMachine([
								(experimentSetup, [gameNotStarted]),
								(gameNotStarted, [playingGame]),
								(playingGame, [gameEndedByRobot, gameEndedByTimer, gameEndedInVictory]),
								(gameEndedByRobot, list()),
								(gameEndedByTimer, list()),
								(gameEndedInVictory, list())
								])
								