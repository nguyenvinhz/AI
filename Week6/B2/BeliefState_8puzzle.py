import copy
import heapq
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


def common_actions(belief_state):
    common = set(find_action(belief_state[0]))
    for state in belief_state[1:]:
        common &= set(find_action(state))
    return sorted(common)


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


def execute_belief_action(belief_state, action):
    next_belief = []

    for state in belief_state:
        next_belief.append(execute_action_with_wall(state, action))

    return next_belief


def manhattan_distance(s):
    distance = 0
    for i in range(3):
        for j in range(3):
            if s[i][j] != '.':
                value = s[i][j]
                goal_i = (value - 1) // 3
                goal_j = (value - 1) % 3
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance


def belief_cost(belief_state):
    return sum(manhattan_distance(state) for state in belief_state)


def is_belief_goal(belief_state):
    return all(state == goal for state in belief_state)


def random_initial_state(min_steps=8, max_steps=16):
    s = copy.deepcopy(goal)
    old_action = None

    for _ in range(random.randint(min_steps, max_steps)):
        actions = find_action(s)
        if old_action == "UP" and "DOWN" in actions:
            actions.remove("DOWN")
        elif old_action == "DOWN" and "UP" in actions:
            actions.remove("UP")
        elif old_action == "LEFT" and "RIGHT" in actions:
            actions.remove("RIGHT")
        elif old_action == "RIGHT" and "LEFT" in actions:
            actions.remove("LEFT")

        action = random.choice(actions)
        s = execute_action(s, action)
        old_action = action

    return s


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


def random_plan(length=10):
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


def random_belief_state(size=3, plan_length=7, max_attempts=1000, min_solution_steps=4):
    for _ in range(max_attempts):
        plan = random_plan(plan_length)
        belief_state = []
        seen = set()
        state_attempts = 0

        while len(belief_state) < size and state_attempts < 100:
            state_attempts += 1
            state = make_state_from_plan(plan)
            if state is None:
                break

            key = state_to_string(state)
            if key not in seen and state != goal and run_plan(state, plan) == goal:
                belief_state.append(state)
                seen.add(key)

        if len(belief_state) == size and belief_cost(belief_state) >= plan_length:
            if min_solution_steps <= 0:
                return belief_state

            result = greedy_belief_state(belief_state, max_expansions=1000, verbose=False)
            if result["success"] and len(result["actions"]) >= min_solution_steps:
                return belief_state

    return random_belief_state(size, plan_length, max_attempts, min_solution_steps - 1)


def greedy_belief_state(initial_belief, max_expansions=5000, verbose=True):
    counter = 0
    start = copy.deepcopy(initial_belief)
    start_key = belief_to_string(start)
    frontier = [(belief_cost(start), counter, start, [])]
    visited = {start_key}

    if verbose:
        print("GREEDY BELIEF STATE")
        print(f"States: {len(start)}")
        print(f"h(n): {belief_cost(start)}")
        print_belief_state(start)

    expansions = 0
    while frontier and expansions < max_expansions:
        cost, _, belief_state, actions_taken = heapq.heappop(frontier)
        expansions += 1

        if verbose:
            print("-" * 60)
            print(f"Expand {expansions}")
            print(f"Path: {actions_taken if actions_taken else 'START'}")
            print(f"h(n): {cost}")
            print_belief_state(belief_state)

        if is_belief_goal(belief_state):
            if verbose:
                print("GOAL")
            return {
                "success": True,
                "actions": actions_taken,
                "final_belief": belief_state
            }

        candidates = []
        for action in all_actions():
            next_belief = execute_belief_action(belief_state, action)
            next_key = belief_to_string(next_belief)
            if next_key in visited:
                continue

            visited.add(next_key)
            next_cost = belief_cost(next_belief)
            counter += 1
            heapq.heappush(frontier, (next_cost, counter, next_belief, actions_taken + [action]))
            candidates.append((next_cost, action))

        candidates.sort()
        if verbose:
            print(f"Next h(n): {candidates}")

    return {
        "success": False,
        "actions": [],
        "final_belief": None
    }


if __name__ == "__main__":
    belief = random_belief_state(size=3)
    greedy_belief_state(belief)
