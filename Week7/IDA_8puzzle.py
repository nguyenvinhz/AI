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
    distance = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != '.':
                goal_i = (val - 1) // 3
                goal_j = (val - 1) % 3
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance


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


def search_with_limit(current_node, g_limit, visited, heuristic):
    current_state = current_node["state"]
    f = current_node["step"] + heuristic(current_state)
    
    if f > g_limit:
        return False, f, None
    
    if current_state == goal:
        return True, g_limit, get_path(current_node)
    
    min_f = float('inf')
    visited.add(state_to_string(current_state))
    
    rules = find_action(current_state)
    
    for rule in rules:
        new_state = execute_action(current_state, rule)
        state_str = state_to_string(new_state)
        
        if state_str not in visited:
            new_node = create_node(
                new_state,
                current_node,
                rule,
                current_node["step"] + 1,
                heuristic(new_state)
            )
            
            found, new_limit, path = search_with_limit(new_node, g_limit, visited, heuristic)
            
            if found:
                return True, g_limit, path
            
            min_f = min(min_f, new_limit)
    
    visited.remove(state_to_string(current_state))
    return False, min_f, None


def solve_ida_star(start, heuristic=heuristic_manhattan):
    if start == goal:
        return True, [create_node(start, None, None, 0, 0)], {'nodes_expanded': 1, 'iterations': 0}
    
    g_limit = heuristic(start)
    iterations = 0
    total_nodes = 0
    
    start_node = create_node(start, None, None, 0, 0)
    
    while True:
        iterations += 1
        visited = set()
        found, new_limit, path = search_with_limit(start_node, g_limit, visited, heuristic)
        total_nodes += len(visited)
        
        if found:
            return True, path, {
                'nodes_expanded': total_nodes,
                'iterations': iterations,
                'final_g_limit': g_limit
            }
        
        if new_limit == float('inf'):
            return False, None, {'nodes_expanded': total_nodes, 'iterations': iterations}
        
        g_limit = new_limit


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
    print("IDA* (Iterative Deepening A*) - 8 Puzzle Solver")
    print("=" * 60)
    
    print("\nTrạng thái ban đầu:")
    print_table(table)
    
    print("Trạng thái đích:")
    print_table(goal)

    success, path, stats = solve_ida_star(table, heuristic_manhattan)
    
    if success:
        print("ĐÃ TÌM THẤY LỜI GIẢI")
        print(f"Số bước: {path[-1]['step']}")
        print(f"Iterations: {stats['iterations']}")
        print(f"Nodes expanded: {stats['nodes_expanded']}")
        print(f"Final G-limit: {stats['final_g_limit']}\n")
        
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
    else:
        print("KHÔNG TÌM THẤY LỜI GIẢI")
        print(f"Nodes expanded: {stats['nodes_expanded']}")
        print(f"Iterations: {stats['iterations']}")


if __name__ == "__main__":
    main()
