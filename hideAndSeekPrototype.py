from math import sqrt
from datetime import now

import viz
import vizact
import vizinput
import steve

# CONSTANTS
START_TIMER_ID = 0
GAME_END_THRESHOLD = 0.65
START_TIME_COUNTDOWN = 10

# game state variables
gameStarted = False
vizardLoadTime = now()
screenText = viz.addText("Waiting for other player to connect...", parent=SCREEN)
startCountDown = START_TIME_COUNTDOWN
gameRole = None

# vizard code below this line
viz.setMultiSample(4)
viz.fov(60)
viz.MainView.collision( viz.ON )
viz.go()

# Use the steve module to represent the other user.
# You will actually have no representation of yourself on your own monitor.
player_matrix = viz.Matrix()
avatar = steve.Steve()
avatar.setTracker(player_matrix)

# Add the world
maze = viz.addChild('maze.osgb')

#Use a prompt to ask the user the network name of the other computer.
target_machine = vizinput.input('Enter the name of the other machine').upper()

#Add a mailbox from which to send messages. This is your outbox.
target_mailbox = viz.addNetwork(target_machine)

def sendUpdates():

    if gameStarted:
        #Retrieve current transform of viewpoint
        mat = viz.MainView.getMatrix()

        #Send position/rotation to target network object
        target_mailbox.send(action=updateGameState, quat=mat.getQuat(), pos=mat.getPosition())
    else:
        target_mailbox.send(action=startGame, otherStartTime=vizardLoadTime)

# Start a timer that sends out data over the network every frame
vizact.ontimer(0,sendPosition)

def calculateDistance(p1, p2):
    vectorSquared = [(dims[0] - dims[1])**2 for dims in zip(p1, p2)]
    sumSquaredVector = sum(vectorSquared)
    return sqrt(sumSquaredVector)

def updateGameState(e):
    player_matrix.setPosition(e.pos)
    player_matrix.setQuat(e.quat)
    
    playerDistance = calculateDistance(e.pos, viz.MainView.getPosition())
    if playerDistance < GAME_END_THRESHOLD:
        viz.quit()

# Listens for any incomming messages
def onNetwork(e):
    if e.sender.upper() == target_machine:
        e.action(e)

# handles any and all timers
def onTimer(timerID):
    if timerID == START_TIMER_ID:
        if startCountDown > 0:
            screenText.message = f"{startCountDown}..."
            startCountDown -= 1
        elif startCountDown == 0:
            screenText.message = f"You are the {gameRole}. Go!"
            startCountDown = -1
            viz.mouse.setOverride(state=viz.OFF)
            gameStarted = True
        elif startCountDown == -1:
            screenText.message = ""

def startCountdownTimer(e):
    if e.sender.upper() == target_machine:
        viz.starttimer(timer=START_TIMER_ID, time=1, repeats=START_TIME_COUNTDOWN)
    

def decideRole(otherStartTime):
    if vizardLoadTime < otherStartTime:
        gameRole = "Seeker"
    else:
        gameRole = "Hider"

def startGame(e):
    decideRole(e.otherStartTime)
    startCountdownTimer(e)

# Causes the game to wait for a player to connect.
def waitForPlayer(e):
    print("Waiting...")
    viz.addText("Waiting for other player to connect...", parent=viz.SCREEN)
    viz.mouse.setOverride()
    

# Register network to listen from incomming messages
viz.callback(viz.NETWORK_EVENT, onNetwork)
viz.callback(viz.INIT_EVENT, waitForPlayer)