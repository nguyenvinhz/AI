import copy
import random
import heapq

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
    """Tính Manhattan distance - heuristic h(n)"""
    distance = 0
    for i in range(3):
        for j in range(3):
            if s[i][j] != '.':
                value = s[i][j]
                goal_i = (value - 1) // 3
                goal_j = (value - 1) % 3
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance


def local_beam_search(initial_state, k=3, max_iterations=1000):
    """
    Thuật toán Local Beam Search
    - Duy trì k trạng thái tốt nhất tại mỗi bước
    - Sử dụng >= để so sánh các giá trị heuristic
    - k: số lượng trạng thái được duy trì
    """
    print("=" * 50)
    print(f"LOCAL BEAM SEARCH (k={k})")
    print("=" * 50)

    # Khởi tạo beam với trạng thái ban đầu
    beam = [initial_state]
    current_h = manhattan_distance(initial_state)
    iteration = 0
    all_states = [copy.deepcopy(initial_state)]
    h_history = [current_h]

    print(f"Trạng thái ban đầu - h(n) = {current_h}:")
    print_table(initial_state)

    while iteration < max_iterations:
        # Nếu trạng thái mục tiêu trong beam
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

        # Sinh tất cả hàng xóm từ mỗi trạng thái trong beam
        successors = []
        for state in beam:
            actions = find_action(state)
            for action in actions:
                next_state = execute_action(state, action)
                next_h = manhattan_distance(next_state)
                successors.append((next_h, next_state))

        # Nếu không có successor, dừng
        if not successors:
            print(f"Đạt cực bộ tại lần lặp {iteration}")
            break

        # Sắp xếp successor theo h(n) và chọn k tốt nhất (sử dụng <=)
        successors.sort(key=lambda x: x[0])
        beam = [successor[1] for successor in successors[:k]]

        iteration += 1
        best_h = successors[0][0]
        h_history.append(best_h)
        all_states.append(copy.deepcopy(beam[0]))

        print(f"Lần lặp {iteration}: {len(successors)} successor, chọn {k} tốt nhất")
        for i, state in enumerate(beam):
            h = manhattan_distance(state)
            print(f"  Trạng thái {i+1}: h(n) = {h}")
            print_table(state)

        # Nếu all_states được lựa chọn bằng nhau (==), có thể dừng
        if len(set(state_to_string(s) for s in beam)) == 1:
            print(f"Beam hội tụ - tất cả trạng thái bằng nhau")
            break

    print(f"Thất bại - không tìm thấy giải pháp sau {iteration} lần lặp")
    best_state = beam[0] if beam else initial_state
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
    result = local_beam_search(initial, k=3)
