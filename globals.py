import viz

from AlexaEngine import StateMachine

from States import gameNotStarted, experimentSetup, playerSprinting, playerWalking

# global game state
globalGameState = StateMachine([
								(experimentSetup, [gameNotStarted]), # Stage 1
								(gameNotStarted, list()) # Stage 2
								])
								
# player movement state
playerSprintState = StateMachine([
									(playerWalking, [playerSprinting]),
									(playerSprinting, [playerWalking])
									])