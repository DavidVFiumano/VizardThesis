import viz
import vizact
import math

from Events import FrameUpdateEvent

walkingSpeed = 6 # unit/sec
sprintingSpeed = 12 # unit/sec
currentSpeed = walkingSpeed

funcsSet = False
forwardFunc = None
leftFunc = None
backwardFunc = None
rightFunc = None	

def resetSpeed():
	global funcsSet, forwardFunc, leftFunc, backwardFunc, rightFunc
	if funcsSet:
		forwardFunc.remove()
		leftFunc.remove()
		backwardFunc.remove()
		rightFunc.remove()
		
def moveMainViewFromKeys(event : FrameUpdateEvent):
	global currentSpeed
	timeSinceLastFrame = viz.getFrameElapsed()
	forwardSpeed = int(viz.key.isDown('w', False))*currentSpeed*timeSinceLastFrame
	leftSpeed = int(viz.key.isDown('a', False))*currentSpeed*timeSinceLastFrame
	rightSpeed = int(viz.key.isDown('d', False))*currentSpeed*timeSinceLastFrame
	backSpeed = int(viz.key.isDown('s', False))*currentSpeed*timeSinceLastFrame
	
	zSpeed = forwardSpeed - backSpeed
	xSpeed = rightSpeed - leftSpeed
	
	if zSpeed != 0 or xSpeed != 0:
		# normalize this so the speed is never greater than the currentSpeed in units/sec
		# if two buttons are pressed without this, the speed doubles.
		maxSpeedForFrame = currentSpeed * timeSinceLastFrame	
		scalingFactor = maxSpeedForFrame / (math.sqrt(zSpeed**2 + xSpeed**2)) # L/|v| for length L and vector V scales vector to L
		
		xSpeed = xSpeed*scalingFactor
		zSpeed = zSpeed*scalingFactor
		# TODO maybe normalize these to ensure it never exceeds currentSpeed when two buttons are pressed?
		viz.MainView.move(xSpeed, 0, zSpeed)
	
		print(f"frameMovement: {abs(xSpeed) + abs(zSpeed)} or {math.sqrt(xSpeed**2 + zSpeed**2)/timeSinceLastFrame} unit/sec.")

def setWalkingSpeed():
	global currentSpeed, walkingSpeed
	currentSpeed = walkingSpeed
	
	
def setSprintingSpeed():
	global currentSpeed, sprintingSpeed
	currentSpeed = sprintingSpeed
	