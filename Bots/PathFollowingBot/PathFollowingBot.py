from typing import List, Tuple, Union, Dict, Any, Callable
from logging import LogRecord, Logger, INFO
from os.path import abspath
import math

import viz
import vizmat

from StateManagement import State, StateMachine
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
            bot.move_towards(target_pos, globalValues["patrol_speed"])
            bot.look_at(target_pos, globalValues["patrol_360_turn_duration"])

            if bot.is_at_position(target_pos, globalValues["patrol_speed"]):
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
        bot.move_towards(player_position, globalValues["chase_speed"])
        bot.look_at(self.playerPosition, globalValues["chase_360_turn_duration"])

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
        if bot.is_at_position(last_known_pos, globalValues["chase_speed"]):
            self.localState["bot_still_looking"] = bot.look_around(5, 135, 5)
        else:
            bot.move_towards(last_known_pos, globalValues["chase_speed"])
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
    
    def __init__(self, name : str, avatar: viz.VizNode, path: List[Tuple[float, float, float]], 
                        catch_distance : float = 1.25,
                        patrol_speed: float = 1.25, patrol_360_turn_duration: float = 1.0,
                        chase_speed: float = 1.25, chase_360_turn_duration: float = 0.75, 
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
        self.patrol_speed = patrol_speed
        self.patrol_360_turn_duration = patrol_360_turn_duration
        self.chase_speed = chase_speed
        self.chase_360_turn_duration = chase_360_turn_duration
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
        state_machine.setGlobalValue('patrol_speed', self.patrol_speed)
        state_machine.setGlobalValue('chase_speed', self.chase_speed)
        state_machine.setGlobalValue('patrol_360_turn_duration', self.patrol_360_turn_duration)
        state_machine.setGlobalValue('chase_360_turn_duration', self.chase_360_turn_duration)
        
        self.look_around_timer = 0.0
        self.look_around_base_angle = 0.0

        self.state_machine = state_machine
    
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
        return self.distance_to(player_position) < self.catch_distance and self.isStarted()

    @classmethod
    def any_robots_caught_player(cls, player_position : Tuple[float, float, float]) -> bool:
        return len([b for b in cls.BotList if isinstance(b, PathFollowingBot) and b.caught_player(player_position)]) > 0