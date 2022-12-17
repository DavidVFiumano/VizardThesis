import viz
import vizact

from Callbacks import networkCallback, frameDrawCallback, sprintKeyDownHandler, sprintKeyUpHandler
from Util import setWalkingSpeed
from Objects import AnimatedSprite

def load():
	viz.addChild('maze.osgb')
	
	#viz.mouse.setOverride(viz.ON)
	
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
	
	# create collectibles
	testSprite = AnimatedSprite('Assets/Coin/scene.gltf', position=[8, 1, 10], scale=5.0, spinDegPerSecond=90)
		
	
if __name__ == "__main__":
	load()
	