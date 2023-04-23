import viz
import vizact

from Callbacks import frameDrawCallback, sprintKeyDownHandler, sprintKeyUpHandler
from PlayerMovement import setWalkingSpeed, disableMovement
from Objects import Collectible
from Bots import PathFollowingBot

import steve

def load():
	viz.addChild('maze.osgb')
	#model = viz.addChild('Assets/Hexagon_Environment_Thesis.osgb')
	viz.clearcolor(viz.SKYBLUE)
	
	#viz.mouse.setOverride(viz.ON)
	viz.setOption('viz.fullscreen.monitor', 2)
	viz.go(viz.FULLSCREEN)
	vizact.ontimer(0, frameDrawCallback)
	
	vizact.onkeydown(viz.KEY_SHIFT_L, sprintKeyDownHandler, viz.KEY_SHIFT_L)
	vizact.onkeyup(viz.KEY_SHIFT_L, sprintKeyUpHandler, viz.KEY_SHIFT_L)
	
	# vizard code below this line
	viz.setMultiSample(4)
	viz.fov(60)
	viz.MainView.collision( viz.ON )
	
	# create collectibles
	c0 = Collectible('Assets/Coin/scene.gltf', position=[8, 1, 10], scale=5.0, spinDegPerSecond=90, value=3)
	c0.getModel().color([1, 0, 0])
	c1 = Collectible('Assets/Coin/scene.gltf', position=[-3.5, 1, 1], scale=5.0, spinDegPerSecond=90, value=2)
	c1.getModel().color([0, 1, 0])
	c2 = Collectible('Assets/Coin/scene.gltf', position=[-10, 1, -4], scale=5.0, spinDegPerSecond=90, value=1)
	c2.getModel().color([0, 0, 1])
	c3 = Collectible('Assets/Coin/scene.gltf', position=[-9, 1, -10], scale=5.0, spinDegPerSecond=90, value=10)
	c4 = Collectible('Assets/Coin/scene.gltf', position=[7.913609981536865, 1, 4.545787334442139], scale=5.0, spinDegPerSecond=90, value=4)
	c4.getModel().color([1, 0, 1])
	c5 = Collectible('Assets/Coin/scene.gltf', position=[8.461063385009766, 1.0, -10.422457695007324], scale=5.0, spinDegPerSecond=90, value=3)
	c5.getModel().color([1, 0, 0])
	c6 = Collectible('Assets/Coin/scene.gltf', position=[2.7147984504699707, 1.0, -9.695528030395508], scale=5.0, spinDegPerSecond=90, value=2)
	c6.getModel().color([0, 1, 0])
	c6 = Collectible('Assets/Coin/scene.gltf', position=[-9.551280975341797, 1.0, 2.0373713970184326], scale=5.0, spinDegPerSecond=90, value=5)
	c6.getModel().color([0, 1, 1])
	
	def angryMode(st : PathFollowingBot):
		st.avatar.setEyeColor([1, 0, 0])
		
	def patrolMode(st : PathFollowingBot):
		st.avatar.setEyeColor([0, 0, 0])
		
	def alertMode(st : PathFollowingBot):
		st.avatar.setEyeColor([1, 1, 0])
		
	
	CoinGuardPath = [(-3.570643663406372, 1.8200000524520874, -6.548458576202393), 
						(-3.5064423084259033, 1.8200000524520874, -11.498076438903809), 
						(-10.481642723083496, 1.8200000524520874, -11.953154563903809), 
						(-11.995747566223145, 1.8200000524520874, -8.496102333068848), 
						(-11.910186767578125, 1.8200000524520874, -5.750005722045898), 
						(-5.884194374084473, 1.8200000524520874, -3.4759459495544434), 
						(-4.840819835662842, 1.8200000524520874, -4.874146938323975)]
						
	coinGuardBot = steve.Steve()
	coinGuardBot = PathFollowingBot("3CoinGuard", coinGuardBot, CoinGuardPath,
							chase_speed=2, patrol_speed=1.25,
							chase_360_turn_duration=0.5, patrol_360_turn_duration=1,
							change_node_theme_to_chase_mode=angryMode, 
							change_node_theme_to_walk_mode=patrolMode, 
							change_node_theme_to_alert_mode=alertMode)
							
	walkerBackAndForthPath = [(9.828619003295898, 1.8200000524520874, -4.095284461975098),
							  (-5.570601463317871, 1.8200000524520874, -3.932171106338501),
							  (-4.003185749053955, 1.8200000524520874, 10.214484214782715)]
						
	walkerBackAndForth = steve.Steve()
	walkerBackAndForth.setBodyColor([0, 0, 1.0])
	walkerBackAndForth = PathFollowingBot("WalkerBackAndForth", walkerBackAndForth, walkerBackAndForthPath,
							chase_speed=2, patrol_speed=1.25,
							chase_360_turn_duration=0.5, patrol_360_turn_duration=1,
							change_node_theme_to_chase_mode=angryMode, 
							change_node_theme_to_walk_mode=patrolMode, 
							change_node_theme_to_alert_mode=alertMode)
							
	dumberGuardBotPath = [(5.5286736488342285, 1.8200000524520874, 1.1839501857757568),
						   (11.186570167541504, 1.8200000524520874, 7.215301990509033),
						   (12.096813201904297, 1.8200000524520874, 8.530780792236328),
						   (4.569991111755371, 1.8200000524520874, 10.155921936035156)]
						
	dumberGuardBot = steve.Steve()
	dumberGuardBot.setBodyColor([1.0, 0, 1.0])
	dumberGuardBot = PathFollowingBot("DumberGuardBot", dumberGuardBot, dumberGuardBotPath,
							chase_speed=2, patrol_speed=1.25,
							chase_360_turn_duration=0.5, patrol_360_turn_duration=1,
							change_node_theme_to_chase_mode=angryMode, 
							change_node_theme_to_walk_mode=patrolMode, 
							change_node_theme_to_alert_mode=alertMode)
	
	viz.MainView.setPosition([12.347145080566406, 1.8200000524520874, -7.345220565795898])
	viz.MainView.setQuat([-0.0, -0.726588249206543, 0.0, -0.6870731115341187])
	
if __name__ == "__main__":
	load()
	