from math import sqrt
from datetime import datetime, timedelta
from typing import List, Dict, Any
from threading import Thread
from os.path import join, abspath
from os import makedirs
from csv import DictWriter

import viz
import vizact
import vizinput
import steve

# Implements Game State Machine
class GameState:
    
    STARTING_SCREEN_TEXT = "Waiting for other player to connect..."
    START_TIME_COUNTDOWN = 10 # seconds
    GAME_DURATION = 30 # minutes
    GAME_END_THRESHOLD = 2
    SAVED_GAME_DIRECTORY = "."
    SEEKER_START_POSITION = [5, 2, 10]
    SEEKER_START_ATTITUDE = [-0.0, -0.7157255673177139, 0.0, 0.6983816379943968]
    HIDER_START_POSITION = [0, 0, -10]
    HIDER_START_ATTITUDE = [0, 0, 0, 1.0]
    
    SCREEN_TEXT_CENTER_ISH = [0.33,0.5,0]
    
    
    @staticmethod
    def saveGameStates(directory : str, history : List[Dict[str, Any]], otherHistory : List[Dict[str, Any]]):
        historyFileName = join(directory, "playerHistory.csv")
        otherHistoryFileName = join(directory, "otherHistory.csv")
        
        historyFields = [f for f in history[0].keys()]
        otherHistoryFields = [f for f in history[0].keys()]
        with open(historyFileName, "w", newline='') as csvfile:
            writer = DictWriter(csvfile, fieldnames=historyFields)
            writer.writeheader()
            writer.writerows(history)
            
        with open(otherHistoryFileName, "w", newline='') as csvfile:
            writer = DictWriter(csvfile, fieldnames=otherHistoryFields)
            writer.writeheader()
            writer.writerows(otherHistory)
        
    
    def __init__(self, playerName : str = "Bobward"):
        self.playerName = playerName
        self.player_matrix = viz.Matrix()
        self.avatar = steve.Steve()
        self.avatar.setTracker(self.player_matrix)
        self.history = list()
        self.otherPlayerHistory = list()
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
            "GAME_END_THRESHOLD" : type(self).GAME_END_THRESHOLD,
            "START_TIME_COUNTDOWN" : type(self).START_TIME_COUNTDOWN,
            "GAME_DURATION" : type(self).GAME_DURATION
        }
        self.otherPlayerState = {k : None for k in self.currentState.keys()}
        
        # not really part of game state (determines other features of game state)
        # NOT STARTED
        self.lastScreenTextUpdateTime = datetime.now()
        self.numDots = 3
        
        # Game saving thread
        self.gameSaveThread = None
    
    def getGameState(self):
        return self.currentState
    
    def updateGameState(self, event : viz.Event, eventType : str):
        if self.currentState["Game Stage"] != "Game Over":
            self.history.append(self.currentState.copy())
            self.currentState["Timestamp"] = datetime.now()
            self.currentState["Position"] = viz.MainView.getPosition()
            self.currentState["Attitude"] = viz.MainView.getQuat()
        
        if eventType == "Network":
            self.otherPlayerHistory.append(self.otherPlayerState)
            self.otherPlayerState = event
            self.player_matrix.setPosition(event["Position"])
            self.player_matrix.setQuat(event["Attitude"])
        elif eventType == "Frame Update":
            pass
            
        
        if self.currentState["Game Stage"] == "Not Started":
            self.updateGameNotStarted(event)
        elif self.currentState["Game Stage"] == "Connected Not Started":
            self.updateGameConnectedNotStarted(event)
        elif self.currentState["Game Stage"] == "Countdown":
            self.updateGameCountdown(event)
        elif self.currentState["Game Stage"] == "Playing":
            self.updateGamePlaying(event)
        elif self.currentState["Game Stage"] == "Game Over":
            self.updateGameOver(event)
    
    def getScreenText(self):
        return self.screenText
        
    def setScreenText(self, text):
        self.currentState["Screen Text"] = text
        self.screenText.message(text)
        
    def calculatePlayerDistances(self):
        squaredResiduals = [(dim-odim)**2 for dim, odim in zip(self.currentState["Position"], self.otherPlayerState["Position"])]
        return sum(squaredResiduals)
    
    # once a connection occurs, sets the location & role of the player character. Doesn't record the other game state yet.
    # after the connection occurs, the game state changes to "Connected Not Started"
    def updateGameNotStarted(self, event : Dict[str, Any]):
        if len(event.keys()) > 0:
            self.currentState["Game Stage"] = "Connected Not Started"
            # better hope they don't start at the same time.
            if event["Game Load Time"] > self.currentState["Game Load Time"]:
                self.currentState["Role"] = "Seeker"
                viz.MainView.setPosition(type(self).SEEKER_START_POSITION)
                viz.MainView.setQuat(type(self).SEEKER_START_ATTITUDE)
            elif event["Game Load Time"] < self.currentState["Game Load Time"]:
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
    
    def updateGameConnectedNotStarted(self, event : Dict[str, Any]):
        if self.currentState["Role"] == "Seeker":
            viz.MainView.setPosition(type(self).SEEKER_START_POSITION)
            viz.MainView.setQuat(type(self).SEEKER_START_ATTITUDE)
        else:
            viz.MainView.setPosition(type(self).HIDER_START_POSITION)
            viz.MainView.setQuat(type(self).HIDER_START_ATTITUDE)
            
        self.currentState["Game Stage"] = "Countdown"
        self.setScreenText(f"You are the {self.currentState['Role']}! Game starts in {self.currentState['START_TIME_COUNTDOWN']}...")
        self.currentState["Game Start Time"] = datetime.now() + timedelta(seconds=self.currentState['START_TIME_COUNTDOWN'])
        self.currentState["Game End Time"] = datetime.now() + timedelta(minutes=self.currentState['GAME_DURATION'], seconds=self.currentState["START_TIME_COUNTDOWN"])
        
    def updateGameCountdown(self, event : Dict[str, Any]):
        if self.currentState["Game Start Time"] > datetime.now():
            countDown = int((self.currentState["Game Start Time"] - datetime.now()).total_seconds())
            self.setScreenText(f"You are the {self.currentState['Role']}! Game starts in {countDown}...")
        else:
            self.setScreenText("Go!")
            self.getScreenText().setPosition(x=0.5, y=0.9)
            self.getScreenText().setScale(x=0.5, y=0.2)
            self.currentState["Game Stage"] = "Playing"
            viz.mouse.setOverride(viz.OFF)
    
    def updateGamePlaying(self, event : Dict[str, Any]):
        dt = datetime.now()
        if dt + timedelta(seconds=1) > self.currentState["Game Start Time"]:
            delta = self.currentState["Game End Time"] - dt
            minutes = delta.seconds // 60
            self.setScreenText(f"{minutes}:{int(delta.seconds) % 60}")
        
        if self.calculatePlayerDistances() < self.currentState["GAME_END_THRESHOLD"]:
            self.currentState["Game Stage"] = "Game Over"
            self.setScreenText(f"Game over! Seeker wins!")
        elif dt > self.currentState["Game End Time"]:
            self.currentState["Game Stage"] = "Game Over"
            self.setScreenText(f"Game over! Hider wins!")
        
            
    def updateGameOver(self, event : Dict[str, Any]):
        if self.gameSaveThread is None:
            saveDirectory = join(abspath(type(self).SAVED_GAME_DIRECTORY), self.playerName)
            makedirs(saveDirectory, exist_ok=True)
            self.gameSaveThread = Thread(target=type(self).saveGameStates, args=(saveDirectory, self.history, self.otherPlayerHistory))
            self.gameSaveThread.start()
        else:
            # Note to anyone editing this code - I haven't tried it but this funciton is called in an event loop
            # Generally, using join() or any other blocking call in an event loop is asking for trouble
            if not self.gameSaveThread.is_alive():
                viz.quit()
                    
        
    
# vizard code below this line
viz.setMultiSample(4)
viz.fov(60)
viz.MainView.collision( viz.ON )
viz.mouse.setOverride(viz.ON)
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

    #print(state.getGameState())
    #Send position/rotation to target network object
    target_mailbox.send(state.getGameState())
    
    state.updateGameState(dict(), "Frame Update")

# Start a timer that sends out data over the network every frame
vizact.ontimer(0,frameUpdate)

# Listens for any incomming messages
def onNetwork(e):
    if e.sender.upper() == target_machine:
        state.updateGameState(e[2], "Network")
        
# Register network to listen from incomming messages
viz.callback(viz.NETWORK_EVENT, onNetwork)