import copy
import random
import sys
from collections import deque

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

PRINT_LIMIT = 180
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


def print_result(solution, final_state):
    if solution is None:
        print("THẤT BẠI")
        return
    print("NGHIỆM")
    print(solution)
    print("Số bước:", len(solution))
    print_table(final_state)


def allowed_pair(first_action, second_action):
    return opposite[first_action] != second_action


def revise(domains, xi, xj):
    revised = False
    for value in domains[xi][:]:
        supported = any(allowed_pair(value, other) for other in domains[xj])
        if not supported:
            domains[xi].remove(value)
            revised = True
            log(f"HIỆU CHỈNH X{xi},X{xj}: xóa {value}")
    return revised


def ac3(domains):
    queue = deque((index, index + 1) for index in range(len(domains) - 1))
    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            if xi > 0:
                queue.append((xi - 1, xi))
    return True


def make_domains(length):
    return {index: all_actions[:] for index in range(length)}


def order_actions(state, domain):
    valid = [action for action in domain if action in find_action(state)]
    return sorted(valid, key=lambda action: manhattan_distance(execute_action(state, action)))


def backtracking_with_ac3(state, limit, domains=None, path=None, visited=None, depth=0):
    if domains is None:
        domains = make_domains(limit)
        ac3(domains)
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

    for action in order_actions(state, domains[depth]):
        next_state = execute_action(state, action)
        key = state_to_string(next_state)

        if key in visited:
            log(f"Độ sâu {depth}: TỈA {action} vì trạng thái bị lặp")
            continue

        next_domains = {index: values[:] for index, values in domains.items()}
        next_domains[depth] = [action]
        if depth + 1 < limit and opposite[action] in next_domains[depth + 1]:
            next_domains[depth + 1].remove(opposite[action])

        log(f"Độ sâu {depth}: GÁN X{depth}={action}, chạy AC-3")
        if not ac3(next_domains):
            log(f"Độ sâu {depth}: AC-3 thất bại")
            continue

        visited.add(key)
        result_path, result_state = backtracking_with_ac3(
            next_state, limit, next_domains, path + [action], visited, depth + 1
        )
        if result_path is not None:
            return result_path, result_state

        log(f"Độ sâu {depth}: QUAY LUI {action}")
        visited.remove(key)

    return None, None


if __name__ == "__main__":
    print("NHẤT QUÁN CUNG AC-3 - 8 PUZZLE")
    start = random_initial_state(depth=10)
    print("Trạng thái ban đầu:")
    print_table(start)

    solution, final_state = backtracking_with_ac3(start, limit=20)
    print_result(solution, final_state)
