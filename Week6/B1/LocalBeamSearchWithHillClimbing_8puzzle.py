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


def local_beam_search_with_hill_climbing(initial_state, k=3, max_iterations=1000):
    print("=" * 50)
    print(f"LOCAL BEAM SEARCH + HILL CLIMBING (k={k})")
    print("=" * 50)

    improved_initial = hill_climbing_improvement(initial_state, max_iter=100)
    beam = [improved_initial]
    current_h = manhattan_distance(improved_initial)
    iteration = 0
    all_states = [copy.deepcopy(improved_initial)]
    h_history = [current_h]

    print(f"Trạng thái ban đầu (sau HC) - h(n) = {current_h}:")
    print_table(improved_initial)

    while iteration < max_iterations:
        for state in beam:
            if state == goal:
                print("✓ Tìm thấy giải pháp!")
                result = {
                    'success': True,
                    'solution': state,
                    'iterations': iteration,
                    'beam_size': len(beam),
                    'k': k
                }
                print(f"Lần lặp: {iteration}")
                print("=" * 50)
                return result

        successors = []
        for state in beam:
            actions = find_action(state)
            for action in actions:
                next_state = execute_action(state, action)
                improved_state = hill_climbing_improvement(next_state, max_iter=50)
                next_h = manhattan_distance(improved_state)
                successors.append((next_h, improved_state))

        if not successors:
            print(f"Đạt cực bộ tại lần lặp {iteration}")
            break

        successors.sort(key=lambda x: x[0])
        
        unique_successors = []
        seen_states = set(state_to_string(s) for s in beam)
        
        for h_val, successor in successors:
            state_str = state_to_string(successor)
            if state_str not in seen_states:
                unique_successors.append((h_val, successor))
                seen_states.add(state_str)

        if not unique_successors:
            print(f"Không có successor mới tại lần lặp {iteration}")
            break

        beam = [successor[1] for successor in unique_successors[:k]]

        iteration += 1
        best_h = unique_successors[0][0]
        h_history.append(best_h)
        all_states.append(copy.deepcopy(beam[0]))

        print(f"Lần lặp {iteration}: {len(successors)} successor (sau HC), chọn {len(beam)} tốt nhất")
        for i, state in enumerate(beam):
            h = manhattan_distance(state)
            print(f"  Trạng thái {i+1}: h(n) = {h}")
            print_table(state)

        if len(unique_successors) < k:
            print(f"Beam hội tụ - chỉ {len(unique_successors)} successor mới")
            if len(unique_successors) == 0:
                break

    print(f"Thất bại - không tìm thấy giải pháp sau {iteration} lần lặp")
    best_state = beam[0] if beam else improved_initial
    print(f"Trạng thái tốt nhất có h(n) = {manhattan_distance(best_state)}")
    print("=" * 50)

    result = {
        'success': False,
        'solution': best_state,
        'iterations': iteration,
        'beam_size': len(beam),
        'k': k,
        'h_history': h_history
    }

    return result


def hill_climbing_improvement(state, max_iter=50):
    current = state
    current_h = manhattan_distance(current)
    iterations = 0

    while iterations < max_iter:
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
            return current

    return current


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
    result = local_beam_search_with_hill_climbing(initial, k=3)
