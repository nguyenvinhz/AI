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

all_actions = ["UP", "DOWN", "LEFT", "RIGHT"]
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


def is_goal(state):
    return state == goal


def random_initial_state(depth=10):
    state = copy.deepcopy(goal)
    previous_action = None
    scramble = []
    for _ in range(depth):
        actions = find_action(state)
        if previous_action:
            reverse = opposite[previous_action]
            filtered = [action for action in actions if action != reverse]
            if filtered:
                actions = filtered
        action = random.choice(actions)
        state = execute_action(state, action)
        scramble.append(action)
        previous_action = action
    return state, [opposite[action] for action in reversed(scramble)]


def print_result(solution, final_state):
    if solution is None:
        print("THẤT BẠI")
        return
    print("NGHIỆM")
    print(solution)
    print("Số bước:", len(solution))
    print_table(final_state)


def forward_check(state, action, visited):
    if action not in find_action(state):
        return None

    next_state = execute_action(state, action)
    if state_to_string(next_state) in visited:
        return None
    return next_state


def ordered_domain(state, previous_action):
    domain = find_action(state)
    if previous_action and opposite[previous_action] in domain:
        domain.remove(opposite[previous_action])
    return sorted(domain, key=lambda action: manhattan_distance(execute_action(state, action)))


def forward_checking(state, limit, path=None, visited=None, depth=0):
    if path is None:
        path = []
    if visited is None:
        visited = {state_to_string(state)}

    log(f"Độ sâu {depth}: h(n)={manhattan_distance(state)}, đường đi={path if path else 'BẮT ĐẦU'}")
    if log_count < PRINT_LIMIT:
        print_table(state)

    if is_goal(state):
        return path, state
    if depth == limit:
        return None, None

    previous_action = path[-1] if path else None
    domain = ordered_domain(state, previous_action)
    log(f"Độ sâu {depth}: miền giá trị={domain}")

    for action in domain:
        next_state = forward_check(state, action, visited)
        if next_state is None:
            log(f"Độ sâu {depth}: TỈA {action}")
            continue

        next_domain = [next_action for next_action in all_actions if next_action in find_action(next_state)]
        if opposite[action] in next_domain:
            next_domain.remove(opposite[action])

        log(f"Độ sâu {depth}: GÁN {action}, miền bước kế={next_domain}")
        if not next_domain and not is_goal(next_state):
            log(f"Độ sâu {depth}: THẤT BẠI vì miền bước kế rỗng")
            continue

        key = state_to_string(next_state)
        visited.add(key)
        result_path, result_state = forward_checking(
            next_state, limit, path + [action], visited, depth + 1
        )
        if result_path is not None:
            return result_path, result_state

        log(f"Độ sâu {depth}: QUAY LUI {action}")
        visited.remove(key)

    return None, None


if __name__ == "__main__":
    print("KIỂM TRA TIẾN - 8 PUZZLE")
    start, hint = random_initial_state(depth=10)
    print("Trạng thái ban đầu:")
    print_table(start)
    print("Gợi ý nghiệm từ bước xáo trộn:", hint)

    solution, final_state = forward_checking(start, limit=20)
    print_result(solution, final_state)
