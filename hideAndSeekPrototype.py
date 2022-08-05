from math import sqrt

import viz
import vizact
import vizinput
import steve

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

def sendPosition():

    #Retrieve current transform of viewpoint
    mat = viz.MainView.getMatrix()

    #Send position/rotation to target network object
    target_mailbox.send(action=updateGameState, quat=mat.getQuat(), pos=mat.getPosition())

# Start a timer that sends out data over the network every frame
vizact.ontimer(0,sendPosition)

def calculateDistance(p1, p2):
    vectorSquared = [(dims[0] - dims[1])**2 for dims in zip(p1, p2)]
    sumSquaredVector = sum(vectorSquared)
    return sqrt(sumSquaredVector)

def updateGameState(e):
    player_matrix.setPosition(e.pos)
    player_matrix.setQuat(e.quat)
    
    print(calculateDistance(e.pos, viz.MainView.getPosition()))

# Listens for any incomming messages
def onNetwork(e):
    if e.sender.upper() == target_machine:
        e.action(e)

# Register network to listen from incomming messages
viz.callback(viz.NETWORK_EVENT, onNetwork)
