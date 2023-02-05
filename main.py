import viz
import vizact

from Callbacks import networkCallback, frameDrawCallback, sprintKeyDownHandler, sprintKeyUpHandler
from Util import setWalkingSpeed
from Objects import Collectible

def load():
	viz.addChild('maze.osgb')
	viz.clearcolor(viz.SKYBLUE)
	child = viz.addChild('Assets/Coin/scene.gltf', viz.DEFAULT_CANVAS_SCREEN)
	#child.setPosition(0.5)
	
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
	
	seekerCoins = viz.addProgressBar("Seeker Coins (6/20)")
	seekerCoins.set(0.3)
	seekerCoins.setPosition(0.93, 0.95)
	seekerCoins.setScale(0.5, 0.75)	
	seekerTheme = viz.Theme()
	seekerTheme.highBackColor = (1, 0, 0, 1)
	seekerTheme.borderColor = (0, 0, 0, 1)
	seekerTheme.backColor = (0.1, 0.1, 0.1, 0.5)
	seekerCoins.setTheme(seekerTheme)
	
	
	hiderCoins = viz.addProgressBar("Hider Coins (4/20)")
	hiderCoins.set(0.2)
	hiderCoins.setPosition(0.93, 0.9)
	hiderCoins.setScale(0.5, 0.75)
	hiderTheme = viz.Theme()
	hiderTheme.highBackColor = (0, 0, 1, 1)
	hiderTheme.borderColor = (0, 0, 0, 1)
	hiderTheme.backColor = (0.1, 0.1, 0.1, 0.5)
	hiderCoins.setTheme(hiderTheme)
	
	sprintBar = viz.addProgressBar("Sprint")
	sprintBar.setPosition(0.5, 0.05)
	sprintBar.set(0.95)
	sprintTheme = viz.Theme()
	sprintTheme.highBackColor = (0, 1, 0, 1)
	sprintTheme.borderColor = (0, 0, 0, 1)
	sprintTheme.backColor = (0.1, 0.1, 0.1, 0.5)
	sprintBar.setTheme(sprintTheme)
	
	
if __name__ == "__main__":
	load()
	