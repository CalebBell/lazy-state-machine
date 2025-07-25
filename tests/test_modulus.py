from enum import Enum

from lazy_state_machine.exceptions import IllegalTransitionError
from lazy_state_machine.lazy_state_machine import LazyFiniteStateMachine


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
        final_states_F=frozenset([States.S0, States.S1, States.S2]),
    )
    state_to_modulus_integer = {States.S0: 0, States.S1: 1, States.S2: 2}

    # Specific test "110"  -> 0
    example1_inputs = BinaryStringBit.bits_from_string("110")
    example1_final_state = machine.process_and_check(example1_inputs)
    example1_result = state_to_modulus_integer[example1_final_state]
    assert example1_result == 0

    # Specific test "1010" -> 1
    example2_inputs = BinaryStringBit.bits_from_string("1010")
    example2_final_state = machine.process_and_check(example2_inputs)
    example2_result = state_to_modulus_integer[example2_final_state]
    assert example2_result == 1

    def check_modulus_3_fa(num):
        """Check if finite automaton correctly computes num % 3"""
        test_inputs = BinaryStringBit.bits_from_string(format(num, "b"))
        calculated_mod_3_state = machine.process_and_check(test_inputs)
        calculated_mod_3 = state_to_modulus_integer[calculated_mod_3_state]
        correct_mod_3 = num % 3
        return calculated_mod_3 == correct_mod_3

    for n in range(1000):
        assert check_modulus_3_fa(n)


def test_modulus_dynamic():
    """This test makes a general purpose state machine to compute the modulus
    of an integer using the bit linear-time calculation concept.

    Although the dynamic state transition function uses the modulus operator,
    it only needs to compute the modulus of numbers up to the modulus number.

    I was curious if it was possible to beat e.g. Python's arbitrary-size integer
    modulus implementation using for example

    example_mersenne_prime = 2**110503 -1
    example_large_modulus = 86243

    Unsurprisingly, Python's implementation was already more efficient
    (3000x in this case).
    """

    def create_dynamic_modulus_machine(modulus):
        def dynamic_transition_function(current_state, input_symbol):
            # guarded from invalid input symbols via our specified alphabet
            if input_symbol == BinaryStringBit.zero:
                bit_value = 0
            elif input_symbol == BinaryStringBit.one:
                bit_value = 1

            # Algorithm from
            # https://electronics.stackexchange.com/questions/345189/vhdl-interview-question-detecting-if-a-number-can-be-divided-by-5-without-rema
            next_state = (current_state * 2 + bit_value) % modulus

            # Example of a case we might want to raise - mathematically this will not happen,
            # but who knows when a bit flip will make it so?
            if next_state < 0 or next_state >= modulus:
                raise IllegalTransitionError(f"Invalid state transition attempted: {next_state}")
            return next_state

        # States are 0 through modulus-1
        all_states = frozenset(range(modulus))

        return LazyFiniteStateMachine(
            transition_delta=dynamic_transition_function,
            alphabet_sigma=frozenset([BinaryStringBit.zero, BinaryStringBit.one]),
            initial_state_q0=0,  # for all cases here
            all_states_Q=all_states,  # all states are valid
        )

    def check_modulus_dynamic(num, modulus):
        machine = create_dynamic_modulus_machine(modulus)
        test_inputs = BinaryStringBit.bits_from_string(format(num, "b"))
        calculated_remainder = machine.process_and_check(test_inputs)
        correct_remainder = num % modulus
        return calculated_remainder == correct_remainder

    # Exhaustively check our code is correct for modulus up to 13, n up to 100
    for modulus in range(1, 14):
        for n in range(101):
            assert check_modulus_dynamic(n, modulus)
