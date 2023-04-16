from typing import Tuple, List
from datetime import datetime

import viz

from .VizardEvent import VizardEvent
from LoggerFactory import LoggerFactory, CSVFormatter, LoggerNotInitializedError
from PlayerMovement import isSprinting

frameLoggerFormatter = CSVFormatter(fieldnames=["FrameNumber", "Time", "Sprinting", "TimeEllapsedSinceLastFrame", "EffectiveInstantaneousFrameRate",
                                                "PlayerPositionX", "PlayerPositionY", "PlayerPositionZ", 
                                                "PlayerVelocityX", "PlayerVelocityY", "PlayerVelocityZ"])

class FrameUpdateEvent(VizardEvent):
    PlayerPosition : List[float] = viz.MainView.getPosition()
    LastPosition : List[float] = viz.MainView.getPosition()
    PlayerVelocity : List[float] = [0.0, 0.0, 0.0]
    FrameNumber : int = 0
    
    def __init__(self, playerPosition : Tuple[float, float, float]):
        type(self).FrameNumber += 1
        type(self).LastPosition = type(self).PlayerPosition
        type(self).PlayerPosition = playerPosition
        type(self).PlayerVelocity = [last - current for last, current in zip(type(self).LastPosition, type(self).PlayerPosition)]
        
def logFrameEvent(frame : FrameUpdateEvent):
    try:
        frameLogger = LoggerFactory.getLogger(name="FrameUpdateLogger", formatter=frameLoggerFormatter, file="FrameLog.csv")
    except LoggerNotInitializedError:
        return
    x, y, z = tuple(frame.PlayerPosition)
    dx, dy, dz = tuple(frame.PlayerVelocity)
    frameNumber = frame.FrameNumber
    frameTime = viz.getFrameElapsed()
    
    eventLog = {
        "FrameNumber" : frameNumber,
        "Time" : datetime.now().strftime("%d/%m/%YT%H:%M:%S.%f"),
        "Sprinting" : isSprinting(),
        "TimeEllapsedSinceLastFrame" : frameTime,
        "EffectiveInstantaneousFrameRate" : 1 / frameTime, 
        "PlayerPositionX" : x,
        "PlayerPositionY" : y,
        "PlayerPositionZ" : z,
        "PlayerVelocityX" : dx,
        "PlayerVelocityY" : dy,
        "PlayerVelocityZ" : dz
    }
    
    frameLogger.info("", extra=eventLog)