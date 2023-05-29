from typing import Tuple, List
from math import pi

import viz
import vizmat

from Events import FrameUpdateEvent

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

class Bot:

	BotList : List["Bot"] = list()
	
	def __init__(self, avatar : viz.VizNode, position : Tuple[float, float, float], facing : Tuple[float, float, float, float]):
		self.avatar = avatar
		self.avatar.setPosition(*position)
		self.avatar.setQuat(*facing)
		self.turn_duration = 0
		self.frameCallback = None
		self.velocity_vector = [0.0, 0.0, 0.0]
		self.current_target = None
		type(self).BotList.append(self)
		
	def frameCallbackFunc(self, event : FrameUpdateEvent):
		if self.started and self.turn_duration > 0.0: # even though the state machine isn't updated when we're not start, we should do this to prevent the robot from turning
						 # this function is called even if the state machine isn't updated every frame yet.
			self.orientation_progress += viz.getFrameElapsed() * (2 * pi) / self.turn_duration
			self.orientation_progress = min(self.orientation_progress, 1.0)
			new_quat = vizmat.slerp(self.current_quat, self.target_quat, self.orientation_progress)
			self.avatar.setQuat(new_quat)

			player_position = event.PlayerPosition
		return event
	
	@classmethod
	def getCallback(cls):
		def callback(event : FrameUpdateEvent):
			for bot in cls.BotList:
				if bot.frameCallback is not None:
					bot.frameCallback(event)
		return callback
		
	def move_towards(self, target: Tuple[float, float, float], speed : float):
		current_position = self.avatar.getPosition()
		self.current_target = target
		direction = viz.Vector(target) - current_position
		distance = direction.length()

		# Calculate the movement vector for this frame
		direction.normalize()
		self.velocity_vector = direction * speed
		direction *= speed * viz.getFrameElapsed()
		new_position = current_position + direction

		# Calculate the distance the avatar will move in this frame
		frame_movement_distance = direction.length()
		
		# Check if the avatar has reached the target in this frame
		if distance < frame_movement_distance:
			self.avatar.setPosition(target)
			return True

		self.avatar.setPosition(new_position)
		return False		

	def is_at_position(self, target: Tuple[float, float, float], speed : float) -> bool:
		current_position = self.avatar.getPosition()
		return vizmat.Distance(current_position, target) < speed * viz.getFrameElapsed()
	
	def get_position(self) -> Tuple[float, float, float]:
		return self.avatar.getPosition()

	def distance_to(self, target: Tuple[float, float, float]) -> float:
		current_position = self.avatar.getPosition()
		return vizmat.Distance(current_position, target)
		
	def look_at(self, target: Tuple[float, float, float], turnDurationSec : float):
		self.turn_duration = turnDurationSec
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
		
	@classmethod
	def start_robots(cls):
		for bot in cls.BotList:
			bot.start()
			
	@classmethod
	def stop_robots(cls):
		for bot in cls.BotList:
			bot.stop()