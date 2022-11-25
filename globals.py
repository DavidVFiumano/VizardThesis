from AlexaEngine import StateMachine

from States import gameNotStarted, experimentSetup

globalGameState = StateMachine([
								(experimentSetup, [gameNotStarted]), # Stage 1
								(gameNotStarted, list()) # Stage 2
								])