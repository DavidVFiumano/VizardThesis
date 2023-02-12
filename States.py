import viz

from AlexaEngine import StateMachine

from GameStates.GlobalGameStates import GameNotStarted, ExperimentSetup
from GameStates.PlayerStates import Sprinting, Walking
from GameStates.InputStates import KeyPressed, KeyReleased

# global game state
gameNotStarted = GameNotStarted()
experimentSetup = ExperimentSetup()

# player states
sprintTheme = viz.Theme()
sprintTheme.highBackColor = (0, 1, 0, 1)
sprintTheme.borderColor = (0, 0, 0, 1)
sprintTheme.backColor = (0.1, 0.1, 0.1, 0.5)

exhaustedTheme = viz.Theme()
exhaustedTheme.highBackColor = (1, 0, 0, 1)
exhaustedTheme.borderColor = (1, 0, 0, 1)
exhaustedTheme.backColor = (0.1, 0.1, 0.1, 0.5)

sprintBar = viz.addProgressBar("")
sprintBar.setPosition(0.5, 0.05)
sprintBar.set(0.95)
sprintBar.setTheme(sprintTheme)
sprintBar.disable()

sprintTimeSeconds = 1
recoveryTimeSeconds = 10
exhaustionRecoveryPercent = 0.5
barFadeSeconds = 2.0

playerSprinting = Sprinting(sprintTimeSeconds, sprintBar,
							sprintTheme, exhaustedTheme)
playerWalking = Walking(recoveryTimeSeconds, sprintBar, 
						exhaustionRecoveryPercent, 
						sprintTheme, exhaustedTheme,
						barFadeSeconds)