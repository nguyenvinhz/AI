import copy
import random
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

goal = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, '.']
]

opposite = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT"
}

PRINT_LIMIT = 160
log_count = 0


def log(message):
    global log_count
    if log_count < PRINT_LIMIT:
        print(message)
    elif log_count == PRINT_LIMIT:
        print("...")
    log_count += 1


def print_table(state):
    for row in state:
        print(row)
    print()


def state_to_string(state):
    return ''.join(str(x) for row in state for x in row)


def find_empty(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == '.':
                return i, j


def find_action(state):
    x, y = find_empty(state)
    actions = []
    if x > 0:
        actions.append("UP")
    if x < 2:
        actions.append("DOWN")
    if y > 0:
        actions.append("LEFT")
    if y < 2:
        actions.append("RIGHT")
    return actions


def execute_action(state, action):
    x, y = find_empty(state)
    moves = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1)
    }
    dx, dy = moves[action]
    new_state = copy.deepcopy(state)
    new_x, new_y = x + dx, y + dy
    new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
    return new_state


def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != '.':
                goal_i = (value - 1) // 3
                goal_j = (value - 1) % 3
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance


def evaluate(state):
    if state == goal:
        return 100
    return -manhattan_distance(state)


def is_goal(state):
    return state == goal


def random_initial_state(depth=10):
    state = copy.deepcopy(goal)
    previous_action = None

    for _ in range(depth):
        actions = find_action(state)
        if previous_action:
            reverse = opposite[previous_action]
            filtered = [action for action in actions if action != reverse]
            if filtered:
                actions = filtered
        action = random.choice(actions)
        state = execute_action(state, action)
        previous_action = action
    return state


def make_initial_state(actions):
    state = copy.deepcopy(goal)
    for action in actions:
        state = execute_action(state, action)
    return state


def ordered_actions(state, previous_action=None):
    actions = find_action(state)
    if previous_action and opposite[previous_action] in actions:
        actions.remove(opposite[previous_action])
    return sorted(actions, key=lambda action: manhattan_distance(execute_action(state, action)))


def minimax(state, depth, maximizing_player, visited, previous_action=None):
    if is_goal(state) or depth == 0:
        return evaluate(state)

    actions = ordered_actions(state, previous_action)
    if not actions:
        return evaluate(state)

    if maximizing_player:
        best_value = -float("inf")
        for action in actions:
            next_state = execute_action(state, action)
            key = state_to_string(next_state)
            if key in visited:
                continue
            visited.add(key)
            value = minimax(next_state, depth - 1, False, visited, action)
            visited.remove(key)
            best_value = max(best_value, value)
        return best_value if best_value != -float("inf") else evaluate(state)

    best_value = float("inf")
    for action in actions:
        next_state = execute_action(state, action)
        key = state_to_string(next_state)
        if key in visited:
            continue
        visited.add(key)
        value = minimax(next_state, depth - 1, True, visited, action)
        visited.remove(key)
        best_value = min(best_value, value)
    return best_value if best_value != float("inf") else evaluate(state)


def choose_move(state, depth, previous_action=None):
    best_action = None
    best_value = -float("inf")
    visited = {state_to_string(state)}

    for action in ordered_actions(state, previous_action):
        next_state = execute_action(state, action)
        key = state_to_string(next_state)
        visited.add(key)
        value = minimax(next_state, depth - 1, False, visited, action)
        visited.remove(key)
        log(f"Thu {action}: value={value}, h(n)={manhattan_distance(next_state)}")
        if value > best_value:
            best_value = value
            best_action = action

    return best_action, best_value


def solve_with_minimax(state, depth=6, max_steps=30):
    current = copy.deepcopy(state)
    path = []
    previous_action = None
    visited = {state_to_string(current)}

    for step in range(max_steps):
        log(f"Buoc {step}: h(n)={manhattan_distance(current)}, duong di={path if path else 'BAT DAU'}")
        if log_count < PRINT_LIMIT:
            print_table(current)

        if is_goal(current):
            return path, current

        action, value = choose_move(current, depth, previous_action)
        if action is None:
            return None, current

        next_state = execute_action(current, action)
        key = state_to_string(next_state)
        log(f"Chon {action}: value={value}")
        if key in visited:
            return None, current

        current = next_state
        visited.add(key)
        path.append(action)
        previous_action = action

    return None, current


def print_result(solution, final_state):
    if solution is None:
        print("THAT BAI")
        print_table(final_state)
        return
    print("NGHIEM")
    print(solution)
    print("So buoc:", len(solution))
    print_table(final_state)


if __name__ == "__main__":
    print("MINIMAX - 8 PUZZLE")
    start = make_initial_state(["UP", "LEFT", "LEFT", "DOWN", "RIGHT", "UP"])
    print("Trang thai ban dau:")
    print_table(start)

    solution, final_state = solve_with_minimax(start, depth=6, max_steps=30)
    print_result(solution, final_state)
