﻿from typing import List, Tuple, Union, Dict, Any, Callable
from logging import LogRecord, Logger, INFO
from os.path import abspath
import math

import viz
import vizmat

from AlexaEngine import State, StateMachine, EventHandler
from Events import FrameUpdateEvent
from LoggerFactory import LoggerFactory, LoggerNotInitializedError, CSVFormatter

from .. import Bot

# GPT-4 wrote this code (mostly). Editted by David Fiumano
loggerName = "PathFollowerLogger"
csvFormatter = CSVFormatter(fieldnames=["FrameNumber", "BotName", "CurrentState", "NextState", "BotX", "BotY", "BotZ", "PlayerX", "PlayerY", "PlayerZ", "DistanceToPlayer", "CanSeePlayer", "CanHearPlayer", "IsObstructed"])

def logTransition(stateTransitionLogger : Logger, frameNumber : int, botName : str, currentState : str, nextState : str, 
                            botPosition : Tuple[float, float, float], playerPosition : Tuple[float, float, float], 
                            canSeePlayer : bool, canHearPlayer : bool, isObstructed : bool):
    
    botX = botPosition[0]
    botY = botPosition[1]
    botZ = botPosition[2]
    playerX = playerPosition[0]
    playerY = playerPosition[1]
    playerZ = playerPosition[2]
    
    fieldValues = {
        "FrameNumber" : frameNumber,
        "BotName" : botName,
        "CurrentState" : currentState,
        "NextState" : nextState,
        "BotX" : botX,
        "BotY" : botY,
        "BotZ" : botZ,
        "PlayerX" : playerX,
        "PlayerY" : playerY,
        "PlayerZ" : playerZ,
        "DistanceToPlayer" : math.sqrt(sum((x2 - x1)**2 for x1, x2 in zip(botPosition, playerPosition))),
        "CanSeePlayer" : canSeePlayer,
        "CanHearPlayer" : canHearPlayer,
        "IsObstructed" : isObstructed
    }
    stateTransitionLogger.info("", extra=fieldValues)

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

class FollowPathState(State):

    def initialize(self, previousState: Union[None, str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        self.localState["path_index"] = 0

    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        self.localState["transition_in_theme"](globalValues["bot"])

    def handle(self, event: FrameUpdateEvent, otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> None:
        bot = globalValues["bot"]
        path = globalValues["path"]
        path_index = self.localState["path_index"]
        self.player_position = event.PlayerPosition
        self.frame_number = event.FrameNumber

        if path_index < len(path):
            target_pos = path[path_index]
            bot.move_towards(target_pos)
            bot.look_at(target_pos)

            if bot.is_at_position(target_pos):
                self.localState["path_index"] += 1
        else:
            self.localState["path_index"] = 0

    def getNextState(self, availableStates: List[str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> Union[str, None]:
        player_position = self.player_position
        hearing_range = self.localState["hearing_range"]
        visual_range = self.localState["vision_range"]
        fov = self.localState["vision_fov"]
        bot = globalValues["bot"]

        can_hear_player = bot.can_hear_point(player_position, hearing_range)
        has_unobstructed_view = bot.has_unobstructed_view(player_position)
        can_see_player = bot.can_see_point(player_position, fov, visual_range)

        try:
            stateTransitionLogger = LoggerFactory.getLogger(loggerName, formatter=csvFormatter, file="PathFollowerBotsLog.csv")
        except LoggerNotInitializedError:
            return None
            
        if can_hear_player or (has_unobstructed_view and can_see_player):
            logTransition(stateTransitionLogger, self.frame_number, bot.name,
                            "FollowPathState", "ChasePlayerState", 
                            bot.get_position(), player_position,
                            can_see_player, can_hear_player, not has_unobstructed_view)
            return "ChasePlayerState"

        return None


class ChasePlayerState(State):

    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        self.localState["transition_in_theme"](globalValues["bot"])

    def handle(self, event: FrameUpdateEvent, otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        bot = globalValues["bot"]
        player_position = event.PlayerPosition
        self.playerPosition = player_position
        self.frame_number = event.FrameNumber
        globalValues["last_known_player_position"] = self.playerPosition
        bot.move_towards(player_position)
        bot.look_at(self.playerPosition)

    def getNextState(self, availableStates: List[str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> Union[str, None]:
        player_position = self.playerPosition
        hearing_range = self.localState["hearing_range"]
        visual_range = self.localState["vision_range"]
        fov = self.localState["vision_fov"]
        bot = globalValues["bot"]
        
        can_hear_player = bot.can_hear_point(player_position, hearing_range)
        has_unobstructed_view = bot.has_unobstructed_view(player_position)
        can_see_player = bot.can_see_point(player_position, fov, visual_range)
        
        try:
            stateTransitionLogger = LoggerFactory.getLogger(loggerName, formatter=csvFormatter, file="PathFollowerBotsLog.csv")
        except LoggerNotInitializedError:
            return None
            
        if not(can_hear_player or (has_unobstructed_view and can_see_player)):
            logTransition(stateTransitionLogger, self.frame_number, bot.name, 
                            "ChasePlayerState", "LookForPlayerState", 
                            bot.get_position(), player_position,
                            can_see_player, can_hear_player, not has_unobstructed_view)
            return "LookForPlayerState"

        return None
        
class LookForPlayerState(State):

    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        self.localState["transition_in_theme"](globalValues["bot"])
        self.localState["bot_still_looking"] = True

    def handle(self, event: FrameUpdateEvent, otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        bot = globalValues["bot"]
        self.frame_number = event.FrameNumber
        last_known_pos = globalValues["last_known_player_position"]
        if bot.is_at_position(last_known_pos):
            self.localState["bot_still_looking"] = bot.look_around(5, 135, 5)
        else:
            bot.move_towards(last_known_pos)
            self.localState["bot_still_looking"]

    def getNextState(self, availableStates: List[str], otherStates: Dict[str, State.LOCAL_STATE_TYPE], globalValues: Dict[str, Any]) -> Union[str, None]:
        player_position = viz.MainView.getPosition() # to check if we can see the player even though we don't 'know' where the player is
        hearing_range = self.localState["hearing_range"]
        visual_range = self.localState["vision_range"]
        fov = self.localState["vision_fov"]
        bot = globalValues["bot"]
        
        can_hear_player = bot.can_hear_point(player_position, hearing_range)
        has_unobstructed_view = bot.has_unobstructed_view(player_position)
        can_see_player = bot.can_see_point(player_position, fov, visual_range)
        
        try:
            stateTransitionLogger = LoggerFactory.getLogger(loggerName, formatter=csvFormatter, file="PathFollowerBotsLog.csv")
        except LoggerNotInitializedError:
            return None
            
        if can_hear_player or (has_unobstructed_view and can_see_player):
            logTransition(stateTransitionLogger, self.frame_number, bot.name,
                            "LookForPlayerState", "ChasePlayerState", 
                            bot.get_position(), player_position,
                            can_see_player, can_hear_player, not has_unobstructed_view)
            return "ChasePlayerState"
        elif not self.localState["bot_still_looking"]:
            logTransition(stateTransitionLogger, self.frame_number, bot.name,
                            "LookForPlayerState", "FollowPathState", 
                            bot.get_position(), player_position,
                            can_see_player, can_hear_player, not has_unobstructed_view)
            return "FollowPathState"
            
        return None
        
    # called after the getNextState if the state has changed.
    # if this state has been transitioned to before, the localState will be the same as the previous time transitionOut was called.
    def transitionOut(self, nextState : str, otherStates : Dict[str, State.LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        bot = globalValues["bot"]
        bot.reset_look_around_time()


class PathFollowingBot(Bot):
    BotList : List["PathFollowingBot"] = list()
    
    def __init__(self, name : str, avatar: viz.VizNode, path: List[Tuple[float, float, float]], 
                        catch_distance : float = 1.25,
                        speed: float = 1.25, turn_duration: float = 0.25, 
                        passive_hearing_range: float = 5.0, chasing_hearing_range : float = 7.5,
                        passive_fov_degrees : float = 60, chasing_fov_degrees : float = 75, 
                        passive_vision_distance : float = 7.5, chasing_vision_distance : float = 12.5,
                        change_node_theme_to_chase_mode : Callable[[viz.VizNode],None] = lambda x : None,
                        change_node_theme_to_walk_mode : Callable[[viz.VizNode],None] = lambda x : None,
                        change_node_theme_to_alert_mode : Callable[[viz.VizNode],None] = lambda x : None):
        start_position = path[0]
        facing_direction = viz.Vector(path[1]) - viz.Vector(path[0])
        start_quat = vizmat.LookToQuat(facing_direction)

        super().__init__(avatar, start_position, start_quat)
        
        self.name = name
        self.path = path
        self.speed = speed
        self.turn_duration = turn_duration
        self.current_target = 1
        self.orientation_progress = 0.0
        self.current_quat = start_quat
        self.target_quat = start_quat
        self.catch_distance = catch_distance
        self.started = False

        follow_path_state = FollowPathState()
        follow_path_state.setLocalState({"path": path, 
                                         "hearing_range": passive_hearing_range,
                                         "vision_range" : passive_vision_distance,
                                         "vision_fov" : passive_fov_degrees,
                                         "transition_in_theme" : change_node_theme_to_walk_mode})

        chase_player_state = ChasePlayerState()
        chase_player_state.setLocalState({"hearing_range" : chasing_hearing_range,
                                            "vision_range" : chasing_vision_distance,
                                            "vision_fov" : chasing_fov_degrees,
                                            "transition_in_theme" : change_node_theme_to_chase_mode})
                                            
        look_for_player_state = LookForPlayerState()
        look_for_player_state.setLocalState({"hearing_range" : chasing_hearing_range,
                                            "vision_range" : chasing_vision_distance,
                                            "vision_fov" : chasing_fov_degrees,
                                            "transition_in_theme" : change_node_theme_to_alert_mode})
        

        state_machine = StateMachine([(follow_path_state, [chase_player_state]), 
                                        (chase_player_state, [follow_path_state, look_for_player_state]),
                                        (look_for_player_state, [follow_path_state, chase_player_state])])
        state_machine.setStartingState(follow_path_state.getName())
        state_machine.setGlobalValue('bot', self)
        state_machine.setGlobalValue('path', path)
        state_machine.setGlobalValue('last_known_player_position', None)
        
        self.look_around_timer = 0.0
        self.look_around_base_angle = 0.0

        self.state_machine = state_machine
        
        type(self).BotList.append(self)

    def start(self):
        self.frameCallback = EventHandler([self.state_machine]).callback(self.frameCallback)
        self.started = True
    
    def stop(self):
        del self.frameCallback
        self.frameCallback = None
        self.started = False
        

    def move_towards(self, target: Tuple[float, float, float]):
        current_position = self.avatar.getPosition()
        direction = viz.Vector(target) - current_position
        distance = direction.length()

        if distance < self.speed * viz.getFrameElapsed():
            self.avatar.setPosition(target)
            return True

        direction.normalize()
        direction *= self.speed * viz.getFrameElapsed()
        new_position = current_position + direction
        self.avatar.setPosition(new_position)
        return False

    def is_at_position(self, target: Tuple[float, float, float]) -> bool:
        current_position = self.avatar.getPosition()
        return vizmat.Distance(current_position, target) < self.speed * viz.getFrameElapsed()
    
    def get_position(self) -> Tuple[float, float, float]:
        return self.avatar.getPosition()

    def distance_to(self, target: Tuple[float, float, float]) -> float:
        current_position = self.avatar.getPosition()
        return vizmat.Distance(current_position, target)
        
    def look_at(self, target: Tuple[float, float, float]):
        current_position = self.avatar.getPosition()
        direction = viz.Vector(target) - current_position
        self.target_quat = vizmat.LookToQuat(direction)
        self.current_quat = self.avatar.getQuat()
        self.orientation_progress = 0.0
        
    def has_unobstructed_view(self, target: Tuple[float, float, float]) -> bool:
        result = viz.intersect(self.avatar.getPosition(), target)
        return not result.valid
        
    def can_hear_point(self, point : Tuple[float, float, float], maxHearingDistance : float) -> bool:
        if self.has_unobstructed_view(point):
            return self.distance_to(point) < maxHearingDistance
        else:
            return self.distance_to(point) < 0.5*maxHearingDistance
        
    def can_see_point(self, point: Tuple[float, float, float], fov: float, maxDistance: float) -> bool:
        if self.distance_to(point) > maxDistance:
            return False
        
        current_position = self.avatar.getPosition()
        current_quat = self.avatar.getQuat()

        forward_direction = viz.Vector(0, 0, -1) * quat_to_mat(current_quat)
        direction_to_point = viz.Vector(point) - current_position

        forward_direction.normalize()
        direction_to_point.normalize()

        angle_between = vizmat.AngleBetweenVector(forward_direction, direction_to_point)

        if angle_between <= fov / 2:
            return True

        return False
    
    def reset_look_around_time(self):
        self.look_around_timer = 0
    
    def look_around(self, speed: float, amplitude: float, time : float) -> bool:
        if self.look_around_timer > time:
            self.reset_look_around_time()
            return False
        current_euler = self.avatar.getEuler()
        self.look_around_timer += viz.getFrameElapsed()
        new_angle = self.look_around_base_angle + amplitude * math.sin(speed * self.look_around_timer)
        self.avatar.setEuler([new_angle, current_euler[1], current_euler[2]])
        return True
        
    def caught_player(self, player_position : Tuple[float, float, float]) -> bool:
        return self.distance_to(player_position) < self.catch_distance

    def frameCallback(self, event: FrameUpdateEvent):
        if self.started: # even though the state machine isn't updated when we're not start, we should do this to prevent the robot from turning
                         # this function is called even if the state machine isn't updated every frame yet.
            self.orientation_progress += viz.getFrameElapsed() / self.turn_duration
            self.orientation_progress = min(self.orientation_progress, 1.0)
            new_quat = vizmat.slerp(self.current_quat, self.target_quat, self.orientation_progress)
            self.avatar.setQuat(new_quat)

            player_position = event.PlayerPosition
            return event

    @classmethod
    def any_robots_caught_player(cls, player_position : Tuple[float, float, float]) -> bool:
        return len([b for b in cls.BotList if b.caught_player(player_position)]) > 0
        
    @classmethod
    def start_robots(cls):
        for bot in cls.BotList:
            bot.start()
            
    @classmethod
    def stop_robots(cls):
        for bot in cls.BotList:
            bot.stop()
            
    @classmethod
    def getCallback(cls):
        def callback(event : FrameUpdateEvent):
            for bot in cls.Bots:
                if bot.frameCallback is not None:
                    bot.frameCallback(event)
        return callback