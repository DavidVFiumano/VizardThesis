import viz
import vizact

walkingSpeed = 0.05
runningSpeed = 0.15

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

def setWalkingSpeed():
	global funcsSet, forwardFunc, leftFunc, backwardFunc, rightFunc
	resetSpeed()
	funcsSet = True
	forwardFunc = vizact.whilekeydown('w', viz.MainView.move, 0, 0, walkingSpeed)
	leftFunc = vizact.whilekeydown('a', viz.MainView.move, -1*walkingSpeed, 0, 0)
	backwardFunc = vizact.whilekeydown('s', viz.MainView.move, 0, 0, -1*walkingSpeed)
	rightFunc = vizact.whilekeydown('d', viz.MainView.move, walkingSpeed, 0, 0)
	
	
def setSprintingSpeed():
	global funcsSet, forwardFunc, leftFunc, backwardFunc, rightFunc
	resetSpeed()
	funcsSet = True
	forwardFunc = vizact.whilekeydown('w', viz.MainView.move, 0, 0, runningSpeed)
	leftFunc = vizact.whilekeydown('a', viz.MainView.move, -1*walkingSpeed, 0, 0)
	backwardFunc = vizact.whilekeydown('s', viz.MainView.move, 0, 0, -1*walkingSpeed)
	rightFunc = vizact.whilekeydown('d', viz.MainView.move, walkingSpeed, 0, 0)
	