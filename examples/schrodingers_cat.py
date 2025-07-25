"""
Example of a non-deterministic finite state machine.
This is a variant of the Schrodinger's cat problem that allows for
multiple time steps, with the probability of the cat surviving all time
steps being 2**-time_steps.

A lab safety toggle is available which ensures the finite state machine
can only perform experiments which do not kill the cat.
"""

import argparse
import sys
from enum import Enum
from random import randint

from lazy_state_machine.exceptions import InvalidFinalStateError
from lazy_state_machine.lazy_state_machine import LazyFiniteStateMachine


class CatStatus(Enum):
    ALIVE = "alive"
    DEAD = "dead"


class TimeInput(Enum):
    ATOM_HALF_LIFE = "atom_half_life"


def create_schrodingers_fsm(lab_safety: bool = False) -> LazyFiniteStateMachine:
    all_states = frozenset([CatStatus.ALIVE, CatStatus.DEAD])
    final_states = frozenset([CatStatus.ALIVE]) if lab_safety else all_states

    def transition_function(state: CatStatus, input_symbol: TimeInput) -> CatStatus:
        if state == CatStatus.DEAD:
            return CatStatus.DEAD
        if state == CatStatus.ALIVE:
            # 50/50
            if randint(0, 1):
                return CatStatus.DEAD
            return CatStatus.ALIVE

    return LazyFiniteStateMachine(
        transition_delta=transition_function,
        initial_state_q0=CatStatus.ALIVE,
        all_states_Q=all_states,
        final_states_F=final_states,
        alphabet_sigma=frozenset([TimeInput.ATOM_HALF_LIFE]),
    )


def main():
    parser = argparse.ArgumentParser(description="Cat in a box!")
    parser.add_argument(
        "--nap-durations",
        type=int,
        default=1,
        dest="nap_durations",
        help="Number of radioactive decay half-lives the cat naps for",
    )
    parser.add_argument("--lab-safety", action="store_true", help="Enable lab safety mode")

    args = parser.parse_args()
    fsm = create_schrodingers_fsm(lab_safety=args.lab_safety)
    inputs = [TimeInput.ATOM_HALF_LIFE] * args.nap_durations

    try:
        final_state = fsm.process_and_check(inputs)
    except InvalidFinalStateError:
        print("The FSM's state after processing input is not in accepting")
        print("Destroying this quantum reality...")
        sys.exit(1)

    if final_state == CatStatus.ALIVE:
        print("The cat saunters out of the box, never knowing it was in any peril.")
    else:
        print("Cruel world! The poison gas is released; the innocent cat dies.")
        print(
            "Your colleagues report you to the university ethics department and you are dismissed from your academic program."
        )


if __name__ == "__main__":
    main()
