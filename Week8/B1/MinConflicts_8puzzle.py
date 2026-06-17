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

PLAN_LENGTH = 18
MAX_STEPS = 2000
MAX_RESTARTS = 30
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


def run_actions(state, actions):
    current = copy.deepcopy(state)
    for action in actions:
        if action not in find_action(current):
            return None
        current = execute_action(current, action)
    return current


def print_result(solution, final_state):
    if solution is None:
        print("THẤT BẠI")
        return
    print("NGHIỆM")
    print(solution)
    print("Số bước:", len(solution))
    print_table(final_state)


def random_plan(length):
    return [random.choice(all_actions) for _ in range(length)]


def score_plan(start, plan):
    state = copy.deepcopy(start)
    invalid = 0

    for index, action in enumerate(plan):
        if action not in find_action(state):
            invalid += 5
            continue
        if index > 0 and action == opposite[plan[index - 1]]:
            invalid += 1
        state = execute_action(state, action)

    return manhattan_distance(state) + invalid, state


def min_conflicts(start, length=PLAN_LENGTH, initial_plan=None):
    for restart in range(1, MAX_RESTARTS + 1):
        if restart == 1 and initial_plan is not None:
            plan = initial_plan[:]
            length = len(plan)
        else:
            plan = random_plan(length)

        best_score, best_state = score_plan(start, plan)
        log(f"KHỞI ĐỘNG LẠI {restart}: điểm={best_score}, kế hoạch={plan}")

        for step in range(1, MAX_STEPS + 1):
            score, current_state = score_plan(start, plan)
            log(f"Bước {step}: điểm={score}, h(n)={manhattan_distance(current_state)}")

            if is_goal(current_state):
                return plan, current_state

            index = random.randrange(length)
            candidates = []
            for action in all_actions:
                candidate = plan[:]
                candidate[index] = action
                candidate_score, candidate_state = score_plan(start, candidate)
                candidates.append((candidate_score, action, candidate_state))

            min_score = min(item[0] for item in candidates)
            best_actions = [item for item in candidates if item[0] == min_score]
            _, best_action, best_candidate_state = random.choice(best_actions)
            log(f"ĐỔI X{index}: {plan[index]} -> {best_action}, điểm={min_score}")
            plan[index] = best_action

            if min_score < best_score:
                best_score = min_score
                best_state = best_candidate_state

        if is_goal(best_state):
            return plan, best_state

    final_state = run_actions(start, plan)
    return None, final_state


if __name__ == "__main__":
    print("MIN-CONFLICTS - 8 PUZZLE")
    start, hint = random_initial_state(depth=10)
    print("Trạng thái ban đầu:")
    print_table(start)
    print("Gợi ý nghiệm từ bước xáo trộn:", hint)

    solution, final_state = min_conflicts(start, initial_plan=hint)
    print_result(solution, final_state)
