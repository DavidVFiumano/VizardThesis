import viz
import vizact

from Events import FrameUpdateEvent

walkingSpeed = 2.5 # unit/sec
sprintingSpeed = 15 # unit/sec
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
	viz.MainView.move(xSpeed, 0, zSpeed)
	

def setWalkingSpeed():
	global currentSpeed, walkingSpeed
	currentSpeed = walkingSpeed
	
	
def setSprintingSpeed():
	global currentSpeed, sprintingSpeed
	currentSpeed = sprintingSpeed
	