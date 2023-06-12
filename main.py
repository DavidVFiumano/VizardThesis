import viz
import vizact
from steve import Steve

from Callbacks import frameDrawCallback, sprintKeyDownHandler, sprintKeyUpHandler
from PlayerMovement import setWalkingSpeed, disableMovement
from Objects import Collectible, AnimatedSprite
from Bots import PathFollowingBot, Bot

coinCounter = 0
def printCoinCreation(*args, **kwargs):
	global coinCounter
	print(f"c{coinCounter} = Collectible(\"Assets\\Coin\\scene.gltf\", position={viz.MainView.getPosition()}, scale=5.0, spinDegPerSecond=90, value=1)")
	coinCounter += 1

nodeCounter = 0
def printRobotPath(*args, **kwargs):
	global nodeCounter
	if nodeCounter == 0:
		print(f"[({viz.MainView.getPosition()}),")
	else:
		print(f"({viz.MainView.getPosition()}),")
	nodeCounter += 1
	
def stopBots(*args, **kwargs):
	Bot.stop_robots()

def startBots(*args, **kwargs):
	Bot.start_robots()

def load():
	model : viz.VizNode = viz.addChild(r"Assets\maze\maze_withCues.osgb")
	viz.MainView.stepSize(0.25)
	viz.clearcolor(viz.SKYBLUE)

	viz.setOption('viz.fullscreen.monitor', 1)
	viz.go(viz.FULLSCREEN)
	vizact.ontimer(0, frameDrawCallback)
	
	vizact.onkeydown(viz.KEY_SHIFT_L, sprintKeyDownHandler, viz.KEY_SHIFT_L)
	vizact.onkeyup(viz.KEY_SHIFT_L, sprintKeyUpHandler, viz.KEY_SHIFT_L)
	vizact.onkeydown('c', printCoinCreation, 'c')
	vizact.onkeydown('v', printRobotPath, 'v')
	vizact.onkeydown('p', stopBots, 'p')
	vizact.onkeydown('r', startBots, 'r')
	
	# vizard code below this line
	viz.setMultiSample(4)
	viz.fov(60)
	viz.MainView.collision( viz.ON )
	
	
	coinPath = r"Assets\\Coin\\scene.gltf"
	# create collectibles
	c0 = Collectible(coinPath, position=[6.998621940612793, 1, 9.737794876098633], scale=5.0, spinDegPerSecond=90, value=1)
	c1 = Collectible(coinPath, position=[8.012781143188477, 1, 5.204422950744629], scale=5.0, spinDegPerSecond=90, value=1)
	c2 = Collectible(coinPath, position=[1.17171311378479, 1, 0.01703565940260887], scale=5.0, spinDegPerSecond=90, value=1)
	c3 = Collectible(coinPath, position=[-9.098871231079102, 1, 2.8148715496063232], scale=5.0, spinDegPerSecond=90, value=1)
	c4 = Collectible(coinPath, position=[-22.395402908325195, 1, 9.070356369018555], scale=5.0, spinDegPerSecond=90, value=1)
	c5 = Collectible(coinPath, position=[-29.99196434020996, 1, 8.297274589538574], scale=5.0, spinDegPerSecond=90, value=1)
	c6 = Collectible(coinPath, position=[-34.22555160522461, 1, 8.750836372375488], scale=5.0, spinDegPerSecond=90, value=1)
	c7 = Collectible(coinPath, position=[-34.775508880615234, 1, -2.2834818363189697], scale=5.0, spinDegPerSecond=90, value=1)
	c8 = Collectible(coinPath, position=[-25.39453887939453, 1, 0.24555906653404236], scale=5.0, spinDegPerSecond=90, value=1)
	c9 = Collectible(coinPath, position=[-20.384464263916016, 1, -2.5303268432617188], scale=5.0, spinDegPerSecond=90, value=1)
	c10 = Collectible(coinPath, position=[-19.111984252929688, 1, -7.447795391082764], scale=5.0, spinDegPerSecond=90, value=1)
	c11 = Collectible(coinPath, position=[-27.709171295166016, 1, -8.581449508666992], scale=5.0, spinDegPerSecond=90, value=1)
	c12 = Collectible(coinPath, position=[-34.75823211669922, 1, -7.902703285217285], scale=5.0, spinDegPerSecond=90, value=1)
	c13 = Collectible(coinPath, position=[-32.98622512817383, 1, -15.244168281555176], scale=5.0, spinDegPerSecond=90, value=1)
	c14 = Collectible(coinPath, position=[-29.37664794921875, 1, -19.854284286499023], scale=5.0, spinDegPerSecond=90, value=1)
	c15 = Collectible(coinPath, position=[-33.51705551147461, 1, -29.140520095825195], scale=5.0, spinDegPerSecond=90, value=1)
	c16 = Collectible(coinPath, position=[-16.204771041870117, 1, -27.151256561279297], scale=5.0, spinDegPerSecond=90, value=1)
	c17 = Collectible(coinPath, position=[-9.295578956604004, 1, -32.522727966308594], scale=5.0, spinDegPerSecond=90, value=1)
	c18 = Collectible(coinPath, position=[-0.13532425463199615, 1, -24.978195190429688], scale=5.0, spinDegPerSecond=90, value=1)
	c19 = Collectible(coinPath, position=[6.141578197479248, 1, -31.804351806640625], scale=5.0, spinDegPerSecond=90, value=1)
	c20 = Collectible(coinPath, position=[1.8556935787200928, 1, -16.247509002685547], scale=5.0, spinDegPerSecond=90, value=1)
	
	def angryMode(st : PathFollowingBot):
		st.avatar.setEyeColor([1, 0, 0])
		
	def patrolMode(st : PathFollowingBot):
		st.avatar.setEyeColor([0, 0, 0])
		
	def alertMode(st : PathFollowingBot):
		st.avatar.setEyeColor([1, 1, 0])
		
	def patrolModeWhite(st : PathFollowingBot):
		st.avatar.setEyeColor([1, 1, 1])

							
	walkerBackAndForthPath = [([3.5011980533599854, 1.8200000524520874, -26.931617736816406]),
								([-6.476590633392334, 1.8200000524520874, -36.37723922729492]),
								([-14.259373664855957, 1.8200000524520874, -29.4940242767334]),
								([-19.796932220458984, 1.8200000524520874, -32.200904846191406]),
								([-27.573156356811523, 1.8200000524520874, -26.78937339782715]),
								([-35.73912048339844, 1.8200000524520874, -18.06804847717285]),
								([-30.543851852416992, 1.8200000524520874, -10.5344877243042]),
								([-24.596569061279297, 1.8200000524520874, -3.603863000869751]),
								([-20.118810653686523, 1.8200000524520874, -11.254183769226074]),
								([-11.245153427124023, 1.8200000524520874, -5.094127655029297]),
								([-5.346099376678467, 1.8200000524520874, -1.4807378053665161]),
								([-3.9131014347076416, 1.8200000524520874, 5.518442630767822]),
								([0.3437487483024597, 1.8200000524520874, 4.540185451507568]),
								([3.7967312335968018, 1.8200000524520874, -0.6116043329238892]),
								([9.07680606842041, 1.8200000524520874, -11.736166000366211]),
								([5.729029655456543, 1.8200000524520874, -16.1121883392334]),
								([-0.583862841129303, 1.8200000524520874, -10.184064865112305]),
								([-3.5532479286193848, 1.8200000524520874, -19.61629295349121]),
								([-0.20412011444568634, 1.8200000524520874, -29.23743438720703]),]
						
	walkerBackAndForth = Steve()
	walkerBackAndForth.setBodyColor([0, 0, 1.0])
	walkerBackAndForth = PathFollowingBot("WalkerBackAndForth", walkerBackAndForth, walkerBackAndForthPath,
							chase_speed=2, patrol_speed=1.25,
							chase_360_turn_duration=0.5, patrol_360_turn_duration=1,
							change_node_theme_to_chase_mode=angryMode, 
							change_node_theme_to_walk_mode=patrolMode, 
							change_node_theme_to_alert_mode=alertMode)
	
	
	
	
if __name__ == "__main__":
	load()
	