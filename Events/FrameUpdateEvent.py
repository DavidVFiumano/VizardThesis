from typing import Tuple, List
from datetime import datetime

import viz
import vizmat

from .VizardEvent import VizardEvent
from LoggerFactory import LoggerFactory, CSVFormatter, LoggerNotInitializedError
from PlayerMovement import isSprinting
from Bots import Bot

frameLoggerFormatter = CSVFormatter(fieldnames=["FrameNumber", "Time", "Sprinting", "TimeEllapsedSinceLastFrame", "EffectiveInstantaneousFrameRate",
                                                "PlayerPositionX", "PlayerPositionY", "PlayerPositionZ", 
                                                "PlayerVelocityX", "PlayerVelocityY", "PlayerVelocityZ",
                                                "PlayerQuat1", "PlayerQuat2", "PlayerQuat3", "PlayerQuat4",
                                                "PlayerCanSeeRobot"])

class FrameUpdateEvent(VizardEvent):
    PlayerPosition : List[float] = viz.MainView.getPosition()
    LastPosition : List[float] = viz.MainView.getPosition()
    PlayerVelocity : List[float] = [0.0, 0.0, 0.0]
    PlayerQuat : List[float] = viz.MainView.getQuat()
    FrameNumber : int = 0
    
    @staticmethod
    def quat_to_mat(quat: Tuple[float, float, float, float]) -> viz.Matrix:
        x = quat[0]
        y = quat[1]
        z = quat[2]
        w = quat[3]

        xx = x * x
        xy = x * y
        xz = x * z
        xw = x * w

        yy = y * y
        yz = y * z
        yw = y * w

        zz = z * z
        zw = z * w

        mat = viz.Matrix()
        mat.set(
            [
                1 - 2 * (yy + zz), 2 * (xy - zw), 2 * (xz + yw), 0,
                2 * (xy + zw), 1 - 2 * (xx + zz), 2 * (yz - xw), 0,
                2 * (xz - yw), 2 * (yz + xw), 1 - 2 * (xx + yy), 0,
                0, 0, 0, 1,
            ]
        )

        return mat
    
    def robot_is_visible_to_player(self, forward_vector = viz.Vector(0, 0, -1)) -> bool:
        """Check if the player can see the robot"""
        """ASPECT_RATIO = 16/9
        FOV = 60*ASPECT_RATIO
        first_bot_pos = Bot.BotList[0].avatar.getPosition()
        unobstructed_view = not viz.intersect(self.PlayerPosition, first_bot_pos).valid

        forward_direction = forward_vector * type(self).quat_to_mat(self.PlayerQuat)
        direction_to_point = viz.Vector(first_bot_pos) - self.PlayerPosition

        forward_direction.normalize()
        direction_to_point.normalize()

        angle_between = vizmat.AngleBetweenVector(direction_to_point, forward_direction)

        within_fov = (angle_between <= FOV / 2)
        return within_fov & unobstructed_view"""
        # Given a world position as a point
        (x, y, z) = Bot.BotList[0].avatar.getPosition()
        first_bot_pos = viz.Vector(x, y, z)

        x, y, distance = viz.MainWindow.worldToScreen(x, y, z)

        is_on_screen = (0.0 < x) and (x < 1.0) and (0.0 < y) and (y < 1.0) and distance >= 0.0
            
        unobstructed_view = not viz.intersect(self.PlayerPosition, first_bot_pos).valid
        
        return is_on_screen and unobstructed_view
    
    def __init__(self, playerPosition : Tuple[float, float, float], playerQuat : Tuple[float,float,float,float]):
        type(self).FrameNumber += 1
        type(self).LastPosition = type(self).PlayerPosition
        type(self).PlayerPosition = playerPosition
        type(self).PlayerVelocity = [last - current for last, current in zip(type(self).LastPosition, type(self).PlayerPosition)]
        type(self).PlayerQuat = playerQuat
        
def logFrameEvent(frame : FrameUpdateEvent):
    try:
        frameLogger = LoggerFactory.getLogger(name="FrameUpdateLogger", formatter=frameLoggerFormatter, file="FrameLog.csv")
    except LoggerNotInitializedError:
        return
    x, y, z = tuple(frame.PlayerPosition)
    dx, dy, dz = tuple(frame.PlayerVelocity)
    quat1, quat2, quat3, quat4 = tuple(frame.PlayerQuat)
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
        "PlayerVelocityZ" : dz,
        "PlayerQuat1" : quat1,
        "PlayerQuat2" : quat2,
        "PlayerQuat3" : quat3,
        "PlayerQuat4" : quat4,
        "PlayerCanSeeRobot" : frame.robot_is_visible_to_player()
    }
    
    frameLogger.info("", extra=eventLog)