import copy
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


def heuristic_manhattan(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == '.':
                return abs(i - 2) + abs(j - 2)
    return 0


def heuristic_misplaced(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j] and state[i][j] != '.':
                count += 1
    return count


def create_node(state, parent, action, step, cost):
    return {
        "state": state,
        "parent": parent,
        "action": action,
        "step": step,
        "cost": cost
    }


def get_path(node):
    path = []
    while node is not None:
        path.append(node)
        node = node["parent"]
    path.reverse()
    return path


def solve_hill_climbing(start, heuristic=heuristic_manhattan, max_iterations=10000):
    current = start
    current_value = heuristic(current)
    iterations = 0
    nodes_expanded = 0
    plateaus = 0
    current_node = create_node(start, None, None, 0, current_value)
    
    while iterations < max_iterations:
        iterations += 1
        
        if current == goal:
            return True, get_path(current_node), {
                'iterations': iterations,
                'nodes_expanded': nodes_expanded,
                'plateaus': plateaus
            }
        
        rules = find_action(current)
        nodes_expanded += len(rules)
        
        best_neighbor = None
        best_value = current_value
        best_action = None
        
        for action in rules:
            neighbor = execute_action(current, action)
            value = heuristic(neighbor)
            if value < best_value:
                best_value = value
                best_neighbor = neighbor
                best_action = action
        
        if best_neighbor is None:
            return False, get_path(current_node), {
                'iterations': iterations,
                'nodes_expanded': nodes_expanded,
                'plateaus': plateaus,
                'stuck_at_local_max': True
            }
        
        if best_value == current_value:
            plateaus += 1
        
        current = best_neighbor
        current_value = best_value
        current_node = create_node(current, current_node, best_action, current_node["step"] + 1, current_value)
    
    return False, get_path(current_node), {
        'iterations': iterations,
        'nodes_expanded': nodes_expanded,
        'plateaus': plateaus,
        'max_iterations_reached': True
    }


def generate_random_solvable_state():
    state = [row[:] for row in goal]
    for _ in range(50):
        rules = find_action(state)
        action = random.choice(rules)
        state = execute_action(state, action)
    
    return state


def main():
    table = generate_random_solvable_state()

    print("=" * 60)
    print("HILL CLIMBING - 8 Puzzle Solver")
    print("=" * 60)
    
    print("\nTrạng thái ban đầu:")
    print_table(table)
    
    print("Trạng thái đích:")
    print_table(goal)

    success_hc, path_hc, stats_hc = solve_hill_climbing(table)
    print(f"Thành công: {success_hc}")
    print(f"Số bước: {path_hc[-1]['step']}")
    print("Các bước đi: ", end="")
    for node in path_hc:
        if node["action"] is not None:
            print(node["action"], end=" ")
    print("\n")
    
    print("Các trạng thái từ đầu đến đích:")
    for node in path_hc:
        if node["action"] is None:
            print("START")
        else:
            print("Đi:", node["action"])
        print(f"Heuristic: {node['cost']}")
        print_table(node["state"])
    
    if not success_hc:
        if 'stuck_at_local_max' in stats_hc:
            print("Bị stuck tại local maximum - không tìm được neighbor tốt hơn!")
        if 'max_iterations_reached' in stats_hc:
            print("Vượt quá max iterations!")
    
    print(f"\nThống kê:")
    for key, val in stats_hc.items():
        print(f"  {key}: {val}")


if __name__ == "__main__":
    main()
