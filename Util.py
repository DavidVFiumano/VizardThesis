import viz
import vizact

funcsSet = False
forwardFunc = None
leftFunc = None
backwardFunc = None
rightFunc = None

def resetSpeed():
	if funcsSet:
		forwardFunc.remove()
		leftFunc.remove()
		backwardFunc.remove()
		rightFunc.remove()

def setWalkingSpeed():
	resetSpeed()
	funcsSet = True
	forwardFunc = vizact.whilekeydown('w', viz.MainView.move, 0, 0, 0.01)
	leftFunc = vizact.whilekeydown('a', viz.MainView.move, -0.01, 0, 0)
	backwardFunc = vizact.whilekeydown('s', viz.MainView.move, 0, 0, -0.01)
	rightFunc = vizact.whilekeydown('d', viz.MainView.move, 0.01, 0, 0)
	
	
def setSprintingSpeed():
	resetSpeed()
	funcsSet = True
	forwardFunc = vizact.whilekeydown('w', viz.MainView.move, 0, 0, 0.05)
	leftFunc = vizact.whilekeydown('a', viz.MainView.move, -0.01, 0, 0)
	backwardFunc = vizact.whilekeydown('s', viz.MainView.move, 0, 0, -0.01)
	rightFunc = vizact.whilekeydown('d', viz.MainView.move, 0.01, 0, 0)
	