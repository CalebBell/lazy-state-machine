__all__ = [
    "IllegalTransitionError",
    "InvalidFinalStateError",
    "InvalidFinalStatesError",
    "InvalidInitialStateError",
    "InvalidInputTokenError",
    "InvalidStateError",
    "TransitionFunctionError",
]


class InvalidFinalStateError(Exception):
    pass


class InvalidFinalStatesError(Exception):
    pass


class InvalidInitialStateError(Exception):
    pass


class InvalidInputTokenError(Exception):
    pass


class InvalidStateError(Exception):
    pass


class IllegalTransitionError(Exception):
    pass


class TransitionFunctionError(Exception):
    pass
