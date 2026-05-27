import copy
import heapq
import random
from collections import deque

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

    dx, dy = moves[action]
    new_x = x + dx
    new_y = y + dy

    new_table = copy.deepcopy(s)

    new_table[x][y], new_table[new_x][new_y] = new_table[new_x][new_y], new_table[x][y]

    return new_table


def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != '.':
                tile = state[i][j]
                for di in range(3):
                    for dj in range(3):
                        if goal[di][dj] == tile:
                            distance += abs(i - di) + abs(j - dj)
    return distance


def create_node(state, parent, action, step):
    return {
        "state": state,
        "parent": parent,
        "action": action,
        "step": step
    }


def get_path(node):
    path = []

    while node is not None:
        path.append(node)
        node = node["parent"]

    path.reverse()
    return path


def solve_astar(start):
    heap = []
    visited = set()
    counter = 0

    start_heuristic = manhattan_distance(start)
    start_node = create_node(start, None, None, 0)
    start_f = 0 + start_heuristic
    
    heapq.heappush(heap, (start_f, counter, state_to_string(start), start_node))
    visited.add(state_to_string(start))

    while heap:
        _, _, _, current_node = heapq.heappop(heap)
        current_state = current_node["state"]

        if current_state == goal:
            print("ĐÃ TÌM THẤY LỜI GIẢI (A*)")
            print(f"Số bước: {current_node['step']}")

            path = get_path(current_node)

            print("Các bước đi:")
            for node in path:
                if node["action"] is not None:
                    print(node["action"], end=" ")
            print("\n")

            print("Các trạng thái từ đầu đến đích:")
            for node in path:
                if node["action"] is None:
                    print("START")
                else:
                    print("Đi:", node["action"])

                print_table(node["state"])

            return current_node["step"]

        rules = find_action(current_state)

        for rule in rules:
            new_state = execute_action(current_state, rule)
            state_str = state_to_string(new_state)

            if state_str not in visited:
                visited.add(state_str)
                g_n = current_node["step"] + 1
                h_n = manhattan_distance(new_state)
                f_n = g_n + h_n
                counter += 1
                new_node = create_node(
                    new_state,
                    current_node,
                    rule,
                    g_n
                )
                heapq.heappush(heap, (f_n, counter, state_str, new_node))

    print("KHÔNG TÌM THẤY LỜI GIẢI")
    return -1


def generate_random_solvable_state():
    state = [row[:] for row in goal]
    for _ in range(50):
        rules = find_action(state)
        action = random.choice(rules)
        state = execute_action(state, action)
    
    return state


def main():
    table = generate_random_solvable_state()

    print("THUẬT TOÁN A* - 8 PUZZLE")
    print()

    print("Trạng thái ban đầu:")
    print_table(table)
    
    print("Trạng thái đích:")
    print_table(goal)

    solve_astar(table)


if __name__ == "__main__":
    main()
