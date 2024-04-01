"""
Finite State Machine

author: Taiga Arai (@araitaiga)

Ref:

- [AI for Games, Third Edition]
(https://www.oreilly.com/library/view/ai-for-games/9781351053280/)

"""

from abc import abstractmethod, ABC
from enum import Enum


class ClockCounter:
    time_now = 0

    @classmethod
    def count_up(cls):
        cls.time_now += 1
        if cls.time_now >= 12:
            cls.time_now = 0

    @classmethod
    def get_time(cls):
        return cls.time_now


class Action(ABC):
    @abstractmethod
    def execute(self):
        pass


class GreetingAction(Action):
    def __init__(self):
        pass

    def execute(self):
        print("[Action] Hello")


class ChatterAction(Action):
    def __init__(self, message):
        self.message = message

    def execute(self):
        print("[Action]", self.message, "Chatter!!!")


class QuietAction(Action):
    def __init__(self, message):
        self.message = message

    def execute(self):
        print("[Action]", self.message, "Quiet...")


class DummyAction(Action):
    def __init__(self, message):
        self.message = message

    def execute(self):
        print("[Action]", self.message, "Dummy")


class Condition(ABC):
    @abstractmethod
    def test(self):
        pass


class TimeRange:
    def __init__(self, time_min, time_max):
        self.time_min = time_min
        self.time_max = time_max


class TimeRangeCondition(Condition):
    def __init__(self, time_ranges):
        self.time_ranges = time_ranges

    def __within_time_range(self, time_range, now):
        return now >= time_range.time_min and now <= time_range.time_max

    def test(self):
        now = ClockCounter.get_time()
        for time_range in self.time_ranges:
            if self.__within_time_range(time_range, now):
                return True


class StateType(Enum):
    CHATTER = 1
    QUIET = 2
    DUMMY = 3


class StateBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build(state_type):
        if state_type == StateType.CHATTER:
            return ChatterState()
        elif state_type == StateType.QUIET:
            return QuietState()
        elif state_type == StateType.DUMMY:
            return DummyState()
        else:
            raise ValueError("Invalid StateType")


class State(ABC):
    @abstractmethod
    def get_actions(self):
        pass

    @abstractmethod
    def get_entry_actions(self):
        pass

    @abstractmethod
    def get_exit_actions(self):
        pass

    @abstractmethod
    def get_transitions(self):
        pass


class ChatterState(State):
    def __init__(self):
        print("ChatterState is initialized")
        self.actions = [GreetingAction(), ChatterAction("State")]
        self.entry_actions = [ChatterAction("Entry")]
        self.exit_actions = [ChatterAction("Exit")]
        self.transitions = [ChatterTransition()]

    def get_actions(self):
        return self.actions

    def get_entry_actions(self):
        return self.entry_actions

    def get_exit_actions(self):
        return self.exit_actions

    def get_transitions(self):
        return self.transitions


class QuietState(State):
    def __init__(self):
        print("QuietState is initialized")
        self.actions = [QuietAction("State")]
        self.entry_actions = [QuietAction("Entry")]
        self.exit_actions = [QuietAction("Exit")]
        self.transitions = [QuietTransition()]

    def get_actions(self):
        return self.actions

    def get_entry_actions(self):
        return self.entry_actions

    def get_exit_actions(self):
        return self.exit_actions

    def get_transitions(self):
        return self.transitions


class DummyState(State):
    def __init__(self):
        print("DummyState is initialized")
        self.actions = [DummyAction("State")]
        self.entry_actions = [DummyAction("Entry")]
        self.exit_actions = [DummyAction("Exit")]
        self.transitions = [DummyTransition()]

    def get_actions(self):
        return self.actions

    def get_entry_actions(self):
        return self.entry_actions

    def get_exit_actions(self):
        return self.exit_actions

    def get_transitions(self):
        return self.transitions


class Transition(ABC):
    @abstractmethod
    def is_triggered(self):
        pass

    @abstractmethod
    def get_actions(self):
        pass

    @abstractmethod
    def get_target_state(self):
        pass


class ChatterTransition(Transition):
    def __init__(self):
        self.actions = [ChatterAction("Transition from")]

        self.target_state_quiet = StateType.QUIET
        self.target_state_dummy = StateType.DUMMY
        self.to_quiet_condition = TimeRangeCondition([TimeRange(2, 2)])
        self.to_dummy_condition = TimeRangeCondition([TimeRange(6, 6)])

    def is_triggered(self):
        return self.to_quiet_condition.test() or self.to_dummy_condition.test()

    def get_actions(self):
        return self.actions

    def get_target_state(self):
        if self.to_quiet_condition.test():
            return self.target_state_quiet
        elif self.to_dummy_condition.test():
            return self.target_state_dummy
        else:
            return StateType.CHATTER


class QuietTransition(Transition):
    def __init__(self):
        self.actions = [QuietAction("Transition from")]

        self.target_state = StateType.CHATTER
        self.to_chatter_condition = TimeRangeCondition(
            [TimeRange(4, 4), TimeRange(9, 9)]
        )

    def is_triggered(self):
        return self.to_chatter_condition.test()

    def get_actions(self):
        return self.actions

    def get_target_state(self):
        return self.target_state


class DummyTransition(Transition):
    def __init__(self):
        self.actions = [DummyAction("Transition from")]
        self.target_state = StateType.QUIET

    def is_triggered(self):
        return True

    def get_actions(self):
        return self.actions

    def get_target_state(self):
        return self.target_state


class FiniteStateMachine:
    def __init__(self):
        self.initial_state = ChatterState()
        self.current_state = self.initial_state
        print("FiniteStateMachine is initialized with ChatterState")

    def update(self):
        # return Action list to execute
        triggered_transition = None

        for transition in self.current_state.get_transitions():
            if transition.is_triggered():
                triggered_transition = transition
                break
        # Check if we have a transition to fire
        if triggered_transition is None:
            return self.current_state.get_actions()
        else:

            exit_actions = self.current_state.get_exit_actions()
            triggered_actions = triggered_transition.get_actions()

            target_state_type = triggered_transition.get_target_state()
            target_state = StateBuilder.build(target_state_type)
            entry_actions = target_state.get_entry_actions()
            actions = exit_actions + triggered_actions + entry_actions

            self.current_state = target_state

            return actions


def main():
    print("===== Start FiniteStateMachine =====")
    finite_state_machine = FiniteStateMachine()

    for i in range(12):
        print("=====Update FiniteStateMachine", i, "=====")
        actions = finite_state_machine.update()
        for action in actions:
            action.execute()

        ClockCounter.count_up()
    print("===== Finish FiniteStateMachine =====")


if __name__ == "__main__":
    main()
