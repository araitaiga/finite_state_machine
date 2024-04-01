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
    """Clock

    Attributes:
        time_now (int): current time
    """

    time_now = 0

    @classmethod
    def count_up(cls):
        """Count up the time"""
        cls.time_now += 1
        if cls.time_now >= 12:
            cls.time_now = 0

    @classmethod
    def get_time(cls):
        """Get the current time"""
        return cls.time_now


class Action(ABC):
    """Action"""

    @abstractmethod
    def execute(self):
        """Execute the action"""
        pass


class GreetingAction(Action):
    """Greeting Action"""

    def __init__(self):
        pass

    def execute(self):
        print("[Action] Hello")


class ChatterAction(Action):
    """Chatter Action
    Attributes:
        message (str): message
    """

    def __init__(self, message):
        self.message = message

    def execute(self):
        print("[Action]", self.message, "Chatter!!!")


class QuietAction(Action):
    """Quiet Action
    Attributes:
        message (str): message
    """

    def __init__(self, message):
        self.message = message

    def execute(self):
        print("[Action]", self.message, "Quiet...")


class DummyAction(Action):
    """ "Dummy Action
    Attributes:
        message (str): message
    """

    def __init__(self, message):
        self.message = message

    def execute(self):
        print("[Action]", self.message, "Dummy")


class Condition(ABC):
    """Condition"""

    @abstractmethod
    def test(self):
        """Test the condition"""
        pass


class TimeRange:
    """Time Range
    Attributes:
        time_min (int): min time
        time_max (int): max time
    """

    def __init__(self, time_min, time_max):
        self.time_min = time_min
        self.time_max = time_max


class TimeRangeCondition(Condition):
    """Time Range Condition
    Attributes:
        time_ranges (list[TimeRange]): list of TimeRange
    """

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
    """State Type"""

    CHATTER = 1
    QUIET = 2
    DUMMY = 3


class StateBuilder:
    """State Builder"""

    def __init__(self):
        pass

    @staticmethod
    def build(state_type):
        """Build State
        Args:
            state_type (StateType): StateType
        """
        if state_type == StateType.CHATTER:
            return ChatterState()
        elif state_type == StateType.QUIET:
            return QuietState()
        elif state_type == StateType.DUMMY:
            return DummyState()
        else:
            raise ValueError("Invalid StateType")


class State(ABC):
    """State"""

    @abstractmethod
    def get_actions(self):
        """Get Actions"""
        pass

    @abstractmethod
    def get_entry_actions(self):
        """Get Entry Actions"""
        pass

    @abstractmethod
    def get_exit_actions(self):
        """Get Exit Actions"""
        pass

    @abstractmethod
    def get_transitions(self):
        """Get Transitions"""
        pass


class ChatterState(State):
    """Chatter State
    Attributes:
        actions (list[Action]): list of Actions
        entry_actions (list[Action]): list of Entry Actions
        exit_actions (list[Action]): list of Exit Actions
        transitions (list[Transition]): list of Transitions
    """

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
    """Quiet State
    Attributes:
        actions (list[Action]): list of Actions
        entry_actions (list[Action]): list of Entry Actions
        exit_actions (list[Action]): list of Exit Actions
        transitions (list[Transition]): list of Transitions
    """

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
    """Dummy State
    Attributes:
        actions (list[Action]): list of Actions
        entry_actions (list[Action]): list of Entry Actions
        exit_actions (list[Action]): list of Exit Actions
        transitions (list[Transition]): list of Transitions
    """

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
    """Transition"""

    @abstractmethod
    def is_triggered(self):
        """Check if the transition is triggered"""
        pass

    @abstractmethod
    def get_actions(self):
        """Get Actions"""
        pass

    @abstractmethod
    def get_target_state(self):
        """Get Target State"""
        pass


class ChatterTransition(Transition):
    """Chatter Transition
    Attributes:
        actions (list[Action]): list of Actions
        target_state_quiet (StateType): target state type (Quiet)
        target_state_dummy (StateType): target state type (Dummy)
        to_quiet_condition (Condition): condition to transition to Quiet
        to_dummy_condition (Condition): condition to transition to Dummy
    """

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
    """Quiet Transition
    Attributes:
        actions (list[Action]): list of Actions
        target_state (StateType): target state type (Chatter)
        to_chatter_condition (Condition): condition to transition to Chatter
    """

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
    """Dummy Transition
    Attributes:
        actions (list[Action]): list of Actions
        target_state (StateType): target state type (Quiet)
    """

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
    """Finite State Machine
    Attributes:
        initial_state (State): initial state
        current_state (State): current state
    """

    def __init__(self):
        self.initial_state = ChatterState()
        self.current_state = self.initial_state
        print("FiniteStateMachine is initialized with ChatterState")

    def update(self):
        """Update the Finite State Machine"""

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
    """Update FiniteStateMachine and ClockCounter"""
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
