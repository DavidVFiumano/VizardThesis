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
	viz.MainView.setPosition(-12.67, 1.82, -11.34)
	viz.MainView.setQuat(0.0, 0.025, 0.0, 1.0)
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
	viz.fov(60) # TODO if you change this go and update the fov value in FrameUpdateEvent.py too.
	viz.MainView.collision( viz.ON )
	
	# coin positions
	high1_positions = [
		(7.19703483581543, 1.0, 9.655489921569824),
		(7.96468448638916, 1.0, 4.984078884124756),
		(1.7242555618286133, 1.0, -0.02603543922305107),
		(8.589869499206543, 1.0, -9.564338684082031),
		(3.786768913269043, 1.0, -9.159051895141602),
		(-7.9711079597473145, 1.0, -9.464898109436035),
		(-8.697246551513672, 1.0, -5.573084831237793),
		(-9.187590599060059, 1.0, 2.979050397872925),
		(2.7452516555786133, 1.0, 8.451804161071777),
	]
	
	high2_positions = [
		(-5.461543560028076, 1.0, -16.47490692138672),
		(2.023087501525879, 1.0, -21.06539535522461),
		(-0.12702786922454834, 1.0, -25.054553985595703),
		(5.49971866607666, 1.0, -31.972972869873047),
		(11.203081130981445, 1.0, -33.463401794433594),
		(-1.7824046611785889, 1.0, -33.31794357299805),
		(-9.409445762634277, 1.0, -32.263893127441406),
		(-9.497700691223145, 1.0, -28.192867279052734),
		(-6.9109296798706055, 1.0, -21.393844604492188),
	]
	
	low1_positions = [
		(-19.448816299438477, 1.0, -7.918258190155029),
		(-30.01082992553711, 1.0, 8.15184211730957),
		(-21.956439971923828, 1.0, 8.746465682983398),
	]
	
	low2_positions = [
		(-32.500118255615234, 1.0, -31.436012268066406),
		(-16.26887321472168, 1.0, -27.380428314208984),
		(-33.070831298828125, 1.0, -16.523576736450195),
	]
	
	quadrant_coins = {
		"quadrant_high1" : high1_positions,
		"quadrant_high2" : high2_positions,
		"quadrant_low1" : low1_positions,
		"quadrant_low2" : low2_positions
	}
	
	coinPath = r"Assets\\Coin\\scene.gltf"

	coins = list()
	for quadrant_prefix, coin_positions in quadrant_coins.items():
		for idx, position in enumerate(coin_positions):
			coins.append(
				Collectible(
					coinPath, 
					position=position, 
					scale=5.0, 
					spinDegPerSecond=90, 
					value=1,
					name=f"{quadrant_prefix}_{idx}"
				)
			)
	

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
							chase_speed=5, patrol_speed=5,
							chase_360_turn_duration=0.5, patrol_360_turn_duration=1,
							change_node_theme_to_chase_mode=angryMode, 
							change_node_theme_to_walk_mode=patrolMode, 
							change_node_theme_to_alert_mode=alertMode)
	
	
if __name__ == "__main__":
	load()
	