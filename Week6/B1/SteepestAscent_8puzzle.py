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


def steepest_ascent_hill_climbing(initial_state, max_iterations=1000):
    current = initial_state
    current_h = manhattan_distance(current)
    iterations = 0
    path = [copy.deepcopy(current)]
    h_values = [current_h]

    print("=" * 50)
    print("STEEPEST ASCENT HILL CLIMBING (Dốc Nhất)")
    print("=" * 50)
    print(f"Trạng thái ban đầu - h(n) = {current_h}:")
    print_table(current)

    while iterations < max_iterations:
        actions = find_action(current)
        
        if not actions:
            print("Không có hành động nào có thể thực hiện")
            break

        best_next = None
        best_h = current_h
        best_action = None

        for action in actions:
            next_state = execute_action(current, action)
            next_h = manhattan_distance(next_state)
            
            if next_h <= best_h:
                best_next = next_state
                best_h = next_h
                best_action = action

        if best_h >= current_h:
            print(f"Đạt cực bộ tại lần lặp {iterations}")
            print(f"h(n) = {current_h}")
            print_table(current)
            break

        current = best_next
        current_h = best_h
        iterations += 1
        path.append(copy.deepcopy(current))
        h_values.append(current_h)

        print(f"Lần lặp {iterations}: Hành động = {best_action}, h(n) = {current_h}")
        print_table(current)

        if current == goal:
            print("✓ Tìm thấy giải pháp!")
            break

    result = {
        'success': current == goal,
        'solution': current,
        'iterations': iterations,
        'path_length': len(path),
        'h_values': h_values
    }

    print(f"\nKết quả: {'Thành công' if result['success'] else 'Thất bại'}")
    print(f"Số lần lặp: {iterations}")
    print(f"Số trạng thái: {len(path)}")
    print("=" * 50)

    return result


def random_initial_state():
    s = copy.deepcopy(goal)
    old_action = None
    for _ in range(random.randint(8, 16)):
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


if __name__ == "__main__":
    initial = random_initial_state()
    result = steepest_ascent_hill_climbing(initial)
