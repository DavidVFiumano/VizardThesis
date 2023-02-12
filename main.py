import viz
import vizact

from Callbacks import networkCallback, frameDrawCallback, sprintKeyDownHandler, sprintKeyUpHandler
from Util import setWalkingSpeed
from Objects import Collectible

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
	
	setWalkingSpeed()
	
	# vizard code below this line
	viz.setMultiSample(4)
	viz.fov(60)
	viz.MainView.collision( viz.ON )
	
	# create collectibles
	testCollectible = Collectible('Assets/Coin/scene.gltf', position=[8, 1, 10], scale=5.0, spinDegPerSecond=90)
	
	
	playerCoins = viz.addProgressBar(f"Seeker Coins (0/?)")
	playerCoins.set(0.0)
	playerCoins.setPosition(0.93, 0.95)
	playerCoins.setScale(0.5, 0.75)	
	coinBarTheme = viz.Theme()
	coinBarTheme.highBackColor = (1, 0, 0, 1)
	coinBarTheme.borderColor = (0, 0, 0, 1)
	coinBarTheme.backColor = (0.1, 0.1, 0.1, 0.5)
	playerCoins.setTheme(coinBarTheme)
	
if __name__ == "__main__":
	load()
	