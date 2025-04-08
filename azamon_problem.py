from typing import Generator

from aima.search import Problem

from azamon_operators import AzamonOperator
from azamon_state import StateRepresentation


class Azamon(Problem):
    def __init__(self, initial_state: StateRepresentation):
        super().__init__(initial_state)

    def actions(self, state: StateRepresentation) -> Generator[AzamonOperator, None, None]:
        if state.params.experiment == 1:
            return state.generate_actions()
        elif state.params.experiment == 2:
            return state.generate_one_action()

    def result(self, state: StateRepresentation, action: AzamonOperator) -> StateRepresentation:
        return state.apply_action(action)

    def value(self, state: StateRepresentation) -> float:
        if state.params.heuristica == 1:
            return -state.heuristic1()
        if state.params.heuristica == 2:
            return -state.heuristic2()

    def goal_test(self, state: StateRepresentation) -> bool:
        return False
