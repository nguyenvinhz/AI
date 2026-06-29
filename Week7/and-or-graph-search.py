import copy
import random

goal = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, '.']
]


def print_table(s):
    for row in s:
        print(row)
    print()


def state_to_string(s):
    return ''.join(str(x) for row in s for x in row)


def find_empty(s):
    for i in range(3):
        for j in range(3):
            if s[i][j] == '.':
                return i, j


def find_action(s):
    x, y = find_empty(s)
    rules = []

    if x > 0:
        rules.append("UP")
    if x < 2:
        rules.append("DOWN")
    if y > 0:
        rules.append("LEFT")
    if y < 2:
        rules.append("RIGHT")

    return rules


def all_actions():
    return ["UP", "DOWN", "LEFT", "RIGHT"]


def opposite_action(action):
    opposites = {
        "UP": "DOWN",
        "DOWN": "UP",
        "LEFT": "RIGHT",
        "RIGHT": "LEFT"
    }
    return opposites[action]


def execute_action(s, action):
    x, y = find_empty(s)

    moves = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1)
    }

    new_x, new_y = x + moves[action][0], y + moves[action][1]
    new_s = copy.deepcopy(s)
    new_s[x][y], new_s[new_x][new_y] = new_s[new_x][new_y], new_s[x][y]

    return new_s


def execute_action_with_wall(s, action):
    if action in find_action(s):
        return execute_action(s, action)
    return copy.deepcopy(s)


def predecessor_states(state, action):
    predecessors = []

    if action not in find_action(state):
        predecessors.append(copy.deepcopy(state))

    reverse_action = opposite_action(action)
    if reverse_action in find_action(state):
        predecessors.append(execute_action(state, reverse_action))

    return predecessors


def random_initial_state(plan_length=5):
    state = copy.deepcopy(goal)
    scramble_actions = []
    previous_action = None

    while len(scramble_actions) < plan_length:
        choices = find_action(state)
        if previous_action:
            reverse = opposite_action(previous_action)
            filtered = [action for action in choices if action != reverse]
            if filtered:
                choices = filtered

        action = random.choice(choices)
        state = execute_action(state, action)
        scramble_actions.append(action)
        previous_action = action

    return state


def make_state_from_plan(plan):
    state = copy.deepcopy(goal)

    for action in reversed(plan):
        choices = predecessor_states(state, action)
        if not choices:
            return None
        state = random.choice(choices)

    return state


def run_plan(state, plan):
    current = copy.deepcopy(state)
    for action in plan:
        current = execute_action_with_wall(current, action)
    return current


def result_states(state, action):
    results = [execute_action_with_wall(state, action)]
    seen = set()
    unique = []

    for result in results:
        key = state_to_string(result)
        if key not in seen:
            unique.append(result)
            seen.add(key)

    return unique


def goal_test(state):
    return state == goal


def and_or_graph_search(initial_state, max_depth=20):
    return or_search(initial_state, [], 0, max_depth)


def or_search(state, path, depth=0, max_depth=20):
    state_key = state_to_string(state)
    print(f"OR_SEARCH depth={depth}: {state_key}")
    print_table(state)

    if goal_test(state):
        return []

    if state_key in path or depth > max_depth:
        return "failure"

    for action in all_actions():
        if action not in find_action(state):
            continue

        states = result_states(state, action)
        plan = and_search(states, path + [state_key], depth + 1, max_depth)

        if plan != "failure":
            return [action, plan]

    return "failure"


def and_search(states, path, depth=0, max_depth=20):
    plans = {}
    print(f"AND_SEARCH: {len(states)} state")

    for state in states:
        plan = or_search(state, path, depth, max_depth)
        if plan == "failure":
            return "failure"
        plans[state_to_string(state)] = plan

    return plans


if __name__ == "__main__":
    initial = random_initial_state()
    plan = and_or_graph_search(initial)
    print("PLAN:")
    print(plan)
