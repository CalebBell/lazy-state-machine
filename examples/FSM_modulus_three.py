"""
Demonstration of the FSM applied to compute modulus three.
"""

from lazy_state_machine.lazy_state_machine import LazyFiniteStateMachine

# An explanation for how to derive the state transitions for a given modulus can be found at
# https://electronics.stackexchange.com/questions/345189/vhdl-interview-question-detecting-if-a-number-can-be-divided-by-5-without-rema
STATE_TRANSITIONS = {
    ("S0", "0"): "S0",
    ("S0", "1"): "S1",
    ("S1", "0"): "S2",
    ("S1", "1"): "S0",
    ("S2", "0"): "S1",
    ("S2", "1"): "S2",
}

ALL_STATES = frozenset(["S0", "S1", "S2"])

FSM = LazyFiniteStateMachine(
    transition_delta=lambda state, input_symbol: STATE_TRANSITIONS[(state, input_symbol)],
    initial_state_q0="S0",
    all_states_Q=ALL_STATES,
    final_states_F=ALL_STATES,
)

STATE_TO_MOD = {"S0": 0, "S1": 1, "S2": 2}


def mod_three(binary_string: str) -> int:
    if not isinstance(binary_string, str):
        raise ValueError("Modulus is computed on strings of `1` and `0` - please provide one")
    if len(binary_string) == 0:
        raise ValueError("Please provide an input number")
    final_state = FSM.process_and_check(binary_string)
    return STATE_TO_MOD[final_state]


if __name__ == "__main__":
    spacing = 8
    print("Finite State Machine: Modulus 3 example\n")
    print("Number   | Binary  | FSM     | CPython")
    print((("-" * (spacing + 1) + "|") * 4)[:-1])

    for i in range(16):
        binary = format(i, "b")
        fsm_result = mod_three(binary)
        std_result = i % 3
        print(f"{i:>{spacing}} |{binary:>{spacing}} |{fsm_result:>{spacing}} |{std_result:>{spacing}}")
