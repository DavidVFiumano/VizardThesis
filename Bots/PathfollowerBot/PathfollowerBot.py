from typing import Iterable, Tuple, Dict, Union, Callable
from math import sqrt, acos, radians, degrees

from viz import ActionData, FOREVER, VizNode, MainView, Matrix, Vector
import viz
from vizact import moveTo, spinTo, sequence, parallel, onupdate

from Events import FrameUpdateEvent
from .. import Bot

# TODO at some point make this it's own class so I can make paths a bit easier.
PATH_TYPE = Iterable[Dict[str, Union[Tuple[float, float, float], Tuple[float, float, float, float], float]]]

class PathfollowerBot(Bot):
	
	def updatePosAndMatrix(self):
		self.avatarCurrentOrientation = self.avatar.getMatrix()
		self.avatarCurrentPosition = self.avatar.getPosition()
	
	def __init__(self, avatar : VizNode, path : PATH_TYPE, seeingDistance : float, fieldOfView : float, hearingDistance : float, 
						chaseSpeed : float, chaseTurnDegPerSecond : float,
						chasingSeeingDistance : float = None, chasingFieldOfView : float = None, chasingHearingDistance : float = None, 
						updateChasePathEveryNFrames : int = 15, endOfPathBehavior : str = "repeat",
						chaseVizNodeFunction : Callable[[VizNode], None] = lambda x : None, 
						resetVizNodeFunction : Callable[[VizNode], None] = lambda x : None,
						debug : bool = False):
		super().__init__(avatar, path[0]["Position"], MainView.getQuat())
		self.avatar = avatar
		self.avatarCurrentOrientation = avatar.getMatrix()
		self.avatarCurrentPosition = avatar.getPosition()
		self.avatarUpdater = onupdate(0, self.updatePosAndMatrix)
		self.path = path
		self.currentAction : Union[None, ActionData] = None
		self.currentPositionInPathList = 0
		self.seeingDistance = seeingDistance
		self.fieldOfView = fieldOfView
		self.hearingDistance = hearingDistance
		self.chaseSpeed = chaseSpeed
		self.chaseTurnDegPerSecond = chaseTurnDegPerSecond
		self.chasing = False
		self.updateChasePathEveryNFrames = updateChasePathEveryNFrames
		self.endOfPathBehavior = endOfPathBehavior
		self.setPath(self.path, self.endOfPathBehavior)
		self.chaseVizNodeFunction = chaseVizNodeFunction
		self.resetVizNodeFunction = resetVizNodeFunction
		self.resetVizNodeFunction(avatar)
		self.chasingHearingDistance = chasingHearingDistance
		self.chasingSeeingDistance = chasingSeeingDistance
		self.chasingFieldOfView = chasingFieldOfView
		self.debug = debug
		if debug:
			self.arrow = viz.addChild('arrow.wrl')
			self.arrow.setScale([1, 1, 1])
		else:
			self.arrow = None
	
	def setPath(self, path, endOfPathBehavior):
		self.actionList = list()
		for i, point in enumerate(path):
			if i > 0:
				moveAction = moveTo(point["Position"], speed=point["Speed"])
			else:
				moveAction = sequence(spinTo(point=path[(i+1)%len(path)]["Position"], speed=point["DegreesPerSecond"]), 
										moveTo(point["Position"], speed=point["Speed"]))
			turnAction = spinTo(point=path[(i+1)%len(path)]["Position"], speed=point["DegreesPerSecond"])
			self.actionList.append(moveAction)
			self.actionList.append(turnAction)
		
		if endOfPathBehavior == "reverse":
			raise NotImplementedError("Reverse not implemented yet")
		elif endOfPathBehavior == "repeat":
			self.action = sequence(*self.actionList, FOREVER)
			
		self.avatar.addAction(self.action)
		
	@staticmethod
	def _distance(viewPosition : Iterable[float], collectiblePosition : Iterable[float]) -> float:
		sumOfSquaredResiduals = sum([(v - c)**2 for v, c in zip(viewPosition, collectiblePosition)])
		return sqrt(sumOfSquaredResiduals)
	
	@classmethod
	def pointInView(cls, observerPosition : Tuple[float, float, float],
					observerMatrix : Tuple[float, float, float, float],
					fovDegrees : float,
					point : Tuple[float, float, float],
					maxDistance : float, arrow : VizNode) -> bool:
						
		#orientation_matrix.transpose()

		# Compute the forward direction of the observer
		forward_direction = viz.Matrix(observerMatrix) * Vector(1, 0, 0)

		# Compute the direction vector from the observer's position to the point
		direction_to_point = Vector(point) - Vector(observerPosition)
		
		if direction_to_point.length() > maxDistance:
			return False

		# Normalize the direction vectors
		if arrow is not None:
			arrow.setPosition(observerPosition)
			default_arrow_direction = viz.Vector(0, 0, -1)
			rotation_axis = default_arrow_direction.cross(direction_to_point)
			rotation_angle = degrees(acos(default_arrow_direction.dot(direction_to_point) / direction_to_point.length()))
			arrow.setAxisAngle(*list(rotation_axis), rotation_angle)
			
			
		forward_direction.normalize()
		direction_to_point.normalize()

		# Calculate the dot product of the two direction vectors
		dot_product = forward_direction.dot(direction_to_point)

		# Calculate the angle (in radians) between the forward direction and the direction to the point
		angle = acos(dot_product)

		# Convert the field-of-view to radians
		fov_radians = radians(fovDegrees)

		# Check if the angle is within half of the field-of-view
		if angle <= fov_radians / 2:
			return True  # The point is in view
		else:
			return False  # The point is not in view
			
	@staticmethod
	# Function to check if a line between two points intersects any objects in the Vizard environment
	def objectInTheWay(start_point : Tuple[float, float, float], end_point : Tuple[float, float, float]) -> bool:
		# Perform a raycast from start_point to end_point
		result = viz.intersect(start_point, end_point)
		return result.valid
	
	def canSeePlayer(self, playerPosition : Tuple[float, float, float]) -> bool:
		botPosition = self.avatar.getPosition()
		botMatrix = self.avatar.head.getQuat()
		print(botMatrix)
		isInFOV = type(self).pointInView(botPosition, botMatrix, self.fieldOfView, playerPosition, self.seeingDistance, arrow=self.arrow)
		isObstructed = type(self).objectInTheWay(botPosition, playerPosition)
		#print(f"Player {'is' if isInFOV else 'is not'} in view, and {'is' if isObstructed else 'is not'} obstructed.")
		return isInFOV and (not isObstructed)
		
	def canHearPlayer(self, playerPosition : Tuple[float, float, float]) -> bool:
		#if not self.chasing:
		#	return self.hearingDistance is not None and type(self)._distance(playerPosition, self.avatar.getPosition()) < self.hearingDistance
		#else:
		#	hearingDistance = self.hearingDistance if self.chasingHearingDistance is None else self.chasingHearingDistance
		#	return hearingDistance is not None and type(self)._distance(playerPosition, self.avatar.getPosition()) < hearingDistance
		return False
			
	def chasePlayer(self, playerPosition : Tuple[float, float, float], playerVelocityVector : Tuple[float, float, float]):
		self.avatar.clearActions()
		chasePoint = playerPosition + playerVelocityVector
		lookAndFollow = parallel(moveTo(chasePoint, speed=self.chaseSpeed), spinTo(point=chasePoint, speed=self.chaseTurnDegPerSecond))
		self.avatar.addAction(lookAndFollow)
	
	def resetPath(self):
		self.setPath(self.path, self.endOfPathBehavior)
	
	def frameCallback(self, event : FrameUpdateEvent):
		playerPosition = FrameUpdateEvent.PlayerPosition
		if not self.chasing:
			if self.canHearPlayer(playerPosition) or self.canSeePlayer(playerPosition):
				self.chasing = True
				self.chaseVizNodeFunction(self.avatar)
				self.chasePlayer(playerPosition, FrameUpdateEvent.PlayerVelocity)
			else:
				self.chasing = False
		
		elif FrameUpdateEvent.FrameNumber % self.updateChasePathEveryNFrames == 0:
			if not (self.canHearPlayer(playerPosition) or self.canSeePlayer(playerPosition)):
				self.chasing = False
				self.resetVizNodeFunction(self.avatar)
				self.resetPath()
			else:
				self.chasePlayer(playerPosition, FrameUpdateEvent.PlayerVelocity)
				