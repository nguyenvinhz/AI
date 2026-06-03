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


def hill_climbing_single(initial_state, max_iterations=1000):
    current = initial_state
    current_h = manhattan_distance(current)
    iterations = 0

    while iterations < max_iterations:
        actions = find_action(current)
        
        if not actions:
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
            break

        current = best_next
        current_h = best_h
        iterations += 1

        if current == goal:
            return {
                'success': True,
                'solution': current,
                'iterations': iterations,
                'final_h': current_h
            }

    return {
        'success': current == goal,
        'solution': current,
        'iterations': iterations,
        'final_h': current_h
    }


def random_restart_hill_climbing(initial_state, num_restarts=10, max_iterations=1000):
    print("=" * 50)
    print("RANDOM RESTART HILL CLIMBING")
    print("=" * 50)
    print(f"Số lần khởi động lại: {num_restarts}\n")

    best_result = None
    best_h = float('inf')
    results = []

    for restart in range(num_restarts):
        print(f"--- Lần khởi động lại #{restart + 1} ---")
        
        random_start = random_initial_state()
        print(f"Trạng thái ban đầu - h(n) = {manhattan_distance(random_start)}:")
        print_table(random_start)

        result = hill_climbing_single(random_start, max_iterations)
        results.append(result)

        final_h = result['final_h']
        print(f"Kết quả: {'Thành công' if result['success'] else 'Thất bại'}, h(n) = {final_h}, Lần lặp = {result['iterations']}\n")

        if result['success']:
            print("✓ Tìm thấy giải pháp!")
            best_result = result
            break
        
        if final_h <= best_h:
            best_h = final_h
            best_result = result

    if best_result and best_result['success']:
        print(f"\n{'=' * 50}")
        print("✓ THÀNH CÔNG! Tìm thấy giải pháp.")
        print(f"Khởi động lại lần: {next(i for i, r in enumerate(results) if r['success']) + 1}")
        print(f"Tổng số lần lặp: {best_result['iterations']}")
    else:
        print(f"\n{'=' * 50}")
        print("Thất bại - Không tìm thấy giải pháp")
        print(f"Cực bộ tốt nhất có h(n) = {best_h}")
        print(f"Tổng số lần khởi động: {num_restarts}")

    result_final = {
        'success': best_result and best_result['success'],
        'solution': best_result['solution'] if best_result else None,
        'num_restarts': num_restarts,
        'best_h': best_h,
        'restart_results': results
    }

    print("=" * 50)
    return result_final


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
    result = random_restart_hill_climbing(initial, num_restarts=10)
