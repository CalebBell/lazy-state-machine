import pytest
from enum import Enum
from lazy_state_machine.lazy_state_machine import LazyFiniteStateMachine
from lazy_state_machine.exceptions import IllegalTransitionError


class BinaryStringBit(Enum):
    zero = "0"
    one = "1"
    
    @staticmethod
    def bits_from_string(s):
        output = []
        for c in s:
            if c == "0":
                output.append(BinaryStringBit.zero)
            elif c == "1":
                output.append(BinaryStringBit.one)
            else:
                raise ValueError(f"Only binary strings accepted, found character `{c}`")
        return output

def test_mod_three_explicit():
    """Direct test case with hardcoded state transitions representing 
    a finite state machine that computes modulus 3 without using division
    via explicit pre-derived logic."""
    
    class States(Enum):
        S0 = "S0"
        S1 = "S1" 
        S2 = "S2"

    # State transition table for modulus 3 finite automaton
    state_transitions = {
        (States.S0, BinaryStringBit.zero): States.S0,
        (States.S0, BinaryStringBit.one): States.S1,
        (States.S1, BinaryStringBit.zero): States.S2,
        (States.S1, BinaryStringBit.one): States.S0,
        (States.S2, BinaryStringBit.zero): States.S1,
        (States.S2, BinaryStringBit.one): States.S2,
    }

    def explicit_transition_function(state, input_symbol):
        # States explicitly accounted for
        return state_transitions[(state, input_symbol)]

    machine = LazyFiniteStateMachine(
        transition_delta=explicit_transition_function,
        initial_state_q0=States.S0,
        all_states_Q=frozenset([States.S0, States.S1, States.S2]),
        final_states_F=frozenset([States.S0, States.S1, States.S2])
    )
    state_to_modulus_integer = {States.S0: 0, States.S1: 1, States.S2: 2}

    def check_modulus_3_fa(num):
        """Check if finite automaton correctly computes num % 3"""
        test_inputs = BinaryStringBit.bits_from_string(format(num, 'b'))
        calculated_mod_3_state = machine.process_and_check(test_inputs)
        calculated_mod_3 = state_to_modulus_integer[calculated_mod_3_state]
        correct_mod_3 = num % 3
        return calculated_mod_3 == correct_mod_3

    for n in range(1000):
        assert check_modulus_3_fa(n)