from AlexaEngine import StateMachine

from GameStates import GameNotStarted

# state machines
gameNotStarted = GameNotStarted()
gameStages = StateMachine((gameNotStarted, list()))