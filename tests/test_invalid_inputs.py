import pytest

from lazy_state_machine.exceptions import (
    IllegalTransitionError,
    InvalidFinalStateError,
    InvalidFinalStatesError,
    InvalidInitialStateError,
    InvalidInputTokenError,
    InvalidStateError,
    TransitionFunctionError,
)
from lazy_state_machine.lazy_state_machine import LazyFiniteStateMachine

"""
This file covers edge cases, and ensures the exceptions
are raised if invalid user input is provided.
"""

turnstile_states = ["locked", "unlocked"]
turnstile_inputs = ["coin", "push"]
turnstile_state_transitions = {
    ("locked", "coin"): "unlocked",
    ("locked", "push"): "locked",
    ("unlocked", "coin"): "unlocked",
    ("unlocked", "push"): "locked",
}


def turnstile_transition_function(state, input_symbol):
    if (state, input_symbol) not in turnstile_state_transitions:
        raise IllegalTransitionError(f"Invalid transition from {state} with input {input_symbol}")
    return turnstile_state_transitions[(state, input_symbol)]


def broken_transition_function(state, input_symbol):
    raise ValueError("TODO")


def test_illegal_transition_error():
    surprise_input = "surprise_input"
    machine = LazyFiniteStateMachine(
        transition_delta=turnstile_transition_function,
        initial_state_q0="locked",
        all_states_Q=frozenset(turnstile_states),
        alphabet_sigma=frozenset([*turnstile_inputs, surprise_input]),
    )

    with pytest.raises(IllegalTransitionError):
        machine.step("locked", surprise_input)


def test_invalid_final_state_error():
    machine = LazyFiniteStateMachine(
        transition_delta=turnstile_transition_function,
        initial_state_q0="locked",
        all_states_Q=frozenset(turnstile_states),
        final_states_F=frozenset(["locked"]),  # At night the machines should be locked
    )

    with pytest.raises(InvalidFinalStateError):
        machine.process_and_check(["coin"])


def test_invalid_final_states_error():
    with pytest.raises(InvalidFinalStatesError):
        LazyFiniteStateMachine(
            transition_delta=turnstile_transition_function,
            initial_state_q0="locked",
            all_states_Q=frozenset(turnstile_states),
            final_states_F=frozenset(["broken_state"]),  # Final state not in states
        )


def test_invalid_initial_state_error():
    with pytest.raises(InvalidInitialStateError):
        LazyFiniteStateMachine(
            transition_delta=turnstile_transition_function,
            initial_state_q0="broken_initial",  # Not in all_states_Q
            all_states_Q=frozenset(turnstile_states),
        )


def test_invalid_state_error():
    def invalid_state_transition_function(state, input_symbol):
        return "What states are we supposed to support again?"

    machine = LazyFiniteStateMachine(
        transition_delta=invalid_state_transition_function,
        initial_state_q0="locked",
        all_states_Q=frozenset(turnstile_states),
    )

    with pytest.raises(InvalidStateError):
        machine.step("locked", "coin")


def test_transition_function_error():
    machine = LazyFiniteStateMachine(
        transition_delta=broken_transition_function,
        initial_state_q0="locked",
        all_states_Q=frozenset(turnstile_states),
    )

    with pytest.raises(TransitionFunctionError):
        machine.step("locked", "coin")


def test_invalid_input_token_error():
    machine = LazyFiniteStateMachine(
        transition_delta=turnstile_transition_function,
        initial_state_q0="locked",
        all_states_Q=frozenset(turnstile_states),
        alphabet_sigma=frozenset(["coin"]),  # no push, only 'coin'
    )

    with pytest.raises(InvalidInputTokenError):
        machine.step("locked", "push")  # accidental push


def test_invalid_current_state_error():
    machine = LazyFiniteStateMachine(
        transition_delta=turnstile_transition_function,
        initial_state_q0="locked",
        all_states_Q=frozenset(turnstile_states),
        final_states_F=frozenset(["locked"]),
    )

    with pytest.raises(InvalidStateError):
        machine.step("broken by an angry customer", "coin")
