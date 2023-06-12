import math
from typing import List

import viz
import vizact
import vizmat

from Events import FrameUpdateEvent
from Bots import Bot

walkingSpeed = 10 # unit/sec
sprintingSpeed = 18 # unit/sec
currentSpeed = 0
sprinting = False

lookSpeed = 90 # deg/sec
currentLookSpeed = 0

def updateFOV(angleChange):
	elapsed_time = viz.getFrameElapsed()
	current_quat = viz.MainView.getQuat()
	
	# Rotate around the Y axis
	axis = [0, 1, 0]
	
	# Compute the axis-angle quaternion
	sin_half_angle = math.sin(math.radians(angleChange) / 2)
	cos_half_angle = math.cos(math.radians(angleChange) / 2)
	rotation_quat = [axis[0] * sin_half_angle, axis[1] * sin_half_angle, axis[2] * sin_half_angle, cos_half_angle]
	
	# Multiply the current quaternion by the rotation quaternion
	x, y, z, w = current_quat
	xr, yr, zr, wr = rotation_quat
	new_quat = [w * xr + x * wr + y * zr - z * yr,
				w * yr - x * zr + y * wr + z * xr,
				w * zr + x * yr - y * xr + z * wr,
				w * wr - x * xr - y * yr - z * zr]
	
	viz.MainView.setQuat(new_quat)
		
def moveMainViewFromKeys(event : FrameUpdateEvent):
	global currentSpeed
	timeSinceLastFrame = viz.getFrameElapsed()
	forwardSpeed = int(viz.key.isDown('w', False))*currentSpeed*timeSinceLastFrame
	leftSpeed = int(viz.key.isDown('a', False))*currentSpeed*timeSinceLastFrame
	rightSpeed = int(viz.key.isDown('d', False))*currentSpeed*timeSinceLastFrame
	backSpeed = int(viz.key.isDown('s', False))*currentSpeed*timeSinceLastFrame
	
	rightLookSpeed = int(viz.key.isDown(viz.KEY_RIGHT, False))*currentSpeed*timeSinceLastFrame
	leftLookSpeed = int(viz.key.isDown(viz.KEY_LEFT, False))*currentSpeed*timeSinceLastFrame
	
	zSpeed = forwardSpeed - backSpeed
	xSpeed = rightSpeed - leftSpeed
	
	if rightLookSpeed + leftLookSpeed != 0:
		lookDirection = 1 if rightLookSpeed > 0 else -1
		angleChange = lookDirection * currentLookSpeed * timeSinceLastFrame
		updateFOV(angleChange)
	
	if zSpeed != 0 or xSpeed != 0:
		# normalize this so the speed is never greater than the currentSpeed in units/sec
		# if two buttons are pressed without this, the speed doubles.
		maxSpeedForFrame = currentSpeed * timeSinceLastFrame	
		scalingFactor = maxSpeedForFrame / (math.sqrt(zSpeed**2 + xSpeed**2)) # L/|v| for length L and vector V scales vector to L
		
		xSpeed = xSpeed*scalingFactor
		zSpeed = zSpeed*scalingFactor
		
		# TODO maybe normalize these to ensure it never exceeds currentSpeed when two buttons are pressed?
		viz.MainView.move(xSpeed, 0, zSpeed)
		

def setWalkingSpeed():
	global currentSpeed, walkingSpeed, currentLookSpeed, lookSpeed, sprinting
	sprinting = False
	currentSpeed = walkingSpeed
	currentLookSpeed = lookSpeed
	
def setSprintingSpeed():
	global currentSpeed, sprintingSpeed, currentLookSpeed, lookSpeed, sprinting
	sprinting = True
	currentSpeed = sprintingSpeed
	currentLookSpeed = lookSpeed

def isSprinting() -> bool:
	global sprinting
	return sprinting

def disableMovement():
	global currentSpeed
	currentSpeed = 0
	currentLookSpeed = 0