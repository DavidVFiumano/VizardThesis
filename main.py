import viz
import vizact

from Callbacks import networkCallback, frameDrawCallback

def load():
	viz.addChild('maze.osgb')
	
	#viz.mouse.setOverride(viz.ON)
	
	viz.go()
	vizact.ontimer(0, frameDrawCallback)
	viz.callback(viz.NETWORK_EVENT, networkCallback)
	
	# vizard code below this line
	viz.setMultiSample(4)
	viz.fov(60)
	viz.MainView.collision( viz.ON )
		
	
if __name__ == "__main__":
	load()
	