from math import sqrt
from datetime import datetime

import viz
import vizact
import vizinput
import steve

# Implements Game State Machine
class GameState:
    
    STARTING_SCREEN_TEXT = "Waiting for other player to connect..."
    START_TIME_COUNTDOWN = 10
    GAME_END_THRESHOLD = 0.65
    SEEKER_START_POSITION = [5, 2, 10]
    SEEKER_START_ATTITUDE = [-0.0, -0.7157255673177139, 0.0, 0.6983816379943968]
    HIDER_START_POSITION = [-5, -2, 10]
    HIDER_START_ATTITUDE = [0, 0, 0, 1.0]
    
    SCREEN_TEXT_CENTER_ISH = [0.33,0.5,0]
    
    def __init__(self):
        self.history = list()
        loadTime = datetime.now()
        self.screenText = viz.addText(type(self).STARTING_SCREEN_TEXT, viz.SCREEN)
        self.screenText.setPosition(type(self).SCREEN_TEXT_CENTER_ISH)
        self.screenText.alignment = viz.ALIGN_CENTER_CENTER
        self.screenText.setScale(0.33, 0.33, 1, mode=viz.ABS_PARENT)
        self.currentState = {
            "Timestamp" : loadTime,
            "Game Stage" : "Not Started", 
            "Game Load Time" : loadTime,
            "Game End Time" : None,
            "Role" : None,
            "Game Start Time" : None,
            "Screen Text" : type(self).STARTING_SCREEN_TEXT,
            "Screen Text Position" : type(self).SCREEN_TEXT_CENTER_ISH,
            "Position" : viz.MainView.getPosition(),
            "Attitude" : viz.MainView.getQuat(),
            "Other Player Game State" : dict(),
            "GAME END THRESHHOLD" : 0.65,
            "START_TIME_COUNTDOWN" : 10
        }
        
        # not really part of game state (determines other features of game state)
        # NOT STARTED
        self.lastScreenTextUpdateTime = datetime.now()
        self.numDots = 3
    
    def getGameState(self):
        return self.currentState.copy()
    
    def updateGameState(self, event : viz.Event, eventType : str):
        self.history.append(self.currentState.copy())
        self.currentState["Timestamp"] = datetime.now()
        self.currentState["Position"] = viz.MainView.getPosition()
        self.currentState["Attitude"] = viz.MainView.getQuat()
        
        if eventType == "Network":
            if "Game State" in event:
                self.currentState["Other Player Game State"] = event["Game State"]            
        elif eventType == "Frame Update":
            pass
        
        if self.currentState["Game Stage"] == "Not Started":
            self.updateGameNotStarted(event)
    
    def getScreenText(self):
        return self.screenText
        
    def setScreenText(self, text):
        self.currentState["Screen Text"] = text
        self.screenText.message(text)
    
    # once a connection occurs, sets the location & role of the player character. Doesn't record the other game state yet.
    # after the connection occurs, the game state changes to "Connected Not Started"
    def updateGameNotStarted(self, event : viz.Event):
        if event.get("Game State", None) is not None:
            self.currentState["Game Stage"] = "Connected Not Started"
            # better hope they don't start at the same time.
            if event["Game State"]["Game Load Time"] < self.currentState["Game Load Time"]:
                self.currentState["Role"] = "Seeker"
                viz.MainView.setPosition(type(self).SEEKER_START_POSITION)
                viz.MainView.setQuat(type(self).SEEKER_START_ATTITUDE)
            elif event["Game State"]["Game Load Time"] > self.currentState["Game Load Time"]:
                self.currentState["Role"] = "Hider"
                viz.MainView.setPosition(type(self).HIDER_START_POSITION)
                viz.MainView.setQuat(type(self).HIDER_START_ATTITUDE)
            else:
                raise RuntimeError("Don't start the two computers at the same time!")
        else:
            timeSinceLastUpdate = (datetime.now() - self.lastScreenTextUpdateTime).total_seconds()
            if timeSinceLastUpdate >= 1.0:
                self.numDots = (self.numDots % 3) + 1
                self.setScreenText("Waiting for other player to connect" + (self.numDots*"."))
                self.lastScreenTextUpdateTime = datetime.now()
        
    
# vizard code below this line
viz.setMultiSample(4)
viz.fov(60)
viz.MainView.collision( viz.ON )
#viz.mouse.setOverride(viz.ON)
viz.go()

# Add the world
maze = viz.addChild('maze.osgb')

# The game state object modifies vizard state on creation, so we should probably 
state = GameState()

#Use a prompt to ask the user the network name of the other computer.
target_machine = vizinput.input('Enter the name of the other machine').upper()
#Add a mailbox from which to send messages. This is your outbox.
target_mailbox = viz.addNetwork(target_machine)

def frameUpdate():

    #Retrieve current transform of viewpoint
    mat = viz.MainView.getMatrix()

    #Send position/rotation to target network object
    target_mailbox.send(gameState=state.getGameState())
    
    state.updateGameState(dict(), "Frame Update")
    
    print(mat.getQuat())

# Start a timer that sends out data over the network every frame
vizact.ontimer(0,frameUpdate)

# Listens for any incomming messages
def onNetwork(e):
    if e.sender.upper() == target_machine:
        state.updateGameState(e, "Network")
        
# Register network to listen from incomming messages
viz.callback(viz.NETWORK_EVENT, onNetwork)