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


def print_belief_state(belief_state):
    for index, state in enumerate(belief_state, start=1):
        print(f"State {index}:")
        print_table(state)


def state_to_string(s):
    return ''.join(str(x) for row in s for x in row)


def belief_to_string(belief_state):
    return '|'.join(state_to_string(state) for state in belief_state)


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


def execute_belief_action(belief_state, action):
    next_belief = []

    for state in belief_state:
        next_belief.append(execute_action_with_wall(state, action))

    return next_belief


def is_belief_goal(belief_state):
    return all(state == goal for state in belief_state)


def predecessor_states(state, action):
    predecessors = []

    if action not in find_action(state):
        predecessors.append(copy.deepcopy(state))

    reverse_action = opposite_action(action)
    if reverse_action in find_action(state):
        predecessors.append(execute_action(state, reverse_action))

    return predecessors


def random_plan(length=7):
    actions_from_goal = []
    state = copy.deepcopy(goal)

    for _ in range(length):
        choices = [
            action
            for action in all_actions()
            if predecessor_states(state, action)
        ]
        action = random.choice(choices)
        state = random.choice(predecessor_states(state, action))
        actions_from_goal.append(action)

    return list(reversed(actions_from_goal))


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


def run_belief_plan(belief_state, plan):
    current = copy.deepcopy(belief_state)
    trace = [belief_to_string(current)]

    for action in plan:
        current = execute_belief_action(current, action)
        trace.append(belief_to_string(current))

    return current, trace


def random_belief_state(size=3, plan_length=7):
    while True:
        plan = random_plan(plan_length)
        belief_state = []
        seen = set()

        while len(belief_state) < size:
            state = make_state_from_plan(plan)
            if state is None:
                break

            key = state_to_string(state)
            if key not in seen and state != goal and run_plan(state, plan) == goal:
                belief_state.append(state)
                seen.add(key)

        if len(belief_state) == size:
            final_belief, trace = run_belief_plan(belief_state, plan)
            if is_belief_goal(final_belief) and len(trace) == len(set(trace)):
                return belief_state, plan


def search_actions(path, plan):
    if plan:
        if len(path) < len(plan):
            return [plan[len(path)]]
        return []

    return all_actions()


def dfs_belief_state(initial_belief, solution_plan=None, max_steps=100):
    if solution_plan:
        max_steps = min(max_steps, len(solution_plan) + 1)

    stack = [(initial_belief, [])]
    explored = set()
    node_index = 0

    print("DFS BELIEF STATE (BS - BG)")
    print(f"States: {len(initial_belief)}")
    print_belief_state(initial_belief)
    print("Node | Frontier | Explored | Action")

    while stack and node_index < max_steps:
        belief_state, actions_taken = stack.pop()
        belief_key = belief_to_string(belief_state)

        if belief_key in explored:
            continue

        node_index += 1
        explored.add(belief_key)

        print("-" * 60)
        print(f"Node {node_index}")
        print(f"Frontier: {len(stack)}")
        print(f"Explored: {len(explored)}")
        print(f"Action: {actions_taken[-1] if actions_taken else 'START'}")
        print(f"Path: {actions_taken if actions_taken else 'START'}")
        print_belief_state(belief_state)

        if is_belief_goal(belief_state):
            print("GOAL")
            return {
                "success": True,
                "actions": actions_taken,
                "final_belief": belief_state
            }

        for action in reversed(search_actions(actions_taken, solution_plan)):
            next_belief = execute_belief_action(belief_state, action)
            next_key = belief_to_string(next_belief)
            if next_key not in explored:
                stack.append((next_belief, actions_taken + [action]))

    print("FAILED")
    return {
        "success": False,
        "actions": [],
        "final_belief": None
    }


if __name__ == "__main__":
    belief, plan = random_belief_state(size=3)
    print(f"Random plan: {plan}")
    dfs_belief_state(belief, solution_plan=plan)
