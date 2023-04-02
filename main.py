import viz
import vizact

from Callbacks import networkCallback, frameDrawCallback, sprintKeyDownHandler, sprintKeyUpHandler
from Util import setWalkingSpeed
from Objects import Collectible
from Bots import PathFollowingBot

import steve

def printLocation():
	print(f"At {viz.MainView.getPosition()} facing {viz.MainView.getQuat()}")
	#print(followerBot.getPosition())

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
	c0 = Collectible('Assets/Coin/scene.gltf', position=[8, 1, 10], scale=5.0, spinDegPerSecond=90, value=3)
	c0.getModel().color([1, 0, 0])
	c1 = Collectible('Assets/Coin/scene.gltf', position=[-3.5, 1, 1], scale=5.0, spinDegPerSecond=90, value=2)
	c1.getModel().color([0, 1, 0])
	c2 = Collectible('Assets/Coin/scene.gltf', position=[-10, 1, -4], scale=5.0, spinDegPerSecond=90, value=1)
	c2.getModel().color([0, 0, 1])
	c3 = Collectible('Assets/Coin/scene.gltf', position=[-9, 1, -10], scale=5.0, spinDegPerSecond=90, value=10)
	
	path = [
		{
			"Position" : [-3.570643663406372, 1.8200000524520874, -6.548458576202393] ,
			"Speed" : 1,
			"DegreesPerSecond" : 90
		},
		{
			"Position" : [-3.5064423084259033, 1.8200000524520874, -11.498076438903809],
			"Speed" : 1,
			"DegreesPerSecond" : 90
		},
		{
			"Position" : [-10.481642723083496, 1.8200000524520874, -11.953154563903809],
			"Speed" : 1,
			"DegreesPerSecond" : 90
		},
		{
			"Position" : [-11.995747566223145, 1.8200000524520874, -8.496102333068848],
			"Speed" : 1,
			"DegreesPerSecond" : 90
		},
		{
			"Position" : [-11.910186767578125, 1.8200000524520874, -5.750005722045898],
			"Speed" : 1,
			"DegreesPerSecond" : 90
		},
		{
			"Position" : [-5.884194374084473, 1.8200000524520874, -3.4759459495544434],
			"Speed" : 1,
			"DegreesPerSecond" : 90
		},
		{
			"Position" : [-4.840819835662842, 1.8200000524520874, -4.874146938323975],
			"Speed" : 1,
			"DegreesPerSecond" : 90
		},
	]
	
	path = [tuple(p["Position"]) for p in path]
	
	def angryMode(st : PathFollowingBot):
		st.avatar.setEyeColor([1, 0, 0])
		
	def patrolMode(st : PathFollowingBot):
		st.avatar.setEyeColor([0, 0, 0])
		
	def alertMode(st : PathFollowingBot):
		st.avatar.setEyeColor([1, 1, 0])
		
	
	followerBot = steve.Steve()
	bot = PathFollowingBot(followerBot, path, 
							change_node_theme_to_chase_mode=angryMode, 
							change_node_theme_to_walk_mode=patrolMode, 
							change_node_theme_to_alert_mode=alertMode)
	
	viz.MainView.setPosition([12.347145080566406, 1.8200000524520874, -7.345220565795898])
	viz.MainView.setQuat([-0.0, -0.45234599709510803, 0.0, 0.8918425440788269])
	
if __name__ == "__main__":
	load()
	