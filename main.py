import viz
import vizact

from Callbacks import networkCallback, frameDrawCallback, sprintKeyDownHandler, sprintKeyUpHandler
from Util import setWalkingSpeed
from Objects import Collectible

def printLocation():
	print(viz.MainView.getPosition())

def load():
	viz.addChild('maze.osgb')
	#model = viz.addChild('Assets/Hexagon_Environment_Thesis.osgb')
	viz.clearcolor(viz.SKYBLUE)
	
	#viz.mouse.setOverride(viz.ON)
	
	viz.go()
	vizact.ontimer(0, frameDrawCallback)
	viz.callback(viz.NETWORK_EVENT, networkCallback)
	
	vizact.onkeydown(viz.KEY_SHIFT_L, sprintKeyDownHandler, viz.KEY_SHIFT_L)
	vizact.onkeyup(viz.KEY_SHIFT_L, sprintKeyUpHandler, viz.KEY_SHIFT_L)
	
	vizact.onkeydown('f', printLocation)
	
	setWalkingSpeed()
	
	# vizard code below this line
	viz.setMultiSample(4)
	viz.fov(60)
	viz.MainView.collision( viz.ON )
	
	# create collectibles
	c0 = Collectible('Assets/Coin/scene.gltf', position=[8, 1, 10], scale=5.0, spinDegPerSecond=90)
	c1 = Collectible('Assets/Coin/scene.gltf', position=[-3.5, 1, 1], scale=5.0, spinDegPerSecond=90)
	c2 = Collectible('Assets/Coin/scene.gltf', position=[-10, 1, -4], scale=5.0, spinDegPerSecond=90)
	c3 = Collectible('Assets/Coin/scene.gltf', position=[3, 1, -10], scale=5.0, spinDegPerSecond=90)
	c4 = Collectible('Assets/Coin/scene.gltf', position=[-9, 1, -10], scale=5.0, spinDegPerSecond=90)
	#c1 = Collectible('Assets/Coin/scene.gltf', position=[-8, -1, 10], scale=5.0, spinDegPerSecond=90)
	#c2 = Collectible('Assets/Coin/scene.gltf', position=[0, 0, 10], scale=5.0, spinDegPerSecond=90)
	
if __name__ == "__main__":
	load()
	