from lazy_state_machine.exceptions import IllegalTransitionError
from lazy_state_machine.lazy_state_machine import LazyFiniteStateMachine

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


def test_turnstile_simple():
    """This test case covers a turnstile, ending with a pushy customer who doesn't have
    a coin"""

    turnstile = LazyFiniteStateMachine(
        transition_delta=turnstile_transition_function,
        initial_state_q0="locked",
        all_states_Q=frozenset(turnstile_states),
        final_states_F=frozenset(turnstile_states),
        alphabet_sigma=frozenset(turnstile_inputs),
    )
    test_inputs = ["coin", "push", "coin", "push", "push", "push", "push"]
    final_state = turnstile.process_and_check(test_inputs)
    assert final_state == "locked"


def test_turnstile_debugging():
    """This test case shows how a developer might debug their implementation
    by manually testing inputs one at a time, e.g. in jupyter notebook"""
    turnstile = LazyFiniteStateMachine(
        transition_delta=turnstile_transition_function,
        initial_state_q0="locked",
        all_states_Q=frozenset(turnstile_states),
        final_states_F=frozenset(turnstile_states),
        alphabet_sigma=frozenset(turnstile_inputs),
    )

    assert turnstile.step("locked", "coin") == "unlocked"
    assert turnstile.step("locked", "push") == "locked"
    assert turnstile.step("unlocked", "coin") == "unlocked"
    assert turnstile.step("unlocked", "push") == "locked"
