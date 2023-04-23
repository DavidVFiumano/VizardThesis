import inspect
from typing import Iterable, List, Union, Dict, Any, Tuple, Optional
from copy import deepcopy

from .State import State

# essentially a directed graph between added state objects
# to avoid bugs caused by forgetting to call super().__init__(), this class also implements a __new__() method
# I don't think that it's super likely that users will want to override __new__().
# That said, if you do override __new__, be sure that the child implementation creates the same object attributes as this class does or things may break.
class StateMachine:
    
    def buildStateGraphFromStateList(self, states : List[Tuple[State, List[State]]]):
        if len(states) == 0:
            return
            
        for state, nextStates in states:
            self.addState(state)
        
        self.setStartingState(states[0][0].getName())

        for state, nextStates in states:
            if nextStates is not None:
                for nextState in nextStates:
                    self.addForwardConnection(state.getName(), nextState.getName())

    def __init__(self, states : List[Tuple[State, List[State]]] = list()):
        self.stateGraph = dict()
        self.otherStateCache : Optional[Dict[str, State.LOCAL_STATE_TYPE]] = None
        self.currentState : Optional[str] = None
        self.previousState : Optional[str] = None
        self.globalValues : Dict[str, Any] = dict()
        self.transitionedOutLastTick = True
        self.buildStateGraphFromStateList(states)

    def __new__(cls, args : Iterable[Any] = list(), kwargs : Dict[str, Any] = dict()):
        obj = object.__new__(cls)
        StateMachine.__init__(obj)
        return obj

    def getCurrentState(self) -> Optional[str]:
        return self.currentState

    # theoretically an expensive funciton, but deep copying prevents bugs so I'm good with this trade
    # if you don't want a deep copy, you can always access the variable directly anyway
    def getGlobalValues(self) -> Dict[str, Any]:
        return deepcopy(self.globalValues)
    
    def setGlobalValue(self, key : str, value : Any):
        self.globalValues[key] = value

    def getAvailableStates(self) -> List[str]:
        return list(self.stateGraph.keys())

    def hasState(self, state : str):
        if isinstance(state, str):
            return state in self.stateGraph.keys() 
        else:
            raise TypeError(f"{state} object is the wrong type for {inspect.stack()[3]}. Must be a string not a {type(state)}.")

    def getState(self, state : str) -> State:
        if isinstance(state, str):
            return self.stateGraph[state]["State"] 
        else:
            raise TypeError(f"{state} object is the wrong type for {inspect.stack()[3]}. Must be a string not a {type(state)}.")

    def getNextStates(self, existingState : str) -> List[str]:
        if not self.hasState(existingState):
            raise RuntimeError(f"State {existingState} isn't in this state machine, no next states can be found.")

        return [s for s in self.stateGraph[existingState]["Next"]] 

    def getPreviousStates(self, existingState : str) -> List[State]:
        if not self.hasState(existingState):
            raise RuntimeError(f"State {existingState} isn't in this state machine, no next states can be found.") 

        return self.stateGraph[existingState]["Previous"] 

    def addState(self, state : State, nextStates : Union[Iterable[str], str, None] = None, previousStates : Union[Iterable[str], str, None] = None):
        
        if self.hasState(state.getName()):
            raise RuntimeError(f"State called {state.getName()} already in state machine.")

        previousStates = previousStates if previousStates is not None else list()
        nextStates = nextStates if nextStates is not None else list()

        # first, ensure that previousStates and nextStates are already in the graph
        if previousStates is not None:
            previousStateList = [previousStates] if isinstance(previousStates, str) else previousStates
        
        if nextStates is not None:
            nextStateList = [nextStates] if isinstance(nextStates, str) else nextStates

        graphNode = {
            "Next" : {nextState : nextState for nextState in nextStateList},
            "Previous" : {previousState : previousState for previousState in previousStateList},
            "State" : state
        }

        self.stateGraph[state.getName()] = graphNode 

    def addForwardConnection(self, existingState : str, nextState : str):
        if not self.hasState(existingState):
            raise RuntimeError(f"{existingState} not in the list of existing states, you may want to use addState() instead.")
            
        if not self.hasState(nextState):
            raise RuntimeError(f"A forward connection cannot be added, {nextState} is not in the state machine yet.")

        self.stateGraph[nextState]["Previous"][existingState] = existingState 
        self.stateGraph[existingState]["Next"][nextState] = nextState 
    
    def addReverseConnection(self, existingState : str, previousState : str):
        if not self.hasState(existingState):
            raise RuntimeError(f"{existingState} not in the list of existing states, you may want to use addState() instead.")
            
        if not self.hasState(previousState):
            raise RuntimeError(f"A reverse connection cannot be added, {previousState} is not in the state machine yet.")
        
        self.stateGraph[existingState]["Previous"][previousState] = previousState 
        self.stateGraph[previousState]["Next"][existingState] = existingState 

    def removeForwardConnection(self, state : str, nextState : str):
        if not self.hasState(state):
            raise RuntimeError(f"{state} not in the list of existing states, so no connections can be removed.")

        if not self.hasState(nextState):
            raise RuntimeError(f"{nextState} not in the list of existing states, so no connections can be removed.")

        self.stateGraph[state]["Next"].pop(nextState) 
        self.stateGraph[nextState]["Previous"].pop(state) 

    def removeReverseConnection(self, state : str, previousState : str):
        if not self.hasState(state):
            raise RuntimeError(f"{state} not in the list of existing states, so no connections can be removed.")

        if not self.hasState(previousState):
            raise RuntimeError(f"{previousState} not in the list of existing states, so no connections can be removed.")

        self.stateGraph[previousState]["Next"].pop(state) 
        self.stateGraph[state]["Previous"].pop(previousState) 
        
    def disconnectState(self, existingState : str):
        if not self.hasState(existingState):
            raise RuntimeError(f"Cannot remove a state that isn't already in the machine, {existingState} must be first added before it can be removed.")

        for nextState in self.stateGraph[existingState]["Next"]: 
            self.removeForwardConnection(existingState, nextState)
        
        for previousState in self.stateGraph[existingState]["Previous"]: 
            self.removeReverseConnection(existingState, previousState)

    def removeState(self, existingState : str) -> State:
        if not self.hasState(existingState):
            raise RuntimeError(f"Cannot remove a state that isn't already in the machine, {existingState} must be first added before it can be removed.")

        self.disconnectState(existingState)

        return self.stateGraph.pop(existingState) 

    def setStartingState(self, existingState : str):
        if not self.hasState(existingState):
            raise RuntimeError(f"State {existingState} is not in the state machine, please select an existing state. Options are {self.getAvailableStates()}.")

        self.currentState = existingState

    def update(self, event : Any):
        currentState = self.getCurrentState()
        if currentState is None:
            raise RuntimeError(f"No starting state is set, please set a start state! Options are {self.getAvailableStates()}.")

        if self.otherStateCache is None:
            self.otherStateCache = {state : self.stateGraph[state]["State"].getLocalState(copyStrategy=self.stateGraph[state]["State"].getMachineCopyStrategy()) 
                                        for state in self.getAvailableStates() 
                                        if state != currentState}

        currentStateObj : State = self.stateGraph[currentState]["State"]
        if not currentStateObj.isInitialized():
            currentStateObj._initialize(self.previousState, self.otherStateCache, self.globalValues)

        if self.transitionedOutLastTick:
            currentStateObj.transitionIn(self.previousState, self.otherStateCache, self.globalValues)

        currentStateObj.handle(event, self.otherStateCache, self.globalValues)
        
        nextState = currentStateObj.getNextState(self.getNextStates(currentState), self.otherStateCache, self.globalValues)
        if nextState is None: # if we don't need to change the state, return None
            self.transitionedOutLastTick = False
            return

        # handle state transition
        if not isinstance(nextState, str):
            raise RuntimeError(f"Object of type {type(nextState)} was returned by the getNextState() function by state {self.currentState} (defined at {type(self.stateGraph).__qualname__}) was not a string. The returned value has to be a string!")
        
        currentStateObj.transitionOut(self.stateGraph[nextState], self.otherStateCache, self.globalValues)
        self.transitionedOutLastTick = True
        self.otherStateCache[currentState] = currentStateObj.getLocalState(currentStateObj.getMachineCopyStrategy())
        self.otherStateCache.pop(nextState)
        
        self.previousState = self.currentState
        self.currentState = nextState