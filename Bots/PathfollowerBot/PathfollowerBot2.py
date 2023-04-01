from typing import List, Tuple

import viz
import vizmat

from Events import FrameUpdateEvent
from .. import Bot

class PathFollowingBot(Bot):
    def __init__(self, avatar: viz.VizNode, path: List[Tuple[float, float, float]], speed: float = 1.0, hearing_range: float = 5.0):
        start_position = path[0]
        facing_direction = viz.Vector(path[1]) - viz.Vector(path[0])
        start_quat = vizmat.LookToQuat(facing_direction)

        super().__init__(avatar, start_position, start_quat)

        self.path = path
        self.speed = speed
        self.hearing_range = hearing_range
        self.current_target = 1

    def frameCallback(self, event: FrameUpdateEvent):
        current_position = self.avatar.getPosition()
        player_position = event.PlayerPosition

        # Check if the player is within hearing range
        distance_to_player = vizmat.Distance(current_position, player_position)
        if distance_to_player <= self.hearing_range:
            target_position = player_position
        else:
            target_position = self.path[self.current_target]

        direction = viz.Vector(target_position) - current_position
        distance = direction.length()

        if distance < self.speed * viz.getFrameElapsed():
            self.current_target = (self.current_target + 1) % len(self.path)
        else:
            direction.normalize()
            direction *= self.speed * viz.getFrameElapsed()
            new_position = current_position + direction

            # Update avatar's position
            self.avatar.setPosition(new_position)

            # Update avatar's orientation to face the target
            quat = vizmat.LookToQuat(direction)
            self.avatar.setQuat(quat)

