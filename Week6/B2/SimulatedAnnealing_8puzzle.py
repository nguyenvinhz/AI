import copy
import math
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


def random_initial_state():
    s = copy.deepcopy(goal)
    old_action = None
    for _ in range(random.randint(12, 22)):
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


def simulated_annealing(initial_state, temperature=100.0, cooling_rate=0.95, min_temperature=0.01, max_iterations=1000):
    current = initial_state
    current_h = manhattan_distance(current)
    best = copy.deepcopy(current)
    best_h = current_h
    path = [copy.deepcopy(current)]
    actions_taken = []

    
    print("SIMULATED ANNEALING - 8 PUZZLE")
    
    print(f"h = {current_h}, T = {temperature:.4f}")
    print_table(current)

    for iteration in range(1, max_iterations + 1):
        if current == goal:
            print("GOAL")
            break

        if temperature < min_temperature:
            print("STOP")
            break

        actions = find_action(current)
        action = random.choice(actions)
        next_state = execute_action(current, action)
        next_h = manhattan_distance(next_state)
        delta = current_h - next_h

        if delta >= 0:
            accepted = True
            probability = 1.0
            reason = "accepted"
        else:
            probability = math.exp(delta / temperature)
            accepted = random.random() < probability
            reason = "accepted" if accepted else "rejected"

        print(f"Step {iteration}")
        print(f"Action: {action}")
        print(f"h: {current_h} -> {next_h}, delta = {delta}")
        print(f"T = {temperature:.4f}, P = {probability:.4f}, {reason}")

        if accepted:
            current = next_state
            current_h = next_h
            path.append(copy.deepcopy(current))
            actions_taken.append(action)

            if current_h < best_h:
                best = copy.deepcopy(current)
                best_h = current_h

            print_table(current)
        else:
            print("Unchanged")
            print_table(current)

        temperature *= cooling_rate

    result = {
        "success": current == goal,
        "solution": current,
        "best_state": best,
        "best_h": best_h,
        "path": path,
        "actions": actions_taken,
        "iterations": len(actions_taken)
    }

    
    print(f"Result: {'success' if result['success'] else 'failed'}")
    print(f"Best h(n): {best_h}")
    print(f"Accepted moves: {len(actions_taken)}")
    print("Best state:")
    print_table(best)

    return result


if __name__ == "__main__":
    initial = random_initial_state()
    simulated_annealing(initial)
