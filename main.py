import viz
import vizact

from Callbacks import networkCallback, frameDrawCallback, sprintKeyDownHandler, sprintKeyUpHandler
from Util import setWalkingSpeed

def load():
	viz.addChild('maze.osgb')
	
	viz.mouse(viz.ON)
	
	viz.go()
	vizact.ontimer(0, frameDrawCallback)
	viz.callback(viz.NETWORK_EVENT, networkCallback)
	
	vizact.onkeydown(viz.KEY_SHIFT_L, sprintKeyDownHandler, viz.KEY_SHIFT_L)
	vizact.onkeyup(viz.KEY_SHIFT_L, sprintKeyUpHandler, viz.KEY_SHIFT_L)
	
	setWalkingSpeed()
	
	# vizard code below this line
	viz.setMultiSample(4)
	viz.fov(60)
	viz.MainView.collision( viz.ON )
		
	
if __name__ == "__main__":
	load()
	