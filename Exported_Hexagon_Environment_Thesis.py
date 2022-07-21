import viz
import viztask
import vizfx
import vizinfo

viz.setMultiSample(4)
viz.fov(40)
viz.go()

#Set up environment, (note for me: do not mess with this or it will not load on screen, it is perfect!)
env = vizfx.addChild('Vizard_Thesis/Hexagon_Environment_Thesis.osgb') 

#Add vizinfo panel to display instructions (needs to be changed to my instructions)
info = vizinfo.InfoPanel("Explore the environment\nPress 'd' to toggle the visibility of the sensors\nPress spacebar to begin the experiment")

#Viewpoint
view = viz.MainView
view.setPosition(10,20,30) #10,20,30 means nothing, just testing this line out
mode = viz.REL_LOCAL #Positional argument

#Ask for Participant Info
def participantInfo():
	
	#Turn off visibility of proximity sensors and disable toggle
	manager.setDebug(viz.OFF)
	debugEventHandle.setEnabled(viz.OFF)

	#Hide info panel currently displayed
	info.visible(viz.OFF)

	#Add an InfoPanel with a title bar
	participantInfo = vizinfo.InfoPanel('',title='Participant Information',align=viz.ALIGN_CENTER, icon=False)

	#Add name and ID fields
	textbox_last = participantInfo.addLabelItem('Last Name',viz.addTextbox())
	textbox_first = participantInfo.addLabelItem('First Name',viz.addTextbox())
	textbox_id = participantInfo.addLabelItem('ID',viz.addTextbox())
	participantInfo.addSeparator(padding=(20,20))

	#Add gender and age fields
	radiobutton_male = participantInfo.addLabelItem('Male',viz.addRadioButton(0))
	radiobutton_female = participantInfo.addLabelItem('Female',viz.addRadioButton(0))
	droplist_age = participantInfo.addLabelItem('Age Group',viz.addDropList())
	ageList = ['20-30','31-40','41-50','51-60','61-70']
	droplist_age.addItems(ageList)
	participantInfo.addSeparator()
	
	#Add submit button aligned to the right and wait until it's pressed
	submitButton = participantInfo.addItem(viz.addButtonLabel('Submit'),align=viz.ALIGN_RIGHT_CENTER)
	yield viztask.waitButtonUp(submitButton)

	#Collect participant data
	data = viz.Data()
	data.lastName = textbox_last.get()
	data.firstName = textbox_first.get()
	data.id = textbox_id.get()
	data.ageGroup = ageList[droplist_age.getSelection()]

	if radiobutton_male.get() == viz.DOWN:
		 data.gender = 'male'
	else:
		 data.gender = 'female'

	participantInfo.remove()

	# Return participant data
	viztask.returnValue(data)

#Portion where participant practices before real task	
def learnPhase():

	#provide instructions for the participant
	info.setText("You'll have 30 seconds to walk around and learn the true color of each sphere")
	info.visible(viz.ON)

	#hide instructions after 5 seconds
	yield viztask.waitTime(5)
	info.visible(viz.OFF)
	
	#let participant know learning phase has ended
	yield viztask.waitTime(30)
	info.setText("Please return to the center of the room to begin the testing phase")
	info.visible(viz.ON)

	#Start testing phase after 5 seconds
	yield viztask.waitTime(5)
	
#Insert def testphase():
	
def experiment():

	#Wait for spacebar to begin experiment
	yield viztask.waitKeyDown(' ')

	#Proceed through experiment phases
	participant = yield participantInfo()
	yield learnPhase()
	results = yield testPhase()