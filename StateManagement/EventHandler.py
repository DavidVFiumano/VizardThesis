from inspect import signature
from typing import Any, List, Union, Iterable, Callable, Optional
from traceback import print_exc

from .StateMachine import StateMachine

class EventHandler:
    
    CALLBACK_FUNCTION_TYPE = Callable[[Any], Optional[Any]]

    @staticmethod
    def __checkCallable(obj : Any) -> bool:
        if not callable(obj):
            return False
        fun = signature(obj)
        if len(fun.parameters) == 1:
            return True
        else:
            return False

    @staticmethod
    def defaultOnError(error : Exception):
        print_exc()

    def __init__(self, callbacks : Union[List[Union[StateMachine, CALLBACK_FUNCTION_TYPE]], StateMachine, CALLBACK_FUNCTION_TYPE], onError : Union[Callable[[Exception], None], None] = None):
        self.errorHandler : Union[Callable[[Exception], None], None] = onError if onError is not None else type(self).defaultOnError
        self.callbacks = list()
        if isinstance(callbacks, Iterable):
            for i, callback in enumerate(callbacks):
                if not isinstance(callback, StateMachine) and not type(self).__checkCallable(callback):
                    raise TypeError(f"Item at index {i} in list passed to EventHandler.__init__() is not a StateMachine object or a funciton matching {type(self).CALLBACK_FUNCTION_TYPE}, it is {type(callback)} which does not extend StateMachine. Please pass only StateMachine object or callables with the correct signature!")
            self.callbacks = list(callbacks)
        elif isinstance(callbacks, StateMachine):
            self.callbacks = [callbacks]
        elif type(self).__checkCallable(callbacks):
            self.callbacks = [callbacks]
        else:
            raise TypeError(f"Pass either an iterable of StateMachine objects/callback functions or a single StateMachine/callback function object to EventHandler.__init__(), not a {type(callbacks)} object. Standalone callable functions must match this signature {type(self).CALLBACK_FUNCTION_TYPE}")

    def handle(self, event : Any):
        for callback in self.callbacks:
            try:
                if isinstance(callback, StateMachine):
                    callback.update(event)
                else:
                    callback(event)
            except Exception as e:
                self.errorHandler(e)

    def callback(self, function : Callable[..., Optional[Any]]) -> Callable[..., Optional[Any]]:
        def wrapper(*args, **kwargs):
            ret = function(*args, **kwargs)
            self.handle(ret)
            return ret
        return wrapper