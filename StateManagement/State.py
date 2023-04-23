from typing import List, Union, Dict, Any, Iterable
from copy import deepcopy, copy
from abc import abstractmethod

# the state class exists to provide structured way of handling transitions into and out of game states on a frame-by-frame basis.
# the first time a game state is transitioned into, the "initialize" function is called
# after that, the "transitionIn" function is called
# then, the handle function is called. This handles state activities
# then, the getNextState function is called. If a state transition handles, transitionOut is called next. Otherwise, handle is called again next event by the StateMachine
# to check if the state has been transitioned to before, check isInitialized()
# When inheriting this class, there is no need to call super().__init__(). However, there is a need to call super().__new__() if ever overriding __new__.
class State:

    LOCAL_STATE_TYPE = Dict[Any, Any]

    # ensures that the name, localState, initialized attributes exist and are set so users don't have to remember to call super().__init__()
    # might be an anti-pattern, since technically it forces __init__ to be called *before* the child __init__ class, but that's not hard to undo
    # in my mind, this is worth it because it prevents a wide variety of bugs caused by simple coding errors
    # And this means that users (probably in the GMU psych department) don't really need to fully understand pythons data model.
    # They probably aren't overriding __new__ given what this class is for (it doesn't make sense to do anything other than the default __new__ behavior)
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        State.__init__(obj)
        cls.__init__(obj, *args, **kwargs)
        return obj

    def __init__(self):
        self.name = type(self).__name__
        self.localState = dict()
        self.initialized = False
        self.defaultMachineCopyStrategy = "deep"

    def getName(self) -> str:
        return self.name # use reflection by default to get the class name, since we essentially use it as a key

    def setName(self, name : str):
        self.name = name

    def setMachineCopyStrategy(self, copyStrategy : str):
        self.defaultMachineCopyStrategy = copyStrategy

    def getMachineCopyStrategy(self):
        return self.defaultMachineCopyStrategy

    # returns a shallow copy of local state
    # copyStrategy is a string or None
    # if copyStrategy == "shallow", only does a shallow copy of the dictionary
    # if copyStrategy == "deep", does a deep copy of the dictionary
    # if copyStrategy == None, does not copy and returns the original dictionary
    def getLocalState(self, copyStrategy : str = "reference") -> LOCAL_STATE_TYPE:
        if copyStrategy.lower() == "reference":
            return self.localState
        elif copyStrategy.lower() == "shallow":
            return copy(self.localState)
        elif copyStrategy.lower() == "deep":
            return deepcopy(self.localState)
        else:
            raise RuntimeError(f"{copyStrategy} is not a valid copy strategy, options are 'reference', 'shallow' or 'deep'")


    def setLocalState(self, localState : LOCAL_STATE_TYPE):
        self.localState = localState


    def isInitialized(self) -> bool:
        return self.initialized

    # called by state machines, calls initialize, then sets the initialized variable to true
    # this is to provide the ability to initialize the object's state after the game has started
    def _initialize(self, previousState : Union[None, str], otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        self.initialize(previousState, otherStates, globalValues)
        self.initialized = True

    # called before the first time this state is transitioned to for the first time
    def initialize(self, previousState : Union[None, str], otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        pass

    # called before the first time the handle function is called, but after initialize.
    # if this state has been transitioned to before, the localState will be the same as the previous time transitionOut was called.

    def transitionIn(self, previousState : Union[None, str], otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        pass

    # calls the handler
    # takes in global state, has access to the state configuration.
    # has read-only access to other state configurations through the state machine
    @abstractmethod
    def handle(self, event : Any, otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        return None

    # decides whether or not to change the current state
    # returns a State object to change to that State
    # returns None to stay in the current state.
    def getNextState(self, availableStates : List[str], otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> Union[str, None]:
        return None

    # called after the getNextState if the state has changed.
    # if this state has been transitioned to before, the localState will be the same as the previous time transitionOut was called.
    def transitionOut(self, nextState : str, otherStates : Dict[str, LOCAL_STATE_TYPE], globalValues : Dict[str, Any]) -> None:
        pass