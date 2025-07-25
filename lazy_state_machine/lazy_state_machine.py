from collections.abc import Iterable
from typing import Any, Callable, Optional

from lazy_state_machine.exceptions import (
    IllegalTransitionError,
    InvalidFinalStateError,
    InvalidFinalStatesError,
    InvalidInitialStateError,
    InvalidInputTokenError,
    InvalidStateError,
    TransitionFunctionError,
)


class LazyFiniteStateMachine:
    """Lazy finite state machine that uses a provided function
    to determine each state transition.

    Although this prevents any analysis to determine that the
    machine will not error on any set of inputs, it allows for the state machines
    to operate in any of the following cases:

    * The set of rules is larger than can fit in memory
    * Computing each step is computationally expensive, and there are too
      many symbols and rules to enumerate them efficiently
    * One or more of the rules is non-deterministic, e.g. a public source
      of verifiable randomness used for cryptographic purposes

    This class contains a stateless implementation to conveniently explore
    how different sets of inputs are processed.

    The machine begins at the initial state provided, a common use case
    (regex, networking, etc).

    The finite automaton state machine 5-tuple symbols (Q, sigma, q0, F, delta) are as follows:

    - Q: finite set of states
    - sigma: finite alphabet of input tokens
    - q0: Initial state, in Q
    - F: Final states, a subset of Q
    - delta: Transition function

    Parameters
    ----------
    transition_delta : Callable[[Any, Any], Any]
        Function that transitions the (current_state, input) to a
        new state. May raise IllegalTransitionError to indicate the
        finite state machine was not in fact correctly specified;
        any other errors are turned into a generic TransitionFunctionError
        and raised
    initial_state_q0 : Any
        Starting state, one of `all_states_Q`
    all_states_Q : frozenset[Any]
        Valid states, may be strings, enums, or any object implementing `__in__`
    final_states_F : Optional[frozenset[Any]]
        Valid final states, may be strings, enums, or any object implementing `__in__`;
        this must be a subset of `all_states_Q`. If not specified, all states will be
        considered valid outputs
    alphabet_sigma : Optional[frozenset[Any]]
        Valid input tokens; if provided, each input character will be required to
        be in this; can be omitted where this is not feasible, e.g.
        all integers or unicode characters including the supplementary planes

    Raises
    ------
    InvalidFinalStatesError
        If any of the specified final states is not in `all_states_Q`
    InvalidInitialStateError
        If any initial_state_q0 not in all_states_Q
    """

    def __init__(
        self,
        transition_delta: Callable[[Any, Any], Any],
        initial_state_q0: Any,
        all_states_Q: frozenset[Any],
        final_states_F: Optional[frozenset[Any]] = None,
        alphabet_sigma: Optional[frozenset[Any]] = None,
    ) -> None:
        self.transition_delta = transition_delta
        self.initial_state_q0 = initial_state_q0
        self.all_states_Q = all_states_Q

        # Convenient for some use cases - default final states to all states
        if final_states_F is None:
            final_states_F = all_states_Q
        self.final_states_F = final_states_F

        self.alphabet_sigma = alphabet_sigma

        # input validation - straightforward, included in __init__ to avoid overengineering
        for valid_final_state in self.final_states_F:
            if valid_final_state not in self.all_states_Q:
                raise InvalidFinalStatesError()

        if initial_state_q0 not in self.all_states_Q:
            raise InvalidInitialStateError()

    def process(self, inputs_sigma: Iterable[Any]) -> Any:
        """Process a provided input, starting with the
        initial state of the machine, and return the state
        after each input is processed. This method *doesn't* make
        the assumption that the last input is the *final*
        token; it provides visibility into intermediate states
        if a subset of the whole input is provided

        Parameters
        ----------
        inputs_sigma : Iterable[Any]
            Input symbols to process sequentially

        Returns
        -------
        Any
            Last state after processing all inputs

        Raises
        ------
        InvalidStateError
            If `current_state` or `new_state` is not in `all_states_Q`
        IllegalTransitionError
            If the provided `transition_delta` raises IllegalTransitionError
        TransitionFunctionError
            If the provided `transition_delta` raises any other exception
        """
        state = self.initial_state_q0
        for val in inputs_sigma:
            state = self.step(state, val)
        return state

    def process_and_check(self, inputs_sigma: Iterable[Any]) -> Any:
        """Process inputs and verify final state is accepting.

        Parameters
        ----------
        inputs_sigma : Iterable[Any]
            Input symbols to process sequentially

        Returns
        -------
        Any
            Final state if it's in final_states_F

        Raises
        ------
        InvalidFinalStateError
            If final state after processing `inputs_sigma` is not in `final_states_F`
        InvalidStateError
            If `current_state` or `new_state` is not in `all_states_Q`
        IllegalTransitionError
            If the provided `transition_delta` raises IllegalTransitionError
        TransitionFunctionError
            If the provided `transition_delta` raises any other exception
        """
        final_state = self.process(inputs_sigma)
        if final_state not in self.final_states_F:
            raise InvalidFinalStateError()
        return final_state

    def step(self, current_state: Any, input_symbol: Any) -> Any:
        """Process one input symbol, given a current state.

        Parameters
        ----------
        current_state : Any
            Current state
        input_symbol : Any
            Input symbol

        Returns
        -------
        Any
            Next state

        Raises
        ------
        InvalidStateError
            If `current_state` or `new_state` is not in `all_states_Q`
        IllegalTransitionError
            If the provided `transition_delta` raises IllegalTransitionError
        TransitionFunctionError
            If the provided `transition_delta` raises any other exception
        """
        if current_state not in self.all_states_Q:
            raise InvalidStateError()
        if self.alphabet_sigma is not None and input_symbol not in self.alphabet_sigma:
            raise InvalidInputTokenError()
        try:
            new_state = self.transition_delta(current_state, input_symbol)
        except IllegalTransitionError:
            raise
        except Exception:
            raise TransitionFunctionError() from None

        if new_state not in self.all_states_Q:
            raise InvalidStateError()

        return new_state
