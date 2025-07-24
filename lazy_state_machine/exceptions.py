__all__ = ['InvalidFinalStateError', 'InvalidFinalStatesError', 
            'InvalidInitialStateError', 'InvalidStateError',
           'IllegalTransitionError', 'TransitionFunctionError']

class InvalidFinalStateError(Exception):
    pass

class InvalidFinalStatesError(Exception):
    pass

class InvalidInitialStateError(Exception):
    pass

class InvalidStateError(Exception):
    pass

class IllegalTransitionError(Exception):
    pass

class TransitionFunctionError(Exception):
    pass

