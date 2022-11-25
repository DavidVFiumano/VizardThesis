from AlexaEngine import StateMachine

globalGameState = StateMachine([(gameNotStarted, [experimentSetup])
                                (experimentSetup, list())])